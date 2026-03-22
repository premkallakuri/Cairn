"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import {
  Server,
  Wifi,
  WifiOff,
  Package,
  FolderSync,
  Download,
  ArrowUpCircle,
  RefreshCw,
  CheckCircle2,
  Clock,
} from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import { AppDockPanel } from "@/features/app_dock";
import { BenchmarkOverview } from "@/features/benchmark";
import {
  applyAllContentUpdates,
  checkContentUpdates,
  refreshManifests,
  requestSystemUpdate,
} from "@/lib/api/client";
import type {
  BenchmarkResult,
  BenchmarkSettings,
  BenchmarkStatusResponse,
  ContentUpdateCheckResult,
  DownloadJobWithProgress,
  LatestVersionResponse,
  ServiceSlim,
  SystemInformationResponse,
  SystemUpdateStatus,
} from "@/lib/types/atlas-haven-api";

function ActionBtn({
  label,
  icon: Icon,
  disabled,
  onClick,
}: {
  label: string;
  icon: typeof RefreshCw;
  disabled: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-surface-1 px-4 py-2 text-sm font-medium text-content-secondary transition hover:border-brand-500/30 hover:bg-surface-2 hover:text-content disabled:cursor-not-allowed disabled:opacity-50"
    >
      <Icon size={14} /> {label}
    </button>
  );
}

export function ControlRoomOverview({
  services,
  systemInfo,
  downloadJobs,
  internetStatus,
  latestVersion,
  updateStatus,
  benchmarkStatus,
  benchmarkSettings,
  latestBenchmark,
  benchmarkResultTotal,
  contentUpdates,
}: {
  services: ServiceSlim[];
  systemInfo: SystemInformationResponse;
  downloadJobs: DownloadJobWithProgress[];
  internetStatus: boolean;
  latestVersion: LatestVersionResponse;
  updateStatus: SystemUpdateStatus;
  benchmarkStatus: BenchmarkStatusResponse;
  benchmarkSettings: BenchmarkSettings;
  latestBenchmark: BenchmarkResult | null;
  benchmarkResultTotal: number;
  contentUpdates: ContentUpdateCheckResult;
}) {
  const router = useRouter();
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function runAction(action: () => Promise<void>) {
    setError(null);
    startTransition(async () => {
      try { await action(); router.refresh(); } catch (e) {
        setError(e instanceof Error ? e.message : "Control Room action failed.");
      }
    });
  }

  const sysStats = [
    { label: "Environment", value: systemInfo.environment, icon: Server },
    { label: "Catalog entries", value: systemInfo.catalog_entries, icon: Package },
    { label: "Internet", value: internetStatus ? "Online" : "Offline", icon: internetStatus ? Wifi : WifiOff },
    { label: "Bundled version", value: latestVersion.currentVersion, icon: FolderSync },
  ];

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
        <SectionCard title="Control Room" eyebrow="System">
          <div className="grid gap-3 sm:grid-cols-2">
            {sysStats.map((s) => {
              const Icon = s.icon;
              return (
                <div key={s.label} className="rounded-xl border border-border-subtle bg-surface-2 p-4 transition hover:border-brand-500/20">
                  <div className="flex items-center gap-2">
                    <Icon size={14} className="text-brand-500 dark:text-brand-400" />
                    <p className="text-xs text-content-tertiary">{s.label}</p>
                  </div>
                  <p className="mt-2 text-lg font-semibold text-content">{s.value}</p>
                </div>
              );
            })}
            <div className="rounded-xl border border-border-subtle bg-surface-2 p-4 sm:col-span-2">
              <p className="text-xs text-content-tertiary">Workspace root</p>
              <p className="mt-1 text-sm font-medium text-content">{systemInfo.workspace_root}</p>
            </div>
          </div>

          <div className="mt-4 rounded-xl border border-border bg-surface-2 p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-content">Release & Update Lane</p>
                <p className="text-xs text-content-tertiary">
                  {latestVersion.message ?? updateStatus.message}
                </p>
              </div>
              <ActionBtn
                label="Request Update"
                icon={ArrowUpCircle}
                disabled={isPending}
                onClick={() => runAction(async () => {
                  const r = await requestSystemUpdate();
                  setStatusMessage(r.note ?? r.message ?? "Update requested.");
                })}
              />
            </div>
            <div className="mt-3 grid gap-3 sm:grid-cols-3">
              <div>
                <p className="text-xs text-content-tertiary">Stage</p>
                <p className="mt-0.5 text-sm font-medium text-content">{updateStatus.stage}</p>
              </div>
              <div>
                <p className="text-xs text-content-tertiary">Progress</p>
                <p className="mt-0.5 text-sm font-medium text-content">{updateStatus.progress}%</p>
              </div>
              <div>
                <p className="text-xs text-content-tertiary">Latest available</p>
                <p className="mt-0.5 text-sm font-medium text-content">{latestVersion.latestVersion}</p>
              </div>
            </div>
          </div>

          {statusMessage ? <p className="mt-3 text-sm text-content-secondary">{statusMessage}</p> : null}
          {error ? <p className="mt-3 text-sm text-red-500 dark:text-red-400">{error}</p> : null}
        </SectionCard>

        <AppDockPanel services={services} title="App Dock" eyebrow="Operations" />
      </div>

      <BenchmarkOverview
        latestResult={latestBenchmark}
        resultTotal={benchmarkResultTotal}
        status={benchmarkStatus}
        settings={benchmarkSettings}
      />

      <SectionCard title="Content Update Lane" eyebrow="Libraries & Maps">
        <div className="grid gap-3 sm:grid-cols-3">
          <div className="rounded-xl border border-border-subtle bg-surface-2 p-4">
            <div className="flex items-center gap-2">
              <ArrowUpCircle size={14} className="text-brand-500 dark:text-brand-400" />
              <p className="text-xs text-content-tertiary">Pending updates</p>
            </div>
            <p className="mt-2 text-xl font-semibold text-content">{contentUpdates.updates.length}</p>
          </div>
          <div className="rounded-xl border border-border-subtle bg-surface-2 p-4">
            <div className="flex items-center gap-2">
              <Clock size={14} className="text-content-tertiary" />
              <p className="text-xs text-content-tertiary">Checked at</p>
            </div>
            <p className="mt-2 text-sm font-medium text-content">
              {new Date(contentUpdates.checked_at).toLocaleString()}
            </p>
          </div>
          <div className="rounded-xl border border-border-subtle bg-surface-2 p-4">
            <div className="flex items-center gap-2">
              <Download size={14} className="text-content-tertiary" />
              <p className="text-xs text-content-tertiary">Download jobs</p>
            </div>
            <p className="mt-2 text-xl font-semibold text-content">{downloadJobs.length}</p>
          </div>
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          <ActionBtn label="Refresh Manifests" icon={RefreshCw} disabled={isPending}
            onClick={() => runAction(async () => {
              const r = await refreshManifests();
              setStatusMessage(`Manifest refresh: maps ${r.changed.maps ? "updated" : "unchanged"}, library ${r.changed.zim_categories ? "updated" : "unchanged"}.`);
            })}
          />
          <ActionBtn label="Recheck Content" icon={FolderSync} disabled={isPending}
            onClick={() => runAction(async () => {
              const r = await checkContentUpdates();
              setStatusMessage(`Found ${r.updates.length} content update candidates.`);
            })}
          />
          <ActionBtn label="Apply All Updates" icon={CheckCircle2}
            disabled={isPending || contentUpdates.updates.length === 0}
            onClick={() => runAction(async () => {
              const r = await applyAllContentUpdates(contentUpdates.updates);
              const succeeded = r.results.filter((i) => i.success).length;
              setStatusMessage(`Queued ${succeeded} content update jobs.`);
            })}
          />
        </div>

        <div className="mt-4 space-y-2">
          {contentUpdates.updates.length === 0 ? (
            <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-center text-sm text-content-tertiary">
              Bundled manifests and installed content are aligned right now.
            </div>
          ) : (
            contentUpdates.updates.map((update) => (
              <div
                key={`${update.resource_type}-${update.resource_id}`}
                className="flex items-center justify-between rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 transition hover:border-brand-500/20"
              >
                <div>
                  <p className="text-sm font-medium text-content">{update.resource_id}</p>
                  <p className="text-xs text-content-tertiary">
                    {update.resource_type.toUpperCase()} • {update.installed_version} → {update.latest_version}
                  </p>
                </div>
                <span className="rounded-full bg-accent-500/10 px-2.5 py-0.5 text-[11px] font-medium text-accent-500">
                  pending
                </span>
              </div>
            ))
          )}
        </div>
      </SectionCard>

      <SectionCard title="Download Activity" eyebrow="Jobs">
        {downloadJobs.length === 0 ? (
          <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-center text-sm text-content-tertiary">
            No active download jobs yet. Maps, ZIM, and model installs will appear here.
          </div>
        ) : (
          <div className="space-y-3">
            {downloadJobs.map((job) => (
              <div key={job.jobId} className="rounded-xl border border-border-subtle bg-surface-2 px-4 py-4">
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <Download size={14} className="text-content-tertiary" />
                    <div>
                      <p className="text-sm font-medium text-content">{job.filetype.toUpperCase()} download</p>
                      <p className="text-xs text-content-tertiary">{job.filepath}</p>
                    </div>
                  </div>
                  <span className="text-sm font-semibold text-brand-500 dark:text-brand-400">{job.progress}%</span>
                </div>
                <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-surface-3">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-400 transition-[width] duration-500"
                    style={{ width: `${Math.max(4, job.progress)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </SectionCard>
    </div>
  );
}
