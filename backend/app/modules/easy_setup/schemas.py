from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


class ManifestResource(BaseModel):
    id: str
    version: str | None = None
    title: str
    description: str
    url: str | None = None
    size_mb: int = 0


class CategoryTierManifest(BaseModel):
    name: str
    slug: str
    description: str
    recommended: bool = False
    includesTier: str | None = None
    resources: list[ManifestResource] = Field(default_factory=list)


class CategoryManifest(BaseModel):
    name: str
    slug: str
    icon: str
    description: str
    language: str
    tiers: list[CategoryTierManifest] = Field(default_factory=list)


class MapCollectionManifest(BaseModel):
    name: str
    slug: str
    description: str
    icon: str
    language: str
    resources: list[ManifestResource] = Field(default_factory=list)


class WikipediaOptionManifest(BaseModel):
    id: str
    name: str
    description: str
    size_mb: int = 0
    url: str | None = None
    version: str | None = None


class SpecTier(BaseModel):
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
    tiers: list[SpecTier] = Field(default_factory=list)


class EasySetupDraft(BaseModel):
    currentStep: int = Field(default=1, ge=1, le=4)
    selectedCapabilityIds: list[str] = Field(default_factory=list)
    selectedMapCollectionSlugs: list[str] = Field(default_factory=list)
    selectedCategoryTierSlugs: dict[str, str] = Field(default_factory=dict)
    selectedAiModelIds: list[str] = Field(default_factory=list)
    selectedWikipediaOptionId: str = "none"

    @field_validator(
        "selectedCapabilityIds",
        "selectedMapCollectionSlugs",
        "selectedAiModelIds",
        mode="before",
    )
    @classmethod
    def normalize_lists(cls, value: Any) -> list[str]:
        if value is None:
            return []
        return _dedupe([str(item) for item in value])


class EasySetupCapabilityOption(BaseModel):
    id: str
    group: str
    name: str
    technicalName: str
    description: str
    features: list[str] = Field(default_factory=list)
    serviceName: str
    installed: bool = False
    recommended: bool = False


class EasySetupMapCollectionOption(BaseModel):
    name: str
    slug: str
    description: str
    icon: str
    language: str
    resourceCount: int
    sizeMb: int


class EasySetupAiModelOption(BaseModel):
    id: str
    label: str
    description: str
    tag: str
    sizeLabel: str
    sizeMb: int
    recommended: bool = False
    thinking: bool = False
    requiresService: str = "nomad_ollama"


class EasySetupWikipediaOption(BaseModel):
    id: str
    name: str
    description: str
    sizeMb: int
    url: str | None = None
    version: str | None = None


class EasySetupBootstrapResponse(BaseModel):
    draft: EasySetupDraft
    capabilities: list[EasySetupCapabilityOption] = Field(default_factory=list)
    additionalTools: list[EasySetupCapabilityOption] = Field(default_factory=list)
    mapCollections: list[EasySetupMapCollectionOption] = Field(default_factory=list)
    curatedCategories: list[CategoryWithStatus] = Field(default_factory=list)
    wikipediaOptions: list[EasySetupWikipediaOption] = Field(default_factory=list)
    aiModels: list[EasySetupAiModelOption] = Field(default_factory=list)


class PlannedService(BaseModel):
    serviceName: str
    friendlyName: str
    reason: str
    alreadyInstalled: bool


class PlannedMapCollection(BaseModel):
    slug: str
    name: str
    resourceCount: int
    sizeMb: int


class PlannedCategorySelection(BaseModel):
    categorySlug: str
    categoryName: str
    tierSlug: str
    tierName: str
    resourceCount: int
    sizeMb: int


class PlannedAiModel(BaseModel):
    id: str
    label: str
    tag: str
    sizeLabel: str
    sizeMb: int


class PlannedWikipediaSelection(BaseModel):
    id: str
    name: str
    description: str
    sizeMb: int
    url: str | None = None
    version: str | None = None


class EasySetupPlanSummary(BaseModel):
    serviceCount: int
    mapCollectionCount: int
    mapResourceCount: int
    categorySelectionCount: int
    categoryResourceCount: int
    aiModelCount: int
    totalEstimatedStorageMb: int
    totalEstimatedStorageLabel: str


class EasySetupPlan(BaseModel):
    draft: EasySetupDraft
    services: list[PlannedService] = Field(default_factory=list)
    maps: list[PlannedMapCollection] = Field(default_factory=list)
    categorySelections: list[PlannedCategorySelection] = Field(default_factory=list)
    aiModels: list[PlannedAiModel] = Field(default_factory=list)
    wikipedia: PlannedWikipediaSelection
    summary: EasySetupPlanSummary
