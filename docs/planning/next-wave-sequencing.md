# Atlas Haven Next-Wave Sequencing

- Status: Current + Planned
- Audience: Maintainers, release planners
- Source of truth: Recommended execution order for the post-`M14` implementation wave
- Related modules/features: settings/update parity, content parity, ops hardening, AI maturity

This document converts the near-term roadmap into a concrete recommended build
sequence. The ordering is based on dependency value, operator impact, and how
much each step unlocks later work.

`M13 Benchmark` and `M14 Extensibility` are now complete. The remaining
recommended execution order starts with the parity work that still sits ahead of
Atlas Haven.

## 1. Settings And Release/Update Parity

Why third:

- settings and update maturity depend on the existing App Dock and Control Room surfaces
- they benefit from the stronger operations foundation established by the first two steps

Prerequisites:

- platform core
- App Dock lifecycle/update patterns
- Control Room shell maturity

Exit criteria:

- settings persistence and retrieval are usable
- release/update state is surfaced coherently in the shell
- operators can understand what version they are on and what can be updated

Docs that must be updated:

- `features/system-settings-and-releases.md`
- troubleshooting and operations guides
- developer deployment/operations docs

Expected tests:

- unit tests for settings and update state logic
- contract tests for `/system/*` additions
- integration tests for update/status flows
- UI or E2E checks for Control Room settings/update paths

## 2. Content Update Parity

Why fourth:

- content update flows depend on stronger settings/update foundations and mature job handling
- this work benefits from already having maps and library domains in place

Prerequisites:

- downloads/jobs
- manifests/content metadata
- Kiwix/ZIM and maps foundations

Exit criteria:

- content update checks produce actionable results
- update application behavior is visible and understandable
- users can distinguish current content, pending updates, and failed updates

Docs that must be updated:

- `features/manifests-and-content-updates.md`
- map and library user guides
- API domain mapping if route behavior changes materially

Expected tests:

- unit tests for update detection
- contract tests for content update routes
- integration tests for queued update execution
- smoke checks where content flows touch app/runtime state

## 3. Ops Hardening And Recovery Workflows

Why fifth:

- this step is most valuable after the main parity and extension gaps are narrowed
- it consolidates earlier work into a more operator-resilient platform

Prerequisites:

- Control Room
- App Dock
- settings/update parity
- content update parity

Exit criteria:

- backup/restore and recovery guidance is stronger and reflected in product behavior where applicable
- key runtime failure modes are easier to diagnose
- operators have clearer workflows for recovery after failed installs, updates, or degraded state

Docs that must be updated:

- `user-guides/manage-storage-backups-and-restores.md`
- `user-guides/troubleshoot-runtime-updates-and-failures.md`
- `developer/deployment-and-operations.md`

Expected tests:

- integration tests around failure and recovery state where product behavior exists
- smoke tests for critical reinstall/update/restart flows
- E2E checks for operator-facing recovery paths when available

## 4. AI And Product Maturity

Why fourth:

- once system, content, and recovery maturity are stronger, the AI-facing experience can be improved on a steadier foundation
- this step turns existing chat, knowledge, and benchmark functionality into a more coherent operator workflow

Prerequisites:

- benchmark workflows
- chat and knowledge base foundations
- content update parity
- stronger App Dock diagnostics

Exit criteria:

- local AI readiness and model state are clearer in the shell
- knowledge workflows expose richer citations and diagnostics
- benchmark interpretation and comparison are more understandable
- app details and troubleshooting surfaces are more useful to operators

Docs that must be updated:

- `features/ai-chat.md`
- `features/knowledge-base.md`
- `features/benchmarks.md`
- relevant user guides and developer diagnostics docs

Expected tests:

- integration tests for AI/KB retrieval and readiness state
- contract coverage for any expanded benchmark or diagnostics routes
- E2E checks for major user-facing AI workflows

## Recommended Rule For The Wave

Do not treat a step as complete until:

- its feature docs match the shipped behavior
- its operator guide is updated if the workflow is user-visible
- its developer docs reflect any new architectural or framework responsibilities
- its test layers match the module’s risk profile

This sequencing keeps the post-`M14` wave focused, incremental, and testable
without pretending the entire long-horizon rebuild must be delivered at once.
