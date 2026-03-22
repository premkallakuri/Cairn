import pytest

from app.modules.easy_setup.schemas import EasySetupDraft
from app.modules.easy_setup.service import EasySetupService

pytestmark = [pytest.mark.unit, pytest.mark.easy_setup]


def test_build_plan_resolves_inherited_category_tiers() -> None:
    service = EasySetupService()

    plan = service.build_plan(
        EasySetupDraft(
            selectedCategoryTierSlugs={"medicine": "medicine-standard"},
        )
    )

    assert len(plan.categorySelections) == 1
    selection = plan.categorySelections[0]
    assert selection.categorySlug == "medicine"
    assert selection.tierSlug == "medicine-standard"
    assert selection.resourceCount == 5
    assert selection.sizeMb == 2131
    assert [service.serviceName for service in plan.services] == ["nomad_kiwix_server"]


def test_build_plan_expands_dependencies_and_storage_summary() -> None:
    service = EasySetupService()

    plan = service.build_plan(
        EasySetupDraft(
            selectedCapabilityIds=["ai", "notes"],
            selectedMapCollectionSlugs=["pacific"],
            selectedCategoryTierSlugs={"medicine": "medicine-essential"},
            selectedAiModelIds=["deepseek-r1:1.5b"],
            selectedWikipediaOptionId="top-mini",
        )
    )

    assert [item.serviceName for item in plan.services] == [
        "nomad_qdrant",
        "nomad_ollama",
        "nomad_flatnotes",
        "nomad_maps",
        "nomad_kiwix_server",
    ]
    assert plan.summary.serviceCount == 5
    assert plan.summary.mapCollectionCount == 1
    assert plan.summary.categorySelectionCount == 1
    assert plan.summary.aiModelCount == 1
    assert plan.summary.totalEstimatedStorageMb == 4427
    assert plan.summary.totalEstimatedStorageLabel == "4.3 GB"
