from pathlib import Path

import httpx
import pytest

from app.modules.downloads.runner import DownloadRunner
from app.modules.downloads.service import DownloadJobService

pytestmark = [pytest.mark.unit, pytest.mark.downloads]


def test_schedule_download_creates_waiting_job(tmp_path: Path) -> None:
    service = DownloadJobService()

    job = service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "file.zim"),
        filetype="zim",
    )

    assert job.status == "waiting"
    assert job.progress == 0
    assert job.filetype == "zim"


def test_schedule_download_deduplicates_active_url(tmp_path: Path) -> None:
    service = DownloadJobService()

    first = service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "a.zim"),
        filetype="zim",
    )
    second = service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "b.zim"),
        filetype="zim",
    )

    assert second.job_id == first.job_id


def test_list_download_jobs_filters_by_filetype_and_sorts(tmp_path: Path) -> None:
    service = DownloadJobService()
    service.schedule_download(
        url="https://example.test/map.pmtiles",
        filepath=str(tmp_path / "map.pmtiles"),
        filetype="map",
    )
    zim = service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "file.zim"),
        filetype="zim",
    )
    service.update_progress(zim.job_id, downloaded_bytes=40, total_bytes=100)

    jobs = service.list_download_jobs("zim")

    assert len(jobs) == 1
    assert jobs[0].filetype == "zim"
    assert jobs[0].progress == 40


@pytest.mark.asyncio
async def test_download_runner_streams_file_and_marks_complete(tmp_path: Path) -> None:
    service = DownloadJobService()
    filepath = tmp_path / "payload.txt"
    job = service.schedule_download(
        url="https://example.test/payload.txt",
        filepath=str(filepath),
        filetype="doc",
    )

    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-length": "11"},
            content=b"hello world",
        )

    runner = DownloadRunner(
        service=service,
        client_factory=lambda: httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    await runner.run(job.job_id)

    final_job = service.get_job(job.job_id)
    assert final_job is not None
    assert final_job.status == "completed"
    assert final_job.progress == 100
    assert filepath.read_bytes() == b"hello world"


def test_completed_downloads_do_not_show_in_active_listing(tmp_path: Path) -> None:
    service = DownloadJobService()
    job = service.schedule_download(
        url="https://example.test/file.zim",
        filepath=str(tmp_path / "file.zim"),
        filetype="zim",
    )
    service.mark_completed(job.job_id)

    jobs = service.list_download_jobs()

    assert jobs == []
