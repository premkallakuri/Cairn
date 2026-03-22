from datetime import datetime
from app.core.compat import UTC

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AppCatalogEntryModel(Base):
    __tablename__ = "app_catalog_entries"

    service_name: Mapped[str] = mapped_column(String(128), primary_key=True)
    kind: Mapped[str] = mapped_column(String(64))
    friendly_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    icon: Mapped[str | None] = mapped_column(String(128), nullable=True)
    powered_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    display_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    container_image: Mapped[str] = mapped_column(String(255))
    ui_location: Mapped[str | None] = mapped_column(String(128), nullable=True)
    manifest_json: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class ServiceRecordModel(Base):
    __tablename__ = "service_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_name: Mapped[str] = mapped_column(String(128), unique=True)
    installed: Mapped[bool] = mapped_column(Boolean, default=False)
    installation_status: Mapped[str] = mapped_column(String(32), default="idle")
    status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    available_update_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
