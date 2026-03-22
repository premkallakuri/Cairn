from __future__ import annotations

import re

from app.modules.chat.repository import ChatRepository
from app.modules.chat.schemas import (
    ChatMessage,
    ChatSessionCreateResponse,
    ChatSessionDetail,
    ChatSessionSummary,
    SuggestionsResponse,
)
from app.modules.platform_core.schemas import SuccessMessageResponse

SUGGESTIONS = (
    "What should I install first for a low-power offline field kit?",
    "Help me plan maps, docs, and AI models for a Pacific deployment.",
    "Summarize the local services I need for a private knowledge assistant.",
    "Give me a checklist for loading medical references and Wikipedia locally.",
)


class ChatService:
    def __init__(self, repository: ChatRepository | None = None) -> None:
        self.repository = repository or ChatRepository()

    def get_suggestions(self) -> SuggestionsResponse:
        return SuggestionsResponse(suggestions=list(SUGGESTIONS))

    def list_sessions(self) -> list[ChatSessionSummary]:
        sessions = self.repository.list_sessions()
        results: list[ChatSessionSummary] = []
        for session in sessions:
            messages = self.repository.list_messages(session.id)
            results.append(
                ChatSessionSummary(
                    id=session.id,
                    title=session.title,
                    model=session.model,
                    timestamp=session.updated_at.isoformat(),
                    lastMessage=messages[-1].content if messages else None,
                )
            )
        return results

    def create_session(self, *, title: str, model: str | None) -> ChatSessionCreateResponse:
        record = self.repository.create_session(title=title.strip(), model=model)
        return ChatSessionCreateResponse(
            id=record.id,
            title=record.title,
            model=record.model,
            timestamp=record.updated_at.isoformat(),
        )

    def get_session(self, session_id: int) -> ChatSessionDetail:
        record = self.repository.get_session(session_id)
        if record is None:
            raise ValueError(f"Unknown chat session: {session_id}")
        messages = self.repository.list_messages(session_id)
        return ChatSessionDetail(
            id=record.id,
            title=record.title,
            model=record.model,
            timestamp=record.updated_at.isoformat(),
            messages=[self._to_message(item) for item in messages],
        )

    def update_session(
        self,
        session_id: int,
        *,
        title: str | None = None,
        model: str | None = None,
    ) -> ChatSessionCreateResponse:
        updates: dict[str, object] = {}
        if title is not None:
            updates["title"] = title.strip()
        if model is not None:
            updates["model"] = model
        if not updates:
            record = self.repository.get_session(session_id)
            if record is None:
                raise ValueError(f"Unknown chat session: {session_id}")
        else:
            record = self.repository.update_session(session_id, **updates)
        return ChatSessionCreateResponse(
            id=record.id,
            title=record.title,
            model=record.model,
            timestamp=record.updated_at.isoformat(),
        )

    def delete_session(self, session_id: int) -> bool:
        return self.repository.delete_session(session_id)

    def delete_all_sessions(self) -> SuccessMessageResponse:
        deleted = self.repository.delete_all_sessions()
        return SuccessMessageResponse(
            success=True,
            message=f"Deleted {deleted} chat sessions",
        )

    def add_message(self, session_id: int, *, role: str, content: str) -> ChatMessage:
        normalized_content = content.strip()
        if not normalized_content:
            raise ValueError("Chat message content must not be blank")
        message = self.repository.add_message(session_id, role=role, content=normalized_content)
        session = self.repository.get_session(session_id)
        if session is None:
            raise ValueError(f"Unknown chat session: {session_id}")

        if role == "user" and self._should_generate_title(session.title):
            self.repository.update_session(
                session_id,
                title=self._generate_title(normalized_content),
            )
        return self._to_message(message)

    def _generate_title(self, content: str) -> str:
        words = re.findall(r"[A-Za-z0-9']+", content)
        if not words:
            return "New chat"
        return " ".join(words[:6])

    def _should_generate_title(self, title: str) -> bool:
        return title.strip().lower() in {"new chat", "untitled chat"}

    def _to_message(self, message) -> ChatMessage:
        return ChatMessage(
            id=message.id,
            role=message.role,
            content=message.content,
            timestamp=message.created_at.isoformat(),
        )
