import { FieldGuideOverview } from "@/features/field_guide";
import { getZimWikipediaState, listDocs, listZimFiles } from "@/lib/api/client";

export default async function DocsPage() {
  const [docs, zimFiles, wikipediaState] = await Promise.all([
    listDocs().catch(() => []),
    listZimFiles().catch(() => ({ files: [] })),
    getZimWikipediaState().catch(() => ({ options: [], currentSelection: null })),
  ]);
  return <FieldGuideOverview docs={docs} zimFiles={zimFiles.files} wikipediaState={wikipediaState} />;
}
