from unittest.mock import MagicMock, patch

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.ollama]


def test_install_service_endpoint_installs_dependencies(client) -> None:
    response = client.post("/api/system/services/install", json={"service_name": "nomad_ollama"})

    assert response.status_code == 200
    assert response.json()["success"] is True

    services = client.get("/api/system/services?installedOnly=true")
    payload = {item["service_name"]: item for item in services.json()}
    assert payload["nomad_qdrant"]["installed"] is True
    assert payload["nomad_qdrant"]["status"] == "running"
    assert payload["nomad_ollama"]["installed"] is True
    assert payload["nomad_ollama"]["status"] == "running"


def test_affect_service_endpoint_changes_runtime_state(client) -> None:
    client.post("/api/system/services/install", json={"service_name": "nomad_qdrant"})

    response = client.post(
        "/api/system/services/affect",
        json={"service_name": "nomad_qdrant", "action": "stop"},
    )

    assert response.status_code == 200
    services = client.get("/api/system/services?installedOnly=true").json()
    qdrant = next(item for item in services if item["service_name"] == "nomad_qdrant")
    assert qdrant["status"] == "stopped"


@patch("app.modules.ollama.service.subprocess.run", return_value=MagicMock(returncode=0))
@patch("app.modules.ollama.service.shutil.which", return_value="/fake/ollama")
def test_ollama_models_endpoints_manage_local_model_inventory(mock_which, mock_run, client) -> None:
    available = client.get("/api/ollama/models", params={"recommendedOnly": "true", "limit": 2})

    assert available.status_code == 200
    payload = available.json()
    assert len(payload["models"]) == 2
    assert payload["hasMore"] is True

    queued = client.post("/api/ollama/models", json={"model": "llama3.2:1b-text-q2_K"})

    assert queued.status_code == 200
    assert queued.json()["success"] is True
    assert mock_run.called

    installed = client.get("/api/ollama/installed-models")
    installed_payload = installed.json()
    assert len(installed_payload) == 1
    assert installed_payload[0]["name"] == "llama3.2:1b-text-q2_K"
    assert installed_payload[0]["status"] == "installed"

    jobs = client.get("/api/downloads/jobs/model")
    assert jobs.status_code == 200
    assert jobs.json() == []

    deleted = client.request(
        "DELETE",
        "/api/ollama/models",
        json={"model": "llama3.2:1b-text-q2_K"},
    )

    assert deleted.status_code == 200
    assert deleted.json()["success"] is True
    assert client.get("/api/ollama/installed-models").json() == []
