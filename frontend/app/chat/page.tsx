import { ChatOverview } from "@/features/chat";
import {
  getChatSession,
  listAvailableModels,
  listChatSessions,
  listChatSuggestions,
  listInstalledModels,
  listRagFiles,
  listServices,
} from "@/lib/api/client";

export default async function ChatPage() {
  const [services, availableModels, installedModels, suggestions, sessions, knowledgeFiles] =
    await Promise.all([
      listServices().catch(() => []),
      listAvailableModels().catch(() => ({ models: [] })),
      listInstalledModels().catch(() => []),
      listChatSuggestions().catch(() => ({ suggestions: [] })),
      listChatSessions().catch(() => []),
      listRagFiles().catch(() => ({ files: [] })),
    ]);

  let activeSession = null;
  if (sessions[0]) {
    try {
      activeSession = await getChatSession(sessions[0].id);
    } catch {
      activeSession = null;
    }
  }

  return (
    <ChatOverview
      services={services}
      availableModels={availableModels.models}
      installedModels={installedModels}
      initialSuggestions={suggestions.suggestions}
      initialSessions={sessions}
      initialActiveSession={activeSession}
      initialKnowledgeFiles={knowledgeFiles.files}
    />
  );
}
