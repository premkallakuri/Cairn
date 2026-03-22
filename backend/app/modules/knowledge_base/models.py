from datetime import datetime
from app.core.compat import UTC

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class KnowledgeFileModel(Base):
    __tablename__ = "knowledge_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(1024), unique=True, index=True)
    extracted_text: Mapped[str] = mapped_column(Text())
    indexed_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class EmbedJobModel(Base):
    __tablename__ = "embed_jobs"

    job_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(1024), index=True)
    progress: Mapped[float] = mapped_column(Float(), default=0)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    error_message: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class KnowledgeChunkModel(Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_path: Mapped[str] = mapped_column(String(1024), index=True)
    source_name: Mapped[str] = mapped_column(String(255))
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text())
