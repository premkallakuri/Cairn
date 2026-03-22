from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.modules.benchmark.schemas import (
    BenchmarkResultsResponse,
    BenchmarkSettings,
    BenchmarkStatusResponse,
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
from app.modules.benchmark.service import (
    BenchmarkAlreadySubmittedError,
    BenchmarkError,
    BenchmarkNotFoundError,
    BenchmarkService,
)

router = APIRouter(tags=["benchmark"])


@router.post("/run")
def run_benchmark(
    payload: RunBenchmarkRequest | None = None,
    sync: bool = Query(False),
) -> RunBenchmarkResponse | RunBenchmarkSyncResponse:
    return BenchmarkService().run_benchmark(payload, sync=sync)


@router.post("/run/system", response_model=SimpleBenchmarkStartResponse)
def run_system_benchmark() -> SimpleBenchmarkStartResponse:
    return BenchmarkService().run_system_benchmark()


@router.post("/run/ai", response_model=SimpleBenchmarkStartResponse)
def run_ai_benchmark() -> SimpleBenchmarkStartResponse:
    return BenchmarkService().run_ai_benchmark()


@router.get("/results", response_model=BenchmarkResultsResponse)
def list_results() -> BenchmarkResultsResponse:
    return BenchmarkService().list_results()


@router.get("/results/latest")
def get_latest_result() -> dict[str, object]:
    return {"result": BenchmarkService().get_latest_result()}


@router.get("/results/{id}")
def get_result(id: str) -> dict[str, object]:
    try:
        return {"result": BenchmarkService().get_result(id)}
    except BenchmarkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/submit", response_model=SubmitBenchmarkSuccessResponse)
def submit_benchmark(
    payload: SubmitBenchmarkRequest | None = None,
) -> SubmitBenchmarkSuccessResponse:
    try:
        return BenchmarkService().submit_benchmark(payload)
    except BenchmarkAlreadySubmittedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except BenchmarkNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/builder-tag", response_model=UpdateBuilderTagResponse)
def update_builder_tag(payload: UpdateBuilderTagRequest) -> UpdateBuilderTagResponse:
    try:
        return BenchmarkService().update_builder_tag(payload)
    except BenchmarkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except BenchmarkError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/comparison")
def get_comparison_stats() -> dict[str, object]:
    return {"stats": BenchmarkService().get_comparison_stats()}


@router.get("/status", response_model=BenchmarkStatusResponse)
def get_status() -> BenchmarkStatusResponse:
    return BenchmarkService().get_status()


@router.get("/settings", response_model=BenchmarkSettings)
def get_settings() -> BenchmarkSettings:
    return BenchmarkService().get_settings()


@router.post("/settings")
def update_settings(payload: UpdateBenchmarkSettingsRequest | None = None) -> dict[str, object]:
    if payload is None:
        payload = UpdateBenchmarkSettingsRequest()
    success, settings = BenchmarkService().update_settings(payload)
    return {"success": success, "settings": settings}
