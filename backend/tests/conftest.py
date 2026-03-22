from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import reset_settings_cache
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory, reset_session_factory
from app.main import create_app


@pytest.fixture(autouse=True)
def reset_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Generator[None]:
    db_path = tmp_path / "atlas-haven-test.db"
    storage_path = tmp_path / "storage"
    bundled_seed_path = tmp_path / "bundled-demo.zim"
    bundled_seed_path.write_bytes(b"atlas-haven-demo-zim")
    monkeypatch.setenv("ATLAS_HAVEN_DATABASE_URL", f"sqlite+pysqlite:///{db_path}")
    monkeypatch.setenv("ATLAS_HAVEN_REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(storage_path))
    monkeypatch.setenv("ATLAS_HAVEN_BUNDLED_SEED_ZIM_PATH", str(bundled_seed_path))
    monkeypatch.setenv("ATLAS_HAVEN_ENQUEUE_DOWNLOAD_WORKER_JOBS", "0")
    fixtures_collections = Path(__file__).resolve().parent / "fixtures" / "collections"
    monkeypatch.setenv("ATLAS_HAVEN_COLLECTIONS_PATH", str(fixtures_collections))
    reset_settings_cache()
    reset_session_factory()
    initialize_session_factory(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(bind=get_engine())
    yield
    reset_settings_cache()
    reset_session_factory()


@pytest.fixture
def client() -> Generator[TestClient]:
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
