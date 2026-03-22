from typing import Any, Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class SystemInformationResponse(BaseModel):
    app_name: str
    version: str
    environment: str
    python_version: str
    workspace_root: str
    storage_path: str
    catalog_entries: int


class ServiceSlim(BaseModel):
    id: int
    service_name: str
    friendly_name: str | None
    description: str | None
    icon: str | None
    installed: bool
    installation_status: str
    status: str | None
    ui_location: str | None
    powered_by: str | None
    display_order: int | None
    container_image: str
    available_update_version: str | None = None
    kind: str | None = None
    current_version: str | None = None
    launch_url: str | None = None


class SuccessMessageResponse(BaseModel):
    success: bool
    message: str


class InstallServiceRequest(BaseModel):
    service_name: str


class AffectServiceRequest(BaseModel):
    service_name: str
    action: Literal["start", "stop", "restart"]


class UpdateServiceRequest(BaseModel):
    service_name: str
    target_version: str


class AvailableVersion(BaseModel):
    tag: str
    isLatest: bool
    releaseUrl: str | None = None


class AvailableVersionsResponse(BaseModel):
    versions: list[AvailableVersion]


class SubscribeReleaseNotesRequest(BaseModel):
    email: str


class LatestVersionResponse(BaseModel):
    success: bool
    updateAvailable: bool
    currentVersion: str
    latestVersion: str
    message: str | None = None


class SystemUpdateStatus(BaseModel):
    stage: Literal["idle", "starting", "pulling", "pulled", "recreating", "complete", "error"]
    progress: float
    message: str
    timestamp: str


class SystemUpdateRequestResponse(BaseModel):
    success: bool | None = None
    message: str | None = None
    note: str | None = None
    error: str | None = None


class SystemUpdateLogsResponse(BaseModel):
    logs: str


class SystemSettingResponse(BaseModel):
    key: str
    value: Any | None = None


class UpdateSystemSettingRequest(BaseModel):
    key: Literal[
        "chat.suggestionsEnabled",
        "chat.lastModel",
        "ui.hasVisitedEasySetup",
        "system.earlyAccess",
        "ai.assistantCustomName",
    ]
    value: Any | None = None
