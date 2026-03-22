from fastapi import APIRouter, Query

from app.modules.zim.schemas import (
    CategoryTierDownloadResponse,
    CategoryWithStatus,
    DownloadCategoryTierRequest,
    ListRemoteZimFilesResponse,
    ListZimFilesResponse,
    RemoteZimDownloadRequest,
    RemoteZimDownloadResponse,
    SelectWikipediaResponse,
    WikipediaSelectionRequest,
    WikipediaState,
)
from app.modules.zim.service import ZimService

router = APIRouter(tags=["zim"])


@router.get("/list", response_model=ListZimFilesResponse)
def list_zim_files() -> ListZimFilesResponse:
    return ZimService().list()


@router.get("/list-remote", response_model=ListRemoteZimFilesResponse)
def list_remote_zim_files(
    start: int = Query(0, ge=0),
    count: int = Query(12, ge=1, le=100),
    query: str | None = Query(None),
) -> ListRemoteZimFilesResponse:
    return ZimService().list_remote(start=start, count=count, query=query)


@router.get("/curated-categories", response_model=list[CategoryWithStatus])
def list_curated_categories() -> list[CategoryWithStatus]:
    return ZimService().list_curated_categories()


@router.post("/download-remote", response_model=RemoteZimDownloadResponse)
def download_remote_zim_file(request: RemoteZimDownloadRequest) -> RemoteZimDownloadResponse:
    return ZimService().download_remote(request)


@router.post("/download-category-tier", response_model=CategoryTierDownloadResponse)
def download_category_tier(request: DownloadCategoryTierRequest) -> CategoryTierDownloadResponse:
    return ZimService().download_category_tier(request)


@router.get("/wikipedia", response_model=WikipediaState)
def get_wikipedia_state() -> WikipediaState:
    return ZimService().get_wikipedia_state()


@router.post("/wikipedia/select", response_model=SelectWikipediaResponse)
def select_wikipedia(request: WikipediaSelectionRequest) -> SelectWikipediaResponse:
    return ZimService().select_wikipedia(request)


@router.delete("/{filename}")
def delete_zim_file(filename: str) -> dict[str, object]:
    ZimService().delete(filename)
    return {"success": True, "filename": filename}
