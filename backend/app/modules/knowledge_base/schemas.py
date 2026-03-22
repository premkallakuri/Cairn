from __future__ import annotations

from pydantic import BaseModel


class RagUploadResponse(BaseModel):
    message: str
    jobId: str | None = None
    fileName: str
    filePath: str
    alreadyProcessing: bool


class EmbedJobWithProgress(BaseModel):
    jobId: str
    fileName: str
    filePath: str
    progress: float
    status: str


class RagFilesResponse(BaseModel):
    files: list[str]


class DeleteRagFileRequest(BaseModel):
    source: str


class RagSyncResponse(BaseModel):
    success: bool = True
    message: str
    filesScanned: int
    filesQueued: int
    details: str | None = None


class MessageResponse(BaseModel):
    message: str
