import { MapPin, Globe2, Paintbrush, Layers, FolderOpen } from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import type {
  BaseStylesFile,
  CollectionWithStatus,
  MapFileEntry,
  ServiceSlim,
} from "@/lib/types/atlas-haven-api";

function formatCollectionProgress(collection: CollectionWithStatus) {
  return `${collection.installed_count}/${collection.total_count} regions`;
}

export function MapsOverview({
  services,
  regions,
  collections,
  styles,
  stylesError,
}: {
  services: ServiceSlim[];
  regions: MapFileEntry[];
  collections: CollectionWithStatus[];
  styles: BaseStylesFile | null;
  stylesError: string | null;
}) {
  const mapsService = services.find((service) => service.service_name === "nomad_maps");

  const statItems = [
    { label: "Local regions", value: regions.length, icon: MapPin },
    { label: "Collections", value: collections.length, icon: FolderOpen },
    { label: "Style sources", value: styles ? Object.keys(styles.sources).length : 0, icon: Paintbrush },
  ];

  return (
    <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
      <div className="space-y-6">
        <SectionCard title="Atlas Maps" eyebrow="Offline Cartography">
          <p className="text-sm text-content-secondary">
            PMTiles storage, curated regional collections, and generated map styles are now wired
            into the Cairn backend.
          </p>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            {statItems.map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.label} className="rounded-xl border border-border-subtle bg-surface-2 p-4 transition hover:border-brand-500/20">
                  <div className="flex items-center gap-2">
                    <Icon size={14} className="text-brand-500 dark:text-brand-400" />
                    <p className="text-xs text-content-tertiary">{item.label}</p>
                  </div>
                  <p className="mt-2 text-2xl font-semibold text-content">{item.value}</p>
                </div>
              );
            })}
          </div>
          {mapsService ? (
            <div className="mt-4 flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4">
              <Globe2 size={16} className="text-content-tertiary" />
              <div>
                <p className="text-sm font-medium text-content">{mapsService.friendly_name}</p>
                <p className="text-xs text-content-tertiary">{mapsService.description}</p>
              </div>
            </div>
          ) : null}
        </SectionCard>

        <SectionCard title="Curated Regions" eyebrow="Collections">
          <div className="space-y-2">
            {collections.map((collection) => (
              <div
                key={collection.slug}
                className="flex items-start justify-between gap-4 rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 transition hover:border-brand-500/20"
              >
                <div>
                  <p className="text-sm font-medium text-content">{collection.name}</p>
                  <p className="mt-0.5 text-xs text-content-tertiary">{collection.description}</p>
                </div>
                <span className="shrink-0 rounded-full bg-brand-500/10 px-2.5 py-0.5 text-[11px] font-medium text-brand-500 dark:bg-brand-400/10 dark:text-brand-400">
                  {formatCollectionProgress(collection)}
                </span>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <div className="space-y-6">
        <SectionCard title="Viewer Readiness" eyebrow="Styles">
          {styles ? (
            <div className="space-y-3">
              <div className="rounded-xl border border-border-subtle bg-surface-2 p-4">
                <p className="text-xs text-content-tertiary">Sprite endpoint</p>
                <p className="mt-1 text-sm font-medium text-content">{styles.sprite}</p>
              </div>
              <div className="rounded-xl border border-border-subtle bg-surface-2 p-4">
                <p className="text-xs text-content-tertiary">Glyph endpoint</p>
                <p className="mt-1 text-sm font-medium text-content">{styles.glyphs}</p>
              </div>
              <div className="rounded-xl border border-border bg-surface-2 p-4">
                <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Sources</p>
                <div className="mt-3 space-y-2">
                  {Object.keys(styles.sources).length === 0 ? (
                    <p className="text-sm text-content-tertiary">
                      Base assets are ready. Add PMTiles files to generate sources.
                    </p>
                  ) : (
                    Object.entries(styles.sources).map(([sourceName, source]) => (
                      <div key={sourceName}>
                        <p className="text-sm font-medium text-content">{sourceName}</p>
                        <p className="text-xs text-content-tertiary">{source.url}</p>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="rounded-xl border border-border-subtle bg-surface-2 p-4 text-sm text-content-secondary">
              {stylesError ?? "Base assets have not been prepared yet."}
            </div>
          )}
        </SectionCard>

        <SectionCard title="Local PMTiles" eyebrow="Files">
          {regions.length === 0 ? (
            <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-sm text-content-tertiary">
              No local PMTiles files yet. Curated collection downloads will appear here.
            </div>
          ) : (
            <div className="space-y-2">
              {regions.map((region) => (
                <div
                  key={region.key}
                  className="flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 transition hover:border-brand-500/20"
                >
                  <Layers size={14} className="text-content-tertiary" />
                  <p className="text-sm font-medium text-content">{region.name}</p>
                </div>
              ))}
            </div>
          )}
        </SectionCard>
      </div>
    </div>
  );
}
