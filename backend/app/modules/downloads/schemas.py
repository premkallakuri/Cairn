from pydantic import BaseModel, Field


class DownloadJobWithProgress(BaseModel):
    jobId: str
    url: str
    progress: float
    filepath: str
    filetype: str


class ScheduledDownload(BaseModel):
    job_id: str
    url: str
    filepath: str
    filetype: str
    status: str = Field(default="waiting")
    progress: float = Field(default=0)
    downloaded_bytes: int = Field(default=0)
    total_bytes: int | None = None
    error_message: str | None = None
