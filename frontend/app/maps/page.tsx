import { MapsOverview } from "@/features/maps";
import { getMapStyles, listCuratedMapCollections, listMapRegions, listServices } from "@/lib/api/client";

export default async function MapsPage() {
  const [services, regions, collections] = await Promise.all([
    listServices().catch(() => []),
    listMapRegions().catch(() => ({ files: [] })),
    listCuratedMapCollections().catch(() => []),
  ]);

  let styles = null;
  let stylesError = null;
  try {
    styles = await getMapStyles();
  } catch (error) {
    stylesError = error instanceof Error ? error.message : "Map styles are not ready yet.";
  }

  return (
    <MapsOverview
      services={services}
      regions={regions.files}
      collections={collections}
      styles={styles}
      stylesError={stylesError}
    />
  );
}
