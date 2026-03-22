from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from shutil import copyfile
from urllib.parse import urlparse
from xml.etree import ElementTree

import httpx

from app.core.config import get_settings
from app.modules.downloads.service import DownloadJobService
from app.modules.zim.repository import WikipediaSelectionRepository
from app.modules.zim.schemas import (
    CategoryTierDownloadResponse,
    CategoryWithStatus,
    CuratedCategoryTier,
    CuratedZimResource,
    DownloadCategoryTierRequest,
    FileEntry,
    ListRemoteZimFilesResponse,
    ListZimFilesResponse,
    RemoteZimDownloadRequest,
    RemoteZimDownloadResponse,
    RemoteZimFileEntry,
    SelectWikipediaResponse,
    WikipediaCurrentSelection,
    WikipediaOption,
    WikipediaSelectionRequest,
    WikipediaState,
    WikipediaUpdateState,
    ZimManifestCategory,
    ZimManifestTier,
)
from app.shared.collections import load_collection_manifest

KIWIX_SEED_FILENAME = "wikipedia_en_100_mini_2025-06.zim"
ZIM_MIME_TYPES = {
    "application/x-zim",
    "application/x-openzim",
    "application/octet-stream",
}


class KiwixSeedService:
    def __init__(self, source_path: Path | None = None) -> None:
        settings = get_settings()
        self.source_path = source_path or settings.resolved_bundled_seed_zim_path

    def seed_demo_zim(self, target_dir: Path | None = None) -> Path:
        settings = get_settings()
        destination_dir = target_dir or settings.storage_path / "zim"
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / KIWIX_SEED_FILENAME

        if not destination.exists():
            copyfile(self.source_path, destination)

        return destination


class KiwixCatalogClient:
    def __init__(
        self,
        base_url: str | None = None,
        client_factory: Callable[[], httpx.Client] | None = None,
    ) -> None:
        settings = get_settings()
        self.base_url = base_url or settings.kiwix_catalog_url
        self.client_factory = client_factory or (
            lambda: httpx.Client(timeout=10.0, follow_redirects=True)
        )

    def list_remote(
        self,
        *,
        start: int,
        count: int,
        query: str | None = None,
    ) -> ListRemoteZimFilesResponse:
        with self.client_factory() as client:
            response = client.get(
                self.base_url,
                params={
                    "start": start,
                    "count": count,
                    "lang": "eng",
                    **({"q": query} if query else {}),
                },
            )
            response.raise_for_status()

        return self._parse_feed(response.text, start=start, count=count)

    def _parse_feed(self, payload: str, *, start: int, count: int) -> ListRemoteZimFilesResponse:
        root = ElementTree.fromstring(payload)
        namespaces = {
            "atom": "http://www.w3.org/2005/Atom",
            "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
        }

        total_count = int(
            root.findtext("opensearch:totalResults", default="0", namespaces=namespaces)
        )
        items: list[RemoteZimFileEntry] = []
        for entry in root.findall("atom:entry", namespaces):
            link = next(
                (
                    item
                    for item in entry.findall("atom:link", namespaces)
                    if item.attrib.get("type") in ZIM_MIME_TYPES
                ),
                None,
            )
            if link is None:
                continue

            href = link.attrib.get("href", "")
            download_url = href[:-6] if href.endswith(".meta4") else href
            file_name = Path(urlparse(download_url).path).name
            items.append(
                RemoteZimFileEntry(
                    id=entry.findtext("atom:id", default="", namespaces=namespaces),
                    title=entry.findtext("atom:title", default="", namespaces=namespaces),
                    updated=entry.findtext("atom:updated", default="", namespaces=namespaces),
                    summary=entry.findtext("atom:summary", default="", namespaces=namespaces),
                    size_bytes=int(link.attrib.get("length") or 0),
                    download_url=download_url,
                    author=entry.findtext(
                        "atom:author/atom:name", default="", namespaces=namespaces
                    ),
                    file_name=file_name,
                )
            )

        return ListRemoteZimFilesResponse(
            items=items,
            has_more=start + count < total_count,
            total_count=total_count,
        )


class ZimService:
    def __init__(
        self,
        repository: WikipediaSelectionRepository | None = None,
        download_service: DownloadJobService | None = None,
        catalog_client: KiwixCatalogClient | None = None,
        seed_service: KiwixSeedService | None = None,
    ) -> None:
        self.repository = repository or WikipediaSelectionRepository()
        self.download_service = download_service or DownloadJobService()
        self.catalog_client = catalog_client or KiwixCatalogClient()
        self.seed_service = seed_service or KiwixSeedService()

    def get_zim_storage_path(self) -> Path:
        settings = get_settings()
        return settings.storage_path / "zim"

    def list(self) -> ListZimFilesResponse:
        storage_path = self.get_zim_storage_path()
        storage_path.mkdir(parents=True, exist_ok=True)
        files = [
            FileEntry(
                key=file.name,
                name=file.name,
                title=file.stem.replace("_", " "),
                size_bytes=file.stat().st_size,
            )
            for file in sorted(storage_path.glob("*.zim"))
            if file.is_file()
        ]
        return ListZimFilesResponse(files=files)

    def list_remote(
        self,
        *,
        start: int,
        count: int,
        query: str | None = None,
    ) -> ListRemoteZimFilesResponse:
        payload = self.catalog_client.list_remote(start=start, count=count, query=query)
        existing_filenames = {file.name for file in self.get_zim_storage_path().glob("*.zim")}
        return ListRemoteZimFilesResponse(
            items=[item for item in payload.items if item.file_name not in existing_filenames],
            has_more=payload.has_more,
            total_count=payload.total_count,
        )

    def list_curated_categories(self) -> list[CategoryWithStatus]:
        manifest = load_collection_manifest(
            "kiwix-categories.json", default={"categories": []}
        )
        categories = [ZimManifestCategory.model_validate(item) for item in manifest["categories"]]
        installed_versions = self.get_installed_resource_versions()
        return [
            self._to_category_with_status(category, installed_versions) for category in categories
        ]

    def list_curated_resources(self) -> list[CuratedZimResource]:
        manifest = load_collection_manifest(
            "kiwix-categories.json", default={"categories": []}
        )
        resources: list[CuratedZimResource] = []
        for category in manifest["categories"]:
            for tier in category["tiers"]:
                for resource in tier["resources"]:
                    resources.append(
                        CuratedZimResource(
                            resource_id=resource["id"],
                            title=resource["title"],
                            version=resource["version"],
                            url=resource["url"],
                        )
                    )
        return resources

    def get_installed_resource_versions(self) -> dict[str, str]:
        versions: dict[str, str] = {}
        for file in self.get_zim_storage_path().glob("*.zim"):
            resource_id, version = self._split_resource_id_and_version(file.stem)
            if not resource_id or not version:
                continue
            current = versions.get(resource_id)
            if current is None or version > current:
                versions[resource_id] = version
        return versions

    def get_wikipedia_installed_version(self) -> str | None:
        selection = self.repository.get_selection()
        if selection is None or not selection.filename:
            return None
        _, version = self._split_resource_id_and_version(Path(selection.filename).stem)
        return version

    def get_wikipedia_update_state(self) -> WikipediaUpdateState:
        state = self.get_wikipedia_state()
        selection = state.currentSelection
        if selection is None or selection.status != "installed":
            return WikipediaUpdateState()
        selected_option = next(
            (option for option in state.options if option.id == selection.optionId),
            None,
        )
        if selected_option is None or not selected_option.version:
            return WikipediaUpdateState()
        installed_version = self.get_wikipedia_installed_version()
        return WikipediaUpdateState(
            installed_version=installed_version,
            latest_version=selected_option.version,
            download_url=selected_option.url,
            needs_update=bool(installed_version and installed_version != selected_option.version),
        )

    def _to_category_with_status(
        self, category: ZimManifestCategory, installed_versions: dict[str, str]
    ) -> CategoryWithStatus:
        tiers = [
            CuratedCategoryTier(
                name=tier.name,
                slug=tier.slug,
                description=tier.description,
                recommended=tier.recommended,
                includesTier=tier.includesTier,
            )
            for tier in category.tiers
        ]
        installed_tier_slug = None
        for tier in reversed(category.tiers):
            if tier.resources and all(
                installed_versions.get(resource.id) == resource.version
                for resource in tier.resources
            ):
                installed_tier_slug = tier.slug
                break
        return CategoryWithStatus(
            name=category.name,
            slug=category.slug,
            icon=category.icon,
            description=category.description,
            language=category.language,
            installedTierSlug=installed_tier_slug,
            tiers=tiers,
        )

    def _split_resource_id_and_version(self, stem: str) -> tuple[str, str | None]:
        if "_" not in stem:
            return stem, None
        resource_id, version = stem.rsplit("_", 1)
        return resource_id, version

    def download_remote(self, request: RemoteZimDownloadRequest) -> RemoteZimDownloadResponse:
        filename = self._get_filename_from_url(request.url)
        filepath = self.get_zim_storage_path() / filename
        job = self.download_service.schedule_download(
            url=request.url,
            filepath=str(filepath),
            filetype="zim",
        )
        return RemoteZimDownloadResponse(
            message="Download queued",
            filename=filename,
            jobId=job.job_id,
            url=request.url,
        )

    def download_category_tier(
        self, request: DownloadCategoryTierRequest
    ) -> CategoryTierDownloadResponse:
        category, tier = self._resolve_category_tier(
            category_slug=request.categorySlug,
            tier_slug=request.tierSlug,
        )
        resources = self._resolve_tier_resources(tier, category.tiers)
        existing_filenames = {file.name for file in self.get_zim_storage_path().glob("*.zim")}

        queued: list[str] = []
        for resource in resources:
            filename = self._get_filename_from_url(resource.url)
            if filename in existing_filenames:
                continue
            job = self.download_service.schedule_download(
                url=resource.url,
                filepath=str(self.get_zim_storage_path() / filename),
                filetype="zim",
            )
            queued.append(Path(job.filepath).name)

        return CategoryTierDownloadResponse(
            message="Tier download queued" if queued else "All tier resources already present",
            categorySlug=request.categorySlug,
            tierSlug=request.tierSlug,
            resources=queued or None,
        )

    def get_wikipedia_state(self) -> WikipediaState:
        manifest = load_collection_manifest("wikipedia.json", default={"options": []})
        options = [WikipediaOption.model_validate(item) for item in manifest["options"]]
        selection = self.repository.get_selection()
        current_selection = None
        if selection is not None:
            current_selection = WikipediaCurrentSelection(
                optionId=selection.option_id,
                status=selection.status,
                filename=selection.filename,
                url=selection.url,
            )
        return WikipediaState(options=options, currentSelection=current_selection)

    def select_wikipedia(self, request: WikipediaSelectionRequest) -> SelectWikipediaResponse:
        state = self.get_wikipedia_state()
        selected_option = next(
            (option for option in state.options if option.id == request.optionId),
            None,
        )
        if selected_option is None:
            raise ValueError(f"Invalid Wikipedia option: {request.optionId}")

        if request.optionId == "none":
            self._remove_wikipedia_files()
            self.repository.save_selection(option_id="none", status="none", filename=None, url=None)
            return SelectWikipediaResponse(success=True, message="Wikipedia removed")

        if request.optionId == "top-mini":
            seeded = self.seed_service.seed_demo_zim(self.get_zim_storage_path())
            self._remove_wikipedia_files(exclude={seeded.name})
            self.repository.save_selection(
                option_id=request.optionId,
                status="installed",
                filename=seeded.name,
                url=selected_option.url,
            )
            return SelectWikipediaResponse(
                success=True,
                message="Bundled demo Wikipedia is ready",
            )

        if not selected_option.url:
            raise ValueError("Selected Wikipedia option has no downloadable URL")

        filename = self._get_filename_from_url(selected_option.url)
        job = self.download_service.schedule_download(
            url=selected_option.url,
            filepath=str(self.get_zim_storage_path() / filename),
            filetype="zim",
        )
        self.repository.save_selection(
            option_id=request.optionId,
            status="downloading",
            filename=filename,
            url=selected_option.url,
        )
        return SelectWikipediaResponse(
            success=True,
            jobId=job.job_id,
            message="Download started",
        )

    def delete(self, filename: str) -> None:
        safe_name = self._normalize_filename(filename)
        base_path = self.get_zim_storage_path().resolve()
        target = (base_path / safe_name).resolve()
        if target.parent != base_path:
            raise ValueError("Invalid filename")
        if not target.exists():
            raise FileNotFoundError(safe_name)

        target.unlink()
        selection = self.repository.get_selection()
        if selection is not None and selection.filename == safe_name:
            self.repository.save_selection(option_id="none", status="none", filename=None, url=None)

    def _remove_wikipedia_files(self, *, exclude: set[str] | None = None) -> None:
        exclude_names = exclude or set()
        storage_path = self.get_zim_storage_path()
        storage_path.mkdir(parents=True, exist_ok=True)
        for file in storage_path.glob("wikipedia_en_*.zim"):
            if file.name in exclude_names:
                continue
            file.unlink()

    def _resolve_category_tier(
        self,
        *,
        category_slug: str,
        tier_slug: str,
    ) -> tuple[ZimManifestCategory, ZimManifestTier]:
        manifest = load_collection_manifest(
            "kiwix-categories.json", default={"categories": []}
        )
        categories = [ZimManifestCategory.model_validate(item) for item in manifest["categories"]]
        category = next((item for item in categories if item.slug == category_slug), None)
        if category is None:
            raise ValueError(f"Category not found: {category_slug}")

        tier = next((item for item in category.tiers if item.slug == tier_slug), None)
        if tier is None:
            raise ValueError(f"Tier not found: {tier_slug}")

        return category, tier

    def _resolve_tier_resources(
        self,
        tier: ZimManifestTier,
        all_tiers: list[ZimManifestTier],
        *,
        visited: set[str] | None = None,
    ):
        active = visited or set()
        if tier.slug in active:
            return []
        active.add(tier.slug)
        resources = []
        if tier.includesTier is not None:
            included = next((item for item in all_tiers if item.slug == tier.includesTier), None)
            if included is not None:
                resources.extend(self._resolve_tier_resources(included, all_tiers, visited=active))
        resources.extend(tier.resources)
        return resources

    def _normalize_filename(self, filename: str) -> str:
        candidate = filename if filename.endswith(".zim") else f"{filename}.zim"
        if candidate != Path(candidate).name:
            raise ValueError("Invalid filename")
        return candidate

    def _get_filename_from_url(self, url: str) -> str:
        parsed = urlparse(url)
        filename = Path(parsed.path).name
        if not filename.endswith(".zim"):
            raise ValueError(f"Invalid ZIM file URL: {url}")
        return filename
