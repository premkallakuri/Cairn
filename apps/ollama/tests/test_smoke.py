from pathlib import Path

import pytest

from app.core.config import reset_settings_cache
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory, reset_session_factory
from app.modules.ollama.service import OllamaService


@pytest.fixture(autouse=True)
def setup_app_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    db_path = tmp_path / "atlas-haven-ollama.db"
    monkeypatch.setenv("ATLAS_HAVEN_DATABASE_URL", f"sqlite+pysqlite:///{db_path}")
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    reset_settings_cache()
    reset_session_factory()
    initialize_session_factory(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(bind=get_engine())
    yield
    reset_settings_cache()
    reset_session_factory()


def test_ollama_smoke_lists_and_queues_models() -> None:
    service = OllamaService()

    available = service.list_available_models(limit=1)
    queued = service.queue_model_download(available.models[0].id)

    assert available.models
    assert queued.success is True
    assert service.list_installed_models()[0]["status"] == "queued"
