export type DocIndexItem = {
  title: string;
  slug: string;
};

export type SpecTier = {
  name: string;
  slug: string;
  description: string;
  recommended?: boolean;
  includesTier?: string | null;
};

export type CategoryWithStatus = {
  name: string;
  slug: string;
  icon: string;
  description: string;
  language: string;
  installedTierSlug?: string;
  tiers: SpecTier[];
};

export type HealthResponse = {
  status: string;
  service: string;
  version: string;
};

export type SystemInformationResponse = {
  app_name: string;
  version: string;
  environment: string;
  python_version: string;
  workspace_root: string;
  storage_path: string;
  catalog_entries: number;
};

export type ServiceSlim = {
  id: number;
  service_name: string;
  friendly_name: string | null;
  description: string | null;
  icon: string | null;
  installed: boolean;
  installation_status: string;
  status: string | null;
  ui_location: string | null;
  powered_by: string | null;
  display_order: number | null;
  container_image: string;
  available_update_version?: string | null;
  kind?: string | null;
  current_version?: string | null;
  launch_url?: string | null;
};

export type SuccessMessageResponse = {
  success: boolean;
  message: string;
};

export type AvailableVersion = {
  tag: string;
  isLatest: boolean;
  releaseUrl?: string | null;
};

export type AvailableVersionsResponse = {
  versions: AvailableVersion[];
};

export type LatestVersionResponse = {
  success: boolean;
  updateAvailable: boolean;
  currentVersion: string;
  latestVersion: string;
  message?: string | null;
};

export type SystemUpdateStatus = {
  stage: "idle" | "starting" | "pulling" | "pulled" | "recreating" | "complete" | "error";
  progress: number;
  message: string;
  timestamp: string;
};

export type SystemUpdateRequestResponse = {
  success?: boolean | null;
  message?: string | null;
  note?: string | null;
  error?: string | null;
};

export type SystemSettingResponse = {
  key: string;
  value?: unknown;
};

export type ResourceUpdateInfo = {
  resource_id: string;
  resource_type: "zim" | "map";
  installed_version: string;
  latest_version: string;
  download_url: string;
};

export type ManifestRefreshResponse = {
  success: boolean;
  changed: {
    zim_categories: boolean;
    maps: boolean;
    wikipedia: boolean;
  };
};

export type ContentUpdateCheckResult = {
  updates: ResourceUpdateInfo[];
  checked_at: string;
  error?: string | null;
};

export type ContentUpdateApplyResponse = {
  success: boolean;
  jobId?: string | null;
  error?: string | null;
};

export type ContentUpdateApplyAllResponse = {
  results: Array<{
    resource_id: string;
    success: boolean;
    jobId?: string | null;
    error?: string | null;
  }>;
};

export type BenchmarkResult = {
  id: number;
  benchmark_id: string;
  benchmark_type: "full" | "system" | "ai";
  cpu_model: string;
  cpu_cores: number;
  cpu_threads: number;
  ram_bytes: number;
  disk_type: string;
  gpu_model?: string | null;
  cpu_score: number;
  memory_score: number;
  disk_read_score: number;
  disk_write_score: number;
  ai_tokens_per_second?: number | null;
  ai_model_used?: string | null;
  ai_time_to_first_token?: number | null;
  nomad_score: number;
  submitted_to_repository: boolean;
  submitted_at?: string | null;
  repository_id?: string | null;
  builder_tag?: string | null;
  created_at: string;
  updated_at: string;
};

export type BenchmarkResultsResponse = {
  results: BenchmarkResult[];
  total: number;
};

export type BenchmarkLatestResultResponse = {
  result: BenchmarkResult | null;
};

export type BenchmarkStatusResponse = {
  status: string;
  benchmarkId?: string | null;
};

export type BenchmarkSettings = {
  allow_anonymous_submission: boolean;
  installation_id?: string | null;
  last_benchmark_run?: string | null;
};

export type RunBenchmarkResponse = {
  success: boolean;
  job_id: string;
  benchmark_id: string;
  message: string;
};

export type RunBenchmarkSyncResponse = {
  success: boolean;
  benchmark_id: string;
  nomad_score: number;
  result: BenchmarkResult;
};

export type SimpleBenchmarkStartResponse = {
  success: boolean;
  benchmark_id: string;
  message: string;
};

export type DownloadJobWithProgress = {
  jobId: string;
  url: string;
  progress: number;
  filepath: string;
  filetype: string;
};

export type NomadOllamaModelTag = {
  name: string;
  size: string;
  context: string;
  input: string;
  cloud: boolean;
  thinking: boolean;
};

export type NomadOllamaModel = {
  id: string;
  name: string;
  description: string;
  estimated_pulls: string;
  model_last_updated: string;
  first_seen: string;
  tags: NomadOllamaModelTag[];
};

export type AvailableModelsResponse = {
  models: NomadOllamaModel[];
  hasMore: boolean;
};

export type InstalledModel = {
  name?: string;
  model?: string;
  status?: string;
  size?: string;
  description?: string;
  storagePath?: string;
  digest?: string | null;
  [key: string]: unknown;
};

export type OllamaChatMessage = {
  role: "system" | "user" | "assistant";
  content: string;
  thinking?: string | null;
};

export type OllamaChatResponse = {
  model: string;
  created_at: string;
  message: OllamaChatMessage;
  done: boolean;
};

export type SuggestionsResponse = {
  suggestions: string[];
};

export type ChatSessionSummary = {
  id: number;
  title: string;
  model?: string | null;
  timestamp?: string | null;
  lastMessage?: string | null;
};

export type ChatMessage = {
  id: number;
  role: "system" | "user" | "assistant";
  content: string;
  timestamp: string;
};

export type ChatSessionDetail = {
  id: number;
  title: string;
  model?: string | null;
  timestamp?: string | null;
  messages: ChatMessage[];
};

export type ChatSessionCreateResponse = {
  id: number;
  title: string;
  model?: string | null;
  timestamp?: string | null;
};

export type RagUploadResponse = {
  message: string;
  jobId?: string | null;
  fileName: string;
  filePath: string;
  alreadyProcessing: boolean;
};

export type EmbedJobWithProgress = {
  jobId: string;
  fileName: string;
  filePath: string;
  progress: number;
  status: string;
};

export type RagFilesResponse = {
  files: string[];
};

export type ZimFileWithMetadata = {
  type: "file";
  key: string;
  name: string;
  title?: string | null;
  summary?: string | null;
  author?: string | null;
  size_bytes?: number | null;
};

export type ListZimFilesResponse = {
  files: ZimFileWithMetadata[];
  next?: string | null;
};

export type WikipediaOption = {
  id: string;
  name: string;
  description: string;
  size_mb: number;
  url?: string | null;
  version?: string | null;
};

export type WikipediaCurrentSelection = {
  optionId: string;
  status: "none" | "downloading" | "installed" | "failed";
  filename?: string | null;
  url?: string | null;
};

export type WikipediaState = {
  options: WikipediaOption[];
  currentSelection?: WikipediaCurrentSelection | null;
};

export type MapFileEntry = {
  type: "file";
  key: string;
  name: string;
};

export type ListMapRegionsResponse = {
  files: MapFileEntry[];
};

export type SpecResource = {
  id: string;
  version: string;
  title: string;
  description: string;
  url: string;
  size_mb: number;
};

export type CollectionWithStatus = {
  name: string;
  slug: string;
  description: string;
  icon: string;
  language: string;
  resources: SpecResource[];
  all_installed: boolean;
  installed_count: number;
  total_count: number;
};

export type SourceDefinition = {
  type: string;
  attribution: string;
  url: string;
};

export type BaseStylesFile = {
  version: number;
  sources: Record<string, SourceDefinition>;
  layers: Record<string, unknown>[];
  sprite: string;
  glyphs: string;
};

export type EasySetupDraft = {
  currentStep: number;
  selectedCapabilityIds: string[];
  selectedMapCollectionSlugs: string[];
  selectedCategoryTierSlugs: Record<string, string>;
  selectedAiModelIds: string[];
  selectedWikipediaOptionId: string;
};

export type EasySetupCapabilityOption = {
  id: string;
  group: string;
  name: string;
  technicalName: string;
  description: string;
  features: string[];
  serviceName: string;
  installed: boolean;
  recommended: boolean;
};

export type EasySetupMapCollectionOption = {
  name: string;
  slug: string;
  description: string;
  icon: string;
  language: string;
  resourceCount: number;
  sizeMb: number;
};

export type EasySetupAiModelOption = {
  id: string;
  label: string;
  description: string;
  tag: string;
  sizeLabel: string;
  sizeMb: number;
  recommended: boolean;
  thinking: boolean;
  requiresService: string;
};

export type EasySetupWikipediaOption = {
  id: string;
  name: string;
  description: string;
  sizeMb: number;
  url?: string | null;
  version?: string | null;
};

export type EasySetupBootstrapResponse = {
  draft: EasySetupDraft;
  capabilities: EasySetupCapabilityOption[];
  additionalTools: EasySetupCapabilityOption[];
  mapCollections: EasySetupMapCollectionOption[];
  curatedCategories: CategoryWithStatus[];
  wikipediaOptions: EasySetupWikipediaOption[];
  aiModels: EasySetupAiModelOption[];
};

export type PlannedService = {
  serviceName: string;
  friendlyName: string;
  reason: string;
  alreadyInstalled: boolean;
};

export type PlannedMapCollection = {
  slug: string;
  name: string;
  resourceCount: number;
  sizeMb: number;
};

export type PlannedCategorySelection = {
  categorySlug: string;
  categoryName: string;
  tierSlug: string;
  tierName: string;
  resourceCount: number;
  sizeMb: number;
};

export type PlannedAiModel = {
  id: string;
  label: string;
  tag: string;
  sizeLabel: string;
  sizeMb: number;
};

export type PlannedWikipediaSelection = {
  id: string;
  name: string;
  description: string;
  sizeMb: number;
  url?: string | null;
  version?: string | null;
};

export type EasySetupPlanSummary = {
  serviceCount: number;
  mapCollectionCount: number;
  mapResourceCount: number;
  categorySelectionCount: number;
  categoryResourceCount: number;
  aiModelCount: number;
  totalEstimatedStorageMb: number;
  totalEstimatedStorageLabel: string;
};

export type EasySetupPlan = {
  draft: EasySetupDraft;
  services: PlannedService[];
  maps: PlannedMapCollection[];
  categorySelections: PlannedCategorySelection[];
  aiModels: PlannedAiModel[];
  wikipedia: PlannedWikipediaSelection;
  summary: EasySetupPlanSummary;
};
