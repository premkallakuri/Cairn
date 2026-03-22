from arq.connections import RedisSettings

from app.core.config import get_settings
from app.modules.downloads.runner import DownloadRunner


async def run_download_job(ctx: dict, job_id: str) -> None:
    await DownloadRunner().run(job_id)


class DownloadWorkerSettings:
    functions = [run_download_job]
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
