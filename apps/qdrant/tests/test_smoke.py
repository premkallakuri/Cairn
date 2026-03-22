from pathlib import Path

import pytest

from app.core.config import reset_settings_cache
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory, reset_session_factory
from app.modules.catalog.service import CatalogSyncService
from app.modules.platform_core.service import SystemServiceManager


@pytest.fixture(autouse=True)
def setup_app_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    db_path = tmp_path / "atlas-haven-qdrant.db"
    monkeypatch.setenv("ATLAS_HAVEN_DATABASE_URL", f"sqlite+pysqlite:///{db_path}")
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    reset_settings_cache()
    reset_session_factory()
    initialize_session_factory(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(bind=get_engine())
    yield
    reset_settings_cache()
    reset_session_factory()


def test_qdrant_smoke_installs_as_dependency_target() -> None:
    CatalogSyncService().sync_from_disk()
    manager = SystemServiceManager()

    result = manager.install_service("nomad_qdrant")

    assert result.installed_services == ["nomad_qdrant"]
    assert manager.list_services(installed_only=True)[0].service_name == "nomad_qdrant"
