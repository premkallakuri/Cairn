from datetime import datetime
from app.core.compat import UTC

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WikipediaSelectionModel(Base):
    __tablename__ = "wikipedia_selections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    option_id: Mapped[str] = mapped_column(String(64), default="none")
    status: Mapped[str] = mapped_column(String(32), default="none")
    filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
