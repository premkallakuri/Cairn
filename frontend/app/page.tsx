import { BridgeDashboard } from "@/features/bridge";
import { getSystemInfo, listCuratedCategories, listDocs, listServices } from "@/lib/api/client";
import type { SystemInformationResponse } from "@/lib/types/atlas-haven-api";

export default async function HomePage() {
  const [services, docs, categories, systemInfo] = await Promise.all([
    listServices().catch(() => []),
    listDocs().catch(() => []),
    listCuratedCategories().catch(() => []),
    getSystemInfo().catch(
      (): SystemInformationResponse => ({
        app_name: "",
        version: "",
        environment: "",
        python_version: "",
        workspace_root: "",
        storage_path: "",
        catalog_entries: 0,
      }),
    ),
  ]);

  return (
    <BridgeDashboard
      docs={docs}
      services={services}
      categories={categories}
      systemInfo={systemInfo}
    />
  );
}
