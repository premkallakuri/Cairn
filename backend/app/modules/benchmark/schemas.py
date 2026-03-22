from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

BenchmarkType = Literal["full", "system", "ai"]


class RunBenchmarkRequest(BaseModel):
    benchmark_type: BenchmarkType = "full"


class BenchmarkResult(BaseModel):
    id: int
    benchmark_id: str
    benchmark_type: BenchmarkType
    cpu_model: str
    cpu_cores: int
    cpu_threads: int
    ram_bytes: int
    disk_type: str
    gpu_model: str | None = None
    cpu_score: float
    memory_score: float
    disk_read_score: float
    disk_write_score: float
    ai_tokens_per_second: float | None = None
    ai_model_used: str | None = None
    ai_time_to_first_token: float | None = None
    nomad_score: float
    submitted_to_repository: bool
    submitted_at: str | None = None
    repository_id: str | None = None
    builder_tag: str | None = None
    created_at: str
    updated_at: str


class RunBenchmarkResponse(BaseModel):
    success: bool
    job_id: str
    benchmark_id: str
    message: str


class RunBenchmarkSyncResponse(BaseModel):
    success: bool
    benchmark_id: str
    nomad_score: float
    result: BenchmarkResult


class SimpleBenchmarkStartResponse(BaseModel):
    success: bool
    benchmark_id: str
    message: str


class BenchmarkConflictResponse(BaseModel):
    success: bool
    error: str
    current_benchmark_id: str | None = None


class BenchmarkResultsResponse(BaseModel):
    results: list[BenchmarkResult]
    total: int


class SubmitBenchmarkRequest(BaseModel):
    benchmark_id: str | None = None
    anonymous: bool = False


class SubmitBenchmarkSuccessResponse(BaseModel):
    success: bool
    repository_id: str
    percentile: float


class SubmitBenchmarkErrorResponse(BaseModel):
    success: bool
    error: str


class UpdateBuilderTagRequest(BaseModel):
    benchmark_id: str
    builder_tag: str | None = None


class UpdateBuilderTagResponse(BaseModel):
    success: bool
    builder_tag: str | None


class UpdateBuilderTagErrorResponse(BaseModel):
    success: bool
    error: str


class RepositoryStatsPercentiles(BaseModel):
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float


class RepositoryStats(BaseModel):
    total_submissions: int
    average_score: float
    median_score: float
    top_score: float
    percentiles: RepositoryStatsPercentiles


class BenchmarkStatusResponse(BaseModel):
    status: str
    benchmarkId: str | None = None


class BenchmarkSettings(BaseModel):
    allow_anonymous_submission: bool
    installation_id: str | None = None
    last_benchmark_run: str | None = None


class UpdateBenchmarkSettingsRequest(BaseModel):
    allow_anonymous_submission: bool | None = None
