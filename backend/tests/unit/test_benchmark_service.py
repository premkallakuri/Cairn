from __future__ import annotations

import pytest

from app.modules.benchmark.repository import BenchmarkRepository
from app.modules.benchmark.schemas import (
    RunBenchmarkRequest,
    SubmitBenchmarkRequest,
    UpdateBenchmarkSettingsRequest,
    UpdateBuilderTagRequest,
)
from app.modules.benchmark.service import BenchmarkService

pytestmark = [pytest.mark.unit, pytest.mark.benchmark]


def test_run_benchmark_creates_result_and_updates_status() -> None:
    service = BenchmarkService(BenchmarkRepository())

    response = service.run_benchmark(RunBenchmarkRequest(benchmark_type="full"), sync=True)

    assert response.success is True
    assert response.result.benchmark_type == "full"
    assert response.result.nomad_score > 0
    assert service.get_status().status == "completed"
    assert service.get_latest_result() is not None


def test_run_system_and_ai_benchmarks_create_distinct_results() -> None:
    service = BenchmarkService(BenchmarkRepository())

    system = service.run_system_benchmark()
    ai = service.run_ai_benchmark()

    assert system.benchmark_id != ai.benchmark_id
    results = service.list_results()
    assert results.total == 2
    assert {result.benchmark_type for result in results.results} == {"system", "ai"}


def test_submit_builder_tag_and_settings_are_persisted() -> None:
    service = BenchmarkService(BenchmarkRepository())
    created = service.run_benchmark(RunBenchmarkRequest(benchmark_type="ai"), sync=True)

    submitted = service.submit_benchmark(SubmitBenchmarkRequest(benchmark_id=created.benchmark_id))
    assert submitted.success is True

    updated = service.update_builder_tag(
        UpdateBuilderTagRequest(benchmark_id=created.benchmark_id, builder_tag="Atlas-Haven-2026")
    )
    assert updated.builder_tag == "Atlas-Haven-2026"

    success, settings = service.update_settings(
        UpdateBenchmarkSettingsRequest(allow_anonymous_submission=True)
    )
    assert success is True
    assert settings.allow_anonymous_submission is True


def test_comparison_stats_reflect_latest_scores() -> None:
    service = BenchmarkService(BenchmarkRepository())
    service.run_benchmark(RunBenchmarkRequest(benchmark_type="system"), sync=True)
    service.run_benchmark(RunBenchmarkRequest(benchmark_type="ai"), sync=True)

    stats = service.get_comparison_stats()

    assert stats is not None
    assert stats.total_submissions == 2
    assert stats.top_score >= stats.median_score
