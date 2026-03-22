from pathlib import Path

import pytest

from app.core.config import get_settings
from app.modules.content_updates.schemas import (
    ContentUpdateApplyAllRequest,
    ResourceUpdateInfo,
)
from app.modules.content_updates.service import ContentUpdatesService
from app.modules.zim.schemas import WikipediaSelectionRequest
from app.modules.zim.service import ZimService

pytestmark = [pytest.mark.unit, pytest.mark.content_updates]


def test_manifest_refresh_copies_bundled_manifests() -> None:
    service = ContentUpdatesService()

    first = service.refresh_manifests()
    second = service.refresh_manifests()

    cache_root = get_settings().storage_path / "content-manifests"
    assert (cache_root / "maps.json").exists()
    assert (cache_root / "kiwix-categories.json").exists()
    assert (cache_root / "wikipedia.json").exists()
    assert first.success is True
    assert first.changed.maps is True
    assert first.changed.zim_categories is True
    assert first.changed.wikipedia is True
    assert second.changed.maps is False
    assert second.changed.zim_categories is False
    assert second.changed.wikipedia is False


def test_check_updates_uses_installed_map_and_wikipedia_versions(tmp_path: Path) -> None:
    settings = get_settings()
    map_dir = settings.storage_path / "maps" / "pmtiles"
    map_dir.mkdir(parents=True, exist_ok=True)
    (map_dir / "alaska_2025-11.pmtiles").write_bytes(b"old-map")

    zim_service = ZimService()
    zim_service.select_wikipedia(WikipediaSelectionRequest(optionId="top-mini"))

    service = ContentUpdatesService()
    result = service.check_updates()
    updates = {item.resource_id: item for item in result.updates}

    assert "alaska" in updates
    assert updates["alaska"].resource_type == "map"
    assert updates["alaska"].installed_version == "2025-11"
    assert updates["alaska"].latest_version == "2025-12"
    assert "top-mini" in updates
    assert updates["top-mini"].resource_type == "zim"
    assert updates["top-mini"].installed_version == "2025-06"
    assert updates["top-mini"].latest_version == "2025-12"


def test_apply_update_and_apply_all_queue_download_jobs() -> None:
    service = ContentUpdatesService()

    single = service.apply_update(
        ResourceUpdateInfo(
            resource_id="alaska",
            resource_type="map",
            installed_version="2025-11",
            latest_version="2025-12",
            download_url="https://maps.projectnomad.local/pmtiles/alaska_2025-12.pmtiles",
        )
    )
    batch = service.apply_all_updates(
        ContentUpdateApplyAllRequest(
            updates=[
                ResourceUpdateInfo(
                    resource_id="colorado",
                    resource_type="map",
                    installed_version="2025-11",
                    latest_version="2025-12",
                    download_url="https://maps.projectnomad.local/pmtiles/colorado_2025-12.pmtiles",
                ),
                ResourceUpdateInfo(
                    resource_id="top-mini",
                    resource_type="zim",
                    installed_version="2025-06",
                    latest_version="2025-12",
                    download_url="https://download.kiwix.org/zim/wikipedia/wikipedia_en_top_mini_2025-12.zim",
                ),
            ]
        )
    )

    assert single.success is True
    assert single.jobId is not None
    assert len(batch.results) == 2
    assert all(result.success for result in batch.results)
    assert {result.resource_id for result in batch.results} == {"colorado", "top-mini"}
