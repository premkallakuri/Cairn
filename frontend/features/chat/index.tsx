"use client";

import { useState, useTransition } from "react";
import {
  Plus,
  Trash2,
  Send,
  Bot,
  User,
  Cpu,
  Sparkles,
  Upload,
  RefreshCw,
  X,
  FileText,
  Brain,
} from "lucide-react";

import { SectionCard } from "@/components/SectionCard";
import {
  addChatMessage,
  createChatSession,
  deleteAllChatSessions,
  deleteChatSession,
  getChatSession,
  listChatSessions,
  sendOllamaChatMessage,
  listRagFiles,
  syncRagStorage,
  uploadKnowledgeFile,
  deleteRagFile,
} from "@/lib/api/client";
import type {
  ChatSessionDetail,
  ChatSessionSummary,
  InstalledModel,
  NomadOllamaModel,
  ServiceSlim,
} from "@/lib/types/atlas-haven-api";

function formatTimestamp(value?: string | null) {
  if (!value) return "No activity yet";
  return new Date(value).toLocaleString();
}

export function ChatOverview({
  services,
  availableModels,
  installedModels,
  initialSuggestions,
  initialSessions,
  initialActiveSession,
  initialKnowledgeFiles,
}: {
  services: ServiceSlim[];
  availableModels: NomadOllamaModel[];
  installedModels: InstalledModel[];
  initialSuggestions: string[];
  initialSessions: ChatSessionSummary[];
  initialActiveSession: ChatSessionDetail | null;
  initialKnowledgeFiles: string[];
}) {
  const ollamaService = services.find((s) => s.service_name === "nomad_ollama");
  const modelOptions = installedModels
    .map((i) => String(i.name ?? i.model ?? ""))
    .filter((v) => v.length > 0);
  const [sessions, setSessions] = useState(initialSessions);
  const [activeSession, setActiveSession] = useState(initialActiveSession);
  const [knowledgeFiles, setKnowledgeFiles] = useState(initialKnowledgeFiles);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [draft, setDraft] = useState("");
  const [selectedModel, setSelectedModel] = useState(
    initialActiveSession?.model ?? modelOptions[0] ?? availableModels[0]?.id ?? "",
  );
  const [status, setStatus] = useState<string | null>(
    modelOptions.length > 0 ? "Local chat is ready." : "Queue a local model to enable chat.",
  );
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  async function refreshSessions(nextActiveId?: number) {
    const nextSessions = await listChatSessions();
    setSessions(nextSessions);
    const targetId = nextActiveId ?? activeSession?.id ?? nextSessions[0]?.id;
    if (!targetId) { setActiveSession(null); return; }
    const detail = await getChatSession(targetId);
    setActiveSession(detail);
    if (detail.model) setSelectedModel(detail.model);
  }

  async function refreshKnowledgeFiles() {
    const payload = await listRagFiles();
    setKnowledgeFiles(payload.files);
  }

  function runAction(action: () => Promise<void>) {
    setError(null);
    startTransition(async () => {
      try { await action(); } catch (e) {
        setError(e instanceof Error ? e.message : "Chat action failed.");
      }
    });
  }

  function ensureModel() {
    const m = selectedModel || modelOptions[0] || "";
    if (!m) throw new Error("Queue a local model from the runtime shelf before sending chat.");
    return m;
  }

  function handleCreateSession(prefill?: string) {
    runAction(async () => {
      const model = ensureModel();
      const created = await createChatSession({ title: "New chat", model });
      await refreshSessions(created.id);
      setDraft(prefill ?? "");
      setStatus("Started a new local chat session.");
    });
  }

  function handleSelectSession(sessionId: number) {
    runAction(async () => {
      const detail = await getChatSession(sessionId);
      setActiveSession(detail);
      if (detail.model) setSelectedModel(detail.model);
      setStatus(`Opened session ${detail.title}.`);
    });
  }

  function handleDeleteSession(sessionId: number) {
    runAction(async () => {
      await deleteChatSession(sessionId);
      await refreshSessions(activeSession?.id === sessionId ? undefined : activeSession?.id);
      setStatus("Deleted the selected session.");
    });
  }

  function handleClearSessions() {
    runAction(async () => {
      await deleteAllChatSessions();
      setSessions([]);
      setActiveSession(null);
      setStatus("Cleared all chat history.");
    });
  }

  function handleSendMessage() {
    const content = draft.trim();
    if (!content) return;
    runAction(async () => {
      const model = ensureModel();
      let currentSession = activeSession;
      if (!currentSession) {
        const created = await createChatSession({ title: "New chat", model });
        currentSession = await getChatSession(created.id);
      }
      const userMessage = await addChatMessage(currentSession.id, { role: "user", content });
      const response = await sendOllamaChatMessage({
        model,
        sessionId: currentSession.id,
        messages: [
          ...currentSession.messages.map((m) => ({ role: m.role, content: m.content })),
          { role: userMessage.role, content: userMessage.content },
        ],
      });
      await addChatMessage(currentSession.id, { role: "assistant", content: response.message.content });
      await refreshSessions(currentSession.id);
      setDraft("");
      setStatus(`Responded locally with ${model}.`);
    });
  }

  function handleUploadKnowledgeFile() {
    if (!selectedFile) return;
    runAction(async () => {
      const response = await uploadKnowledgeFile(selectedFile);
      await refreshKnowledgeFiles();
      setSelectedFile(null);
      setStatus(response.message);
    });
  }

  function handleSyncKnowledgeBase() {
    runAction(async () => {
      const response = await syncRagStorage();
      await refreshKnowledgeFiles();
      setStatus(`${response.message} (${response.filesQueued} queued).`);
    });
  }

  function handleDeleteKnowledgeFile(source: string) {
    runAction(async () => {
      const response = await deleteRagFile(source);
      await refreshKnowledgeFiles();
      setStatus(response.message);
    });
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
      {/* ── Left panel ── */}
      <div className="space-y-6">
        <SectionCard title="Session Deck" eyebrow="Local Assistant">
          <p className="text-sm text-content-secondary">
            Create multiple local chat threads, keep them on-device, and send prompts through the
            Ollama-compatible API surface.
          </p>

          {ollamaService ? (
            <div className="mt-4 flex items-center gap-3 rounded-xl border border-border-subtle bg-surface-2 p-3">
              <Cpu size={16} className="text-content-tertiary" />
              <div className="flex-1">
                <p className="text-sm font-medium text-content">{ollamaService.friendly_name}</p>
                <p className="text-xs text-content-tertiary">{ollamaService.description}</p>
              </div>
              <span className="rounded-full bg-brand-500/10 px-2.5 py-0.5 text-[11px] font-medium text-brand-500 dark:bg-brand-400/10 dark:text-brand-400">
                {ollamaService.status ?? "idle"}
              </span>
            </div>
          ) : null}

          <div className="mt-4 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => handleCreateSession()}
              className="inline-flex items-center gap-1.5 rounded-xl bg-brand-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-brand-600 disabled:opacity-50"
              disabled={isPending}
            >
              <Plus size={14} /> New Session
            </button>
            <button
              type="button"
              onClick={handleClearSessions}
              className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-surface-1 px-4 py-2 text-sm font-medium text-content-secondary transition hover:bg-surface-2 hover:text-content disabled:opacity-50"
              disabled={isPending || sessions.length === 0}
            >
              <Trash2 size={14} /> Clear All
            </button>
          </div>

          <label className="mt-4 block text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">
            Active model
          </label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="mt-1.5 w-full rounded-xl border border-border bg-surface-2 px-3 py-2.5 text-sm text-content outline-none transition focus:border-brand-500 focus:ring-1 focus:ring-brand-500/30"
          >
            <option value="">Select a local model</option>
            {modelOptions.map((model) => (
              <option key={model} value={model}>{model}</option>
            ))}
          </select>

          <div className="mt-5 space-y-2">
            {sessions.length > 0 ? (
              sessions.map((session) => (
                <div
                  key={session.id}
                  className={`rounded-xl border px-4 py-3 transition ${
                    activeSession?.id === session.id
                      ? "border-brand-500/30 bg-brand-500/5"
                      : "border-border-subtle bg-surface-2 hover:border-brand-500/20"
                  }`}
                >
                  <button type="button" onClick={() => handleSelectSession(session.id)} className="w-full text-left">
                    <p className="text-sm font-medium text-content">{session.title}</p>
                    <p className="mt-0.5 text-xs text-content-tertiary line-clamp-1">
                      {session.lastMessage ?? "No messages yet"}
                    </p>
                    <p className="mt-1.5 text-[10px] uppercase tracking-wider text-content-tertiary">
                      {formatTimestamp(session.timestamp)}
                    </p>
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDeleteSession(session.id)}
                    className="mt-2 inline-flex items-center gap-1 text-[11px] font-medium text-accent-500 transition hover:text-accent-600"
                  >
                    <X size={12} /> Delete
                  </button>
                </div>
              ))
            ) : (
              <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-center text-sm text-content-tertiary">
                No chat sessions yet. Start with a suggestion or open a new session.
              </div>
            )}
          </div>
        </SectionCard>

        <SectionCard title="Starter Prompts" eyebrow="Suggestions">
          <div className="space-y-2">
            {initialSuggestions.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() => setDraft(suggestion)}
                className="w-full rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 text-left text-sm text-content transition hover:border-brand-500/20 hover:bg-brand-500/5"
              >
                <div className="flex items-start gap-2">
                  <Sparkles size={14} className="mt-0.5 shrink-0 text-accent-400" />
                  {suggestion}
                </div>
              </button>
            ))}
          </div>
        </SectionCard>
      </div>

      {/* ── Right panel ── */}
      <div className="space-y-6">
        <SectionCard title="Conversation" eyebrow="Workspace">
          {status ? (
            <div className="rounded-xl bg-surface-2 px-4 py-2.5 text-sm text-content-secondary">{status}</div>
          ) : null}
          {error ? (
            <div className="mt-2 rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-2.5 text-sm text-red-500 dark:text-red-400">
              {error}
            </div>
          ) : null}

          <div className="mt-4 rounded-2xl border border-border bg-surface-2 p-4">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border pb-3">
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-widest text-content-tertiary">Current session</p>
                <p className="mt-1 text-base font-medium text-content">
                  {activeSession?.title ?? "Ready to start"}
                </p>
              </div>
              <span className="rounded-full bg-surface-3 px-2.5 py-0.5 text-[11px] font-medium text-content-secondary">
                {(activeSession?.model ?? selectedModel) || "No model"}
              </span>
            </div>

            <div className="mt-4 max-h-96 space-y-3 overflow-y-auto pr-1">
              {activeSession?.messages.length ? (
                activeSession.messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 rounded-xl p-3 text-sm ${
                      message.role === "assistant"
                        ? "bg-brand-500/5"
                        : "bg-surface-3"
                    }`}
                  >
                    <div className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ${
                      message.role === "assistant" ? "bg-brand-500/10 text-brand-500" : "bg-surface-3 text-content-secondary"
                    }`}>
                      {message.role === "assistant" ? <Bot size={14} /> : <User size={14} />}
                    </div>
                    <div className="flex-1">
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-content-tertiary">{message.role}</p>
                      <p className="mt-1 whitespace-pre-wrap text-content">{message.content}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="rounded-xl border border-dashed border-border p-4 text-center text-sm text-content-tertiary">
                  This session does not have messages yet. Choose a suggestion or type your own prompt below.
                </div>
              )}
            </div>

            <div className="mt-4">
              <textarea
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
                rows={4}
                placeholder="Ask Cairn to help with offline setup, maps, docs, or local AI planning..."
                className="w-full resize-none rounded-xl border border-border bg-surface-1 px-4 py-3 text-sm text-content outline-none transition placeholder:text-content-tertiary focus:border-brand-500 focus:ring-1 focus:ring-brand-500/30"
              />
              <div className="mt-3 flex flex-wrap justify-between gap-2">
                <button
                  type="button"
                  onClick={() => handleCreateSession(draft)}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-surface-1 px-4 py-2 text-sm font-medium text-content-secondary transition hover:bg-surface-2 hover:text-content disabled:opacity-50"
                  disabled={isPending}
                >
                  <Plus size={14} /> Start New From Draft
                </button>
                <button
                  type="button"
                  onClick={handleSendMessage}
                  className="inline-flex items-center gap-1.5 rounded-xl bg-brand-500 px-5 py-2 text-sm font-medium text-white transition hover:bg-brand-600 disabled:opacity-50"
                  disabled={isPending || draft.trim().length === 0}
                >
                  <Send size={14} /> Send
                </button>
              </div>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Runtime Shelf" eyebrow="Models">
          <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="space-y-2">
              {availableModels.map((model) => (
                <div key={model.id} className="flex items-center justify-between rounded-xl border border-border-subtle bg-surface-2 px-4 py-3 transition hover:border-brand-500/20">
                  <div className="flex items-center gap-3">
                    <Brain size={14} className="text-brand-500 dark:text-brand-400" />
                    <div>
                      <p className="text-sm font-medium text-content">{model.name}</p>
                      <p className="text-xs text-content-tertiary">{model.description}</p>
                    </div>
                  </div>
                  <span className="rounded-full bg-surface-3 px-2.5 py-0.5 text-[11px] text-content-secondary">
                    {model.tags[0]?.size ?? "Local"}
                  </span>
                </div>
              ))}
            </div>
            <div className="space-y-2">
              {installedModels.length > 0 ? (
                installedModels.map((model) => (
                  <div
                    key={String(model.name ?? model.model ?? "tracked-model")}
                    className="rounded-xl border border-border-subtle bg-surface-2 px-4 py-3"
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-content">
                        {String(model.name ?? model.model ?? "Unnamed model")}
                      </p>
                      <span className="rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-[11px] font-medium text-emerald-600 dark:text-emerald-400">
                        {String(model.status ?? "unknown")}
                      </span>
                    </div>
                    {typeof model.description === "string" ? (
                      <p className="mt-1 text-xs text-content-tertiary">{model.description}</p>
                    ) : null}
                  </div>
                ))
              ) : (
                <div className="rounded-xl border border-dashed border-border bg-surface-2 p-4 text-sm text-content-tertiary">
                  No tracked local models yet.
                </div>
              )}
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Knowledge Base" eyebrow="Local Retrieval">
          <div className="rounded-xl border border-border bg-surface-2 p-4">
            <p className="text-sm text-content-secondary">
              Upload text or PDF-style local documents, index them on-device, and let matching
              chat replies cite relevant file context automatically.
            </p>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              <input
                type="file"
                onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
                className="max-w-full text-sm text-content"
              />
              <button
                type="button"
                onClick={handleUploadKnowledgeFile}
                className="inline-flex items-center gap-1.5 rounded-xl bg-brand-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-brand-600 disabled:opacity-50"
                disabled={isPending || selectedFile === null}
              >
                <Upload size={14} /> Upload
              </button>
              <button
                type="button"
                onClick={handleSyncKnowledgeBase}
                className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-surface-1 px-4 py-2 text-sm font-medium text-content-secondary transition hover:bg-surface-2 hover:text-content disabled:opacity-50"
                disabled={isPending}
              >
                <RefreshCw size={14} /> Sync Storage
              </button>
            </div>

            <div className="mt-4 space-y-2">
              {knowledgeFiles.length > 0 ? (
                knowledgeFiles.map((source) => (
                  <div
                    key={source}
                    className="flex items-center justify-between rounded-xl border border-border-subtle bg-surface-1 px-4 py-3"
                  >
                    <div className="flex items-center gap-2">
                      <FileText size={14} className="text-content-tertiary" />
                      <div>
                        <p className="text-sm font-medium text-content">{source.split("/").pop()}</p>
                        <p className="text-[10px] text-content-tertiary">{source}</p>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleDeleteKnowledgeFile(source)}
                      className="inline-flex items-center gap-1 text-[11px] font-medium text-accent-500 transition hover:text-accent-600"
                    >
                      <X size={12} /> Delete
                    </button>
                  </div>
                ))
              ) : (
                <div className="rounded-xl border border-dashed border-border p-4 text-center text-sm text-content-tertiary">
                  No indexed knowledge files yet.
                </div>
              )}
            </div>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
