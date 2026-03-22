import pytest

pytestmark = [pytest.mark.integration, pytest.mark.platform]


def test_app_roundout_install_and_restart_flow(client) -> None:
    response = client.post("/api/system/services/install", json={"service_name": "nomad_flatnotes"})

    assert response.status_code == 200
    services = {
        item["service_name"]: item
        for item in client.get("/api/system/services?installedOnly=true").json()
    }
    assert services["nomad_flatnotes"]["launch_url"] == "http://127.0.0.1:8081"
    assert services["nomad_flatnotes"]["status"] == "running"

    restarted = client.post(
        "/api/system/services/affect",
        json={"service_name": "nomad_flatnotes", "action": "restart"},
    )

    assert restarted.status_code == 200
    refreshed = {
        item["service_name"]: item
        for item in client.get("/api/system/services?installedOnly=true").json()
    }
    assert refreshed["nomad_flatnotes"]["status"] == "running"


def test_versions_and_update_endpoints_work_for_installed_service(client) -> None:
    client.post("/api/system/services/install", json={"service_name": "nomad_qdrant"})

    versions = client.get("/api/system/services/nomad_qdrant/available-versions")
    assert versions.status_code == 200
    assert versions.json()["versions"][-1]["tag"] == "v1.14.2"

    checked = client.post("/api/system/services/check-updates")
    assert checked.status_code == 200

    services = {
        item["service_name"]: item
        for item in client.get("/api/system/services?installedOnly=true").json()
    }
    assert services["nomad_qdrant"]["available_update_version"] == "v1.14.2"

    updated = client.post(
        "/api/system/services/update",
        json={"service_name": "nomad_qdrant", "target_version": "v1.14.2"},
    )
    assert updated.status_code == 200

    refreshed = {
        item["service_name"]: item
        for item in client.get("/api/system/services?installedOnly=true").json()
    }
    assert refreshed["nomad_qdrant"]["current_version"] == "v1.14.2"
    assert refreshed["nomad_qdrant"]["available_update_version"] is None


def test_force_reinstall_endpoint_keeps_service_installed(client) -> None:
    client.post("/api/system/services/install", json={"service_name": "nomad_cyberchef"})

    response = client.post(
        "/api/system/services/force-reinstall",
        json={"service_name": "nomad_cyberchef"},
    )

    assert response.status_code == 200
    services = {
        item["service_name"]: item
        for item in client.get("/api/system/services?installedOnly=true").json()
    }
    assert services["nomad_cyberchef"]["installed"] is True
    assert services["nomad_cyberchef"]["status"] == "running"


def test_system_metadata_and_settings_endpoints_work(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.modules.platform_core.state.SystemUpdateService.internet_reachable",
        lambda self: True,
    )

    internet = client.get("/api/system/internet-status")
    assert internet.status_code == 200
    assert internet.json() is True

    latest = client.get("/api/system/latest-version")
    assert latest.status_code == 200
    assert latest.json()["updateAvailable"] is False

    setting = client.get("/api/system/settings", params={"key": "chat.suggestionsEnabled"})
    assert setting.status_code == 200
    assert setting.json()["value"] is True

    updated = client.patch(
        "/api/system/settings",
        json={"key": "chat.suggestionsEnabled", "value": False},
    )
    assert updated.status_code == 200

    refreshed = client.get("/api/system/settings", params={"key": "chat.suggestionsEnabled"})
    assert refreshed.status_code == 200
    assert refreshed.json()["value"] is False


def test_system_update_and_release_notes_endpoints_work(client) -> None:
    subscribed = client.post(
        "/api/system/subscribe-release-notes",
        json={"email": "operator@example.test"},
    )
    assert subscribed.status_code == 200

    update = client.post("/api/system/update")
    assert update.status_code == 200
    assert update.json()["success"] is True

    status = client.get("/api/system/update/status")
    assert status.status_code == 200
    assert status.json()["stage"] == "complete"

    logs = client.get("/api/system/update/logs")
    assert logs.status_code == 200
    assert "bundled version already active" in logs.json()["logs"]
