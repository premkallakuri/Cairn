from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.downloads.models import DownloadJobModel


class DownloadJobRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def create_job(self, payload: dict[str, Any]) -> DownloadJobModel:
        if self._session is not None:
            return self._create_job(self._session, payload)

        session = next(get_session())
        try:
            return self._create_job(session, payload)
        finally:
            session.close()

    def list_jobs(
        self,
        *,
        filetype: str | None = None,
        statuses: Iterable[str] | None = None,
    ) -> list[DownloadJobModel]:
        if self._session is not None:
            return self._list_jobs(self._session, filetype=filetype, statuses=statuses)

        session = next(get_session())
        try:
            return self._list_jobs(session, filetype=filetype, statuses=statuses)
        finally:
            session.close()

    def get_by_job_id(self, job_id: str) -> DownloadJobModel | None:
        if self._session is not None:
            return self._get_by_job_id(self._session, job_id)

        session = next(get_session())
        try:
            return self._get_by_job_id(session, job_id)
        finally:
            session.close()

    def get_by_url(
        self, url: str, *, statuses: Iterable[str] | None = None
    ) -> DownloadJobModel | None:
        if self._session is not None:
            return self._get_by_url(self._session, url, statuses=statuses)

        session = next(get_session())
        try:
            return self._get_by_url(session, url, statuses=statuses)
        finally:
            session.close()

    def get_by_filepath(
        self, filepath: str, *, statuses: Iterable[str] | None = None
    ) -> DownloadJobModel | None:
        if self._session is not None:
            return self._get_by_filepath(self._session, filepath, statuses=statuses)

        session = next(get_session())
        try:
            return self._get_by_filepath(session, filepath, statuses=statuses)
        finally:
            session.close()

    def update_job(self, job_id: str, **updates: Any) -> DownloadJobModel:
        if self._session is not None:
            return self._update_job(self._session, job_id, **updates)

        session = next(get_session())
        try:
            return self._update_job(session, job_id, **updates)
        finally:
            session.close()

    def _create_job(self, session: Session, payload: dict[str, Any]) -> DownloadJobModel:
        job = DownloadJobModel(**payload)
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def _list_jobs(
        self,
        session: Session,
        *,
        filetype: str | None = None,
        statuses: Iterable[str] | None = None,
    ) -> list[DownloadJobModel]:
        query = session.query(DownloadJobModel)
        if filetype:
            query = query.filter(DownloadJobModel.filetype == filetype)
        if statuses:
            query = query.filter(DownloadJobModel.status.in_(list(statuses)))
        return query.order_by(
            DownloadJobModel.progress.desc(), DownloadJobModel.created_at.desc()
        ).all()

    def _get_by_job_id(self, session: Session, job_id: str) -> DownloadJobModel | None:
        return session.query(DownloadJobModel).filter(DownloadJobModel.job_id == job_id).first()

    def _get_by_url(
        self,
        session: Session,
        url: str,
        *,
        statuses: Iterable[str] | None = None,
    ) -> DownloadJobModel | None:
        query = session.query(DownloadJobModel).filter(DownloadJobModel.url == url)
        if statuses:
            query = query.filter(DownloadJobModel.status.in_(list(statuses)))
        return query.first()

    def _get_by_filepath(
        self,
        session: Session,
        filepath: str,
        *,
        statuses: Iterable[str] | None = None,
    ) -> DownloadJobModel | None:
        query = session.query(DownloadJobModel).filter(DownloadJobModel.filepath == filepath)
        if statuses:
            query = query.filter(DownloadJobModel.status.in_(list(statuses)))
        return query.first()

    def _update_job(self, session: Session, job_id: str, **updates: Any) -> DownloadJobModel:
        job = session.query(DownloadJobModel).filter(DownloadJobModel.job_id == job_id).one()
        for key, value in updates.items():
            setattr(job, key, value)
        session.commit()
        session.refresh(job)
        return job
