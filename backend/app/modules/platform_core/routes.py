from fastapi import APIRouter, HTTPException, Query

from app.modules.platform_core.schemas import (
    AffectServiceRequest,
    AvailableVersionsResponse,
    HealthResponse,
    InstallServiceRequest,
    LatestVersionResponse,
    ServiceSlim,
    SubscribeReleaseNotesRequest,
    SuccessMessageResponse,
    SystemInformationResponse,
    SystemSettingResponse,
    SystemUpdateLogsResponse,
    SystemUpdateRequestResponse,
    SystemUpdateStatus,
    UpdateServiceRequest,
    UpdateSystemSettingRequest,
)
from app.modules.platform_core.service import (
    PlatformStatusService,
    SystemServiceManager,
    SystemUpdateManager,
)

router = APIRouter(tags=["platform"])


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return PlatformStatusService().get_health()


@router.get("/system/info", response_model=SystemInformationResponse)
def get_system_info() -> SystemInformationResponse:
    return PlatformStatusService().get_system_information()


@router.get("/system/internet-status", response_model=bool)
def get_internet_status() -> bool:
    return PlatformStatusService().get_internet_status()


@router.get("/system/services", response_model=list[ServiceSlim])
def list_services(installed_only: bool = Query(False, alias="installedOnly")) -> list[ServiceSlim]:
    return PlatformStatusService().list_services(installed_only=installed_only)


@router.post("/system/services/install", response_model=SuccessMessageResponse)
def install_service(payload: InstallServiceRequest) -> SuccessMessageResponse:
    try:
        result = SystemServiceManager().install_service(payload.service_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    installed = (
        ", ".join(result.installed_services) if result.installed_services else payload.service_name
    )
    return SuccessMessageResponse(success=True, message=f"Installed services: {installed}")


@router.post("/system/services/affect", response_model=SuccessMessageResponse)
def affect_service(payload: AffectServiceRequest) -> SuccessMessageResponse:
    try:
        SystemServiceManager().affect_service(payload.service_name, payload.action)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SuccessMessageResponse(
        success=True,
        message=f"{payload.action.title()} requested for {payload.service_name}",
    )


@router.post("/system/services/force-reinstall", response_model=SuccessMessageResponse)
def force_reinstall_service(payload: InstallServiceRequest) -> SuccessMessageResponse:
    try:
        return SystemServiceManager().force_reinstall_service(payload.service_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/system/services/check-updates", response_model=SuccessMessageResponse)
def check_service_updates() -> SuccessMessageResponse:
    return SystemServiceManager().check_service_updates()


@router.get(
    "/system/services/{name}/available-versions",
    response_model=AvailableVersionsResponse,
)
def get_available_service_versions(name: str) -> AvailableVersionsResponse:
    try:
        return SystemServiceManager().get_available_versions(name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/system/services/update", response_model=SuccessMessageResponse)
def update_service(payload: UpdateServiceRequest) -> SuccessMessageResponse:
    try:
        return SystemServiceManager().update_service(
            payload.service_name,
            payload.target_version,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/system/subscribe-release-notes", response_model=SuccessMessageResponse)
def subscribe_release_notes(payload: SubscribeReleaseNotesRequest) -> SuccessMessageResponse:
    return SystemUpdateManager().subscribe_release_notes(payload)


@router.get("/system/latest-version", response_model=LatestVersionResponse)
def get_latest_version(force: bool = Query(False)) -> LatestVersionResponse:
    del force
    return SystemUpdateManager().get_latest_version()


@router.post("/system/update", response_model=SystemUpdateRequestResponse)
def request_system_update() -> SystemUpdateRequestResponse:
    try:
        return SystemUpdateManager().request_update()
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/system/update/status", response_model=SystemUpdateStatus)
def get_system_update_status() -> SystemUpdateStatus:
    return SystemUpdateManager().get_update_status()


@router.get("/system/update/logs", response_model=SystemUpdateLogsResponse)
def get_system_update_logs() -> SystemUpdateLogsResponse:
    return SystemUpdateManager().get_update_logs()


@router.get("/system/settings", response_model=SystemSettingResponse)
def get_system_setting(key: str = Query(...)) -> SystemSettingResponse:
    return SystemUpdateManager().get_setting(key)


@router.patch("/system/settings", response_model=SuccessMessageResponse)
def update_system_setting(payload: UpdateSystemSettingRequest) -> SuccessMessageResponse:
    return SystemUpdateManager().update_setting(payload.key, payload.value)
