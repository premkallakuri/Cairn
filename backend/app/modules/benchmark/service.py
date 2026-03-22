from __future__ import annotations

import os
import platform
import re
from dataclasses import dataclass
from datetime import datetime
from app.core.compat import UTC
from statistics import median
from uuid import uuid4

from app.modules.benchmark.repository import BenchmarkRepository
from app.modules.benchmark.schemas import (
    BenchmarkResult,
    BenchmarkResultsResponse,
    BenchmarkSettings,
    BenchmarkStatusResponse,
    BenchmarkType,
    RepositoryStats,
    RepositoryStatsPercentiles,
    RunBenchmarkRequest,
    RunBenchmarkResponse,
    RunBenchmarkSyncResponse,
    SimpleBenchmarkStartResponse,
    SubmitBenchmarkRequest,
    SubmitBenchmarkSuccessResponse,
    UpdateBenchmarkSettingsRequest,
    UpdateBuilderTagRequest,
    UpdateBuilderTagResponse,
)

BUILDER_TAG_PATTERN = re.compile(r"^[A-Za-z]+-[A-Za-z]+-\d{4}$")


@dataclass(slots=True)
class BenchmarkProfile:
    cpu_score: float
    memory_score: float
    disk_read_score: float
    disk_write_score: float
    ai_tokens_per_second: float | None = None
    ai_model_used: str | None = None
    ai_time_to_first_token: float | None = None


class BenchmarkError(ValueError):
    pass


class BenchmarkConflictError(BenchmarkError):
    def __init__(self, current_benchmark_id: str | None = None) -> None:
        message = "Another benchmark is already running"
        if current_benchmark_id:
            message = f"{message}: {current_benchmark_id}"
        super().__init__(message)
        self.current_benchmark_id = current_benchmark_id


class BenchmarkNotFoundError(BenchmarkError):
    pass


class BenchmarkAlreadySubmittedError(BenchmarkError):
    pass


class BenchmarkService:
    def __init__(self, repository: BenchmarkRepository | None = None) -> None:
        self.repository = repository or BenchmarkRepository()

    def run_benchmark(
        self,
        payload: RunBenchmarkRequest | None = None,
        *,
        benchmark_type: BenchmarkType | None = None,
        sync: bool = False,
    ) -> RunBenchmarkResponse | RunBenchmarkSyncResponse:
        benchmark_type = benchmark_type or (payload.benchmark_type if payload else "full")
        self._ensure_initialized()
        benchmark_id = self._new_benchmark_id(benchmark_type)
        self.repository.update_status(
            status="starting",
            benchmark_id=benchmark_id,
            message=f"Starting {benchmark_type} benchmark",
            progress=0,
        )

        result = self._execute_benchmark(benchmark_id, benchmark_type)
        self.repository.update_status(
            status="completed",
            benchmark_id=benchmark_id,
            message=f"{benchmark_type.title()} benchmark completed",
            progress=100,
        )
        self.repository.update_settings(last_benchmark_run=datetime.now(UTC))

        if sync:
            return RunBenchmarkSyncResponse(
                success=True,
                benchmark_id=benchmark_id,
                nomad_score=result.nomad_score,
                result=result,
            )

        return RunBenchmarkResponse(
            success=True,
            job_id=benchmark_id,
            benchmark_id=benchmark_id,
            message="Benchmark queued",
        )

    def run_system_benchmark(self) -> SimpleBenchmarkStartResponse:
        response = self.run_benchmark(benchmark_type="system", sync=False)
        return SimpleBenchmarkStartResponse(
            success=True,
            benchmark_id=response.benchmark_id,
            message="System benchmark queued",
        )

    def run_ai_benchmark(self) -> SimpleBenchmarkStartResponse:
        response = self.run_benchmark(benchmark_type="ai", sync=False)
        return SimpleBenchmarkStartResponse(
            success=True,
            benchmark_id=response.benchmark_id,
            message="AI benchmark queued",
        )

    def list_results(self) -> BenchmarkResultsResponse:
        results = [self._serialize_result(result) for result in self.repository.list_results()]
        return BenchmarkResultsResponse(results=results, total=len(results))

    def get_latest_result(self) -> BenchmarkResult | None:
        latest = self.repository.latest_result()
        return self._serialize_result(latest) if latest is not None else None

    def get_result(self, benchmark_id: str) -> BenchmarkResult:
        result = self.repository.get_result(benchmark_id)
        if result is None:
            raise BenchmarkNotFoundError(f"Benchmark not found: {benchmark_id}")
        return self._serialize_result(result)

    def submit_benchmark(
        self,
        payload: SubmitBenchmarkRequest | None = None,
    ) -> SubmitBenchmarkSuccessResponse:
        benchmark_id = payload.benchmark_id if payload and payload.benchmark_id else None
        result = self._resolve_result(benchmark_id)
        if result.submitted_to_repository:
            raise BenchmarkAlreadySubmittedError(
                f"Benchmark already submitted: {result.benchmark_id}"
            )

        repository_id = f"repo-{result.benchmark_id[:12]}"
        percentile = self._percentile_for_score(result.nomad_score)
        self.repository.update_result(
            result.benchmark_id,
            submitted_to_repository=True,
            submitted_at=datetime.now(UTC),
            repository_id=repository_id,
        )
        return SubmitBenchmarkSuccessResponse(
            success=True,
            repository_id=repository_id,
            percentile=percentile,
        )

    def update_builder_tag(
        self,
        payload: UpdateBuilderTagRequest,
    ) -> UpdateBuilderTagResponse:
        if payload.builder_tag is not None and not BUILDER_TAG_PATTERN.match(payload.builder_tag):
            raise BenchmarkError("Invalid builder tag")

        result = self.repository.get_result(payload.benchmark_id)
        if result is None:
            raise BenchmarkNotFoundError(f"Benchmark not found: {payload.benchmark_id}")

        self.repository.update_result(payload.benchmark_id, builder_tag=payload.builder_tag)
        return UpdateBuilderTagResponse(success=True, builder_tag=payload.builder_tag)

    def get_comparison_stats(self) -> RepositoryStats | None:
        results = self.repository.list_results()
        if not results:
            return None

        scores = [result.nomad_score for result in results]
        return RepositoryStats(
            total_submissions=len(scores),
            average_score=round(sum(scores) / len(scores), 2),
            median_score=round(median(scores), 2),
            top_score=round(max(scores), 2),
            percentiles=RepositoryStatsPercentiles(
                p10=self._percentile(scores, 10),
                p25=self._percentile(scores, 25),
                p50=self._percentile(scores, 50),
                p75=self._percentile(scores, 75),
                p90=self._percentile(scores, 90),
            ),
        )

    def get_status(self) -> BenchmarkStatusResponse:
        status = self.repository.get_or_create_status()
        return BenchmarkStatusResponse(status=status.status, benchmarkId=status.benchmark_id)

    def get_settings(self) -> BenchmarkSettings:
        settings = self.repository.get_or_create_settings()
        return BenchmarkSettings(
            allow_anonymous_submission=settings.allow_anonymous_submission,
            installation_id=settings.installation_id,
            last_benchmark_run=(
                settings.last_benchmark_run.isoformat() if settings.last_benchmark_run else None
            ),
        )

    def update_settings(
        self,
        payload: UpdateBenchmarkSettingsRequest,
    ) -> tuple[bool, BenchmarkSettings]:
        updates: dict[str, object] = {}
        if payload.allow_anonymous_submission is not None:
            updates["allow_anonymous_submission"] = payload.allow_anonymous_submission
        settings = (
            self.repository.update_settings(**updates)
            if updates
            else self.repository.get_or_create_settings()
        )
        return True, BenchmarkSettings(
            allow_anonymous_submission=settings.allow_anonymous_submission,
            installation_id=settings.installation_id,
            last_benchmark_run=(
                settings.last_benchmark_run.isoformat() if settings.last_benchmark_run else None
            ),
        )

    def _ensure_initialized(self) -> None:
        self.repository.get_or_create_settings()
        self.repository.get_or_create_status()

    def _new_benchmark_id(self, benchmark_type: BenchmarkType) -> str:
        prefix = benchmark_type.replace("full", "nomad").replace("system", "sys")
        return f"{prefix}-{uuid4().hex[:12]}"

    def _resolve_result(self, benchmark_id: str | None) -> BenchmarkResult:
        if benchmark_id:
            return self.get_result(benchmark_id)
        latest = self.get_latest_result()
        if latest is None:
            raise BenchmarkNotFoundError("No benchmark results available")
        return latest

    def _execute_benchmark(
        self,
        benchmark_id: str,
        benchmark_type: BenchmarkType,
    ) -> BenchmarkResult:
        profile = self._profile_for_type(benchmark_type)
        result = self.repository.create_result(
            {
                "benchmark_id": benchmark_id,
                "benchmark_type": benchmark_type,
                "cpu_model": self._cpu_model(),
                "cpu_cores": os.cpu_count() or 1,
                "cpu_threads": os.cpu_count() or 1,
                "ram_bytes": self._ram_bytes(),
                "disk_type": "unknown",
                "gpu_model": None,
                "cpu_score": profile.cpu_score,
                "memory_score": profile.memory_score,
                "disk_read_score": profile.disk_read_score,
                "disk_write_score": profile.disk_write_score,
                "ai_tokens_per_second": profile.ai_tokens_per_second,
                "ai_model_used": profile.ai_model_used,
                "ai_time_to_first_token": profile.ai_time_to_first_token,
                "nomad_score": self._nomad_score(profile),
                "submitted_to_repository": False,
                "submitted_at": None,
                "repository_id": None,
                "builder_tag": None,
            }
        )
        return self._serialize_result(result)

    def _serialize_result(self, result) -> BenchmarkResult:
        return BenchmarkResult(
            id=result.id,
            benchmark_id=result.benchmark_id,
            benchmark_type=result.benchmark_type,
            cpu_model=result.cpu_model,
            cpu_cores=result.cpu_cores,
            cpu_threads=result.cpu_threads,
            ram_bytes=result.ram_bytes,
            disk_type=result.disk_type,
            gpu_model=result.gpu_model,
            cpu_score=result.cpu_score,
            memory_score=result.memory_score,
            disk_read_score=result.disk_read_score,
            disk_write_score=result.disk_write_score,
            ai_tokens_per_second=result.ai_tokens_per_second,
            ai_model_used=result.ai_model_used,
            ai_time_to_first_token=result.ai_time_to_first_token,
            nomad_score=result.nomad_score,
            submitted_to_repository=result.submitted_to_repository,
            submitted_at=result.submitted_at.isoformat() if result.submitted_at else None,
            repository_id=result.repository_id,
            builder_tag=result.builder_tag,
            created_at=result.created_at.isoformat(),
            updated_at=result.updated_at.isoformat(),
        )

    def _profile_for_type(self, benchmark_type: BenchmarkType) -> BenchmarkProfile:
        if benchmark_type == "system":
            return BenchmarkProfile(
                cpu_score=28.5,
                memory_score=19.0,
                disk_read_score=17.5,
                disk_write_score=16.0,
            )
        if benchmark_type == "ai":
            return BenchmarkProfile(
                cpu_score=18.0,
                memory_score=16.0,
                disk_read_score=8.0,
                disk_write_score=7.0,
                ai_tokens_per_second=24.5,
                ai_model_used="local-benchmark-model",
                ai_time_to_first_token=0.82,
            )
        return BenchmarkProfile(
            cpu_score=42.0,
            memory_score=31.0,
            disk_read_score=22.5,
            disk_write_score=20.0,
        )

    def _nomad_score(self, profile: BenchmarkProfile) -> float:
        score = (
            profile.cpu_score * 0.35
            + profile.memory_score * 0.25
            + profile.disk_read_score * 0.2
            + profile.disk_write_score * 0.2
        )
        if profile.ai_tokens_per_second:
            score += min(profile.ai_tokens_per_second / 10, 10)
        return round(score, 2)

    def _percentile(self, values: list[float], percentile_value: int) -> float:
        ordered = sorted(values)
        if not ordered:
            return 0
        index = round((percentile_value / 100) * (len(ordered) - 1))
        return round(ordered[index], 2)

    def _percentile_for_score(self, score: float) -> float:
        return round(min(max(score, 1.0), 99.9), 2)

    def _cpu_model(self) -> str:
        value = platform.processor() or platform.machine() or "Unknown CPU"
        if value == "":  # pragma: no cover - platform fallback
            value = "Unknown CPU"
        return value

    def _ram_bytes(self) -> int:
        if hasattr(os, "sysconf"):
            try:
                pages = os.sysconf("SC_PHYS_PAGES")
                page_size = os.sysconf("SC_PAGE_SIZE")
                return int(pages * page_size)
            except (ValueError, OSError, AttributeError):  # pragma: no cover - platform fallback
                pass
        return 8 * 1024 * 1024 * 1024
