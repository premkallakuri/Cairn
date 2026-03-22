import httpx
import pytest

from app.modules.maps.schemas import DownloadCollectionRequest, RemoteDownloadRequest
from app.modules.maps.service import MapRemoteClient, MapService

pytestmark = [pytest.mark.unit, pytest.mark.maps]


def test_generate_styles_requires_base_assets() -> None:
    service = MapService()

    with pytest.raises(ValueError, match="Base map assets are missing"):
        service.generate_styles()


def test_download_base_assets_creates_template_files() -> None:
    service = MapService()

    service.download_base_assets()

    maps_root = service.get_maps_storage_path()
    assert (maps_root / "nomad-base-styles.json").exists()
    assert (maps_root / "basemaps-assets" / "sprites" / "v4" / "light.json").exists()
    assert (maps_root / "basemaps-assets" / "sprites" / "v4" / "light.png").exists()


def test_generate_styles_uses_local_pmtiles_files() -> None:
    service = MapService()
    service.download_base_assets()
    pmtiles_dir = service.get_pmtiles_storage_path()
    pmtiles_dir.mkdir(parents=True, exist_ok=True)
    (pmtiles_dir / "alaska_2025-12.pmtiles").write_bytes(b"map")

    styles = service.generate_styles()

    assert "alaska" in styles.sources
    assert styles.sources["alaska"].url.endswith("/api/maps/files/alaska_2025-12.pmtiles")
    assert any(layer["source"] == "alaska" for layer in styles.layers if "source" in layer)


def test_curated_collections_report_install_counts() -> None:
    service = MapService()
    pmtiles_dir = service.get_pmtiles_storage_path()
    pmtiles_dir.mkdir(parents=True, exist_ok=True)
    (pmtiles_dir / "alaska_2025-12.pmtiles").write_bytes(b"map")
    (pmtiles_dir / "hawaii_2025-12.pmtiles").write_bytes(b"map")

    collections = service.list_curated_collections()
    pacific = next(collection for collection in collections if collection.slug == "pacific")

    assert pacific.installed_count == 2
    assert pacific.total_count == 5
    assert pacific.all_installed is False


def test_download_remote_preflight_returns_filename_and_size() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "HEAD"
        return httpx.Response(200, headers={"content-length": "456"})

    service = MapService(
        remote_client=MapRemoteClient(
            client_factory=lambda: httpx.Client(transport=httpx.MockTransport(handler))
        )
    )

    response = service.download_remote_preflight("https://maps.example.test/oregon_2025-12.pmtiles")

    assert response.filename == "oregon_2025-12.pmtiles"
    assert response.size == 456


def test_download_collection_schedules_missing_resources_only() -> None:
    service = MapService()
    pmtiles_dir = service.get_pmtiles_storage_path()
    pmtiles_dir.mkdir(parents=True, exist_ok=True)
    (pmtiles_dir / "alaska_2025-12.pmtiles").write_bytes(b"map")

    response = service.download_collection(DownloadCollectionRequest(slug="pacific"))

    assert response.slug == "pacific"
    assert response.resources is not None
    assert "alaska_2025-12.pmtiles" not in response.resources
    assert len(response.resources) == 4


def test_installed_resource_versions_use_latest_local_file() -> None:
    service = MapService()
    pmtiles_dir = service.get_pmtiles_storage_path()
    pmtiles_dir.mkdir(parents=True, exist_ok=True)
    (pmtiles_dir / "alaska_2025-11.pmtiles").write_bytes(b"old")
    (pmtiles_dir / "alaska_2025-12.pmtiles").write_bytes(b"new")

    versions = service.get_installed_resource_versions()

    assert versions["alaska"] == "2025-12"


def test_download_remote_rejects_non_pmtiles_urls() -> None:
    service = MapService()

    with pytest.raises(ValueError, match="Invalid PMTiles file URL"):
        service.download_remote(RemoteDownloadRequest(url="https://maps.example.test/alaska.txt"))
