import platform
from dataclasses import dataclass

from app.core.config import get_settings
from app.modules.catalog.repository import CatalogRepository
from app.modules.catalog.service import AppManifest, CatalogSyncService, ManifestScanner
from app.modules.orchestration.service import AppOrchestrator
from app.modules.platform_core.schemas import (
    AvailableVersion,
    AvailableVersionsResponse,
    HealthResponse,
    LatestVersionResponse,
    ServiceSlim,
    SubscribeReleaseNotesRequest,
    SuccessMessageResponse,
    SystemInformationResponse,
    SystemSettingResponse,
    SystemUpdateLogsResponse,
    SystemUpdateRequestResponse,
    SystemUpdateStatus,
)
from app.modules.platform_core.state import SystemSettingsService, SystemUpdateService

SERVICE_VERSION_CATALOG: dict[str, tuple[str, ...]] = {
    "nomad_kiwix_server": ("3.8.1", "3.9.0"),
    "nomad_qdrant": ("v1.13.4", "v1.14.2"),
    "nomad_ollama": ("0.11.0", "0.11.2"),
    "nomad_flatnotes": ("latest",),
    "nomad_cyberchef": ("latest",),
    "nomad_kolibri": ("latest",),
    "nomad_maps": ("builtin-local",),
    "nomad_benchmark_helper": ("3.20",),
}


@dataclass(slots=True)
class ServiceInstallResult:
    service_name: str
    installed_services: list[str]


class ServiceRecordContainerAdapter:
    def __init__(self, repository: CatalogRepository | None = None) -> None:
        self.repository = repository or CatalogRepository()

    def install(self, manifest: AppManifest) -> None:
        self.repository.update_service_record(
            manifest.id,
            installed=True,
            installation_status="installing",
            status="starting",
        )

    def start(self, service_name: str) -> None:
        self.repository.update_service_record(
            service_name,
            installed=True,
            installation_status="installed",
            status="running",
        )

    def stop(self, service_name: str) -> None:
        self.repository.update_service_record(service_name, status="stopped")

    def remove(self, service_name: str) -> None:
        self.repository.update_service_record(
            service_name,
            installed=False,
            installation_status="idle",
            status=None,
        )

    def update(self, manifest: AppManifest) -> None:
        self.repository.update_service_record(
            manifest.id,
            available_update_version=None,
            installation_status="installed",
        )


class PlatformStatusService:
    def get_health(self) -> HealthResponse:
        settings = get_settings()
        return HealthResponse(status="ok", service="atlas-haven-api", version=settings.version)

    def get_system_information(self) -> SystemInformationResponse:
        settings = get_settings()
        catalog_count = len(CatalogRepository().list_services())
        return SystemInformationResponse(
            app_name="Atlas Haven",
            version=settings.version,
            environment=settings.environment,
            python_version=platform.python_version(),
            workspace_root=str(settings.workspace_root),
            storage_path=str(settings.storage_path),
            catalog_entries=catalog_count,
        )

    def get_internet_status(self) -> bool:
        return SystemUpdateService().internet_reachable()

    def list_services(self, installed_only: bool = False) -> list[ServiceSlim]:
        services = CatalogRepository().list_services(installed_only=installed_only)
        return [self._to_service_slim(service) for service in services]

    def _to_service_slim(self, payload: dict[str, object]) -> ServiceSlim:
        manifest = payload.get("manifest", {})
        if not isinstance(manifest, dict):
            manifest = {}
        runtime = manifest.get("runtime", {})
        if not isinstance(runtime, dict):
            runtime = {}
        ports = runtime.get("ports", [])
        launch_url = None
        if payload["service_name"] == "nomad_maps":
            launch_url = "http://127.0.0.1:3000/maps"
        elif isinstance(ports, list) and ports:
            first_port = ports[0]
            if isinstance(first_port, dict) and "host" in first_port:
                launch_url = f"http://127.0.0.1:{first_port['host']}"

        container_image = str(payload["container_image"])
        current_version = self._extract_image_version(container_image)
        return ServiceSlim.model_validate(
            {
                **payload,
                "kind": payload.get("manifest", {}).get("kind")
                if isinstance(payload.get("manifest"), dict)
                else payload.get("kind"),
                "current_version": current_version,
                "launch_url": launch_url,
            }
        )

    def _extract_image_version(self, image: str) -> str | None:
        if image.startswith("builtin://"):
            return image.removeprefix("builtin://")
        if ":" not in image:
            return None
        return image.rsplit(":", 1)[1]


class SystemServiceManager:
    def __init__(
        self,
        repository: CatalogRepository | None = None,
        scanner: ManifestScanner | None = None,
    ) -> None:
        self.repository = repository or CatalogRepository()
        self.scanner = scanner or ManifestScanner()
        self.adapter = ServiceRecordContainerAdapter(self.repository)

    def list_services(self, installed_only: bool = False) -> list[ServiceSlim]:
        services = self.repository.list_services(installed_only=installed_only)
        platform_status = PlatformStatusService()
        return [platform_status._to_service_slim(service) for service in services]

    def install_service(self, service_name: str) -> ServiceInstallResult:
        self._ensure_catalog()
        manifests = {manifest.id: manifest for manifest in self.scanner.scan()}
        if service_name not in manifests:
            raise ValueError(f"Unknown service: {service_name}")

        install_order = self._resolve_install_order(service_name, manifests)
        installed_services: list[str] = []
        for target in install_order:
            existing = self.repository.get_service(target)
            if existing and existing["installed"]:
                continue
            AppOrchestrator(self.adapter).install_app(manifests[target])
            installed_services.append(target)

        return ServiceInstallResult(
            service_name=service_name,
            installed_services=installed_services,
        )

    def affect_service(self, service_name: str, action: str) -> None:
        self._ensure_catalog()
        service = self.repository.get_service(service_name)
        if service is None:
            raise ValueError(f"Unknown service: {service_name}")
        if not service["installed"]:
            raise ValueError(f"Service is not installed: {service_name}")

        if action == "start":
            self.adapter.start(service_name)
            return
        if action == "stop":
            self.adapter.stop(service_name)
            return
        if action == "restart":
            self.adapter.stop(service_name)
            self.adapter.start(service_name)
            return
        raise ValueError(f"Unsupported action: {action}")

    def force_reinstall_service(self, service_name: str) -> SuccessMessageResponse:
        self._ensure_catalog()
        manifests = {manifest.id: manifest for manifest in self.scanner.scan()}
        manifest = manifests.get(service_name)
        if manifest is None:
            raise ValueError(f"Unknown service: {service_name}")
        service = self.repository.get_service(service_name)
        orchestrator = AppOrchestrator(self.adapter)
        if service and service["installed"]:
            orchestrator.reinstall_app(manifest)
        else:
            orchestrator.install_app(manifest)
        return SuccessMessageResponse(
            success=True,
            message=f"Reinstalled service {service_name}",
        )

    def check_service_updates(self) -> SuccessMessageResponse:
        self._ensure_catalog()
        for service in self.repository.list_services(installed_only=True):
            versions = SERVICE_VERSION_CATALOG.get(service["service_name"], ())
            latest = versions[-1] if versions else None
            current = PlatformStatusService()._extract_image_version(
                str(service["container_image"])
            )
            self.repository.update_service_record(
                service["service_name"],
                available_update_version=(latest if latest and latest != current else None),
            )
        return SuccessMessageResponse(
            success=True,
            message="Checked installed services for updates",
        )

    def get_available_versions(self, service_name: str) -> AvailableVersionsResponse:
        self._ensure_catalog()
        service = self.repository.get_service(service_name)
        if service is None:
            raise ValueError(f"Unknown service: {service_name}")
        versions = SERVICE_VERSION_CATALOG.get(service_name)
        if versions is None:
            current = PlatformStatusService()._extract_image_version(
                str(service["container_image"])
            )
            versions = tuple(filter(None, [current]))
        latest = versions[-1] if versions else None
        return AvailableVersionsResponse(
            versions=[
                AvailableVersion(
                    tag=tag,
                    isLatest=tag == latest,
                    releaseUrl=f"https://atlas-haven.local/releases/{service_name}/{tag}",
                )
                for tag in versions
            ]
        )

    def update_service(self, service_name: str, target_version: str) -> SuccessMessageResponse:
        self._ensure_catalog()
        service = self.repository.get_service(service_name)
        if service is None:
            raise ValueError(f"Unknown service: {service_name}")
        if not service["installed"]:
            raise ValueError(f"Service is not installed: {service_name}")
        versions = [version.tag for version in self.get_available_versions(service_name).versions]
        if target_version not in versions:
            raise ValueError(f"Unsupported target version for {service_name}: {target_version}")

        manifest = service.get("manifest", {})
        runtime = manifest.get("runtime", {}) if isinstance(manifest, dict) else {}
        if runtime.get("builtin"):
            next_image = str(service["container_image"])
        else:
            next_image = self._replace_image_tag(str(service["container_image"]), target_version)
        self.repository.update_catalog_entry(service_name, container_image=next_image)
        self.repository.update_service_record(
            service_name,
            available_update_version=None,
            installation_status="installed",
            status="running",
        )
        return SuccessMessageResponse(
            success=True,
            message=f"Updated {service_name} to {target_version}",
        )

    def _ensure_catalog(self) -> None:
        if not self.repository.list_services():
            CatalogSyncService(repository=self.repository).sync_from_disk()

    def _resolve_install_order(
        self,
        service_name: str,
        manifests: dict[str, AppManifest],
    ) -> list[str]:
        order: list[str] = []
        visited: set[str] = set()

        def visit(target: str) -> None:
            if target in visited:
                return
            manifest = manifests.get(target)
            if manifest is None:
                raise ValueError(f"Unknown dependency: {target}")
            visited.add(target)
            for dependency in manifest.dependencies:
                visit(dependency)
            order.append(target)

        visit(service_name)
        return order

    def _replace_image_tag(self, image: str, target_version: str) -> str:
        if ":" not in image:
            return f"{image}:{target_version}"
        repository, _ = image.rsplit(":", 1)
        return f"{repository}:{target_version}"


class SystemUpdateManager:
    def __init__(
        self,
        update_service: SystemUpdateService | None = None,
        settings_service: SystemSettingsService | None = None,
    ) -> None:
        self.update_service = update_service or SystemUpdateService()
        self.settings_service = settings_service or SystemSettingsService()

    def get_latest_version(self) -> LatestVersionResponse:
        return LatestVersionResponse.model_validate(self.update_service.get_latest_version())

    def subscribe_release_notes(
        self, payload: SubscribeReleaseNotesRequest
    ) -> SuccessMessageResponse:
        self.update_service.subscribe_release_notes(payload.email)
        return SuccessMessageResponse(
            success=True,
            message=f"Subscribed {payload.email} to Atlas Haven release notes.",
        )

    def request_update(self) -> SystemUpdateRequestResponse:
        return SystemUpdateRequestResponse.model_validate(self.update_service.request_update())

    def get_update_status(self) -> SystemUpdateStatus:
        return SystemUpdateStatus.model_validate(self.update_service.get_status())

    def get_update_logs(self) -> SystemUpdateLogsResponse:
        return SystemUpdateLogsResponse(logs=self.update_service.get_logs())

    def get_setting(self, key: str) -> SystemSettingResponse:
        return SystemSettingResponse(key=key, value=self.settings_service.get_setting(key))

    def update_setting(self, key: str, value: object | None) -> SuccessMessageResponse:
        self.settings_service.update_setting(key, value)
        return SuccessMessageResponse(
            success=True,
            message=f"Updated system setting {key}",
        )
