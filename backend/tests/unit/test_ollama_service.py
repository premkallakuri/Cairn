import pytest

from app.modules.catalog.service import CatalogSyncService
from app.modules.downloads.service import DownloadJobService
from app.modules.ollama.service import OllamaService
from app.modules.platform_core.service import SystemServiceManager

pytestmark = [pytest.mark.unit, pytest.mark.ollama]


def test_available_models_support_filtering_and_limits() -> None:
    service = OllamaService()

    response = service.list_available_models(recommended_only=True, query="llama", limit=1)

    assert len(response.models) == 1
    assert response.models[0].id == "llama3.2:1b-text-q2_K"
    assert response.hasMore is True


def test_download_and_delete_model_updates_local_inventory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(OllamaService, "_pull_ollama_model", lambda self, tag: None)
    monkeypatch.setattr(OllamaService, "_delete_ollama_model", lambda self, tag: None)
    service = OllamaService()

    queued = service.queue_model_download("llama3.2:1b-text-q2_K")
    installed = service.list_installed_models()

    assert queued.success is True
    assert installed[0]["name"] == "llama3.2:1b-text-q2_K"
    assert installed[0]["status"] == "installed"
    assert DownloadJobService().list_download_jobs("model") == []

    deleted = service.delete_model("llama3.2:1b-text-q2_K")

    assert deleted.success is True
    assert service.list_installed_models() == []


def test_install_service_resolves_qdrant_before_ollama() -> None:
    CatalogSyncService().sync_from_disk()
    manager = SystemServiceManager()

    result = manager.install_service("nomad_ollama")

    assert result.installed_services == ["nomad_qdrant", "nomad_ollama"]
    services = {
        service.service_name: service for service in manager.list_services(installed_only=True)
    }
    assert services["nomad_qdrant"].status == "running"
    assert services["nomad_ollama"].status == "running"
