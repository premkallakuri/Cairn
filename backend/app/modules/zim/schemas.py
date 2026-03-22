from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ZimManifestResource(BaseModel):
    id: str
    version: str | None = None
    title: str
    description: str
    url: str
    size_mb: int


class ZimManifestTier(BaseModel):
    name: str
    slug: str
    description: str
    recommended: bool = False
    includesTier: str | None = None
    resources: list[ZimManifestResource] = Field(default_factory=list)


class ZimManifestCategory(BaseModel):
    name: str
    slug: str
    icon: str
    description: str
    language: str
    tiers: list[ZimManifestTier] = Field(default_factory=list)


class CuratedCategoryTier(BaseModel):
    name: str
    slug: str
    description: str
    recommended: bool = False
    includesTier: str | None = None


class CategoryWithStatus(BaseModel):
    name: str
    slug: str
    icon: str
    description: str
    language: str
    installedTierSlug: str | None = None
    tiers: list[CuratedCategoryTier] = Field(default_factory=list)


class CuratedZimResource(BaseModel):
    resource_id: str
    title: str
    version: str
    url: str


class WikipediaOption(BaseModel):
    id: str
    name: str
    description: str
    size_mb: int
    url: str | None = None
    version: str | None = None


class WikipediaCurrentSelection(BaseModel):
    optionId: str
    status: Literal["none", "downloading", "installed", "failed"]
    filename: str | None = None
    url: str | None = None


class WikipediaState(BaseModel):
    options: list[WikipediaOption]
    currentSelection: WikipediaCurrentSelection | None = None


class WikipediaUpdateState(BaseModel):
    installed_version: str | None = None
    latest_version: str | None = None
    download_url: str | None = None
    needs_update: bool = False


class SelectWikipediaResponse(BaseModel):
    success: bool
    jobId: str | None = None
    message: str | None = None


class WikipediaSelectionRequest(BaseModel):
    optionId: str


class FileEntry(BaseModel):
    type: Literal["file"] = "file"
    key: str
    name: str
    title: str | None = None
    summary: str | None = None
    author: str | None = None
    size_bytes: int | None = None


class ListZimFilesResponse(BaseModel):
    files: list[FileEntry] = Field(default_factory=list)
    next: str | None = None


class RemoteZimFileEntry(BaseModel):
    id: str
    title: str
    updated: str
    summary: str
    size_bytes: int
    download_url: str
    author: str
    file_name: str


class ListRemoteZimFilesResponse(BaseModel):
    items: list[RemoteZimFileEntry] = Field(default_factory=list)
    has_more: bool
    total_count: int


class RemoteZimDownloadRequest(BaseModel):
    url: str


class RemoteZimDownloadResponse(BaseModel):
    message: str
    filename: str
    jobId: str | None = None
    url: str


class DownloadCategoryTierRequest(BaseModel):
    categorySlug: str
    tierSlug: str


class CategoryTierDownloadResponse(BaseModel):
    message: str
    categorySlug: str
    tierSlug: str
    resources: list[str] | None = None
