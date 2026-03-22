from fastapi import APIRouter

from app.modules.downloads.schemas import DownloadJobWithProgress
from app.modules.downloads.service import DownloadJobService

router = APIRouter(tags=["downloads"])


@router.get("/jobs", response_model=list[DownloadJobWithProgress])
def list_download_jobs() -> list[DownloadJobWithProgress]:
    return DownloadJobService().list_download_jobs()


@router.get("/jobs/{filetype}", response_model=list[DownloadJobWithProgress])
def list_download_jobs_by_filetype(filetype: str) -> list[DownloadJobWithProgress]:
    return DownloadJobService().list_download_jobs(filetype=filetype)
