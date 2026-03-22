import pytest

pytestmark = [pytest.mark.integration, pytest.mark.maps]


def test_maps_regions_and_collections_endpoints(client) -> None:
    regions_response = client.get("/api/maps/regions")
    collections_response = client.get("/api/maps/curated-collections")

    assert regions_response.status_code == 200
    assert collections_response.status_code == 200
    assert regions_response.json()["files"] == []
    assert any(collection["slug"] == "pacific" for collection in collections_response.json())


def test_maps_base_assets_and_styles_endpoints(client) -> None:
    download_response = client.post("/api/maps/download-base-assets")
    styles_response = client.get("/api/maps/styles")

    assert download_response.status_code == 200
    assert download_response.json()["success"] is True
    assert styles_response.status_code == 200
    assert styles_response.json()["version"] == 8


def test_maps_download_endpoints_queue_jobs(client) -> None:
    remote_response = client.post(
        "/api/maps/download-remote",
        json={"url": "https://maps.example.test/oregon_2025-12.pmtiles"},
    )
    collection_response = client.post("/api/maps/download-collection", json={"slug": "pacific"})
    jobs_response = client.get("/api/downloads/jobs/map")

    assert remote_response.status_code == 200
    assert collection_response.status_code == 200
    assert jobs_response.status_code == 200
    assert remote_response.json()["filename"] == "oregon_2025-12.pmtiles"
    assert collection_response.json()["slug"] == "pacific"
    assert len(jobs_response.json()) == 5
