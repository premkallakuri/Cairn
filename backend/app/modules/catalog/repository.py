import json

from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.catalog.models import AppCatalogEntryModel, ServiceRecordModel


class CatalogRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def upsert_catalog_entry(self, payload: dict[str, object]) -> None:
        if self._session is not None:
            self._upsert_catalog_entry(self._session, payload)
            return

        session = next(get_session())
        try:
            self._upsert_catalog_entry(session, payload)
        finally:
            session.close()

    def list_services(self, installed_only: bool = False) -> list[dict[str, object]]:
        if self._session is not None:
            return self._list_services(self._session, installed_only=installed_only)

        session = next(get_session())
        try:
            return self._list_services(session, installed_only=installed_only)
        finally:
            session.close()

    def get_service(self, service_name: str) -> dict[str, object] | None:
        if self._session is not None:
            return self._get_service(self._session, service_name)

        session = next(get_session())
        try:
            return self._get_service(session, service_name)
        finally:
            session.close()

    def update_service_record(self, service_name: str, **updates: object) -> None:
        if self._session is not None:
            self._update_service_record(self._session, service_name, **updates)
            return

        session = next(get_session())
        try:
            self._update_service_record(session, service_name, **updates)
        finally:
            session.close()

    def update_catalog_entry(self, service_name: str, **updates: object) -> None:
        if self._session is not None:
            self._update_catalog_entry(self._session, service_name, **updates)
            return

        session = next(get_session())
        try:
            self._update_catalog_entry(session, service_name, **updates)
        finally:
            session.close()

    def _upsert_catalog_entry(self, session: Session, payload: dict[str, object]) -> None:
        entry = session.get(AppCatalogEntryModel, payload["service_name"])
        if entry is None:
            entry = AppCatalogEntryModel(**payload)
            session.add(entry)
        else:
            for key, value in payload.items():
                setattr(entry, key, value)

        if (
            session.query(ServiceRecordModel)
            .filter_by(service_name=payload["service_name"])
            .first()
            is None
        ):
            session.add(ServiceRecordModel(service_name=payload["service_name"]))

        session.commit()

    def _list_services(
        self, session: Session, installed_only: bool = False
    ) -> list[dict[str, object]]:
        query = session.query(ServiceRecordModel, AppCatalogEntryModel).join(
            AppCatalogEntryModel,
            ServiceRecordModel.service_name == AppCatalogEntryModel.service_name,
        )
        if installed_only:
            query = query.filter(ServiceRecordModel.installed.is_(True))

        services: list[dict[str, object]] = []
        for service_record, catalog_entry in query.order_by(
            AppCatalogEntryModel.display_order.asc()
        ).all():
            services.append(self._serialize_service(service_record, catalog_entry))
        return services

    def _get_service(self, session: Session, service_name: str) -> dict[str, object] | None:
        row = (
            session.query(ServiceRecordModel, AppCatalogEntryModel)
            .join(
                AppCatalogEntryModel,
                ServiceRecordModel.service_name == AppCatalogEntryModel.service_name,
            )
            .filter(ServiceRecordModel.service_name == service_name)
            .first()
        )
        if row is None:
            return None
        service_record, catalog_entry = row
        return self._serialize_service(service_record, catalog_entry)

    def _update_service_record(
        self,
        session: Session,
        service_name: str,
        **updates: object,
    ) -> None:
        record = session.query(ServiceRecordModel).filter_by(service_name=service_name).first()
        if record is None:
            raise ValueError(f"Unknown service: {service_name}")
        for key, value in updates.items():
            setattr(record, key, value)
        session.commit()

    def _serialize_service(
        self,
        service_record: ServiceRecordModel,
        catalog_entry: AppCatalogEntryModel,
    ) -> dict[str, object]:
        return {
            "id": service_record.id,
            "service_name": service_record.service_name,
            "friendly_name": catalog_entry.friendly_name,
            "description": catalog_entry.description,
            "icon": catalog_entry.icon,
            "installed": service_record.installed,
            "installation_status": service_record.installation_status,
            "status": service_record.status,
            "ui_location": catalog_entry.ui_location,
            "powered_by": catalog_entry.powered_by,
            "display_order": catalog_entry.display_order,
            "container_image": catalog_entry.container_image,
            "available_update_version": service_record.available_update_version,
            "manifest": json.loads(catalog_entry.manifest_json),
        }

    def _update_catalog_entry(
        self,
        session: Session,
        service_name: str,
        **updates: object,
    ) -> None:
        entry = session.get(AppCatalogEntryModel, service_name)
        if entry is None:
            raise ValueError(f"Unknown catalog entry: {service_name}")
        for key, value in updates.items():
            setattr(entry, key, value)
        session.commit()
