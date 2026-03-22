from __future__ import annotations

from dataclasses import dataclass

from app.modules.catalog.repository import CatalogRepository
from app.modules.catalog.service import CatalogSyncService
from app.modules.easy_setup.repository import EasySetupRepository
from app.modules.easy_setup.schemas import (
    CategoryManifest,
    CategoryTierManifest,
    CategoryWithStatus,
    EasySetupAiModelOption,
    EasySetupBootstrapResponse,
    EasySetupCapabilityOption,
    EasySetupDraft,
    EasySetupMapCollectionOption,
    EasySetupPlan,
    EasySetupPlanSummary,
    EasySetupWikipediaOption,
    MapCollectionManifest,
    PlannedAiModel,
    PlannedCategorySelection,
    PlannedMapCollection,
    PlannedService,
    PlannedWikipediaSelection,
    SpecTier,
    WikipediaOptionManifest,
)
from app.shared.collections import load_collection_manifest


@dataclass(frozen=True, slots=True)
class CapabilityDefinition:
    id: str
    group: str
    name: str
    technical_name: str
    description: str
    features: tuple[str, ...]
    service_name: str
    recommended: bool = False


CORE_CAPABILITIES: tuple[CapabilityDefinition, ...] = (
    CapabilityDefinition(
        id="information",
        group="core",
        name="Information Library",
        technical_name="Kiwix",
        description="Offline access to encyclopedias, medical references, and field guides.",
        features=(
            "Wikipedia and medical references",
            "Repair guides and survival content",
            "Local-first reading with no account",
        ),
        service_name="nomad_kiwix_server",
        recommended=True,
    ),
    CapabilityDefinition(
        id="education",
        group="core",
        name="Education Platform",
        technical_name="Kolibri",
        description="Offline education platform for courses, videos, and exercises.",
        features=(
            "Structured learning paths",
            "Interactive exercises and lessons",
            "Device-local curriculum access",
        ),
        service_name="nomad_kolibri",
        recommended=True,
    ),
    CapabilityDefinition(
        id="ai",
        group="core",
        name="AI Assistant Runtime",
        technical_name="Ollama",
        description="Local chat and model runtime that stays on your own hardware.",
        features=(
            "Private local AI sessions",
            "Offline use after models are installed",
            "Reusable runtime for chat and retrieval",
        ),
        service_name="nomad_ollama",
        recommended=True,
    ),
)

ADDITIONAL_TOOLS: tuple[CapabilityDefinition, ...] = (
    CapabilityDefinition(
        id="notes",
        group="tool",
        name="Notes",
        technical_name="FlatNotes",
        description="Simple local notes for field logs and knowledge capture.",
        features=(
            "Markdown-first note taking",
            "Local storage",
            "Fast search and lightweight editing",
        ),
        service_name="nomad_flatnotes",
    ),
    CapabilityDefinition(
        id="datatools",
        group="tool",
        name="Data Tools",
        technical_name="CyberChef",
        description="Transform, inspect, and decode data with a browser-based toolkit.",
        features=(
            "Encoding and decoding",
            "Hashing and transformation recipes",
            "Local browser workflow",
        ),
        service_name="nomad_cyberchef",
    ),
)

FALLBACK_AI_MODELS: tuple[EasySetupAiModelOption, ...] = (
    EasySetupAiModelOption(
        id="llama3.1:8b-text-q4_1",
        label="Llama 3.1 8B",
        description="Balanced general-purpose local assistant for writing and Q&A.",
        tag="llama3.1:8b-text-q4_1",
        sizeLabel="5.1 GB",
        sizeMb=5222,
        recommended=True,
    ),
    EasySetupAiModelOption(
        id="deepseek-r1:1.5b",
        label="DeepSeek R1 1.5B",
        description="Small reasoning-focused model for lightweight local inference.",
        tag="deepseek-r1:1.5b",
        sizeLabel="1.1 GB",
        sizeMb=1126,
        recommended=True,
        thinking=True,
    ),
    EasySetupAiModelOption(
        id="llama3.2:1b-text-q2_K",
        label="Llama 3.2 1B",
        description="Very small text model for constrained hardware and quick setup.",
        tag="llama3.2:1b-text-q2_K",
        sizeLabel="581 MB",
        sizeMb=581,
        recommended=True,
    ),
)


class EasySetupService:
    def __init__(
        self,
        repository: EasySetupRepository | None = None,
        catalog_repository: CatalogRepository | None = None,
    ) -> None:
        self.repository = repository or EasySetupRepository()
        self.catalog_repository = catalog_repository or CatalogRepository()

    def list_curated_categories(self) -> list[CategoryWithStatus]:
        return [
            CategoryWithStatus(
                name=category.name,
                slug=category.slug,
                icon=category.icon,
                description=category.description,
                language=category.language,
                installedTierSlug=None,
                tiers=[
                    SpecTier(
                        name=tier.name,
                        slug=tier.slug,
                        description=tier.description,
                        recommended=tier.recommended,
                        includesTier=tier.includesTier,
                    )
                    for tier in category.tiers
                ],
            )
            for category in self._load_categories()
        ]

    def get_draft(self) -> EasySetupDraft:
        return self.repository.get_draft()

    def save_draft(self, draft: EasySetupDraft) -> EasySetupDraft:
        return self.repository.save_draft(draft)

    def get_bootstrap(self) -> EasySetupBootstrapResponse:
        installed_services = {
            service["service_name"]: bool(service["installed"])
            for service in self.catalog_repository.list_services()
        }
        return EasySetupBootstrapResponse(
            draft=self.get_draft(),
            capabilities=[
                self._to_capability_option(item, installed_services) for item in CORE_CAPABILITIES
            ],
            additionalTools=[
                self._to_capability_option(item, installed_services) for item in ADDITIONAL_TOOLS
            ],
            mapCollections=self._build_map_collection_options(),
            curatedCategories=self.list_curated_categories(),
            wikipediaOptions=self._build_wikipedia_options(),
            aiModels=list(FALLBACK_AI_MODELS),
        )

    def build_plan(self, draft: EasySetupDraft) -> EasySetupPlan:
        services = self._build_services(draft)
        map_selections = self._build_map_selections(draft)
        category_selections = self._build_category_selections(draft)
        ai_models = self._build_ai_model_selections(draft)
        wikipedia = self._build_wikipedia_selection(draft)

        total_storage_mb = (
            sum(item.sizeMb for item in map_selections)
            + sum(item.sizeMb for item in category_selections)
            + sum(item.sizeMb for item in ai_models)
            + wikipedia.sizeMb
        )
        summary = EasySetupPlanSummary(
            serviceCount=len(services),
            mapCollectionCount=len(map_selections),
            mapResourceCount=sum(item.resourceCount for item in map_selections),
            categorySelectionCount=len(category_selections),
            categoryResourceCount=sum(item.resourceCount for item in category_selections),
            aiModelCount=len(ai_models),
            totalEstimatedStorageMb=total_storage_mb,
            totalEstimatedStorageLabel=self._format_storage(total_storage_mb),
        )
        return EasySetupPlan(
            draft=draft,
            services=services,
            maps=map_selections,
            categorySelections=category_selections,
            aiModels=ai_models,
            wikipedia=wikipedia,
            summary=summary,
        )

    def _build_services(self, draft: EasySetupDraft) -> list[PlannedService]:
        if not self.catalog_repository.list_services():
            CatalogSyncService(repository=self.catalog_repository).sync_from_disk()
        definitions = {item.id: item for item in (*CORE_CAPABILITIES, *ADDITIONAL_TOOLS)}
        catalog_entries = {
            service["service_name"]: service for service in self.catalog_repository.list_services()
        }
        planned: list[PlannedService] = []
        added: set[str] = set()

        def add_service(service_name: str, reason: str) -> None:
            if service_name in added:
                return
            service = catalog_entries.get(service_name)
            if service is None:
                raise ValueError(f"Unknown service in easy setup plan: {service_name}")
            manifest = service["manifest"]
            for dependency in manifest.get("dependencies", []):
                dependency_entry = catalog_entries.get(dependency)
                if dependency_entry is None:
                    raise ValueError(f"Unknown dependency in easy setup plan: {dependency}")
                add_service(
                    dependency,
                    f"Dependency for {service['friendly_name'] or service_name}",
                )
            added.add(service_name)
            planned.append(
                PlannedService(
                    serviceName=service_name,
                    friendlyName=service["friendly_name"] or service_name,
                    reason=reason,
                    alreadyInstalled=bool(service["installed"]),
                )
            )

        for capability_id in draft.selectedCapabilityIds:
            definition = definitions.get(capability_id)
            if definition is None:
                continue
            add_service(definition.service_name, f"Selected {definition.name}")

        if draft.selectedMapCollectionSlugs:
            add_service("nomad_maps", "Required to open selected map collections")
        if draft.selectedCategoryTierSlugs or draft.selectedWikipediaOptionId != "none":
            add_service("nomad_kiwix_server", "Required for selected offline library content")
        if draft.selectedAiModelIds:
            add_service("nomad_ollama", "Required to run selected AI models")

        return planned

    def _build_map_collection_options(self) -> list[EasySetupMapCollectionOption]:
        return [
            EasySetupMapCollectionOption(
                name=collection.name,
                slug=collection.slug,
                description=collection.description,
                icon=collection.icon,
                language=collection.language,
                resourceCount=len(collection.resources),
                sizeMb=sum(resource.size_mb for resource in collection.resources),
            )
            for collection in self._load_map_collections()
        ]

    def _build_map_selections(self, draft: EasySetupDraft) -> list[PlannedMapCollection]:
        collections = {collection.slug: collection for collection in self._load_map_collections()}
        selections: list[PlannedMapCollection] = []
        for slug in draft.selectedMapCollectionSlugs:
            collection = collections.get(slug)
            if collection is None:
                continue
            selections.append(
                PlannedMapCollection(
                    slug=collection.slug,
                    name=collection.name,
                    resourceCount=len(collection.resources),
                    sizeMb=sum(resource.size_mb for resource in collection.resources),
                )
            )
        return selections

    def _build_category_selections(self, draft: EasySetupDraft) -> list[PlannedCategorySelection]:
        categories = {category.slug: category for category in self._load_categories()}
        selections: list[PlannedCategorySelection] = []
        for category_slug, tier_slug in draft.selectedCategoryTierSlugs.items():
            category = categories.get(category_slug)
            if category is None:
                continue
            tier = next((item for item in category.tiers if item.slug == tier_slug), None)
            if tier is None:
                continue
            resources = self._resolve_tier_resources(tier, category.tiers)
            selections.append(
                PlannedCategorySelection(
                    categorySlug=category.slug,
                    categoryName=category.name,
                    tierSlug=tier.slug,
                    tierName=tier.name,
                    resourceCount=len(resources),
                    sizeMb=sum(resource.size_mb for resource in resources),
                )
            )
        return selections

    def _build_ai_model_selections(self, draft: EasySetupDraft) -> list[PlannedAiModel]:
        models = {model.id: model for model in FALLBACK_AI_MODELS}
        selections: list[PlannedAiModel] = []
        for model_id in draft.selectedAiModelIds:
            model = models.get(model_id)
            if model is None:
                continue
            selections.append(
                PlannedAiModel(
                    id=model.id,
                    label=model.label,
                    tag=model.tag,
                    sizeLabel=model.sizeLabel,
                    sizeMb=model.sizeMb,
                )
            )
        return selections

    def _build_wikipedia_options(self) -> list[EasySetupWikipediaOption]:
        return [
            EasySetupWikipediaOption(
                id=option.id,
                name=option.name,
                description=option.description,
                sizeMb=option.size_mb,
                url=option.url,
                version=option.version,
            )
            for option in self._load_wikipedia_options()
        ]

    def _build_wikipedia_selection(self, draft: EasySetupDraft) -> PlannedWikipediaSelection:
        options = {option.id: option for option in self._load_wikipedia_options()}
        selected = options.get(draft.selectedWikipediaOptionId) or options["none"]
        return PlannedWikipediaSelection(
            id=selected.id,
            name=selected.name,
            description=selected.description,
            sizeMb=selected.size_mb,
            url=selected.url,
            version=selected.version,
        )

    def _to_capability_option(
        self,
        definition: CapabilityDefinition,
        installed_services: dict[str, bool],
    ) -> EasySetupCapabilityOption:
        return EasySetupCapabilityOption(
            id=definition.id,
            group=definition.group,
            name=definition.name,
            technicalName=definition.technical_name,
            description=definition.description,
            features=list(definition.features),
            serviceName=definition.service_name,
            installed=installed_services.get(definition.service_name, False),
            recommended=definition.recommended,
        )

    def _resolve_tier_resources(
        self,
        tier: CategoryTierManifest,
        all_tiers: list[CategoryTierManifest],
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

    def _load_categories(self) -> list[CategoryManifest]:
        manifest = load_collection_manifest(
            "kiwix-categories.json", default={"categories": []}
        )
        return [CategoryManifest.model_validate(item) for item in manifest["categories"]]

    def _load_map_collections(self) -> list[MapCollectionManifest]:
        manifest = load_collection_manifest("maps.json", default={"collections": []})
        return [MapCollectionManifest.model_validate(item) for item in manifest["collections"]]

    def _load_wikipedia_options(self) -> list[WikipediaOptionManifest]:
        manifest = load_collection_manifest("wikipedia.json", default={"options": []})
        return [WikipediaOptionManifest.model_validate(item) for item in manifest["options"]]

    def _format_storage(self, total_storage_mb: int) -> str:
        if total_storage_mb >= 1024:
            return f"{total_storage_mb / 1024:.1f} GB"
        return f"{total_storage_mb} MB"
