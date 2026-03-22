# Atlas Haven Release Phasing

- Status: Current + Planned
- Audience: Product owners, maintainers, release planners
- Source of truth: Rewrite milestone and release-shape document
- Related modules/features: `M00-M14`, rebuild generation plans, parity planning

## Phase Model

Atlas Haven uses two phasing lenses:

- module delivery slices in the rewrite workspace
- broader product releases that group those slices into operator-facing milestones

## Current Module Status

### Delivered In The Active Workspace

- `M00` Bootstrap
- `M01` Platform Core
- `M02` Catalog Core
- `M03` Orchestration Core
- `M04` Shell And Dashboard
- `M05` Downloads And Jobs
- `M06` Easy Setup
- `M07` Kiwix And ZIM
- `M08` Maps
- `M09` Ollama And Qdrant
- `M10` Chat
- `M11` Knowledge Base
- `M12` App Roundout

### Planned Next Slices

- `M13` Benchmark
- `M14` Extensibility

## Proposed Product Releases

### Release A: Local Core Platform

Scope:

- compose bootstrap
- platform health
- catalog sync
- app lifecycle basics
- shell navigation

Primary outcome:

- a bootable rewrite workspace with a usable control surface

### Release B: Local Content And Setup

Scope:

- Easy Setup
- Kiwix and ZIM workflows
- maps
- docs shell
- downloads visibility

Primary outcome:

- first-run usefulness for offline knowledge and map workflows

### Release C: Local AI Workspace

Scope:

- Ollama and Qdrant
- AI Chat
- Knowledge Base

Primary outcome:

- private local chat and retrieval-assisted workflows

### Release D: Full App And Ops Surface

Scope:

- FlatNotes, CyberChef, Kolibri
- richer App Dock flows
- release/update parity
- benchmark parity
- restore and troubleshooting maturity

Primary outcome:

- a broader self-contained local platform with strong operator controls

### Release E: Extension Platform

Scope:

- app author tooling
- scaffolded new-app flow
- import/export of catalog metadata
- full manifest-driven extension documentation

Primary outcome:

- maintainers and app authors can extend Atlas Haven predictably

## Release Acceptance Expectations

Each release should include:

- updated feature documentation
- updated user guides
- updated developer docs
- verified API mappings
- test evidence for included domains

## Documentation Synchronization Rule

No release is considered documentation-complete until:

- the PRD reflects the delivered scope
- affected feature pages are updated
- user guides exist for new operator workflows
- developer docs explain any new extension points or architecture changes
