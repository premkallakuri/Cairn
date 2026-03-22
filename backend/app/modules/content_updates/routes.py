from fastapi import APIRouter

from app.modules.content_updates.schemas import (
    ContentUpdateApplyAllRequest,
    ContentUpdateApplyAllResponse,
    ContentUpdateApplyResponse,
    ContentUpdateCheckResult,
    ManifestRefreshResponse,
    ResourceUpdateInfo,
)
from app.modules.content_updates.service import ContentUpdatesService

router = APIRouter(tags=["content-updates"])


@router.post("/manifests/refresh", response_model=ManifestRefreshResponse)
def refresh_manifests() -> ManifestRefreshResponse:
    return ContentUpdatesService().refresh_manifests()


@router.post("/content-updates/check", response_model=ContentUpdateCheckResult)
def check_content_updates() -> ContentUpdateCheckResult:
    return ContentUpdatesService().check_updates()


@router.post("/content-updates/apply", response_model=ContentUpdateApplyResponse)
def apply_content_update(update: ResourceUpdateInfo) -> ContentUpdateApplyResponse:
    return ContentUpdatesService().apply_update(update)


@router.post("/content-updates/apply-all", response_model=ContentUpdateApplyAllResponse)
def apply_all_content_updates(
    request: ContentUpdateApplyAllRequest,
) -> ContentUpdateApplyAllResponse:
    return ContentUpdatesService().apply_all_updates(request)
