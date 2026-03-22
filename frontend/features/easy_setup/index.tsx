"use client";

import { useRef, useState, useTransition } from "react";
import {
  Box,
  Map,
  BookOpen,
  ClipboardCheck,
  Check,
  Loader2,
  AlertCircle,
  Layers,
  Brain,
} from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import { buildEasySetupPlan, saveEasySetupDraft } from "@/lib/api/client";
import type {
  EasySetupBootstrapResponse,
  EasySetupCapabilityOption,
  EasySetupDraft,
  EasySetupPlan,
} from "@/lib/types/atlas-haven-api";

const steps = [
  { id: 1, label: "Apps", icon: Box },
  { id: 2, label: "Maps", icon: Map },
  { id: 3, label: "Content", icon: BookOpen },
  { id: 4, label: "Review", icon: ClipboardCheck },
] as const;

function formatStorage(sizeMb: number) {
  if (sizeMb >= 1024) return `${(sizeMb / 1024).toFixed(1)} GB`;
  return `${sizeMb} MB`;
}

function toggleItem(items: string[], value: string) {
  return items.includes(value) ? items.filter((i) => i !== value) : [...items, value];
}

function toggleCapability(draft: EasySetupDraft, capabilityId: string): EasySetupDraft {
  return { ...draft, selectedCapabilityIds: toggleItem(draft.selectedCapabilityIds, capabilityId) };
}

function toggleMapCollection(draft: EasySetupDraft, slug: string): EasySetupDraft {
  return { ...draft, selectedMapCollectionSlugs: toggleItem(draft.selectedMapCollectionSlugs, slug) };
}

function toggleAiModel(draft: EasySetupDraft, modelId: string): EasySetupDraft {
  return { ...draft, selectedAiModelIds: toggleItem(draft.selectedAiModelIds, modelId) };
}

function updateCategoryTier(draft: EasySetupDraft, categorySlug: string, tierSlug: string): EasySetupDraft {
  const next = { ...draft.selectedCategoryTierSlugs };
  if (tierSlug === "") delete next[categorySlug];
  else next[categorySlug] = tierSlug;
  return { ...draft, selectedCategoryTierSlugs: next };
}

function updateStep(draft: EasySetupDraft, currentStep: number): EasySetupDraft {
  return { ...draft, currentStep };
}

function OptionCard({
  title, description, selected, meta, onClick,
}: {
  title: string; description: string; selected: boolean; meta: string; onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`w-full rounded-xl border px-4 py-4 text-left transition ${
        selected
          ? "border-brand-500/30 bg-brand-500/5"
          : "border-border-subtle bg-surface-2 hover:border-brand-500/20"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-content">{title}</p>
          <p className="mt-0.5 text-xs text-content-tertiary">{description}</p>
        </div>
        <span
          className={`shrink-0 rounded-full px-2.5 py-0.5 text-[11px] font-medium ${
            selected
              ? "bg-brand-500 text-white"
              : "bg-surface-3 text-content-secondary"
          }`}
        >
          {selected ? <Check size={12} className="inline" /> : meta}
        </span>
      </div>
    </button>
  );
}

function CapabilityGrid({
  title, items, draft, onToggle,
}: {
  title: string; items: EasySetupCapabilityOption[]; draft: EasySetupDraft; onToggle: (id: string) => void;
}) {
  return (
    <div>
      <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">{title}</p>
      <div className="mt-3 space-y-2">
        {items.map((item) => {
          const selected = draft.selectedCapabilityIds.includes(item.id);
          return (
            <OptionCard
              key={item.id}
              title={item.name}
              description={item.description}
              selected={selected}
              meta={item.installed ? "Installed" : item.technicalName}
              onClick={() => onToggle(item.id)}
            />
          );
        })}
      </div>
    </div>
  );
}

export function EasySetupOverview({
  initialBootstrap,
  initialPlan,
}: {
  initialBootstrap: EasySetupBootstrapResponse;
  initialPlan: EasySetupPlan;
}) {
  const [draft, setDraft] = useState(initialBootstrap.draft);
  const [plan, setPlan] = useState(initialPlan);
  const [status, setStatus] = useState<string | null>("Draft synced.");
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();
  const requestIdRef = useRef(0);

  function syncDraft(nextDraft: EasySetupDraft, statusMessage: string) {
    setDraft(nextDraft);
    setStatus(statusMessage);
    setError(null);
    const requestId = requestIdRef.current + 1;
    requestIdRef.current = requestId;
    startTransition(async () => {
      try {
        const saved = await saveEasySetupDraft(nextDraft);
        const nextPlan = await buildEasySetupPlan(saved);
        if (requestIdRef.current !== requestId) return;
        setDraft(saved);
        setPlan(nextPlan);
        setStatus(statusMessage);
      } catch (e) {
        if (requestIdRef.current !== requestId) return;
        setError(e instanceof Error ? e.message : "Failed to sync the easy setup draft.");
      }
    });
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[1.35fr_0.95fr]">
      <div className="space-y-6">
        <SectionCard title="Easy Setup" eyebrow="Provisioning">
          {/* Step tabs */}
          <div className="flex flex-wrap gap-2">
            {steps.map((step) => {
              const active = draft.currentStep === step.id;
              const Icon = step.icon;
              return (
                <button
                  key={step.id}
                  type="button"
                  onClick={() => syncDraft(updateStep(draft, step.id), `Moved to ${step.label}.`)}
                  className={`inline-flex items-center gap-1.5 rounded-xl px-4 py-2 text-sm font-medium transition ${
                    active
                      ? "bg-brand-500 text-white shadow-glow"
                      : "border border-border bg-surface-1 text-content-secondary hover:bg-surface-2 hover:text-content"
                  }`}
                >
                  <Icon size={14} />
                  {step.id}. {step.label}
                </button>
              );
            })}
          </div>
          <p className="mt-4 max-w-2xl text-sm text-content-secondary">
            Build an install plan for core apps, offline content, maps, and local models. Each
            change is saved back to the backend so the plan is ready for later execution modules.
          </p>
        </SectionCard>

        {draft.currentStep === 1 ? (
          <SectionCard title="Choose Apps" eyebrow="Step 1">
            <div className="space-y-6">
              <CapabilityGrid
                title="Core capabilities"
                items={initialBootstrap.capabilities}
                draft={draft}
                onToggle={(id) => syncDraft(toggleCapability(draft, id), "Updated app selections.")}
              />
              <CapabilityGrid
                title="Additional tools"
                items={initialBootstrap.additionalTools}
                draft={draft}
                onToggle={(id) => syncDraft(toggleCapability(draft, id), "Updated tool selections.")}
              />
            </div>
          </SectionCard>
        ) : null}

        {draft.currentStep === 2 ? (
          <SectionCard title="Pick Map Regions" eyebrow="Step 2">
            <div className="space-y-2">
              {initialBootstrap.mapCollections.map((c) => (
                <OptionCard
                  key={c.slug}
                  title={c.name}
                  description={c.description}
                  selected={draft.selectedMapCollectionSlugs.includes(c.slug)}
                  meta={`${c.resourceCount} files • ${formatStorage(c.sizeMb)}`}
                  onClick={() => syncDraft(toggleMapCollection(draft, c.slug), "Updated map selections.")}
                />
              ))}
            </div>
          </SectionCard>
        ) : null}

        {draft.currentStep === 3 ? (
          <SectionCard title="Content & Models" eyebrow="Step 3">
            <div className="space-y-6">
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Curated categories</p>
                <div className="mt-3 space-y-2">
                  {initialBootstrap.curatedCategories.map((cat) => (
                    <div key={cat.slug} className="flex items-start justify-between gap-4 rounded-xl border border-border-subtle bg-surface-2 p-4">
                      <div>
                        <p className="text-sm font-medium text-content">{cat.name}</p>
                        <p className="mt-0.5 text-xs text-content-tertiary">{cat.description}</p>
                      </div>
                      <select
                        className="rounded-lg border border-border bg-surface-1 px-3 py-2 text-sm text-content outline-none transition focus:border-brand-500"
                        value={draft.selectedCategoryTierSlugs[cat.slug] ?? ""}
                        onChange={(e) => syncDraft(updateCategoryTier(draft, cat.slug, e.target.value), `Updated ${cat.name} tier.`)}
                      >
                        <option value="">Skip</option>
                        {cat.tiers.map((tier) => (
                          <option key={tier.slug} value={tier.slug}>{tier.name}</option>
                        ))}
                      </select>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid gap-6 lg:grid-cols-2">
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Wikipedia</p>
                  <div className="mt-3 space-y-2">
                    {initialBootstrap.wikipediaOptions.map((option) => (
                      <OptionCard
                        key={option.id}
                        title={option.name}
                        description={option.description}
                        selected={draft.selectedWikipediaOptionId === option.id}
                        meta={formatStorage(option.sizeMb)}
                        onClick={() => syncDraft({ ...draft, selectedWikipediaOptionId: option.id }, `Selected ${option.name}.`)}
                      />
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">AI models</p>
                  <div className="mt-3 space-y-2">
                    {initialBootstrap.aiModels.map((model) => (
                      <OptionCard
                        key={model.id}
                        title={model.label}
                        description={model.description}
                        selected={draft.selectedAiModelIds.includes(model.id)}
                        meta={model.sizeLabel}
                        onClick={() => syncDraft(toggleAiModel(draft, model.id), "Updated AI model selections.")}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </SectionCard>
        ) : null}

        {draft.currentStep === 4 ? (
          <SectionCard title="Review Plan" eyebrow="Step 4">
            <div className="grid gap-6 lg:grid-cols-2">
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Services</p>
                <div className="mt-3 space-y-2">
                  {plan.services.length === 0 ? (
                    <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-sm text-content-tertiary">
                      No services selected yet.
                    </div>
                  ) : (
                    plan.services.map((s) => (
                      <div key={s.serviceName} className="rounded-xl border border-border-subtle bg-surface-2 p-4">
                        <p className="text-sm font-medium text-content">{s.friendlyName}</p>
                        <p className="mt-0.5 text-xs text-content-tertiary">{s.reason}</p>
                      </div>
                    ))
                  )}
                </div>
              </div>
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Payload</p>
                <div className="mt-3 space-y-2">
                  {plan.maps.map((item) => (
                    <div key={item.slug} className="flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4">
                      <Map size={14} className="text-content-tertiary" />
                      <div>
                        <p className="text-sm font-medium text-content">{item.name}</p>
                        <p className="text-xs text-content-tertiary">{item.resourceCount} map files • {formatStorage(item.sizeMb)}</p>
                      </div>
                    </div>
                  ))}
                  {plan.categorySelections.map((item) => (
                    <div key={`${item.categorySlug}-${item.tierSlug}`} className="flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4">
                      <Layers size={14} className="text-content-tertiary" />
                      <div>
                        <p className="text-sm font-medium text-content">{item.categoryName}: {item.tierName}</p>
                        <p className="text-xs text-content-tertiary">{item.resourceCount} resources • {formatStorage(item.sizeMb)}</p>
                      </div>
                    </div>
                  ))}
                  {plan.aiModels.map((item) => (
                    <div key={item.id} className="flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4">
                      <Brain size={14} className="text-content-tertiary" />
                      <div>
                        <p className="text-sm font-medium text-content">{item.label}</p>
                        <p className="text-xs text-content-tertiary">{item.sizeLabel}</p>
                      </div>
                    </div>
                  ))}
                  {plan.wikipedia.id !== "none" ? (
                    <div className="flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 p-4">
                      <BookOpen size={14} className="text-content-tertiary" />
                      <div>
                        <p className="text-sm font-medium text-content">{plan.wikipedia.name}</p>
                        <p className="text-xs text-content-tertiary">{formatStorage(plan.wikipedia.sizeMb)}</p>
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            </div>
          </SectionCard>
        ) : null}
      </div>

      {/* ── Right sidebar ── */}
      <div className="space-y-6">
        <SectionCard title="Plan Snapshot" eyebrow="Summary">
          <div className="grid gap-3 sm:grid-cols-2">
            {[
              { label: "Services", value: plan.summary.serviceCount },
              { label: "Storage", value: plan.summary.totalEstimatedStorageLabel },
              { label: "Map collections", value: plan.summary.mapCollectionCount },
              { label: "AI models", value: plan.summary.aiModelCount },
            ].map((s) => (
              <div key={s.label} className="rounded-xl border border-border-subtle bg-surface-2 p-4">
                <p className="text-xs text-content-tertiary">{s.label}</p>
                <p className="mt-1 text-xl font-semibold text-content">{s.value}</p>
              </div>
            ))}
          </div>
          <div className="mt-4 rounded-xl border border-border bg-surface-2 p-4">
            <div className="flex items-center gap-2">
              {isPending ? (
                <Loader2 size={14} className="animate-spin text-brand-500" />
              ) : error ? (
                <AlertCircle size={14} className="text-red-500" />
              ) : (
                <Check size={14} className="text-emerald-500" />
              )}
              <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Status</p>
            </div>
            <p className="mt-2 text-sm text-content-secondary">
              {isPending ? "Syncing draft with the backend..." : status}
            </p>
            {error ? <p className="mt-2 text-sm text-red-500 dark:text-red-400">{error}</p> : null}
          </div>
        </SectionCard>

        <SectionCard title="Readiness" eyebrow="What this covers">
          <div className="space-y-3 text-sm text-content-secondary">
            <p>
              The plan currently calculates install targets, dependency order, content payload, and
              estimated storage. Execution stays in later modules so this surface remains safe to
              iterate on.
            </p>
            <p>
              Category content and Wikipedia selections automatically pull in the offline library
              runtime. Map collections pull in Cairn Maps. AI models pull in the local runtime and
              its dependencies.
            </p>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
