from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.easy_setup.models import EasySetupDraftModel
from app.modules.easy_setup.schemas import EasySetupDraft

DEFAULT_DRAFT_ID = "default"


class EasySetupRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def get_draft(self) -> EasySetupDraft:
        if self._session is not None:
            model = self._get_or_create_default_draft(self._session)
            return self._to_schema(model)

        session = next(get_session())
        try:
            model = self._get_or_create_default_draft(session)
            return self._to_schema(model)
        finally:
            session.close()

    def save_draft(self, draft: EasySetupDraft) -> EasySetupDraft:
        if self._session is not None:
            model = self._save_draft(self._session, draft)
            return self._to_schema(model)

        session = next(get_session())
        try:
            model = self._save_draft(session, draft)
            return self._to_schema(model)
        finally:
            session.close()

    def _get_or_create_default_draft(self, session: Session) -> EasySetupDraftModel:
        draft = session.get(EasySetupDraftModel, DEFAULT_DRAFT_ID)
        if draft is None:
            draft = EasySetupDraftModel(draft_id=DEFAULT_DRAFT_ID)
            session.add(draft)
            session.commit()
            session.refresh(draft)
        return draft

    def _save_draft(self, session: Session, draft: EasySetupDraft) -> EasySetupDraftModel:
        model = self._get_or_create_default_draft(session)
        model.current_step = draft.currentStep
        model.selected_capability_ids_json = json.dumps(draft.selectedCapabilityIds)
        model.selected_map_collection_slugs_json = json.dumps(draft.selectedMapCollectionSlugs)
        model.selected_category_tier_slugs_json = json.dumps(draft.selectedCategoryTierSlugs)
        model.selected_ai_model_ids_json = json.dumps(draft.selectedAiModelIds)
        model.selected_wikipedia_option_id = draft.selectedWikipediaOptionId
        session.add(model)
        session.commit()
        session.refresh(model)
        return model

    def _to_schema(self, model: EasySetupDraftModel) -> EasySetupDraft:
        return EasySetupDraft(
            currentStep=model.current_step,
            selectedCapabilityIds=json.loads(model.selected_capability_ids_json),
            selectedMapCollectionSlugs=json.loads(model.selected_map_collection_slugs_json),
            selectedCategoryTierSlugs=json.loads(model.selected_category_tier_slugs_json),
            selectedAiModelIds=json.loads(model.selected_ai_model_ids_json),
            selectedWikipediaOptionId=model.selected_wikipedia_option_id,
        )
