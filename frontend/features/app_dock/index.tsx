"use client";

import Link from "next/link";
import { useState, useTransition } from "react";
import {
  Play,
  Square,
  RotateCcw,
  Download,
  ExternalLink,
  RefreshCw,
  ChevronRight,
  Package,
  Zap,
  ArrowUpCircle,
  Layers,
  Check,
} from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import {
  affectService,
  checkServiceUpdates,
  forceReinstallService,
  getAvailableServiceVersions,
  installService,
  listServices,
  updateService,
} from "@/lib/api/client";
import type { AvailableVersion, ServiceSlim } from "@/lib/types/atlas-haven-api";

function formatKind(kind?: string | null) {
  if (!kind) return "service";
  return kind.replaceAll("_", " ");
}

function getServiceLabel(service: ServiceSlim) {
  return service.friendly_name ?? service.service_name;
}

function getServiceState(service: ServiceSlim) {
  if (!service.installed) return "available";
  if (service.status === "running") return "running";
  if (service.status === "stopped") return "stopped";
  return service.installation_status;
}

function getStateTone(service: ServiceSlim) {
  const state = getServiceState(service);
  if (state === "running") return "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400";
  if (state === "stopped") return "bg-amber-500/10 text-amber-600 dark:text-amber-400";
  if (state === "available") return "bg-surface-3 text-content-secondary";
  return "bg-blue-500/10 text-blue-600 dark:text-blue-400";
}

function sortServices(services: ServiceSlim[]) {
  return [...services].sort((a, b) => {
    const d = (a.display_order ?? 999) - (b.display_order ?? 999);
    return d !== 0 ? d : getServiceLabel(a).localeCompare(getServiceLabel(b));
  });
}

function Btn({
  label,
  icon: Icon,
  disabled,
  tone = "secondary",
  onClick,
}: {
  label: string;
  icon: typeof Play;
  disabled: boolean;
  tone?: "primary" | "secondary";
  onClick: () => void;
}) {
  const base =
    tone === "primary"
      ? "bg-brand-500 text-white hover:bg-brand-600"
      : "border border-border bg-surface-1 text-content-secondary hover:border-brand-500/30 hover:bg-surface-2 hover:text-content";
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-xs font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${base}`}
    >
      <Icon size={12} /> {label}
    </button>
  );
}

export function AppDockPanel({
  services: initialServices,
  title = "App Dock",
  eyebrow = "Operations",
  limit,
}: {
  services: ServiceSlim[];
  title?: string;
  eyebrow?: string;
  limit?: number;
}) {
  const [services, setServices] = useState(() => sortServices(initialServices));
  const [availableVersions, setAvailableVersions] = useState<Record<string, AvailableVersion[]>>({});
  const [selectedVersions, setSelectedVersions] = useState<Record<string, string>>({});
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const installedCount = services.filter((s) => s.installed).length;
  const runningCount = services.filter((s) => s.status === "running").length;
  const updatesCount = services.filter((s) => Boolean(s.available_update_version)).length;
  const visibleServices = limit ? services.slice(0, limit) : services;

  async function refreshServices() {
    const next = await listServices();
    setServices(sortServices(next));
  }

  function runAction(action: () => Promise<void>) {
    setError(null);
    startTransition(async () => {
      try { await action(); } catch (e) {
        setError(e instanceof Error ? e.message : "App Dock action failed.");
      }
    });
  }

  function handleInstall(name: string) {
    runAction(async () => {
      const r = await installService(name);
      await refreshServices();
      setStatus(r.message);
    });
  }

  function handleAffect(name: string, action: "start" | "stop" | "restart") {
    runAction(async () => {
      const r = await affectService(name, action);
      await refreshServices();
      setStatus(r.message);
    });
  }

  function handleReinstall(name: string) {
    runAction(async () => {
      const r = await forceReinstallService(name);
      await refreshServices();
      setStatus(r.message);
    });
  }

  function handleCheckUpdates() {
    runAction(async () => {
      const r = await checkServiceUpdates();
      await refreshServices();
      setStatus(r.message);
    });
  }

  function handleLoadVersions(service: ServiceSlim) {
    runAction(async () => {
      const r = await getAvailableServiceVersions(service.service_name);
      setAvailableVersions((c) => ({ ...c, [service.service_name]: r.versions }));
      const preferred =
        r.versions.find((v) => v.tag === service.available_update_version)?.tag ??
        r.versions.find((v) => v.tag === service.current_version)?.tag ??
        r.versions.find((v) => v.isLatest)?.tag ??
        r.versions[0]?.tag ?? "";
      setSelectedVersions((c) => ({ ...c, [service.service_name]: preferred }));
      setStatus(`Loaded ${r.versions.length} versions for ${getServiceLabel(service)}.`);
    });
  }

  function handleUpdate(name: string) {
    const v = selectedVersions[name];
    if (!v) { setError("Load available versions before applying an update."); return; }
    runAction(async () => {
      const r = await updateService(name, v);
      await refreshServices();
      setStatus(r.message);
    });
  }

  const summaryStats = [
    { label: "Installed", value: installedCount, icon: Package },
    { label: "Running", value: runningCount, icon: Zap },
    { label: "Updates", value: updatesCount, icon: ArrowUpCircle },
  ];

  return (
    <SectionCard title={title} eyebrow={eyebrow}>
      <div className="grid gap-3 sm:grid-cols-3">
        {summaryStats.map((s) => {
          const Icon = s.icon;
          return (
            <div key={s.label} className="rounded-xl border border-border-subtle bg-surface-2 p-3">
              <div className="flex items-center gap-2">
                <Icon size={13} className="text-brand-500 dark:text-brand-400" />
                <p className="text-xs text-content-tertiary">{s.label}</p>
              </div>
              <p className="mt-1 text-xl font-semibold text-content">{s.value}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Btn label="Check Updates" icon={RefreshCw} disabled={isPending} onClick={handleCheckUpdates} />
        <p className="text-xs text-content-tertiary">
          {status ?? "Install, launch, update, and recover sibling apps."}
        </p>
      </div>

      {error ? <p className="mt-3 text-xs text-red-500 dark:text-red-400">{error}</p> : null}

      <div className="mt-4 space-y-3">
        {visibleServices.map((service) => {
          const serviceVersions = availableVersions[service.service_name] ?? [];
          const selectedVersion = selectedVersions[service.service_name] ?? "";

          return (
            <article
              key={service.service_name}
              className="rounded-xl border border-border-subtle bg-surface-2 p-4 transition hover:border-brand-500/20"
            >
              <div className="flex flex-col gap-3 xl:flex-row xl:items-start xl:justify-between">
                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-sm font-semibold text-content">{getServiceLabel(service)}</h3>
                    <span className="rounded-md bg-surface-3 px-2 py-0.5 text-[10px] uppercase tracking-wider text-content-tertiary">
                      {formatKind(service.kind)}
                    </span>
                    <span className={`rounded-md px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider ${getStateTone(service)}`}>
                      {getServiceState(service)}
                    </span>
                    {service.available_update_version ? (
                      <span className="rounded-md bg-accent-500/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider text-accent-500">
                        Update {service.available_update_version}
                      </span>
                    ) : null}
                  </div>
                  <p className="mt-1.5 text-xs text-content-tertiary">{service.description ?? "No description yet."}</p>
                  <div className="mt-2 flex flex-wrap gap-3 text-[10px] uppercase tracking-wider text-content-tertiary">
                    <span>{service.service_name}</span>
                    <span>v{service.current_version ?? "—"}</span>
                    <span>{service.powered_by ?? "Cairn"}</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5">
                  {service.launch_url ? (
                    <a
                      href={service.launch_url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-surface-1 px-3 py-1.5 text-xs font-medium text-content-secondary transition hover:border-brand-500/30 hover:text-content"
                    >
                      <ExternalLink size={12} /> Open
                    </a>
                  ) : null}
                  {!service.installed ? (
                    <Btn label="Install" icon={Download} tone="primary" disabled={isPending} onClick={() => handleInstall(service.service_name)} />
                  ) : (
                    <>
                      <Btn
                        label={service.status === "running" ? "Stop" : "Start"}
                        icon={service.status === "running" ? Square : Play}
                        disabled={isPending}
                        onClick={() => handleAffect(service.service_name, service.status === "running" ? "stop" : "start")}
                      />
                      <Btn label="Restart" icon={RotateCcw} disabled={isPending} onClick={() => handleAffect(service.service_name, "restart")} />
                      <Btn label="Reinstall" icon={Download} disabled={isPending} onClick={() => handleReinstall(service.service_name)} />
                    </>
                  )}
                </div>
              </div>

              {service.installed ? (
                <div className="mt-3 rounded-lg border border-border bg-surface-1 p-3">
                  <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
                    <div>
                      <p className="text-xs font-medium text-content">Service update lane</p>
                      <p className="text-[10px] text-content-tertiary">
                        Load tags, pick a version, and apply through orchestration.
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      <Btn label="Load Versions" icon={Layers} disabled={isPending} onClick={() => handleLoadVersions(service)} />
                      <select
                        value={selectedVersion}
                        onChange={(e) => setSelectedVersions((c) => ({ ...c, [service.service_name]: e.target.value }))}
                        className="rounded-lg border border-border bg-surface-2 px-3 py-1.5 text-xs text-content outline-none transition focus:border-brand-500"
                      >
                        <option value="">Select version</option>
                        {serviceVersions.map((v) => (
                          <option key={v.tag} value={v.tag}>
                            {v.tag}{v.isLatest ? " (latest)" : ""}
                          </option>
                        ))}
                      </select>
                      <Btn
                        label="Apply"
                        icon={Check}
                        tone="primary"
                        disabled={isPending || serviceVersions.length === 0 || selectedVersion.length === 0}
                        onClick={() => handleUpdate(service.service_name)}
                      />
                    </div>
                  </div>
                </div>
              ) : null}
            </article>
          );
        })}
      </div>

      {limit && services.length > limit ? (
        <div className="mt-4 flex items-center justify-between text-xs text-content-tertiary">
          <p>Showing {limit} of {services.length} services</p>
          <Link href="/control-room" className="inline-flex items-center gap-1 font-medium text-brand-500 transition hover:text-brand-600 dark:text-brand-400">
            Full Control Room <ChevronRight size={14} />
          </Link>
        </div>
      ) : null}
    </SectionCard>
  );
}

export function AppDockSummary({ services }: { services: ServiceSlim[] }) {
  return <AppDockPanel services={services} title="App Dock" eyebrow="Operations" limit={4} />;
}
