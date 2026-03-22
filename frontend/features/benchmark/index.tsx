"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { Activity, Cpu, HardDrive, MemoryStick, Play, Shield, Zap, ToggleLeft, ToggleRight } from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import {
  runAiBenchmark,
  runBenchmark,
  runSystemBenchmark,
  updateBenchmarkSettings,
} from "@/lib/api/client";
import type {
  BenchmarkResult,
  BenchmarkSettings,
  BenchmarkStatusResponse,
} from "@/lib/types/atlas-haven-api";

function formatRam(bytes: number) {
  const gb = bytes / (1024 * 1024 * 1024);
  return `${gb.toFixed(1)} GB`;
}

function ActionBtn({
  label,
  icon: Icon,
  disabled,
  onClick,
}: {
  label: string;
  icon: typeof Play;
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

export function BenchmarkOverview({
  latestResult,
  resultTotal,
  status,
  settings,
}: {
  latestResult: BenchmarkResult | null;
  resultTotal: number;
  status: BenchmarkStatusResponse;
  settings: BenchmarkSettings;
}) {
  const router = useRouter();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function runAction(action: () => Promise<void>) {
    setError(null);
    startTransition(async () => {
      try { await action(); router.refresh(); } catch (e) {
        setError(e instanceof Error ? e.message : "Benchmark action failed.");
      }
    });
  }

  const stats = [
    { label: "Benchmark status", value: status.status, icon: Activity },
    { label: "Latest score", value: latestResult ? latestResult.nomad_score.toFixed(1) : "No run yet", icon: Zap },
    { label: "History depth", value: resultTotal, icon: HardDrive },
    { label: "Anonymous submit", value: settings.allow_anonymous_submission ? "On" : "Off", icon: Shield },
  ];

  return (
    <SectionCard title="Benchmark Lane" eyebrow="Performance">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => {
          const Icon = s.icon;
          return (
            <div key={s.label} className="rounded-xl border border-border-subtle bg-surface-2 p-4 transition hover:border-brand-500/20">
              <div className="flex items-center gap-2">
                <Icon size={14} className="text-brand-500 dark:text-brand-400" />
                <p className="text-xs text-content-tertiary">{s.label}</p>
              </div>
              <p className="mt-2 text-xl font-semibold text-content">{s.value}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <ActionBtn
          label="Run Full"
          icon={Play}
          disabled={isPending}
          onClick={() => runAction(async () => {
            const response = await runBenchmark("full", { sync: true });
            setMessage("result" in response ? `Full benchmark scored ${response.nomad_score.toFixed(1)}.` : response.message);
          })}
        />
        <ActionBtn
          label="System Only"
          icon={Cpu}
          disabled={isPending}
          onClick={() => runAction(async () => {
            const response = await runSystemBenchmark();
            setMessage(response.message);
          })}
        />
        <ActionBtn
          label="AI Only"
          icon={Zap}
          disabled={isPending}
          onClick={() => runAction(async () => {
            const response = await runAiBenchmark();
            setMessage(response.message);
          })}
        />
        <ActionBtn
          label={settings.allow_anonymous_submission ? "Disable Anon" : "Enable Anon"}
          icon={settings.allow_anonymous_submission ? ToggleRight : ToggleLeft}
          disabled={isPending}
          onClick={() => runAction(async () => {
            const response = await updateBenchmarkSettings(!settings.allow_anonymous_submission);
            setMessage(`Anonymous benchmark submission ${response.settings.allow_anonymous_submission ? "enabled" : "disabled"}.`);
          })}
        />
      </div>

      {message ? <p className="mt-3 text-sm text-content-secondary">{message}</p> : null}
      {error ? <p className="mt-3 text-sm text-red-500 dark:text-red-400">{error}</p> : null}

      {latestResult ? (
        <div className="mt-4 rounded-xl border border-border bg-surface-2 p-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-brand-500/10 px-2.5 py-0.5 text-[11px] font-medium text-brand-500 dark:bg-brand-400/10 dark:text-brand-400">
              {latestResult.benchmark_type}
            </span>
            <span className="rounded-full bg-accent-500/10 px-2.5 py-0.5 text-[11px] font-medium text-accent-500">
              {latestResult.benchmark_id}
            </span>
          </div>
          <div className="mt-4 grid gap-4 sm:grid-cols-3">
            <div className="flex items-start gap-3">
              <Cpu size={16} className="mt-0.5 text-content-tertiary" />
              <div>
                <p className="text-xs text-content-tertiary">CPU</p>
                <p className="text-sm font-medium text-content">{latestResult.cpu_model}</p>
                <p className="text-xs text-content-tertiary">
                  {latestResult.cpu_cores} cores • {latestResult.cpu_threads} threads
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <MemoryStick size={16} className="mt-0.5 text-content-tertiary" />
              <div>
                <p className="text-xs text-content-tertiary">Memory</p>
                <p className="text-sm font-medium text-content">{formatRam(latestResult.ram_bytes)}</p>
                <p className="text-xs text-content-tertiary">Score {latestResult.memory_score.toFixed(1)}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <HardDrive size={16} className="mt-0.5 text-content-tertiary" />
              <div>
                <p className="text-xs text-content-tertiary">Disk</p>
                <p className="text-sm font-medium text-content">{latestResult.disk_type}</p>
                <p className="text-xs text-content-tertiary">
                  Read {latestResult.disk_read_score.toFixed(1)} • Write {latestResult.disk_write_score.toFixed(1)}
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="mt-4 rounded-xl border border-dashed border-border bg-surface-2 p-4 text-center text-sm text-content-tertiary">
          No benchmark history yet. Start a run to capture the first local result.
        </div>
      )}
    </SectionCard>
  );
}
