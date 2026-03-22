from pathlib import Path

import pytest

from app.core.config import reset_settings_cache
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory, reset_session_factory
from app.modules.catalog.service import CatalogSyncService
from app.modules.platform_core.service import SystemServiceManager


@pytest.fixture(autouse=True)
def setup_app_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    db_path = tmp_path / "atlas-haven-flatnotes.db"
    monkeypatch.setenv("ATLAS_HAVEN_DATABASE_URL", f"sqlite+pysqlite:///{db_path}")
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    reset_settings_cache()
    reset_session_factory()
    initialize_session_factory(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(bind=get_engine())
    yield
    reset_settings_cache()
    reset_session_factory()


def test_flatnotes_smoke_installs_with_launch_url() -> None:
    CatalogSyncService().sync_from_disk()
    manager = SystemServiceManager()

    manager.install_service("nomad_flatnotes")

    service = next(
        item for item in manager.list_services(installed_only=True) if item.service_name == "nomad_flatnotes"
    )
    assert service.status == "running"
    assert service.launch_url == "http://127.0.0.1:8081"
