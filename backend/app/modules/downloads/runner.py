from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import httpx

from app.modules.downloads.service import DownloadJobService


class DownloadRunner:
    def __init__(
        self,
        service: DownloadJobService | None = None,
        client_factory: Callable[[], httpx.AsyncClient] | None = None,
    ) -> None:
        self.service = service or DownloadJobService()
        self.client_factory = client_factory or (lambda: httpx.AsyncClient(follow_redirects=True))

    async def run(self, job_id: str) -> None:
        job = self.service.get_job(job_id)
        if job is None:
            raise ValueError(f"Unknown download job: {job_id}")

        filepath = Path(job.filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        downloaded_bytes = filepath.stat().st_size if filepath.exists() else 0
        headers: dict[str, str] = {}
        if downloaded_bytes > 0:
            headers["Range"] = f"bytes={downloaded_bytes}-"

        self.service.mark_active(
            job_id, downloaded_bytes=downloaded_bytes, total_bytes=job.total_bytes
        )

        try:
            async with self.client_factory() as client:
                async with client.stream("GET", job.url, headers=headers) as response:
                    response.raise_for_status()
                    total_bytes = self._resolve_total_bytes(
                        response.headers.get("content-length"),
                        downloaded_bytes,
                    )
                    self.service.update_progress(
                        job_id,
                        downloaded_bytes=downloaded_bytes,
                        total_bytes=total_bytes,
                    )

                    mode = "ab" if downloaded_bytes > 0 else "wb"
                    with filepath.open(mode) as file_handle:
                        async for chunk in response.aiter_bytes():
                            if not chunk:
                                continue
                            file_handle.write(chunk)
                            downloaded_bytes += len(chunk)
                            self.service.update_progress(
                                job_id,
                                downloaded_bytes=downloaded_bytes,
                                total_bytes=total_bytes,
                            )

            self.service.mark_completed(job_id)
        except Exception as exc:
            self.service.mark_failed(job_id, str(exc))
            raise

    def _resolve_total_bytes(
        self, content_length_header: str | None, existing_bytes: int
    ) -> int | None:
        if content_length_header is None:
            return None
        return int(content_length_header) + existing_bytes
