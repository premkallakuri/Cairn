from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.modules.ollama.schemas import (
    AvailableModelsResponse,
    ModelNameRequest,
    OllamaChatRequest,
    OllamaChatResponse,
)
from app.modules.ollama.service import OllamaService
from app.modules.platform_core.schemas import SuccessMessageResponse

router = APIRouter(tags=["ollama"])


@router.get("/models", response_model=AvailableModelsResponse)
def list_available_models(
    sort: str | None = Query(None),
    recommended_only: bool = Query(False, alias="recommendedOnly"),
    query: str | None = Query(None),
    limit: int | None = Query(None, ge=1),
    force: bool = Query(False),
) -> AvailableModelsResponse:
    return OllamaService().list_available_models(
        sort=sort,
        recommended_only=recommended_only,
        query=query,
        limit=limit,
        force=force,
    )


@router.post("/models", response_model=SuccessMessageResponse)
def download_model(payload: ModelNameRequest) -> SuccessMessageResponse:
    return OllamaService().queue_model_download(payload.model)


@router.delete("/models", response_model=SuccessMessageResponse)
def delete_model(payload: ModelNameRequest) -> SuccessMessageResponse:
    return OllamaService().delete_model(payload.model)


@router.get("/installed-models", response_model=list[dict[str, object]])
def list_installed_models() -> list[dict[str, object]]:
    return OllamaService().list_installed_models()


@router.post("/chat", response_model=OllamaChatResponse)
def send_chat_message(payload: OllamaChatRequest):
    try:
        if payload.stream:
            events = OllamaService().stream_chat(
                model=payload.model,
                messages=list(payload.messages),
            )
            return StreamingResponse(iter(events), media_type="text/event-stream")
        return OllamaService().send_chat(
            model=payload.model,
            messages=list(payload.messages),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
