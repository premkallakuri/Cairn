from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class FileEntry(BaseModel):
    type: Literal["file"] = "file"
    key: str
    name: str


class ListMapRegionsResponse(BaseModel):
    files: list[FileEntry] = Field(default_factory=list)


class SpecResource(BaseModel):
    id: str
    version: str
    title: str
    description: str
    url: str
    size_mb: int


class CollectionWithStatus(BaseModel):
    name: str
    slug: str
    description: str
    icon: str
    language: str
    resources: list[SpecResource] = Field(default_factory=list)
    all_installed: bool
    installed_count: int
    total_count: int


class SourceDefinition(BaseModel):
    type: str
    attribution: str
    url: str


class BaseStylesFile(BaseModel):
    version: int
    sources: dict[str, SourceDefinition]
    layers: list[dict[str, object]] = Field(default_factory=list)
    sprite: str
    glyphs: str


class RemoteDownloadRequest(BaseModel):
    url: str


class RemoteMapDownloadResponse(BaseModel):
    message: str
    filename: str
    jobId: str | None = None
    url: str


class MapRemotePreflightResponse(BaseModel):
    filename: str | None = None
    size: int | None = None
    message: str | None = None


class DownloadCollectionRequest(BaseModel):
    slug: str


class CollectionDownloadResponse(BaseModel):
    message: str
    slug: str
    resources: list[str] | None = None
