from fastapi import APIRouter, HTTPException, Response, status

from app.modules.chat.schemas import (
    AddChatMessageRequest,
    ChatMessage,
    ChatSessionCreateResponse,
    ChatSessionDetail,
    ChatSessionSummary,
    CreateChatSessionRequest,
    SuggestionsResponse,
    UpdateChatSessionRequest,
)
from app.modules.chat.service import ChatService
from app.modules.platform_core.schemas import SuccessMessageResponse

router = APIRouter(tags=["chat"])


@router.get("/suggestions", response_model=SuggestionsResponse)
def get_chat_suggestions() -> SuggestionsResponse:
    return ChatService().get_suggestions()


@router.get("/sessions", response_model=list[ChatSessionSummary])
def list_chat_sessions() -> list[ChatSessionSummary]:
    return ChatService().list_sessions()


@router.post(
    "/sessions",
    response_model=ChatSessionCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_session(payload: CreateChatSessionRequest) -> ChatSessionCreateResponse:
    return ChatService().create_session(title=payload.title, model=payload.model)


@router.delete("/sessions/all", response_model=SuccessMessageResponse)
def delete_all_chat_sessions() -> SuccessMessageResponse:
    return ChatService().delete_all_sessions()


@router.get("/sessions/{id}", response_model=ChatSessionDetail)
def get_chat_session(id: int) -> ChatSessionDetail:
    try:
        return ChatService().get_session(id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/sessions/{id}", response_model=ChatSessionCreateResponse)
def update_chat_session(
    id: int,
    payload: UpdateChatSessionRequest,
) -> ChatSessionCreateResponse:
    try:
        return ChatService().update_session(
            id,
            title=payload.title,
            model=payload.model,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/sessions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_session(id: int) -> Response:
    deleted = ChatService().delete_session(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Unknown chat session: {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/sessions/{id}/messages",
    response_model=ChatMessage,
    status_code=status.HTTP_201_CREATED,
)
def add_chat_message(id: int, payload: AddChatMessageRequest) -> ChatMessage:
    try:
        return ChatService().add_message(
            id,
            role=payload.role,
            content=payload.content,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
