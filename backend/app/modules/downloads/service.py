from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from uuid import uuid4

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import get_settings
from app.modules.downloads.repository import DownloadJobRepository
from app.modules.downloads.schemas import DownloadJobWithProgress, ScheduledDownload

logger = logging.getLogger(__name__)


def enqueue_download_worker_job(job_id: str) -> None:
    settings = get_settings()

    async def _enqueue() -> None:
        redis = await create_pool(RedisSettings.from_dsn(settings.redis_url))
        try:
            await redis.enqueue_job("run_download_job", job_id)
        finally:
            await redis.aclose()

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_enqueue())
    except Exception:
        logger.exception(
            "Failed to enqueue download job %s — check Redis at %s",
            job_id,
            settings.redis_url,
        )
    finally:
        loop.close()
        asyncio.set_event_loop(None)

ACTIVE_DOWNLOAD_STATUSES = ("waiting", "active", "delayed")


class DownloadJobService:
    def __init__(self, repository: DownloadJobRepository | None = None) -> None:
        self.repository = repository or DownloadJobRepository()

    def schedule_download(self, *, url: str, filepath: str, filetype: str) -> ScheduledDownload:
        existing = self.repository.get_by_url(url, statuses=ACTIVE_DOWNLOAD_STATUSES)
        if existing is not None:
            return self._to_scheduled_download(existing)

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing_filepath = self.repository.get_by_filepath(
            str(path), statuses=ACTIVE_DOWNLOAD_STATUSES
        )
        if existing_filepath is not None:
            return self._to_scheduled_download(existing_filepath)

        job = self.repository.create_job(
            {
                "job_id": str(uuid4()),
                "url": url,
                "filepath": str(path),
                "filetype": filetype,
                "status": "waiting",
                "progress": 0,
                "downloaded_bytes": 0,
                "total_bytes": None,
                "error_message": None,
            }
        )
        if get_settings().enqueue_download_worker_jobs:
            enqueue_download_worker_job(job.job_id)
        return self._to_scheduled_download(job)

    def list_download_jobs(self, filetype: str | None = None) -> list[DownloadJobWithProgress]:
        jobs = self.repository.list_jobs(filetype=filetype, statuses=ACTIVE_DOWNLOAD_STATUSES)
        return [self._to_api_job(job) for job in jobs]

    def mark_active(
        self, job_id: str, *, downloaded_bytes: int = 0, total_bytes: int | None = None
    ) -> ScheduledDownload:
        job = self.repository.update_job(
            job_id,
            status="active",
            downloaded_bytes=downloaded_bytes,
            total_bytes=total_bytes,
            error_message=None,
        )
        return self._to_scheduled_download(job)

    def update_progress(
        self,
        job_id: str,
        *,
        downloaded_bytes: int,
        total_bytes: int | None,
    ) -> ScheduledDownload:
        progress = self._calculate_progress(downloaded_bytes, total_bytes)
        job = self.repository.update_job(
            job_id,
            status="active",
            progress=progress,
            downloaded_bytes=downloaded_bytes,
            total_bytes=total_bytes,
        )
        return self._to_scheduled_download(job)

    def mark_completed(self, job_id: str) -> ScheduledDownload:
        job = self.repository.get_by_job_id(job_id)
        if job is None:
            raise ValueError(f"Unknown download job: {job_id}")
        job = self.repository.update_job(
            job_id,
            status="completed",
            progress=100,
            downloaded_bytes=job.total_bytes or job.downloaded_bytes,
        )
        return self._to_scheduled_download(job)

    def mark_failed(self, job_id: str, message: str) -> ScheduledDownload:
        job = self.repository.update_job(job_id, status="failed", error_message=message)
        return self._to_scheduled_download(job)

    def get_job(self, job_id: str) -> ScheduledDownload | None:
        job = self.repository.get_by_job_id(job_id)
        if job is None:
            return None
        return self._to_scheduled_download(job)

    def _to_api_job(self, job) -> DownloadJobWithProgress:
        return DownloadJobWithProgress(
            jobId=job.job_id,
            url=job.url,
            progress=job.progress,
            filepath=job.filepath,
            filetype=job.filetype,
        )

    def _to_scheduled_download(self, job) -> ScheduledDownload:
        return ScheduledDownload(
            job_id=job.job_id,
            url=job.url,
            filepath=job.filepath,
            filetype=job.filetype,
            status=job.status,
            progress=job.progress,
            downloaded_bytes=job.downloaded_bytes,
            total_bytes=job.total_bytes,
            error_message=job.error_message,
        )

    def _calculate_progress(self, downloaded_bytes: int, total_bytes: int | None) -> float:
        if not total_bytes or total_bytes <= 0:
            return 0
        return round(min(downloaded_bytes / total_bytes * 100, 100), 2)
