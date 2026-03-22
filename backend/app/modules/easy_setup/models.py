from datetime import datetime
from app.core.compat import UTC

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EasySetupDraftModel(Base):
    __tablename__ = "easy_setup_drafts"

    draft_id: Mapped[str] = mapped_column(String(32), primary_key=True, default="default")
    current_step: Mapped[int] = mapped_column(Integer, default=1)
    selected_capability_ids_json: Mapped[str] = mapped_column(Text(), default="[]")
    selected_map_collection_slugs_json: Mapped[str] = mapped_column(Text(), default="[]")
    selected_category_tier_slugs_json: Mapped[str] = mapped_column(Text(), default="{}")
    selected_ai_model_ids_json: Mapped[str] = mapped_column(Text(), default="[]")
    selected_wikipedia_option_id: Mapped[str] = mapped_column(String(64), default="none")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
