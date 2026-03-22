from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ManifestRefreshChanged(BaseModel):
    zim_categories: bool
    maps: bool
    wikipedia: bool


class ManifestRefreshResponse(BaseModel):
    success: bool
    changed: ManifestRefreshChanged


class ResourceUpdateInfo(BaseModel):
    resource_id: str
    resource_type: Literal["zim", "map"]
    installed_version: str
    latest_version: str
    download_url: str


class ContentUpdateCheckResult(BaseModel):
    updates: list[ResourceUpdateInfo] = Field(default_factory=list)
    checked_at: datetime
    error: str | None = None


class ContentUpdateApplyResponse(BaseModel):
    success: bool
    jobId: str | None = None
    error: str | None = None


class ContentUpdateApplyAllRequest(BaseModel):
    updates: list[ResourceUpdateInfo] = Field(default_factory=list)


class ContentUpdateApplyAllItemResult(BaseModel):
    resource_id: str
    success: bool
    jobId: str | None = None
    error: str | None = None


class ContentUpdateApplyAllResponse(BaseModel):
    results: list[ContentUpdateApplyAllItemResult] = Field(default_factory=list)
