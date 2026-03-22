from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.modules.knowledge_base.schemas import (
    DeleteRagFileRequest,
    EmbedJobWithProgress,
    MessageResponse,
    RagFilesResponse,
    RagSyncResponse,
    RagUploadResponse,
)
from app.modules.knowledge_base.service import KnowledgeBaseService

router = APIRouter(tags=["knowledge-base"])


@router.post("/upload", response_model=RagUploadResponse, status_code=status.HTTP_202_ACCEPTED)
def upload_document(file: Annotated[UploadFile, File(...)]) -> RagUploadResponse:
    try:
        return KnowledgeBaseService().upload_document(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/files", response_model=RagFilesResponse)
def list_rag_files() -> RagFilesResponse:
    return KnowledgeBaseService().list_files()


@router.delete("/files", response_model=MessageResponse)
def delete_rag_file(payload: DeleteRagFileRequest) -> MessageResponse:
    try:
        return KnowledgeBaseService().delete_file(payload.source)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/active-jobs", response_model=list[EmbedJobWithProgress])
def list_active_embed_jobs() -> list[EmbedJobWithProgress]:
    return KnowledgeBaseService().list_active_jobs()


@router.get("/job-status", response_model=dict[str, object])
def get_embed_job_status(filePath: str = Query(...)) -> dict[str, object]:
    try:
        return KnowledgeBaseService().get_job_status(filePath)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/sync", response_model=RagSyncResponse)
def sync_rag_storage() -> RagSyncResponse:
    return KnowledgeBaseService().sync_storage()
