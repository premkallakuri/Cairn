from __future__ import annotations

from datetime import datetime
from app.core.compat import UTC

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BenchmarkResultModel(Base):
    __tablename__ = "benchmark_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    benchmark_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    benchmark_type: Mapped[str] = mapped_column(String(32))
    cpu_model: Mapped[str] = mapped_column(String(255))
    cpu_cores: Mapped[int] = mapped_column(Integer)
    cpu_threads: Mapped[int] = mapped_column(Integer)
    ram_bytes: Mapped[int] = mapped_column(Integer)
    disk_type: Mapped[str] = mapped_column(String(32))
    gpu_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cpu_score: Mapped[float] = mapped_column(Float)
    memory_score: Mapped[float] = mapped_column(Float)
    disk_read_score: Mapped[float] = mapped_column(Float)
    disk_write_score: Mapped[float] = mapped_column(Float)
    ai_tokens_per_second: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_model_used: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ai_time_to_first_token: Mapped[float | None] = mapped_column(Float, nullable=True)
    nomad_score: Mapped[float] = mapped_column(Float)
    submitted_to_repository: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    repository_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    builder_tag: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class BenchmarkSettingsModel(Base):
    __tablename__ = "benchmark_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    allow_anonymous_submission: Mapped[bool] = mapped_column(Boolean, default=False)
    installation_id: Mapped[str] = mapped_column(String(128), unique=True)
    last_benchmark_run: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class BenchmarkStatusModel(Base):
    __tablename__ = "benchmark_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    status: Mapped[str] = mapped_column(String(64), default="idle")
    benchmark_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    message: Mapped[str] = mapped_column(Text(), default="Idle")
    progress: Mapped[float] = mapped_column(Float, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
