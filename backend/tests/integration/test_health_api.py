import pytest

pytestmark = [pytest.mark.integration, pytest.mark.platform]


def test_health_endpoint_returns_ok(client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_services_endpoint_is_seeded_from_app_catalog(client) -> None:
    response = client.get("/api/system/services")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 8
    assert any(service["service_name"] == "nomad_kiwix_server" for service in payload)


def test_docs_endpoint_lists_workspace_docs(client) -> None:
    response = client.get("/api/docs/list")

    assert response.status_code == 200
    payload = response.json()
    assert any(item["slug"] == "architecture/overview" for item in payload)
