from app.core.config import reset_settings_cache
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory, reset_session_factory
from app.modules.maps.schemas import RemoteDownloadRequest
from app.modules.maps.service import MapService


def test_maps_service_prepares_assets_and_styles(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "maps-smoke.db"
    monkeypatch.setenv("ATLAS_HAVEN_DATABASE_URL", f"sqlite+pysqlite:///{db_path}")
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    monkeypatch.setenv("ATLAS_HAVEN_REDIS_URL", "redis://127.0.0.1:6379/0")
    reset_settings_cache()
    reset_session_factory()
    initialize_session_factory(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(bind=get_engine())

    service = MapService()
    service.download_base_assets()

    pmtiles_dir = service.get_pmtiles_storage_path()
    pmtiles_dir.mkdir(parents=True, exist_ok=True)
    (pmtiles_dir / "alaska_2025-12.pmtiles").write_bytes(b"map")

    styles = service.generate_styles()
    response = service.download_remote(
        RemoteDownloadRequest(url="https://maps.example.test/oregon_2025-12.pmtiles")
    )

    assert "alaska" in styles.sources
    assert response.filename == "oregon_2025-12.pmtiles"
