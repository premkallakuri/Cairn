from pathlib import Path

import pytest

from app.modules.downloads.service import DownloadJobService

pytestmark = [pytest.mark.integration, pytest.mark.downloads]


def test_download_jobs_endpoint_lists_active_jobs(client, tmp_path: Path) -> None:
    service = DownloadJobService()
    service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "file.zim"),
        filetype="zim",
    )

    response = client.get("/api/downloads/jobs")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["filetype"] == "zim"


def test_download_jobs_endpoint_filters_by_filetype(client, tmp_path: Path) -> None:
    service = DownloadJobService()
    service.schedule_download(
        url="https://example.test/map.pmtiles",
        filepath=str(tmp_path / "map.pmtiles"),
        filetype="map",
    )
    service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "file.zim"),
        filetype="zim",
    )

    response = client.get("/api/downloads/jobs/zim")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["filetype"] == "zim"
