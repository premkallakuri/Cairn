import pytest

from app.core.config import get_settings

pytestmark = [pytest.mark.integration, pytest.mark.content_updates]


def test_manifest_refresh_and_content_update_check_endpoints(client) -> None:
    settings = get_settings()
    map_dir = settings.storage_path / "maps" / "pmtiles"
    map_dir.mkdir(parents=True, exist_ok=True)
    (map_dir / "alaska_2025-11.pmtiles").write_bytes(b"old-map")

    refresh_response = client.post("/api/manifests/refresh")
    check_response = client.post("/api/content-updates/check")

    assert refresh_response.status_code == 200
    assert refresh_response.json()["success"] is True
    assert check_response.status_code == 200
    updates = {item["resource_id"]: item for item in check_response.json()["updates"]}
    assert updates["alaska"]["resource_type"] == "map"
    assert updates["alaska"]["installed_version"] == "2025-11"


def test_content_update_apply_endpoints_queue_download_jobs(client) -> None:
    single_response = client.post(
        "/api/content-updates/apply",
        json={
            "resource_id": "alaska",
            "resource_type": "map",
            "installed_version": "2025-11",
            "latest_version": "2025-12",
            "download_url": "https://maps.projectnomad.local/pmtiles/alaska_2025-12.pmtiles",
        },
    )
    batch_response = client.post(
        "/api/content-updates/apply-all",
        json={
            "updates": [
                {
                    "resource_id": "colorado",
                    "resource_type": "map",
                    "installed_version": "2025-11",
                    "latest_version": "2025-12",
                    "download_url": "https://maps.projectnomad.local/pmtiles/colorado_2025-12.pmtiles",
                },
                {
                    "resource_id": "top-mini",
                    "resource_type": "zim",
                    "installed_version": "2025-06",
                    "latest_version": "2025-12",
                    "download_url": "https://download.kiwix.org/zim/wikipedia/wikipedia_en_top_mini_2025-12.zim",
                },
            ]
        },
    )
    jobs_response = client.get("/api/downloads/jobs")

    assert single_response.status_code == 200
    assert single_response.json()["success"] is True
    assert single_response.json()["jobId"]
    assert batch_response.status_code == 200
    assert len(batch_response.json()["results"]) == 2
    assert jobs_response.status_code == 200
    assert len(jobs_response.json()) >= 3
