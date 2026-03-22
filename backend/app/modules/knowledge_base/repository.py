from __future__ import annotations

from datetime import datetime
from app.core.compat import UTC
from typing import Any

from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.knowledge_base.models import EmbedJobModel, KnowledgeChunkModel, KnowledgeFileModel


class KnowledgeBaseRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def create_job(self, payload: dict[str, Any]) -> EmbedJobModel:
        if self._session is not None:
            return self._create_job(self._session, payload)

        session = next(get_session())
        try:
            return self._create_job(session, payload)
        finally:
            session.close()

    def get_active_job(self, file_path: str) -> EmbedJobModel | None:
        if self._session is not None:
            return self._get_active_job(self._session, file_path)

        session = next(get_session())
        try:
            return self._get_active_job(session, file_path)
        finally:
            session.close()

    def get_latest_job(self, file_path: str) -> EmbedJobModel | None:
        if self._session is not None:
            return self._get_latest_job(self._session, file_path)

        session = next(get_session())
        try:
            return self._get_latest_job(session, file_path)
        finally:
            session.close()

    def get_job(self, job_id: str) -> EmbedJobModel | None:
        if self._session is not None:
            return self._get_job(self._session, job_id)

        session = next(get_session())
        try:
            return self._get_job(session, job_id)
        finally:
            session.close()

    def update_job(self, job_id: str, **updates: Any) -> EmbedJobModel:
        if self._session is not None:
            return self._update_job(self._session, job_id, **updates)

        session = next(get_session())
        try:
            return self._update_job(session, job_id, **updates)
        finally:
            session.close()

    def list_active_jobs(self) -> list[EmbedJobModel]:
        if self._session is not None:
            return self._list_active_jobs(self._session)

        session = next(get_session())
        try:
            return self._list_active_jobs(session)
        finally:
            session.close()

    def upsert_file(
        self,
        *,
        file_name: str,
        file_path: str,
        extracted_text: str,
    ) -> KnowledgeFileModel:
        if self._session is not None:
            return self._upsert_file(
                self._session,
                file_name=file_name,
                file_path=file_path,
                extracted_text=extracted_text,
            )

        session = next(get_session())
        try:
            return self._upsert_file(
                session,
                file_name=file_name,
                file_path=file_path,
                extracted_text=extracted_text,
            )
        finally:
            session.close()

    def get_file(self, file_path: str) -> KnowledgeFileModel | None:
        if self._session is not None:
            return self._get_file(self._session, file_path)

        session = next(get_session())
        try:
            return self._get_file(session, file_path)
        finally:
            session.close()

    def list_files(self) -> list[KnowledgeFileModel]:
        if self._session is not None:
            return self._list_files(self._session)

        session = next(get_session())
        try:
            return self._list_files(session)
        finally:
            session.close()

    def replace_chunks(
        self,
        *,
        source_path: str,
        source_name: str,
        chunks: list[str],
    ) -> None:
        if self._session is not None:
            self._replace_chunks(
                self._session,
                source_path=source_path,
                source_name=source_name,
                chunks=chunks,
            )
            return

        session = next(get_session())
        try:
            self._replace_chunks(
                session,
                source_path=source_path,
                source_name=source_name,
                chunks=chunks,
            )
        finally:
            session.close()

    def list_chunks(self) -> list[KnowledgeChunkModel]:
        if self._session is not None:
            return self._list_chunks(self._session)

        session = next(get_session())
        try:
            return self._list_chunks(session)
        finally:
            session.close()

    def delete_source(self, source_path: str) -> bool:
        if self._session is not None:
            return self._delete_source(self._session, source_path)

        session = next(get_session())
        try:
            return self._delete_source(session, source_path)
        finally:
            session.close()

    def _create_job(self, session: Session, payload: dict[str, Any]) -> EmbedJobModel:
        job = EmbedJobModel(**payload)
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def _get_active_job(self, session: Session, file_path: str) -> EmbedJobModel | None:
        return (
            session.query(EmbedJobModel)
            .filter(
                EmbedJobModel.file_path == file_path,
                EmbedJobModel.status.in_(["queued", "processing"]),
            )
            .order_by(EmbedJobModel.created_at.desc())
            .first()
        )

    def _get_latest_job(self, session: Session, file_path: str) -> EmbedJobModel | None:
        return (
            session.query(EmbedJobModel)
            .filter(EmbedJobModel.file_path == file_path)
            .order_by(EmbedJobModel.created_at.desc())
            .first()
        )

    def _get_job(self, session: Session, job_id: str) -> EmbedJobModel | None:
        return session.get(EmbedJobModel, job_id)

    def _update_job(self, session: Session, job_id: str, **updates: Any) -> EmbedJobModel:
        job = session.get(EmbedJobModel, job_id)
        if job is None:
            raise ValueError(f"Unknown embed job: {job_id}")
        for key, value in updates.items():
            setattr(job, key, value)
        job.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(job)
        return job

    def _list_active_jobs(self, session: Session) -> list[EmbedJobModel]:
        return (
            session.query(EmbedJobModel)
            .filter(EmbedJobModel.status.in_(["queued", "processing"]))
            .order_by(EmbedJobModel.created_at.desc())
            .all()
        )

    def _upsert_file(
        self,
        session: Session,
        *,
        file_name: str,
        file_path: str,
        extracted_text: str,
    ) -> KnowledgeFileModel:
        record = session.query(KnowledgeFileModel).filter_by(file_path=file_path).first()
        if record is None:
            record = KnowledgeFileModel(
                file_name=file_name,
                file_path=file_path,
                extracted_text=extracted_text,
                indexed_at=datetime.now(UTC),
            )
            session.add(record)
        else:
            record.file_name = file_name
            record.extracted_text = extracted_text
            record.indexed_at = datetime.now(UTC)
        session.commit()
        session.refresh(record)
        return record

    def _get_file(self, session: Session, file_path: str) -> KnowledgeFileModel | None:
        return session.query(KnowledgeFileModel).filter_by(file_path=file_path).first()

    def _list_files(self, session: Session) -> list[KnowledgeFileModel]:
        return session.query(KnowledgeFileModel).order_by(KnowledgeFileModel.file_name.asc()).all()

    def _replace_chunks(
        self,
        session: Session,
        *,
        source_path: str,
        source_name: str,
        chunks: list[str],
    ) -> None:
        session.query(KnowledgeChunkModel).filter_by(source_path=source_path).delete()
        for index, chunk in enumerate(chunks):
            session.add(
                KnowledgeChunkModel(
                    source_path=source_path,
                    source_name=source_name,
                    chunk_index=index,
                    content=chunk,
                )
            )
        session.commit()

    def _list_chunks(self, session: Session) -> list[KnowledgeChunkModel]:
        return session.query(KnowledgeChunkModel).order_by(KnowledgeChunkModel.id.asc()).all()

    def _delete_source(self, session: Session, source_path: str) -> bool:
        file_record = session.query(KnowledgeFileModel).filter_by(file_path=source_path).first()
        if file_record is None:
            return False
        session.query(KnowledgeChunkModel).filter_by(source_path=source_path).delete()
        session.query(EmbedJobModel).filter_by(file_path=source_path).delete()
        session.delete(file_record)
        session.commit()
        return True
