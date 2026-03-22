from __future__ import annotations

from datetime import datetime
from app.core.compat import UTC

from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.chat.models import ChatMessageModel, ChatSessionModel


class ChatRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def create_session(self, *, title: str, model: str | None) -> ChatSessionModel:
        if self._session is not None:
            return self._create_session(self._session, title=title, model=model)

        session = next(get_session())
        try:
            return self._create_session(session, title=title, model=model)
        finally:
            session.close()

    def list_sessions(self) -> list[ChatSessionModel]:
        if self._session is not None:
            return self._list_sessions(self._session)

        session = next(get_session())
        try:
            return self._list_sessions(session)
        finally:
            session.close()

    def get_session(self, session_id: int) -> ChatSessionModel | None:
        if self._session is not None:
            return self._get_session(self._session, session_id)

        session = next(get_session())
        try:
            return self._get_session(session, session_id)
        finally:
            session.close()

    def update_session(self, session_id: int, **updates: object) -> ChatSessionModel:
        if self._session is not None:
            return self._update_session(self._session, session_id, **updates)

        session = next(get_session())
        try:
            return self._update_session(session, session_id, **updates)
        finally:
            session.close()

    def delete_session(self, session_id: int) -> bool:
        if self._session is not None:
            return self._delete_session(self._session, session_id)

        session = next(get_session())
        try:
            return self._delete_session(session, session_id)
        finally:
            session.close()

    def delete_all_sessions(self) -> int:
        if self._session is not None:
            return self._delete_all_sessions(self._session)

        session = next(get_session())
        try:
            return self._delete_all_sessions(session)
        finally:
            session.close()

    def add_message(self, session_id: int, *, role: str, content: str) -> ChatMessageModel:
        if self._session is not None:
            return self._add_message(self._session, session_id, role=role, content=content)

        session = next(get_session())
        try:
            return self._add_message(session, session_id, role=role, content=content)
        finally:
            session.close()

    def list_messages(self, session_id: int) -> list[ChatMessageModel]:
        if self._session is not None:
            return self._list_messages(self._session, session_id)

        session = next(get_session())
        try:
            return self._list_messages(session, session_id)
        finally:
            session.close()

    def _create_session(
        self,
        session: Session,
        *,
        title: str,
        model: str | None,
    ) -> ChatSessionModel:
        record = ChatSessionModel(title=title, model=model)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

    def _list_sessions(self, session: Session) -> list[ChatSessionModel]:
        return session.query(ChatSessionModel).order_by(ChatSessionModel.updated_at.desc()).all()

    def _get_session(self, session: Session, session_id: int) -> ChatSessionModel | None:
        return session.get(ChatSessionModel, session_id)

    def _update_session(
        self,
        session: Session,
        session_id: int,
        **updates: object,
    ) -> ChatSessionModel:
        record = session.get(ChatSessionModel, session_id)
        if record is None:
            raise ValueError(f"Unknown chat session: {session_id}")
        for key, value in updates.items():
            setattr(record, key, value)
        record.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(record)
        return record

    def _delete_session(self, session: Session, session_id: int) -> bool:
        record = session.get(ChatSessionModel, session_id)
        if record is None:
            return False
        session.query(ChatMessageModel).filter(ChatMessageModel.session_id == session_id).delete()
        session.delete(record)
        session.commit()
        return True

    def _delete_all_sessions(self, session: Session) -> int:
        count = session.query(ChatSessionModel).count()
        session.query(ChatMessageModel).delete()
        session.query(ChatSessionModel).delete()
        session.commit()
        return count

    def _add_message(
        self,
        session: Session,
        session_id: int,
        *,
        role: str,
        content: str,
    ) -> ChatMessageModel:
        record = session.get(ChatSessionModel, session_id)
        if record is None:
            raise ValueError(f"Unknown chat session: {session_id}")
        message = ChatMessageModel(session_id=session_id, role=role, content=content)
        session.add(message)
        record.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(message)
        return message

    def _list_messages(self, session: Session, session_id: int) -> list[ChatMessageModel]:
        return (
            session.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.created_at.asc(), ChatMessageModel.id.asc())
            .all()
        )
