import { ControlRoomOverview } from "@/features/control_room";
import {
  checkContentUpdates,
  getBenchmarkSettings,
  getBenchmarkStatus,
  getInternetStatus,
  getLatestBenchmarkResult,
  getLatestVersion,
  getSystemInfo,
  getSystemUpdateStatus,
  listBenchmarkResults,
  listDownloadJobs,
  listServices,
} from "@/lib/api/client";
import type {
  BenchmarkStatusResponse,
  ContentUpdateCheckResult,
  LatestVersionResponse,
  SystemInformationResponse,
  SystemUpdateStatus,
} from "@/lib/types/atlas-haven-api";

export default async function ControlRoomPage() {
  const [
    services,
    systemInfo,
    downloadJobs,
    internetStatus,
    latestVersion,
    updateStatus,
    benchmarkStatus,
    benchmarkSettings,
    latestBenchmark,
    benchmarkResults,
    contentUpdates,
  ] = await Promise.all([
    listServices().catch(() => []),
    getSystemInfo().catch(
      (): SystemInformationResponse => ({
        app_name: "",
        version: "",
        environment: "",
        python_version: "",
        workspace_root: "",
        storage_path: "",
        catalog_entries: 0,
      }),
    ),
    listDownloadJobs().catch(() => []),
    getInternetStatus().catch(() => false),
    getLatestVersion().catch(
      (): LatestVersionResponse => ({
        success: false,
        updateAvailable: false,
        currentVersion: "",
        latestVersion: "",
      }),
    ),
    getSystemUpdateStatus().catch(
      (): SystemUpdateStatus => ({
        stage: "idle",
        progress: 0,
        message: "",
        timestamp: "",
      }),
    ),
    getBenchmarkStatus().catch(
      (): BenchmarkStatusResponse => ({
        status: "unknown",
      }),
    ),
    getBenchmarkSettings().catch(() => ({ allow_anonymous_submission: false })),
    getLatestBenchmarkResult().catch(() => ({ result: null })),
    listBenchmarkResults().catch(() => ({ results: [], total: 0 })),
    checkContentUpdates().catch(
      (): ContentUpdateCheckResult => ({ updates: [], checked_at: "" }),
    ),
  ]);
  return (
    <ControlRoomOverview
      services={services}
      systemInfo={systemInfo}
      downloadJobs={downloadJobs}
      internetStatus={internetStatus}
      latestVersion={latestVersion}
      updateStatus={updateStatus}
      benchmarkStatus={benchmarkStatus}
      benchmarkSettings={benchmarkSettings}
      latestBenchmark={latestBenchmark.result}
      benchmarkResultTotal={benchmarkResults.total}
      contentUpdates={contentUpdates}
    />
  );
}
