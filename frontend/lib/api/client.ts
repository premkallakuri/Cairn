import type {
  AvailableVersionsResponse,
  AvailableModelsResponse,
  BaseStylesFile,
  BenchmarkLatestResultResponse,
  BenchmarkResultsResponse,
  BenchmarkSettings,
  BenchmarkStatusResponse,
  CollectionWithStatus,
  ContentUpdateApplyAllResponse,
  ContentUpdateApplyResponse,
  ContentUpdateCheckResult,
  InstalledModel,
  LatestVersionResponse,
  ListMapRegionsResponse,
  ManifestRefreshResponse,
  RunBenchmarkResponse,
  RunBenchmarkSyncResponse,
  SimpleBenchmarkStartResponse,
  ResourceUpdateInfo,
  SuccessMessageResponse,
  SystemSettingResponse,
  SystemUpdateRequestResponse,
  SystemUpdateStatus,
} from "@/lib/types/atlas-haven-api";
import type {
  CategoryWithStatus,
  ChatMessage,
  ChatSessionCreateResponse,
  ChatSessionDetail,
  ChatSessionSummary,
  DownloadJobWithProgress,
  DocIndexItem,
  EasySetupBootstrapResponse,
  EasySetupDraft,
  EasySetupPlan,
  ListZimFilesResponse,
  OllamaChatResponse,
  RagFilesResponse,
  RagUploadResponse,
  ServiceSlim,
  SuggestionsResponse,
  SystemInformationResponse,
  WikipediaState,
} from "@/lib/types/atlas-haven-api";

function getApiBaseUrl() {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (init?.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status}`);
  }
  return (await response.json()) as T;
}

async function fetchVoid(path: string, init?: RequestInit): Promise<void> {
  const headers = new Headers(init?.headers);
  if (init?.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status}`);
  }
}

export async function listServices(options?: { installedOnly?: boolean }): Promise<ServiceSlim[]> {
  const query = options?.installedOnly ? "?installedOnly=true" : "";
  return fetchJson<ServiceSlim[]>(`/api/system/services${query}`);
}

export async function installService(service_name: string): Promise<SuccessMessageResponse> {
  return fetchJson<SuccessMessageResponse>("/api/system/services/install", {
    method: "POST",
    body: JSON.stringify({ service_name }),
  });
}

export async function affectService(
  service_name: string,
  action: "start" | "stop" | "restart",
): Promise<SuccessMessageResponse> {
  return fetchJson<SuccessMessageResponse>("/api/system/services/affect", {
    method: "POST",
    body: JSON.stringify({ service_name, action }),
  });
}

export async function forceReinstallService(service_name: string): Promise<SuccessMessageResponse> {
  return fetchJson<SuccessMessageResponse>("/api/system/services/force-reinstall", {
    method: "POST",
    body: JSON.stringify({ service_name }),
  });
}

export async function checkServiceUpdates(): Promise<SuccessMessageResponse> {
  return fetchJson<SuccessMessageResponse>("/api/system/services/check-updates", {
    method: "POST",
  });
}

export async function getAvailableServiceVersions(
  serviceName: string,
): Promise<AvailableVersionsResponse> {
  return fetchJson<AvailableVersionsResponse>(
    `/api/system/services/${serviceName}/available-versions`,
  );
}

export async function updateService(
  service_name: string,
  target_version: string,
): Promise<SuccessMessageResponse> {
  return fetchJson<SuccessMessageResponse>("/api/system/services/update", {
    method: "POST",
    body: JSON.stringify({ service_name, target_version }),
  });
}

export async function listDocs(): Promise<DocIndexItem[]> {
  return fetchJson<DocIndexItem[]>("/api/docs/list");
}

export async function listCuratedCategories(): Promise<CategoryWithStatus[]> {
  return fetchJson<CategoryWithStatus[]>("/api/easy-setup/curated-categories");
}

export async function getSystemInfo(): Promise<SystemInformationResponse> {
  return fetchJson<SystemInformationResponse>("/api/system/info");
}

export async function getInternetStatus(): Promise<boolean> {
  return fetchJson<boolean>("/api/system/internet-status");
}

export async function getLatestVersion(): Promise<LatestVersionResponse> {
  return fetchJson<LatestVersionResponse>("/api/system/latest-version");
}

export async function getSystemUpdateStatus(): Promise<SystemUpdateStatus> {
  return fetchJson<SystemUpdateStatus>("/api/system/update/status");
}

export async function requestSystemUpdate(): Promise<SystemUpdateRequestResponse> {
  return fetchJson<SystemUpdateRequestResponse>("/api/system/update", {
    method: "POST",
  });
}

export async function getSystemSetting(key: string): Promise<SystemSettingResponse> {
  const query = new URLSearchParams({ key }).toString();
  return fetchJson<SystemSettingResponse>(`/api/system/settings?${query}`);
}

export async function updateSystemSetting(
  key: string,
  value: unknown,
): Promise<SuccessMessageResponse> {
  return fetchJson<SuccessMessageResponse>("/api/system/settings", {
    method: "PATCH",
    body: JSON.stringify({ key, value }),
  });
}

export async function refreshManifests(): Promise<ManifestRefreshResponse> {
  return fetchJson<ManifestRefreshResponse>("/api/manifests/refresh", {
    method: "POST",
  });
}

export async function checkContentUpdates(): Promise<ContentUpdateCheckResult> {
  return fetchJson<ContentUpdateCheckResult>("/api/content-updates/check", {
    method: "POST",
  });
}

export async function applyContentUpdate(
  update: ResourceUpdateInfo,
): Promise<ContentUpdateApplyResponse> {
  return fetchJson<ContentUpdateApplyResponse>("/api/content-updates/apply", {
    method: "POST",
    body: JSON.stringify(update),
  });
}

export async function applyAllContentUpdates(
  updates: ResourceUpdateInfo[],
): Promise<ContentUpdateApplyAllResponse> {
  return fetchJson<ContentUpdateApplyAllResponse>("/api/content-updates/apply-all", {
    method: "POST",
    body: JSON.stringify({ updates }),
  });
}

export async function runBenchmark(
  benchmark_type: "full" | "system" | "ai" = "full",
  options?: { sync?: boolean },
): Promise<RunBenchmarkResponse | RunBenchmarkSyncResponse> {
  const query = options?.sync ? "?sync=true" : "";
  return fetchJson<RunBenchmarkResponse | RunBenchmarkSyncResponse>(`/api/benchmark/run${query}`, {
    method: "POST",
    body: JSON.stringify({ benchmark_type }),
  });
}

export async function runSystemBenchmark(): Promise<SimpleBenchmarkStartResponse> {
  return fetchJson<SimpleBenchmarkStartResponse>("/api/benchmark/run/system", {
    method: "POST",
  });
}

export async function runAiBenchmark(): Promise<SimpleBenchmarkStartResponse> {
  return fetchJson<SimpleBenchmarkStartResponse>("/api/benchmark/run/ai", {
    method: "POST",
  });
}

export async function listBenchmarkResults(): Promise<BenchmarkResultsResponse> {
  return fetchJson<BenchmarkResultsResponse>("/api/benchmark/results");
}

export async function getLatestBenchmarkResult(): Promise<BenchmarkLatestResultResponse> {
  return fetchJson<BenchmarkLatestResultResponse>("/api/benchmark/results/latest");
}

export async function getBenchmarkStatus(): Promise<BenchmarkStatusResponse> {
  return fetchJson<BenchmarkStatusResponse>("/api/benchmark/status");
}

export async function getBenchmarkSettings(): Promise<BenchmarkSettings> {
  return fetchJson<BenchmarkSettings>("/api/benchmark/settings");
}

export async function updateBenchmarkSettings(
  allow_anonymous_submission: boolean,
): Promise<{ success: boolean; settings: BenchmarkSettings }> {
  return fetchJson<{ success: boolean; settings: BenchmarkSettings }>("/api/benchmark/settings", {
    method: "POST",
    body: JSON.stringify({ allow_anonymous_submission }),
  });
}

export async function listDownloadJobs(): Promise<DownloadJobWithProgress[]> {
  return fetchJson<DownloadJobWithProgress[]>("/api/downloads/jobs");
}

export async function listAvailableModels(): Promise<AvailableModelsResponse> {
  return fetchJson<AvailableModelsResponse>("/api/ollama/models?recommendedOnly=true&limit=3");
}

export async function listInstalledModels(): Promise<InstalledModel[]> {
  return fetchJson<InstalledModel[]>("/api/ollama/installed-models");
}

export async function sendOllamaChatMessage(payload: {
  model: string;
  messages: Array<{ role: "system" | "user" | "assistant"; content: string }>;
  sessionId?: number;
}): Promise<OllamaChatResponse> {
  return fetchJson<OllamaChatResponse>("/api/ollama/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listZimFiles(): Promise<ListZimFilesResponse> {
  return fetchJson<ListZimFilesResponse>("/api/zim/list");
}

export async function getZimWikipediaState(): Promise<WikipediaState> {
  return fetchJson<WikipediaState>("/api/zim/wikipedia");
}

export async function listMapRegions(): Promise<ListMapRegionsResponse> {
  return fetchJson<ListMapRegionsResponse>("/api/maps/regions");
}

export async function listCuratedMapCollections(): Promise<CollectionWithStatus[]> {
  return fetchJson<CollectionWithStatus[]>("/api/maps/curated-collections");
}

export async function getMapStyles(): Promise<BaseStylesFile> {
  return fetchJson<BaseStylesFile>("/api/maps/styles");
}

export async function listChatSuggestions(): Promise<SuggestionsResponse> {
  return fetchJson<SuggestionsResponse>("/api/chat/suggestions");
}

export async function listChatSessions(): Promise<ChatSessionSummary[]> {
  return fetchJson<ChatSessionSummary[]>("/api/chat/sessions");
}

export async function getChatSession(sessionId: number): Promise<ChatSessionDetail> {
  return fetchJson<ChatSessionDetail>(`/api/chat/sessions/${sessionId}`);
}

export async function createChatSession(payload: {
  title: string;
  model?: string | null;
}): Promise<ChatSessionCreateResponse> {
  return fetchJson<ChatSessionCreateResponse>("/api/chat/sessions", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateChatSession(
  sessionId: number,
  payload: { title?: string; model?: string | null },
): Promise<ChatSessionCreateResponse> {
  return fetchJson<ChatSessionCreateResponse>(`/api/chat/sessions/${sessionId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export async function deleteChatSession(sessionId: number): Promise<void> {
  return fetchVoid(`/api/chat/sessions/${sessionId}`, {
    method: "DELETE",
  });
}

export async function deleteAllChatSessions(): Promise<{ success: boolean; message: string }> {
  return fetchJson<{ success: boolean; message: string }>("/api/chat/sessions/all", {
    method: "DELETE",
  });
}

export async function addChatMessage(
  sessionId: number,
  payload: { role: "system" | "user" | "assistant"; content: string },
): Promise<ChatMessage> {
  return fetchJson<ChatMessage>(`/api/chat/sessions/${sessionId}/messages`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function uploadKnowledgeFile(file: File): Promise<RagUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${getApiBaseUrl()}/api/rag/upload`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    throw new Error(`Failed to upload knowledge file: ${response.status}`);
  }
  return (await response.json()) as RagUploadResponse;
}

export async function listRagFiles(): Promise<RagFilesResponse> {
  return fetchJson<RagFilesResponse>("/api/rag/files");
}

export async function syncRagStorage(): Promise<{
  success: boolean;
  message: string;
  filesScanned: number;
  filesQueued: number;
  details?: string | null;
}> {
  return fetchJson("/api/rag/sync", {
    method: "POST",
  });
}

export async function deleteRagFile(source: string): Promise<{ message: string }> {
  return fetchJson("/api/rag/files", {
    method: "DELETE",
    body: JSON.stringify({ source }),
  });
}

export async function getEasySetupBootstrap(): Promise<EasySetupBootstrapResponse> {
  return fetchJson<EasySetupBootstrapResponse>("/api/easy-setup/bootstrap");
}

export async function getEasySetupDraft(): Promise<EasySetupDraft> {
  return fetchJson<EasySetupDraft>("/api/easy-setup/draft");
}

export async function saveEasySetupDraft(draft: EasySetupDraft): Promise<EasySetupDraft> {
  return fetchJson<EasySetupDraft>("/api/easy-setup/draft", {
    method: "PUT",
    body: JSON.stringify(draft),
  });
}

export async function buildEasySetupPlan(draft: EasySetupDraft): Promise<EasySetupPlan> {
  return fetchJson<EasySetupPlan>("/api/easy-setup/plan", {
    method: "POST",
    body: JSON.stringify(draft),
  });
}
