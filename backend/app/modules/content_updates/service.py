from __future__ import annotations

from datetime import datetime
from app.core.compat import UTC
from pathlib import Path

from app.core.config import get_settings
from app.modules.content_updates.schemas import (
    ContentUpdateApplyAllItemResult,
    ContentUpdateApplyAllRequest,
    ContentUpdateApplyAllResponse,
    ContentUpdateApplyResponse,
    ContentUpdateCheckResult,
    ManifestRefreshChanged,
    ManifestRefreshResponse,
    ResourceUpdateInfo,
)
from app.modules.downloads.service import DownloadJobService
from app.modules.maps.schemas import RemoteDownloadRequest
from app.modules.maps.service import MapService
from app.modules.zim.schemas import RemoteZimDownloadRequest
from app.modules.zim.service import ZimService
from app.shared.collections import load_collection_manifest


class ContentManifestStore:
    def __init__(self, cache_root: Path | None = None) -> None:
        settings = get_settings()
        self.cache_root = cache_root or settings.storage_path / "content-manifests"

    def refresh(self) -> ManifestRefreshChanged:
        self.cache_root.mkdir(parents=True, exist_ok=True)
        return ManifestRefreshChanged(
            zim_categories=self._copy_if_changed("kiwix-categories.json"),
            maps=self._copy_if_changed("maps.json"),
            wikipedia=self._copy_if_changed("wikipedia.json"),
        )

    def load(self, filename: str) -> dict[str, object]:
        cached = self.cache_root / filename
        if cached.exists():
            import json

            return json.loads(cached.read_text())
        _defaults: dict[str, dict[str, object]] = {
            "maps.json": {"collections": []},
            "kiwix-categories.json": {"categories": []},
            "wikipedia.json": {"options": []},
        }
        return load_collection_manifest(filename, default=_defaults.get(filename))

    def _copy_if_changed(self, filename: str) -> bool:
        settings = get_settings()
        source = settings.resolved_collections_path / filename
        destination = self.cache_root / filename
        try:
            source_text = source.read_text()
        except FileNotFoundError:
            return False
        if destination.exists() and destination.read_text() == source_text:
            return False
        destination.write_text(source_text)
        return True


class ContentUpdatesService:
    def __init__(
        self,
        manifest_store: ContentManifestStore | None = None,
        map_service: MapService | None = None,
        zim_service: ZimService | None = None,
        download_service: DownloadJobService | None = None,
    ) -> None:
        self.manifest_store = manifest_store or ContentManifestStore()
        self.map_service = map_service or MapService()
        self.zim_service = zim_service or ZimService()
        self.download_service = download_service or DownloadJobService()

    def refresh_manifests(self) -> ManifestRefreshResponse:
        return ManifestRefreshResponse(success=True, changed=self.manifest_store.refresh())

    def check_updates(self) -> ContentUpdateCheckResult:
        updates: list[ResourceUpdateInfo] = []
        updates.extend(self._check_map_updates())
        updates.extend(self._check_zim_updates())
        updates.extend(self._check_wikipedia_updates())
        updates.sort(key=lambda item: (item.resource_type, item.resource_id))
        return ContentUpdateCheckResult(updates=updates, checked_at=datetime.now(UTC))

    def apply_update(self, update: ResourceUpdateInfo) -> ContentUpdateApplyResponse:
        try:
            job_id = self._queue_update(update)
        except Exception as exc:  # pragma: no cover - defensive response shaping
            return ContentUpdateApplyResponse(success=False, error=str(exc))
        return ContentUpdateApplyResponse(success=True, jobId=job_id)

    def apply_all_updates(
        self, request: ContentUpdateApplyAllRequest
    ) -> ContentUpdateApplyAllResponse:
        results = [
            ContentUpdateApplyAllItemResult(
                resource_id=update.resource_id,
                success=(response := self.apply_update(update)).success,
                jobId=response.jobId,
                error=response.error,
            )
            for update in request.updates
        ]
        return ContentUpdateApplyAllResponse(results=results)

    def _check_map_updates(self) -> list[ResourceUpdateInfo]:
        installed_versions = self.map_service.get_installed_resource_versions()
        manifest = self.manifest_store.load("maps.json")
        updates: list[ResourceUpdateInfo] = []
        for collection in manifest["collections"]:
            for resource in collection["resources"]:
                resource_id = str(resource["id"])
                latest_version = str(resource["version"])
                installed_version = installed_versions.get(resource_id)
                if installed_version and installed_version != latest_version:
                    updates.append(
                        ResourceUpdateInfo(
                            resource_id=resource_id,
                            resource_type="map",
                            installed_version=installed_version,
                            latest_version=latest_version,
                            download_url=str(resource["url"]),
                        )
                    )
        return updates

    def _check_zim_updates(self) -> list[ResourceUpdateInfo]:
        installed_versions = self.zim_service.get_installed_resource_versions()
        manifest = self.manifest_store.load("kiwix-categories.json")
        updates: list[ResourceUpdateInfo] = []
        for category in manifest["categories"]:
            for tier in category["tiers"]:
                for resource in tier["resources"]:
                    resource_id = str(resource["id"])
                    latest_version = str(resource["version"])
                    installed_version = installed_versions.get(resource_id)
                    if installed_version and installed_version != latest_version:
                        updates.append(
                            ResourceUpdateInfo(
                                resource_id=resource_id,
                                resource_type="zim",
                                installed_version=installed_version,
                                latest_version=latest_version,
                                download_url=str(resource["url"]),
                            )
                        )
        return updates

    def _check_wikipedia_updates(self) -> list[ResourceUpdateInfo]:
        state = self.zim_service.get_wikipedia_state()
        selection = state.currentSelection
        if selection is None or selection.status != "installed":
            return []
        selected_option = next(
            (option for option in state.options if option.id == selection.optionId),
            None,
        )
        if selected_option is None or not selected_option.version:
            return []

        installed_version = self.zim_service.get_wikipedia_installed_version()
        if installed_version is None or installed_version == selected_option.version:
            return []

        return [
            ResourceUpdateInfo(
                resource_id=selected_option.id,
                resource_type="zim",
                installed_version=installed_version,
                latest_version=selected_option.version,
                download_url=selected_option.url or "",
            )
        ]

    def _queue_update(self, update: ResourceUpdateInfo) -> str:
        if update.resource_type == "map":
            response = self.map_service.download_remote(
                RemoteDownloadRequest(url=update.download_url)
            )
            if response.jobId is None:
                raise RuntimeError("Map update did not return a job identifier")
            return response.jobId

        response = self.zim_service.download_remote(
            RemoteZimDownloadRequest(url=update.download_url)
        )
        if response.jobId is None:
            raise RuntimeError("ZIM update did not return a job identifier")
        return response.jobId
