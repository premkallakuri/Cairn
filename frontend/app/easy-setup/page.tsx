import { EasySetupOverview } from "@/features/easy_setup";
import { buildEasySetupPlan, getEasySetupBootstrap } from "@/lib/api/client";
import type { EasySetupDraft } from "@/lib/types/atlas-haven-api";

const emptyDraft: EasySetupDraft = {
  currentStep: 0,
  selectedCapabilityIds: [],
  selectedMapCollectionSlugs: [],
  selectedCategoryTierSlugs: {},
  selectedAiModelIds: [],
  selectedWikipediaOptionId: "none",
};

export default async function EasySetupPage() {
  let bootstrap;
  try {
    bootstrap = await getEasySetupBootstrap();
  } catch {
    bootstrap = {
      draft: emptyDraft,
      capabilities: [],
      additionalTools: [],
      mapCollections: [],
      curatedCategories: [],
      wikipediaOptions: [],
      aiModels: [],
    };
  }

  let plan;
  try {
    plan = await buildEasySetupPlan(bootstrap.draft);
  } catch {
    plan = {
      draft: bootstrap.draft,
      services: [],
      maps: [],
      categorySelections: [],
      aiModels: [],
      wikipedia: {
        id: "none",
        name: "None",
        description: "No Wikipedia download",
        sizeMb: 0,
        url: null,
        version: null,
      },
      summary: {
        serviceCount: 0,
        mapCollectionCount: 0,
        mapResourceCount: 0,
        categorySelectionCount: 0,
        categoryResourceCount: 0,
        aiModelCount: 0,
        totalEstimatedStorageMb: 0,
        totalEstimatedStorageLabel: "0 MB",
      },
    };
  }

  return <EasySetupOverview initialBootstrap={bootstrap} initialPlan={plan} />;
}
