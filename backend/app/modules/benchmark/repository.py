from __future__ import annotations

from datetime import datetime
from app.core.compat import UTC
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.benchmark.models import (
    BenchmarkResultModel,
    BenchmarkSettingsModel,
    BenchmarkStatusModel,
)


class BenchmarkRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def get_or_create_settings(self) -> BenchmarkSettingsModel:
        if self._session is not None:
            return self._get_or_create_settings(self._session)

        session = next(get_session())
        try:
            return self._get_or_create_settings(session)
        finally:
            session.close()

    def update_settings(self, **updates: object) -> BenchmarkSettingsModel:
        if self._session is not None:
            return self._update_settings(self._session, **updates)

        session = next(get_session())
        try:
            return self._update_settings(session, **updates)
        finally:
            session.close()

    def get_or_create_status(self) -> BenchmarkStatusModel:
        if self._session is not None:
            return self._get_or_create_status(self._session)

        session = next(get_session())
        try:
            return self._get_or_create_status(session)
        finally:
            session.close()

    def update_status(self, **updates: object) -> BenchmarkStatusModel:
        if self._session is not None:
            return self._update_status(self._session, **updates)

        session = next(get_session())
        try:
            return self._update_status(session, **updates)
        finally:
            session.close()

    def create_result(self, payload: dict[str, object]) -> BenchmarkResultModel:
        if self._session is not None:
            return self._create_result(self._session, payload)

        session = next(get_session())
        try:
            return self._create_result(session, payload)
        finally:
            session.close()

    def list_results(self) -> list[BenchmarkResultModel]:
        if self._session is not None:
            return self._list_results(self._session)

        session = next(get_session())
        try:
            return self._list_results(session)
        finally:
            session.close()

    def get_result(self, benchmark_id: str) -> BenchmarkResultModel | None:
        if self._session is not None:
            return self._get_result(self._session, benchmark_id)

        session = next(get_session())
        try:
            return self._get_result(session, benchmark_id)
        finally:
            session.close()

    def update_result(self, benchmark_id: str, **updates: object) -> BenchmarkResultModel:
        if self._session is not None:
            return self._update_result(self._session, benchmark_id, **updates)

        session = next(get_session())
        try:
            return self._update_result(session, benchmark_id, **updates)
        finally:
            session.close()

    def latest_result(self) -> BenchmarkResultModel | None:
        results = self.list_results()
        return results[0] if results else None

    def _get_or_create_settings(self, session: Session) -> BenchmarkSettingsModel:
        settings = session.get(BenchmarkSettingsModel, 1)
        if settings is None:
            settings = BenchmarkSettingsModel(
                id=1,
                allow_anonymous_submission=False,
                installation_id=str(uuid4()),
                last_benchmark_run=None,
            )
            session.add(settings)
            session.commit()
            session.refresh(settings)
        return settings

    def _update_settings(self, session: Session, **updates: object) -> BenchmarkSettingsModel:
        settings = self._get_or_create_settings(session)
        for key, value in updates.items():
            setattr(settings, key, value)
        session.commit()
        session.refresh(settings)
        return settings

    def _get_or_create_status(self, session: Session) -> BenchmarkStatusModel:
        status = session.get(BenchmarkStatusModel, 1)
        if status is None:
            status = BenchmarkStatusModel(
                id=1,
                status="idle",
                benchmark_id=None,
                message="Idle",
                progress=0,
                updated_at=datetime.now(UTC),
            )
            session.add(status)
            session.commit()
            session.refresh(status)
        return status

    def _update_status(self, session: Session, **updates: object) -> BenchmarkStatusModel:
        status = self._get_or_create_status(session)
        for key, value in updates.items():
            setattr(status, key, value)
        status.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(status)
        return status

    def _create_result(self, session: Session, payload: dict[str, object]) -> BenchmarkResultModel:
        result = BenchmarkResultModel(**payload)
        session.add(result)
        session.commit()
        session.refresh(result)
        return result

    def _list_results(self, session: Session) -> list[BenchmarkResultModel]:
        return (
            session.query(BenchmarkResultModel)
            .order_by(BenchmarkResultModel.created_at.desc(), BenchmarkResultModel.id.desc())
            .all()
        )

    def _get_result(self, session: Session, benchmark_id: str) -> BenchmarkResultModel | None:
        return (
            session.query(BenchmarkResultModel)
            .filter(BenchmarkResultModel.benchmark_id == benchmark_id)
            .first()
        )

    def _update_result(
        self,
        session: Session,
        benchmark_id: str,
        **updates: object,
    ) -> BenchmarkResultModel:
        result = self._get_result(session, benchmark_id)
        if result is None:
            raise ValueError(f"Benchmark not found: {benchmark_id}")
        for key, value in updates.items():
            setattr(result, key, value)
        result.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(result)
        return result
