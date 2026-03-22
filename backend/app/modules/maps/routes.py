from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.modules.maps.schemas import (
    BaseStylesFile,
    CollectionDownloadResponse,
    CollectionWithStatus,
    DownloadCollectionRequest,
    ListMapRegionsResponse,
    MapRemotePreflightResponse,
    RemoteDownloadRequest,
    RemoteMapDownloadResponse,
)
from app.modules.maps.service import MapService

router = APIRouter(tags=["maps"])


@router.get("/regions", response_model=ListMapRegionsResponse)
def list_map_regions() -> ListMapRegionsResponse:
    return MapService().list_regions()


@router.get("/styles", response_model=BaseStylesFile)
def get_map_styles() -> BaseStylesFile:
    try:
        return MapService().generate_styles()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/curated-collections", response_model=list[CollectionWithStatus])
def list_curated_map_collections() -> list[CollectionWithStatus]:
    return MapService().list_curated_collections()


@router.post("/fetch-latest-collections")
def fetch_latest_map_collections() -> dict[str, bool]:
    return {"success": MapService().fetch_latest_collections()}


@router.post("/download-base-assets")
def download_base_map_assets(payload: dict[str, str] | None = None) -> dict[str, bool]:
    url = payload.get("url") if payload else None
    return {"success": MapService().download_base_assets(url=url)}


@router.post("/download-remote", response_model=RemoteMapDownloadResponse)
def download_remote_map_region(request: RemoteDownloadRequest) -> RemoteMapDownloadResponse:
    return MapService().download_remote(request)


@router.post("/download-remote-preflight", response_model=MapRemotePreflightResponse)
def download_remote_map_region_preflight(
    request: RemoteDownloadRequest,
) -> MapRemotePreflightResponse:
    try:
        return MapService().download_remote_preflight(request.url)
    except Exception as exc:
        return MapRemotePreflightResponse(message=f"Preflight check failed: {exc}")


@router.post("/download-collection", response_model=CollectionDownloadResponse)
def download_curated_collection(request: DownloadCollectionRequest) -> CollectionDownloadResponse:
    return MapService().download_collection(request)


@router.delete("/{filename}")
def delete_map_region(filename: str) -> dict[str, object]:
    MapService().delete(filename)
    return {"success": True, "filename": filename}


@router.get("/files/{filename}")
def get_map_region_file(filename: str) -> FileResponse:
    path = MapService().resolve_map_file(filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Map file not found")
    return FileResponse(path)


@router.get("/assets/{asset_path:path}")
def get_map_asset(asset_path: str) -> FileResponse:
    path = MapService().resolve_asset_file(asset_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Map asset not found")
    return FileResponse(path)
