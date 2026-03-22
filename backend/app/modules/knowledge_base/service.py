from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings
from app.modules.knowledge_base.repository import KnowledgeBaseRepository
from app.modules.knowledge_base.schemas import (
    EmbedJobWithProgress,
    MessageResponse,
    RagFilesResponse,
    RagSyncResponse,
    RagUploadResponse,
)

ALLOWED_SUFFIXES = {".txt", ".md", ".markdown", ".json", ".html", ".htm", ".csv", ".pdf"}


@dataclass(frozen=True, slots=True)
class SearchResult:
    source_path: str
    source_name: str
    content: str
    score: int


class KnowledgeBaseService:
    def __init__(self, repository: KnowledgeBaseRepository | None = None) -> None:
        self.repository = repository or KnowledgeBaseRepository()
        self.settings = get_settings()

    def upload_document(self, upload: UploadFile) -> RagUploadResponse:
        filename = Path(upload.filename or "").name
        if not filename:
            raise ValueError("Uploaded file is missing a filename")
        destination = self._files_path() / filename
        active_job = self.repository.get_active_job(str(destination))
        if active_job is not None:
            return RagUploadResponse(
                message="Embedding job is already running for this file",
                jobId=active_job.job_id,
                fileName=filename,
                filePath=str(destination),
                alreadyProcessing=True,
            )

        self._validate_suffix(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = upload.file.read()
        destination.write_bytes(payload)

        job = self.repository.create_job(
            {
                "job_id": str(uuid4()),
                "file_name": filename,
                "file_path": str(destination),
                "progress": 0,
                "status": "queued",
                "error_message": None,
            }
        )
        self.process_job(job.job_id)
        return RagUploadResponse(
            message="Upload accepted and embedding queued",
            jobId=job.job_id,
            fileName=filename,
            filePath=str(destination),
            alreadyProcessing=False,
        )

    def list_files(self) -> RagFilesResponse:
        files = self.repository.list_files()
        return RagFilesResponse(files=[item.file_path for item in files])

    def delete_file(self, source: str) -> MessageResponse:
        path = Path(source)
        deleted = self.repository.delete_source(str(path))
        if not deleted:
            raise ValueError(f"Unknown knowledge base file: {source}")
        if path.exists():
            path.unlink()
        return MessageResponse(message=f"Deleted knowledge base file {path.name}")

    def list_active_jobs(self) -> list[EmbedJobWithProgress]:
        jobs = self.repository.list_active_jobs()
        return [self._to_job(item) for item in jobs]

    def get_job_status(self, file_path: str) -> dict[str, object]:
        job = self.repository.get_latest_job(file_path)
        if job is None:
            raise ValueError(f"No embed job found for {file_path}")
        return {
            "jobId": job.job_id,
            "fileName": job.file_name,
            "filePath": job.file_path,
            "progress": job.progress,
            "status": job.status,
            "error": job.error_message,
        }

    def sync_storage(self) -> RagSyncResponse:
        storage_root = self._files_path()
        storage_root.mkdir(parents=True, exist_ok=True)
        files = sorted(path for path in storage_root.iterdir() if path.is_file())
        queued = 0
        for path in files:
            self._validate_suffix(path)
            if self.repository.get_file(str(path)) is not None:
                continue
            job = self.repository.create_job(
                {
                    "job_id": str(uuid4()),
                    "file_name": path.name,
                    "file_path": str(path),
                    "progress": 0,
                    "status": "queued",
                    "error_message": None,
                }
            )
            self.process_job(job.job_id)
            queued += 1
        return RagSyncResponse(
            success=True,
            message="Knowledge base sync completed",
            filesScanned=len(files),
            filesQueued=queued,
            details=None,
        )

    def extract_text(self, file_path: Path) -> str:
        self._validate_suffix(file_path)
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            text = self._extract_pdf_text(file_path)
        else:
            text = file_path.read_text(errors="ignore")
        if suffix in {".html", ".htm"}:
            text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def chunk_text(self, text: str, *, chunk_size: int = 80) -> list[str]:
        words = text.split()
        if not words:
            return []
        return [
            " ".join(words[index : index + chunk_size])
            for index in range(0, len(words), chunk_size)
        ]

    def index_path(self, file_path: Path) -> None:
        text = self.extract_text(file_path)
        chunks = self.chunk_text(text)
        self.repository.upsert_file(
            file_name=file_path.name,
            file_path=str(file_path),
            extracted_text=text,
        )
        self.repository.replace_chunks(
            source_path=str(file_path),
            source_name=file_path.name,
            chunks=chunks,
        )

    def search(self, query: str, *, limit: int = 3) -> list[SearchResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        results: list[SearchResult] = []
        for chunk in self.repository.list_chunks():
            score = len(query_tokens & self._tokenize(chunk.content))
            if score <= 0:
                continue
            results.append(
                SearchResult(
                    source_path=chunk.source_path,
                    source_name=chunk.source_name,
                    content=chunk.content,
                    score=score,
                )
            )
        results.sort(key=lambda item: (item.score, len(item.content)), reverse=True)
        return results[:limit]

    def assemble_context(self, query: str, *, limit: int = 2) -> str | None:
        results = self.search(query, limit=limit)
        if not results:
            return None
        lines = [f"[{result.source_name}] {result.content[:180]}" for result in results]
        return "Relevant local docs: " + " | ".join(lines)

    def process_job(self, job_id: str) -> None:
        job = self.repository.get_job(job_id)
        if job is None:
            raise ValueError(f"Unknown embed job: {job_id}")
        try:
            self.repository.update_job(job_id, status="processing", progress=10, error_message=None)
            path = Path(job.file_path)
            text = self.extract_text(path)
            self.repository.update_job(job_id, status="processing", progress=45)
            chunks = self.chunk_text(text)
            self.repository.update_job(job_id, status="processing", progress=75)
            self.repository.upsert_file(
                file_name=job.file_name,
                file_path=job.file_path,
                extracted_text=text,
            )
            self.repository.replace_chunks(
                source_path=job.file_path,
                source_name=job.file_name,
                chunks=chunks,
            )
            self.repository.update_job(job_id, status="completed", progress=100)
        except Exception as exc:
            self.repository.update_job(job_id, status="failed", error_message=str(exc))
            raise

    def _files_path(self) -> Path:
        return self.settings.storage_path / "rag" / "files"

    def _validate_suffix(self, path: Path) -> None:
        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError(f"Unsupported knowledge base file type: {path.suffix}")

    def _extract_pdf_text(self, file_path: Path) -> str:
        raw = file_path.read_bytes().decode("latin-1", errors="ignore")
        matches = re.findall(r"\(([^()]*(?:\\.[^()]*)*)\)\s*T[Jj]", raw)
        if not matches:
            return raw
        return " ".join(match.replace("\\(", "(").replace("\\)", ")") for match in matches)

    def _tokenize(self, text: str) -> set[str]:
        return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 1}

    def _to_job(self, job) -> EmbedJobWithProgress:
        return EmbedJobWithProgress(
            jobId=job.job_id,
            fileName=job.file_name,
            filePath=job.file_path,
            progress=job.progress,
            status=job.status,
        )
