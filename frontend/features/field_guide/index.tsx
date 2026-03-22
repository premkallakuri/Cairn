import { FileText, Library, BookOpen } from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import type {
  DocIndexItem,
  WikipediaState,
  ZimFileWithMetadata,
} from "@/lib/types/atlas-haven-api";

function formatSize(sizeBytes?: number | null) {
  if (!sizeBytes) {
    return "Unknown size";
  }
  const sizeMb = sizeBytes / (1024 * 1024);
  if (sizeMb >= 1024) {
    return `${(sizeMb / 1024).toFixed(1)} GB`;
  }
  return `${sizeMb.toFixed(1)} MB`;
}

export function FieldGuideOverview({
  docs,
  zimFiles,
  wikipediaState,
}: {
  docs: DocIndexItem[];
  zimFiles: ZimFileWithMetadata[];
  wikipediaState: WikipediaState;
}) {
  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
      <SectionCard title="Field Guide" eyebrow="Documentation">
        <div className="space-y-2">
          {docs.map((doc) => (
            <div
              key={doc.slug}
              className="flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 transition hover:border-brand-500/20"
            >
              <FileText size={14} className="shrink-0 text-content-tertiary" />
              <div>
                <p className="text-sm font-medium text-content">{doc.title}</p>
                <p className="text-xs text-content-tertiary">{doc.slug}</p>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Library Shelf" eyebrow="Kiwix And ZIM">
        <div className="space-y-4">
          <div className="flex items-start gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4">
            <Library size={16} className="mt-0.5 text-brand-500 dark:text-brand-400" />
            <div>
              <p className="text-xs text-content-tertiary">Local ZIM files</p>
              <p className="mt-1 text-2xl font-semibold text-content">{zimFiles.length}</p>
            </div>
          </div>

          <div className="rounded-xl border border-border-subtle bg-surface-2 p-4">
            <div className="flex items-center gap-2">
              <BookOpen size={14} className="text-content-tertiary" />
              <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Wikipedia</p>
            </div>
            {wikipediaState.currentSelection ? (
              <div className="mt-3">
                <p className="text-sm font-medium text-content">
                  {wikipediaState.currentSelection.optionId}
                </p>
                <p className="text-xs text-content-tertiary">
                  {wikipediaState.currentSelection.status} •{" "}
                  {wikipediaState.currentSelection.filename ?? "No file selected"}
                </p>
              </div>
            ) : (
              <p className="mt-3 text-sm text-content-tertiary">No Wikipedia package selected yet.</p>
            )}
          </div>

          <div className="space-y-2">
            {zimFiles.length === 0 ? (
              <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-sm text-content-tertiary">
                No local ZIM files yet. The bundled demo library will appear here after Kiwix seed
                or Wikipedia selection.
              </div>
            ) : (
              zimFiles.map((file) => (
                <div
                  key={file.key}
                  className="flex items-center justify-between rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 transition hover:border-brand-500/20"
                >
                  <p className="text-sm font-medium text-content">{file.title ?? file.name}</p>
                  <span className="text-xs text-content-tertiary">{formatSize(file.size_bytes)}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
