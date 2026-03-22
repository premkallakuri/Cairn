from fastapi import APIRouter

from app.modules.easy_setup.schemas import (
    CategoryWithStatus,
    EasySetupBootstrapResponse,
    EasySetupDraft,
    EasySetupPlan,
)
from app.modules.easy_setup.service import EasySetupService

router = APIRouter(tags=["easy-setup"])


@router.get("/curated-categories", response_model=list[CategoryWithStatus])
def list_curated_categories() -> list[CategoryWithStatus]:
    return EasySetupService().list_curated_categories()


@router.get("/bootstrap", response_model=EasySetupBootstrapResponse)
def get_bootstrap() -> EasySetupBootstrapResponse:
    return EasySetupService().get_bootstrap()


@router.get("/draft", response_model=EasySetupDraft)
def get_draft() -> EasySetupDraft:
    return EasySetupService().get_draft()


@router.put("/draft", response_model=EasySetupDraft)
def save_draft(draft: EasySetupDraft) -> EasySetupDraft:
    return EasySetupService().save_draft(draft)


@router.post("/plan", response_model=EasySetupPlan)
def build_plan(draft: EasySetupDraft) -> EasySetupPlan:
    return EasySetupService().build_plan(draft)
