# Atlas Haven Requirements Matrix

- Status: Current + Planned
- Audience: Product owners, maintainers, QA, implementers
- Source of truth: Requirement traceability matrix for the rewrite
- Related modules/features: All major product domains and API tags

## Requirement Mapping

| Requirement ID | Requirement | Feature Area | Primary API Domains | Primary Modules |
| --- | --- | --- | --- | --- |
| R-001 | The product must provide one local-first shell for navigation and summary workflows. | Bridge, Control Room, Field Guide | `/health`, `/system/info`, `/docs/list` | `platform_core`, `docs`, `dashboard`, `M04` |
| R-002 | The product must support manifest-driven app discovery and catalog synchronization. | App Dock, app framework | `/system/services` | `catalog`, `platform_core`, `M02` |
| R-003 | Users must be able to install, start, stop, restart, reinstall, and update supported apps from the platform UI. | App Dock | `/system/services/install`, `/system/services/affect`, `/system/services/force-reinstall`, `/system/services/update` | `platform_core`, `orchestration`, `M03`, `M12` |
| R-004 | The product must provide a task-based first-run planning workflow. | Easy Setup | `/easy-setup/*` | `easy_setup`, `catalog`, `M06` |
| R-005 | The platform must ship with bundled manifest data and seed content for first-run usefulness. | Library Explorer, Library Shelf, Easy Setup | `/manifests/refresh`, `/zim/wikipedia` | `catalog`, `zim`, `M07` |
| R-006 | Users must be able to browse and use offline reference content through Kiwix. | Library Shelf, Kiwix and ZIM | `/zim/*` | `zim`, `platform_core`, `M07` |
| R-007 | The product must support local maps workflows and PMTiles-based viewing. | Atlas Maps | `/maps/*` | `maps`, `downloads`, `M08` |
| R-008 | Users must be able to manage local model runtimes and installed models. | Ollama Runtime | `/ollama/models`, `/ollama/installed-models` | `ollama`, `downloads`, `M09` |
| R-009 | The platform must support local chat sessions with persistent history. | AI Chat | `/chat/*`, `/ollama/chat` | `chat`, `ollama`, `M10` |
| R-010 | Users must be able to upload local files and use them in retrieval-assisted chat. | Knowledge Base | `/rag/*`, `/ollama/chat` | `knowledge_base`, `ollama`, `M11` |
| R-011 | The platform must expose download progress and job state. | Downloads and Jobs, Control Room | `/downloads/jobs*` | `downloads`, `M05` |
| R-012 | The system must expose release and runtime update awareness. | Control Room, system settings and releases | `/system/latest-version`, `/system/update*`, `/system/services/check-updates` | `platform_core`, planned parity work |
| R-013 | The product must support hardware and AI benchmark workflows. | Benchmarks | `/benchmark/*` | `benchmark`, `benchmark-helper`, `M13` |
| R-014 | The documentation surface must be navigable inside the product. | Field Guide | `/docs/list` | `docs`, `M04` |
| R-015 | The platform must be extensible through manifest-driven app packages. | App framework | `/system/services`, catalog sync paths | `catalog`, `orchestration`, `M14` |

## Requirement Coverage Notes

- `R-001` through `R-011` have at least partial implementation through `M00-M12`.
- `R-013` and `R-015` have baseline delivery through `M13` Benchmark and `M14` Extensibility; deeper parity (long-running benchmarks, app-author polish) remains planned per [`../planning/completed-features.md`](../planning/completed-features.md).
- `R-012` (settings, release/update awareness) remains the main matrix row still short of end-state parity; see [`../planning/next-wave-sequencing.md`](../planning/next-wave-sequencing.md).
- Feature docs under `../features/` explain the user-facing contract for each requirement.
- Developer docs under `../developer/` explain the implementation and extension responsibilities for each requirement family.

## Validation Expectations

Each requirement should eventually be validated through a mix of:

- unit tests for planners, validators, and service logic
- contract tests for API route availability and schema shape
- integration tests for DB, Redis, storage, and orchestration behavior
- app smoke tests for manifest packages
- E2E tests for core UI workflows
