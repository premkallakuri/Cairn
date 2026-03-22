# Atlas Haven Endpoint Domain Map

- Status: Current + Planned
- Audience: Maintainers, QA, documentation authors
- Source of truth: Mapping from API domains to feature docs and user guides
- Related modules/features: all API domains

## Domain Mapping

| API Domain | Primary Paths | Feature Docs | User Guides |
| --- | --- | --- | --- |
| Health | `/health` | `../../features/bridge.md`, `../../features/control-room.md` | `../../user-guides/first-run-and-bootstrap.md` |
| Easy Setup | `/easy-setup/*` | `../../features/easy-setup.md` | `../../user-guides/first-run-and-bootstrap.md` |
| Content Updates | `/manifests/refresh`, `/content-updates/*` | `../../features/manifests-and-content-updates.md` | `../../user-guides/troubleshoot-runtime-updates-and-failures.md` |
| Maps | `/maps/*` | `../../features/atlas-maps.md` | `../../user-guides/download-and-use-maps.md` |
| Docs | `/docs/list` | `../../features/field-guide.md` | `../../user-guides/first-run-and-bootstrap.md` |
| Downloads | `/downloads/jobs*` | `../../features/downloads-and-jobs.md` | `../../user-guides/troubleshoot-runtime-updates-and-failures.md` |
| Ollama | `/ollama/*` | `../../features/ollama-runtime.md` | `../../user-guides/run-local-ai-chat.md` |
| Chat Sessions | `/chat/*` | `../../features/ai-chat.md` | `../../user-guides/run-local-ai-chat.md` |
| Knowledge Base | `/rag/*` | `../../features/knowledge-base.md` | `../../user-guides/build-and-search-the-knowledge-base.md` |
| System | `/system/*` | `../../features/app-dock.md`, `../../features/system-settings-and-releases.md` | `../../user-guides/install-and-manage-apps.md`, `../../user-guides/troubleshoot-runtime-updates-and-failures.md` |
| ZIM | `/zim/*` | `../../features/kiwix-and-zim.md`, `../../features/library-explorer.md`, `../../features/library-shelf.md` | `../../user-guides/manage-zim-and-wikipedia.md`, `../../user-guides/use-the-offline-library.md` |
| Benchmark | `/benchmark/*` | `../../features/benchmarks.md` | `../../user-guides/run-benchmarks.md` |

## Coverage Rule

Every new API domain or route family added to Atlas Haven should be reflected in:

- a feature specification
- at least one task-based user guide if the route changes operator workflow
- developer docs if the route changes architecture or extension points
