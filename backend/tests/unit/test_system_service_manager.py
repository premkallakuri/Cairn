import pytest

from app.modules.catalog.service import CatalogSyncService
from app.modules.platform_core.service import (
    PlatformStatusService,
    SystemServiceManager,
    SystemUpdateManager,
)

pytestmark = [pytest.mark.unit, pytest.mark.platform]


def test_service_manager_exposes_launch_urls_for_sibling_apps() -> None:
    CatalogSyncService().sync_from_disk()
    manager = SystemServiceManager()

    services = {service.service_name: service for service in manager.list_services()}

    assert services["nomad_flatnotes"].launch_url == "http://127.0.0.1:8081"
    assert services["nomad_cyberchef"].launch_url == "http://127.0.0.1:8001"
    assert services["nomad_kolibri"].launch_url == "http://127.0.0.1:8085"


def test_service_manager_checks_updates_and_applies_target_version() -> None:
    CatalogSyncService().sync_from_disk()
    manager = SystemServiceManager()
    manager.install_service("nomad_qdrant")

    versions = manager.get_available_versions("nomad_qdrant")
    assert versions.versions[-1].tag == "v1.14.2"
    assert versions.versions[-1].isLatest is True

    result = manager.check_service_updates()
    assert result.success is True

    installed = {
        service.service_name: service for service in manager.list_services(installed_only=True)
    }
    assert installed["nomad_qdrant"].available_update_version == "v1.14.2"

    updated = manager.update_service("nomad_qdrant", "v1.14.2")

    assert updated.success is True
    refreshed = {
        service.service_name: service for service in manager.list_services(installed_only=True)
    }
    assert refreshed["nomad_qdrant"].current_version == "v1.14.2"
    assert refreshed["nomad_qdrant"].available_update_version is None


def test_force_reinstall_keeps_app_running() -> None:
    CatalogSyncService().sync_from_disk()
    manager = SystemServiceManager()
    manager.install_service("nomad_flatnotes")

    reinstalled = manager.force_reinstall_service("nomad_flatnotes")

    assert reinstalled.success is True
    service = next(
        item
        for item in manager.list_services(installed_only=True)
        if item.service_name == "nomad_flatnotes"
    )
    assert service.installed is True
    assert service.status == "running"


def test_system_update_manager_tracks_local_version_and_settings() -> None:
    manager = SystemUpdateManager()

    latest = manager.get_latest_version()
    assert latest.success is True
    assert latest.updateAvailable is False
    assert latest.currentVersion == latest.latestVersion

    updated = manager.update_setting("chat.lastModel", "llama3.2:1b-text-q2_K")
    assert updated.success is True

    setting = manager.get_setting("chat.lastModel")
    assert setting.value == "llama3.2:1b-text-q2_K"

    request = manager.request_update()
    assert request.success is True

    status = manager.get_update_status()
    assert status.stage == "complete"
    assert status.progress == 100

    logs = manager.get_update_logs()
    assert "bundled version already active" in logs.logs


def test_platform_status_service_reports_internet_state(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.modules.platform_core.state.SystemUpdateService.internet_reachable",
        lambda self: True,
    )

    assert PlatformStatusService().get_internet_status() is True
