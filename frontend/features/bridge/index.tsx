import Link from "next/link";
import { Layers, FolderOpen, FileText, Tag, Rocket } from "lucide-react";

import { AppDockPanel } from "@/features/app_dock";
import { SectionCard } from "@/components/SectionCard";
import type { CategoryWithStatus, DocIndexItem, ServiceSlim, SystemInformationResponse } from "@/lib/types/atlas-haven-api";

const statIcons = [Layers, Tag, FileText, FolderOpen] as const;

export function BridgeDashboard({
  services,
  docs,
  categories,
  systemInfo,
}: {
  services: ServiceSlim[];
  docs: DocIndexItem[];
  categories: CategoryWithStatus[];
  systemInfo: SystemInformationResponse;
}) {
  const stats = [
    { label: "Catalog services", value: services.length },
    { label: "Curated categories", value: categories.length },
    { label: "Docs available", value: docs.length },
    { label: "Runtime version", value: systemInfo.version },
  ];

  return (
    <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
      <SectionCard title="Dashboard" eyebrow="Command Center">
        <div className="grid gap-3 sm:grid-cols-2">
          {stats.map((stat, index) => {
            const Icon = statIcons[index];
            return (
              <div
                key={stat.label}
                className="group flex items-start gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4 transition hover:border-brand-500/20 hover:shadow-glow"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-brand-500/10 text-brand-500 dark:bg-brand-400/10 dark:text-brand-400">
                  <Icon size={16} strokeWidth={2} />
                </div>
                <div>
                  <p className="text-xs text-content-tertiary">{stat.label}</p>
                  <p className="mt-1 text-2xl font-semibold text-content">{stat.value}</p>
                </div>
              </div>
            );
          })}
        </div>
        <div className="mt-5">
          <Link
            href="/easy-setup"
            className="inline-flex items-center gap-2 rounded-xl bg-brand-500 px-5 py-2.5 text-sm font-medium text-white shadow-glow transition hover:bg-brand-600"
          >
            <Rocket size={15} />
            Open Easy Setup
          </Link>
        </div>
      </SectionCard>

      <AppDockPanel services={services} title="App Dock" eyebrow="Launch Surface" limit={6} />
    </div>
  );
}
