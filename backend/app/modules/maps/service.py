from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

import httpx

from app.core.config import get_settings
from app.modules.downloads.service import DownloadJobService
from app.modules.maps.schemas import (
    BaseStylesFile,
    CollectionDownloadResponse,
    CollectionWithStatus,
    DownloadCollectionRequest,
    FileEntry,
    ListMapRegionsResponse,
    MapRemotePreflightResponse,
    RemoteDownloadRequest,
    RemoteMapDownloadResponse,
    SourceDefinition,
    SpecResource,
)
from app.shared.collections import load_collection_manifest

PMTILES_ATTRIBUTION = (
    '<a href="https://github.com/protomaps/basemaps">Protomaps</a> '
    '© <a href="https://openstreetmap.org">OpenStreetMap</a>'
)
BASE_STYLE_FILENAME = "nomad-base-styles.json"
BASE_ASSETS_DIRNAME = "basemaps-assets"
SPRITE_RELATIVE_PATH = Path(BASE_ASSETS_DIRNAME) / "sprites" / "v4" / "light"
FONT_RELATIVE_PATH = Path(BASE_ASSETS_DIRNAME) / "fonts" / "Noto Sans Regular" / "0-255.pbf"
TRANSPARENT_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc`\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)
BASE_STYLE_TEMPLATE = {
    "version": 8,
    "sources": {},
    "layers": [
        {"id": "background", "type": "background", "paint": {"background-color": "#eef1e7"}},
        {
            "id": "landcover-template",
            "type": "fill",
            "source": "__template__",
            "source-layer": "landcover",
            "paint": {"fill-color": "#dde6cf", "fill-opacity": 0.9},
        },
        {
            "id": "water-template",
            "type": "fill",
            "source": "__template__",
            "source-layer": "water",
            "paint": {"fill-color": "#8cb8d9"},
        },
        {
            "id": "roads-template",
            "type": "line",
            "source": "__template__",
            "source-layer": "roads",
            "paint": {"line-color": "#6f7c86", "line-width": 1},
        },
        {
            "id": "places-template",
            "type": "symbol",
            "source": "__template__",
            "source-layer": "places",
            "layout": {
                "text-field": ["get", "name"],
                "text-font": ["Noto Sans Regular"],
                "text-size": 11,
            },
            "paint": {"text-color": "#163847"},
        },
    ],
    "sprite": "",
    "glyphs": "",
}


class MapRemoteClient:
    def __init__(self, client_factory: Callable[[], httpx.Client] | None = None) -> None:
        self.client_factory = client_factory or (lambda: httpx.Client(timeout=10.0))

    def preflight(self, url: str) -> MapRemotePreflightResponse:
        with self.client_factory() as client:
            response = client.head(url)
            response.raise_for_status()

        filename = Path(urlparse(url).path).name
        return MapRemotePreflightResponse(
            filename=filename,
            size=int(response.headers.get("content-length", "0")),
        )


class MapService:
    def __init__(
        self,
        download_service: DownloadJobService | None = None,
        remote_client: MapRemoteClient | None = None,
    ) -> None:
        self.download_service = download_service or DownloadJobService()
        self.remote_client = remote_client or MapRemoteClient()

    def get_maps_storage_path(self) -> Path:
        settings = get_settings()
        return settings.storage_path / "maps"

    def get_pmtiles_storage_path(self) -> Path:
        return self.get_maps_storage_path() / "pmtiles"

    def get_base_styles_path(self) -> Path:
        return self.get_maps_storage_path() / BASE_STYLE_FILENAME

    def get_sprite_json_path(self) -> Path:
        return self.get_maps_storage_path() / f"{SPRITE_RELATIVE_PATH}.json"

    def get_sprite_png_path(self) -> Path:
        return self.get_maps_storage_path() / f"{SPRITE_RELATIVE_PATH}.png"

    def get_font_path(self) -> Path:
        return self.get_maps_storage_path() / FONT_RELATIVE_PATH

    def list_regions(self) -> ListMapRegionsResponse:
        pmtiles_dir = self.get_pmtiles_storage_path()
        pmtiles_dir.mkdir(parents=True, exist_ok=True)
        return ListMapRegionsResponse(
            files=[
                FileEntry(type="file", key=item.name, name=item.name)
                for item in sorted(pmtiles_dir.glob("*.pmtiles"))
                if item.is_file()
            ]
        )

    def list_curated_collections(self) -> list[CollectionWithStatus]:
        manifest = load_collection_manifest("maps.json", default={"collections": []})
        existing_filenames = {
            file.name for file in self.get_pmtiles_storage_path().glob("*.pmtiles")
        }
        collections: list[CollectionWithStatus] = []

        for raw_collection in manifest["collections"]:
            resources = [
                SpecResource.model_validate(resource) for resource in raw_collection["resources"]
            ]
            installed_count = sum(
                1
                for resource in resources
                if self._filename_from_url(resource.url) in existing_filenames
            )
            collections.append(
                CollectionWithStatus(
                    name=raw_collection["name"],
                    slug=raw_collection["slug"],
                    description=raw_collection["description"],
                    icon=raw_collection["icon"],
                    language=raw_collection["language"],
                    resources=resources,
                    all_installed=installed_count == len(resources),
                    installed_count=installed_count,
                    total_count=len(resources),
                )
            )

        return collections

    def get_installed_resource_versions(self) -> dict[str, str]:
        versions: dict[str, str] = {}
        for file in self.get_pmtiles_storage_path().glob("*.pmtiles"):
            resource_id, version = self._split_resource_id_and_version(file.stem)
            if not resource_id or not version:
                continue
            current = versions.get(resource_id)
            if current is None or version > current:
                versions[resource_id] = version
        return versions

    def fetch_latest_collections(self) -> bool:
        return True

    def download_base_assets(self, url: str | None = None) -> bool:
        maps_root = self.get_maps_storage_path()
        maps_root.mkdir(parents=True, exist_ok=True)
        self.get_pmtiles_storage_path().mkdir(parents=True, exist_ok=True)
        self.get_sprite_json_path().parent.mkdir(parents=True, exist_ok=True)
        self.get_font_path().parent.mkdir(parents=True, exist_ok=True)

        if not self.get_base_styles_path().exists():
            self.get_base_styles_path().write_text(json.dumps(BASE_STYLE_TEMPLATE, indent=2))
        if not self.get_sprite_json_path().exists():
            self.get_sprite_json_path().write_text("{}")
        if not self.get_sprite_png_path().exists():
            self.get_sprite_png_path().write_bytes(TRANSPARENT_PNG_BYTES)
        if not self.get_font_path().exists():
            self.get_font_path().write_bytes(b"")
        return True

    def base_assets_ready(self) -> bool:
        return (
            self.get_base_styles_path().exists()
            and self.get_sprite_json_path().exists()
            and self.get_sprite_png_path().exists()
            and self.get_font_path().exists()
        )

    def generate_styles(self) -> BaseStylesFile:
        if not self.base_assets_ready():
            raise ValueError("Base map assets are missing from storage/maps")

        template = json.loads(self.get_base_styles_path().read_text())
        region_files = self.list_regions().files
        sources = {
            self._resource_id_from_filename(region.name): SourceDefinition(
                type="vector",
                attribution=PMTILES_ATTRIBUTION,
                url=f"pmtiles://{self._api_base_url()}/api/maps/files/{region.name}",
            )
            for region in region_files
        }

        layers = [layer for layer in template["layers"] if "source" not in layer]
        template_layers = [layer for layer in template["layers"] if "source" in layer]
        for source_name in sources:
            for layer in template_layers:
                next_layer = dict(layer)
                next_layer["id"] = next_layer["id"].replace("-template", f"-{source_name}")
                next_layer["source"] = source_name
                layers.append(next_layer)

        return BaseStylesFile(
            version=template["version"],
            sources=sources,
            layers=layers,
            sprite=f"{self._api_base_url()}/api/maps/assets/{SPRITE_RELATIVE_PATH}",
            glyphs=f"{self._api_base_url()}/api/maps/assets/{BASE_ASSETS_DIRNAME}/fonts/{{fontstack}}/{{range}}.pbf",
        )

    def download_remote(self, request: RemoteDownloadRequest) -> RemoteMapDownloadResponse:
        filename = self._validate_pmtiles_url(request.url)
        filepath = self.get_pmtiles_storage_path() / filename
        job = self.download_service.schedule_download(
            url=request.url,
            filepath=str(filepath),
            filetype="map",
        )
        return RemoteMapDownloadResponse(
            message="Download queued",
            filename=filename,
            jobId=job.job_id,
            url=request.url,
        )

    def download_remote_preflight(self, url: str) -> MapRemotePreflightResponse:
        filename = self._validate_pmtiles_url(url)
        response = self.remote_client.preflight(url)
        return MapRemotePreflightResponse(filename=filename, size=response.size)

    def download_collection(self, request: DownloadCollectionRequest) -> CollectionDownloadResponse:
        collection = next(
            (item for item in self.list_curated_collections() if item.slug == request.slug),
            None,
        )
        if collection is None:
            raise ValueError(f"Unknown collection: {request.slug}")

        existing_filenames = {
            file.name for file in self.get_pmtiles_storage_path().glob("*.pmtiles")
        }
        queued: list[str] = []
        for resource in collection.resources:
            filename = self._filename_from_url(resource.url)
            if filename in existing_filenames:
                continue
            job = self.download_service.schedule_download(
                url=resource.url,
                filepath=str(self.get_pmtiles_storage_path() / filename),
                filetype="map",
            )
            queued.append(Path(job.filepath).name)

        return CollectionDownloadResponse(
            message=(
                "Collection download queued" if queued else "All collection files already present"
            ),
            slug=request.slug,
            resources=queued or None,
        )

    def delete(self, filename: str) -> None:
        safe_name = filename if filename.endswith(".pmtiles") else f"{filename}.pmtiles"
        if safe_name != Path(safe_name).name:
            raise ValueError("Invalid filename")

        base_path = self.get_pmtiles_storage_path().resolve()
        target = (base_path / safe_name).resolve()
        if target.parent != base_path:
            raise ValueError("Invalid filename")
        if not target.exists():
            raise FileNotFoundError(safe_name)
        target.unlink()

    def resolve_map_file(self, filename: str) -> Path:
        safe_name = filename if filename.endswith(".pmtiles") else f"{filename}.pmtiles"
        if safe_name != Path(safe_name).name:
            raise ValueError("Invalid filename")
        path = (self.get_pmtiles_storage_path() / safe_name).resolve()
        if path.parent != self.get_pmtiles_storage_path().resolve():
            raise ValueError("Invalid filename")
        return path

    def resolve_asset_file(self, relative_path: str) -> Path:
        candidate = (self.get_maps_storage_path() / relative_path).resolve()
        maps_root = self.get_maps_storage_path().resolve()
        if not str(candidate).startswith(str(maps_root)):
            raise ValueError("Invalid asset path")
        return candidate

    def _validate_pmtiles_url(self, url: str) -> str:
        filename = self._filename_from_url(url)
        if not filename.endswith(".pmtiles"):
            raise ValueError(f"Invalid PMTiles file URL: {url}")
        return filename

    def _filename_from_url(self, url: str) -> str:
        return Path(urlparse(url).path).name

    def _resource_id_from_filename(self, filename: str) -> str:
        stem = filename.removesuffix(".pmtiles")
        if "_" in stem:
            return stem.rsplit("_", 1)[0]
        return stem

    def _split_resource_id_and_version(self, stem: str) -> tuple[str, str | None]:
        if "_" not in stem:
            return stem, None
        resource_id, version = stem.rsplit("_", 1)
        return resource_id, version

    def _api_base_url(self) -> str:
        settings = get_settings()
        return settings.frontend_api_base_url.rstrip("/")
