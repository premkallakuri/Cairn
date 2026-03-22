# Atlas Haven Completed Features

- Status: Current
- Audience: Product owners, maintainers, release planners
- Source of truth: Canonical completed-feature inventory for the active rewrite through `M14`
- Related modules/features: `M00-M14`, App Dock, Atlas Maps, AI Chat, Knowledge Base

This document consolidates what is complete in the rewrite through `M14`. It is
grouped by user-facing capability rather than by file or commit. Module notes in
[`../modules/`](../modules/) remain the authoritative engineering evidence for
each completion claim.

## Completion Legend

- `Complete for current wave`: delivered and usable for the current rewrite phase
- `Partial`: delivered enough to use or validate, but not yet full parity

## Platform Bootstrap And Runtime Core

Status: `Complete for current wave`

Implemented now:

- rewrite workspace structure and bootstrap commands
- local compose stack with `api`, `worker`, `web`, `mysql`, `redis`, and `disk-collector`
- environment/config loading, logging, error handling, DB initialization
- health and basic system information endpoints

Delivered by:

- `M00 Bootstrap`
- `M01 Platform Core`

Still partial:

- runtime health is foundational, but fuller system settings and operational parity are still ahead

Primary evidence:

- [`../modules/M00-bootstrap.md`](../modules/M00-bootstrap.md)
- [`../modules/M01-platform-core.md`](../modules/M01-platform-core.md)

## Catalog And Orchestration Foundations

Status: `Complete for current wave`

Implemented now:

- manifest scan and sync from disk
- app catalog persistence
- dependency ordering
- basic lifecycle orchestration primitives

Delivered by:

- `M02 Catalog Core`
- `M03 Orchestration Core`

Still partial:

- current orchestration behavior is sufficient for the rewrite wave, but deeper container-backed parity and richer event/rollback behavior remain future work

Primary evidence:

- [`../modules/M02-catalog-core.md`](../modules/M02-catalog-core.md)
- [`../modules/M03-orchestration-core.md`](../modules/M03-orchestration-core.md)

## Shell And Navigation

Status: `Complete for current wave`

Implemented now:

- Atlas Haven shell
- top navigation for `Bridge`, `Atlas Maps`, `AI Chat`, `Field Guide`, and `Control Room`
- backend-backed route skeletons and branded shell navigation

Delivered by:

- `M04 Shell And Dashboard`

Still partial:

- the shell is in place, but some destinations still have planned parity depth beyond the current wave

Primary evidence:

- [`../modules/M04-shell-and-dashboard.md`](../modules/M04-shell-and-dashboard.md)

## Downloads And Jobs

Status: `Complete for current wave`

Implemented now:

- durable download job persistence
- job listing APIs
- worker-facing download runner
- Control Room visibility of active download jobs

Delivered by:

- `M05 Downloads And Jobs`

Still partial:

- broader job families, history, and richer event streaming are future work

Primary evidence:

- [`../modules/M05-downloads-and-jobs.md`](../modules/M05-downloads-and-jobs.md)

## Easy Setup

Status: `Complete for current wave`

Implemented now:

- persisted setup drafts
- capability and content bootstrap payload
- setup plan generation for apps, content, maps, and models
- reviewable estimated storage summary

Delivered by:

- `M06 Easy Setup`

Still partial:

- the current wave plans installations but does not yet deliver full one-click end-to-end plan execution

Primary evidence:

- [`../modules/M06-easy-setup.md`](../modules/M06-easy-setup.md)

## Kiwix And ZIM

Status: `Complete for current wave`

Implemented now:

- local ZIM listing and safe deletion
- bundled demo Wikipedia path
- Kiwix preinstall seeding behavior
- curated category and remote catalog groundwork
- Field Guide-facing library visibility

Delivered by:

- `M07 Kiwix And ZIM`

Still partial:

- richer remote explorer UX, broader metadata, and full parity replacement/update flows are still planned

Primary evidence:

- [`../modules/M07-kiwix-and-zim.md`](../modules/M07-kiwix-and-zim.md)

## Atlas Maps

Status: `Partial`

Implemented now:

- built-in maps capability package
- PMTiles file listing
- curated collection visibility
- style generation
- Atlas Maps route and page foundation

Delivered by:

- `M08 Maps`

Still partial:

- full remote collection acquisition, base-asset maturity, and richer viewer parity remain next-wave or later work

Primary evidence:

- [`../modules/M08-maps.md`](../modules/M08-maps.md)

## Ollama And Qdrant

Status: `Complete for current wave`

Implemented now:

- available and installed model APIs
- model queue/delete lifecycle
- dependency-aware install of `nomad_ollama` and `nomad_qdrant`
- shared download tracking for model pulls
- AI runtime visibility in the shell

Delivered by:

- `M09 Ollama And Qdrant`

Still partial:

- current runtime metadata is intentionally simplified and not yet a full live-runtime parity layer

Primary evidence:

- [`../modules/M09-ollama-and-qdrant.md`](../modules/M09-ollama-and-qdrant.md)

## AI Chat

Status: `Complete for current wave`

Implemented now:

- local multi-session chat
- chat session CRUD
- persistent messages
- starter prompts
- title generation
- JSON and SSE-compatible chat response support

Delivered by:

- `M10 Chat`

Still partial:

- richer streaming UX and deeper model/citation ergonomics are still planned

Primary evidence:

- [`../modules/M10-chat.md`](../modules/M10-chat.md)

## Knowledge Base

Status: `Complete for current wave`

Implemented now:

- local file upload
- file indexing and sync
- indexed file inventory
- retrieval-assisted chat context
- chat workspace Knowledge Base controls

Delivered by:

- `M11 Knowledge Base`

Still partial:

- broader format support, richer vector workflows, and more advanced indexing diagnostics remain planned

Primary evidence:

- [`../modules/M11-knowledge-base.md`](../modules/M11-knowledge-base.md)

## App Dock And Day-One App Coverage

Status: `Complete for current wave`

Implemented now:

- App Dock on Bridge and Control Room
- install, start, stop, restart, reinstall, update, and check-updates flows
- launch URL visibility
- current-version visibility
- deterministic available-version handling for the current app set
- completed day-one app coverage in the shell

Delivered by:

- `M12 App Roundout`

Still partial:

- richer per-app detail pages, deeper health diagnostics, and stronger release/update parity are still planned

Primary evidence:

- [`../modules/M12-app-roundout.md`](../modules/M12-app-roundout.md)

## Benchmark Workflows

Status: `Complete for current wave`

Implemented now:

- persisted local benchmark runs and result history
- system, AI, and full benchmark entrypoints
- latest-result, status, settings, submission, builder-tag, and comparison routes
- Control Room benchmark lane for running and reviewing local performance snapshots
- benchmark helper package retained as the runtime marker inside the app framework

Delivered by:

- `M13 Benchmark`

Still partial:

- long-running worker-driven benchmark execution, richer comparison UX, and deeper interpretation guidance are still planned

Primary evidence:

- [`../modules/M13-benchmark.md`](../modules/M13-benchmark.md)

## Extensibility And New-App Scaffolding

Status: `Complete for current wave`

Implemented now:

- stronger manifest validation for ids, slugs, hooks, dependencies, storage refs, and runtime ports
- app scaffolder service for generating new app packages from the existing framework
- shell wrapper for scaffold generation from the workspace root
- sample app package under `apps/sample-notes` that can be catalog-scanned without core changes
- extended orchestration hook lifecycle support for install, update, rollback, and uninstall stages

Delivered by:

- `M14 Extensibility`

Still partial:

- the scaffolder is intentionally opinionated and still leaves room for app-specific runtime polish

Primary evidence:

- [`../modules/M14-extensibility.md`](../modules/M14-extensibility.md)

## Completed App Matrix

| App / Capability | Current State | Delivered In | Notes |
| --- | --- | --- | --- |
| Kiwix | Complete for current wave | `M07` | Bundled demo Wikipedia and local ZIM serving path are in place |
| Qdrant | Complete for current wave | `M09` | Dependency-aware install and runtime visibility delivered |
| Ollama | Complete for current wave | `M09` | Model lifecycle and chat integration are delivered |
| FlatNotes | Complete for current wave | `M12` | Install, launch, restart, reinstall, and update surface delivered |
| CyberChef | Complete for current wave | `M12` | Day-one utility app coverage delivered |
| Kolibri | Complete for current wave | `M12` | Education app coverage delivered |
| Benchmark Helper | Complete for current wave | `M13` | Local benchmark routes and persisted results now use the benchmark lane |
| Sample Notes | Complete for current wave | `M14` | Sample package proves the catalog and scaffold flow |
| Atlas Maps | Partial | `M08` | First-class route and local capability exist; full parity still ahead |

## Completed Top-Level Product Areas

These top-level product areas now have delivered or partially delivered rewrite coverage:

- `Bridge`
- `Atlas Maps`
- `AI Chat`
- `Field Guide`
- `Control Room`
- `App Dock`
- `Easy Setup`
- `Library Explorer` foundations
- `Library Shelf` foundations

## What This Means Operationally

Atlas Haven is now beyond scaffold stage. Through `M12`, the rewrite has a
usable local shell, working service/app management for the current wave, local AI
and library workflows, and a documented structure for moving into the next build
wave. The most important remaining work is not basic shell creation, but parity
completion, benchmark delivery, extensibility, and operations hardening.
