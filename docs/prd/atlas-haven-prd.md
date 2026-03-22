# Atlas Haven Product Requirements Document

- Status: Current + Planned
- Audience: Product owners, maintainers, designers, implementers
- Source of truth: Primary product contract for the Atlas Haven rewrite
- Related modules/features: `M00-M12`, app framework, API contract, all top-level navigation areas

## 1. Product Definition

Atlas Haven is a local-first platform that combines offline knowledge access,
maps, private AI, and Docker-managed utility apps into one operator-controlled
system. It is designed to remain useful when connectivity is slow, unreliable,
or intentionally unavailable.

Atlas Haven replaces the legacy admin implementation with a Python backend and a
Next.js frontend while preserving the operational model:

- local-first storage
- Docker-managed sibling applications
- MySQL and Redis for platform state
- a no-login local operator experience
- bundled startup data for first-run usefulness

## 2. Problem Statement

People who need resilient local knowledge and tools usually assemble them from
unrelated dashboards, scripts, containers, and content archives. That creates
five recurring problems:

1. Operators need multiple interfaces to manage content, apps, and models.
2. Offline content, maps, and AI tooling are difficult to install and maintain.
3. Knowledge workflows break when internet access is poor or intentionally absent.
4. Local infrastructure is powerful but too fragmented for non-expert operators.
5. Extending the platform with new apps often requires core code changes.

Atlas Haven solves this by providing one coherent local control surface for
installing apps, managing content, using private AI, and maintaining the system.

## 3. Product Vision

Atlas Haven should feel like a modern field library and command bridge:

- calm and capable rather than noisy
- private by default rather than cloud-first
- operationally clear rather than dev-tool-centric
- useful on day one with bundled manifests and seed content
- extensible through a manifest-driven app framework

The product should support education, preparedness, field research, homelab
operations, offline-first learning, and local AI experimentation without
requiring users to stitch together separate tools.

## 4. Target Users

### Primary Users

- Local operator: installs, updates, monitors, and repairs the system
- Knowledge-oriented user: consumes library content, maps, and AI chat
- Maintainer: evolves the rewrite, preserves parity, and ships features
- App author: adds new manifest-driven apps without editing core orchestration

### Secondary Users

- Educator deploying offline learning content
- Researcher building a local reference and retrieval workflow
- Preparedness or field-use operator curating maps and reference content
- Benchmarking or hardware-evaluation user measuring device capabilities

## 5. Core Value Proposition

Atlas Haven provides:

- one interface for local apps, offline content, and AI
- one install model for sibling app containers
- one task-driven operator workflow for setup and maintenance
- one product language that unifies maps, libraries, chat, and system controls
- one extension framework for future apps

## 6. Current State Versus Target State

### Current State

The rewrite workspace currently delivers:

- `Bridge`, `Atlas Maps`, `AI Chat`, `Field Guide`, and `Control Room`
- service catalog sync and install/start/stop/restart/reinstall/update primitives
- Easy Setup planning
- Kiwix and ZIM workflows with bundled demo Wikipedia
- maps collection visibility and viewer scaffolding
- Ollama and Qdrant runtime management
- multi-session local chat
- Knowledge Base upload, indexing, and retrieval-assisted chat
- App Dock coverage for Kiwix, Qdrant, Ollama, FlatNotes, CyberChef, and Kolibri

### Planned End State

The full platform must additionally deliver:

- complete content update flows and release/update management parity
- richer benchmark execution and result interpretation
- complete map acquisition and base-asset workflows
- stronger system settings, restore, backup, and troubleshooting flows
- fuller app detail surfaces and deeper install diagnostics
- mature app authoring documentation and scaffolding

## 7. Success Metrics

### Operator Success

- A clean local bootstrap should result in a working system without manual code edits.
- A user should be able to install core apps from the App Dock without Docker CLI use.
- A user should be able to access bundled library content on first run.

### Product Success

- Every major domain has a documented feature spec, operator guide, and API mapping.
- Every current app is installable and describable through the manifest framework.
- New apps can be added with documented manifest, hook, and test contracts.

### Reliability Success

- Local storage persists across restarts and reinstalls.
- Updates and reinstalls do not require users to understand internal container wiring.
- Core workflows remain usable when external internet is unavailable after initial setup.

## 8. Non-Goals

Atlas Haven is not intended to be:

- a multi-tenant SaaS platform
- a cloud-managed fleet system
- an identity-heavy enterprise portal
- a generic container dashboard for arbitrary Docker stacks
- a military or survivalist-branded product

## 9. Functional Requirements

### Shell And Navigation

- Provide top-level navigation for `Bridge`, `Atlas Maps`, `AI Chat`, `Field Guide`, and `Control Room`.
- Use a consistent Atlas Haven brand system and terminology.
- Surface major system capabilities without requiring a settings maze.

### App Dock And Service Lifecycle

- Discover manifest-driven apps from the catalog.
- Install apps and dependency chains.
- Start, stop, restart, force reinstall, and update supported apps.
- Surface launch URLs, current version, available update version, and operator-facing status.

### Easy Setup

- Convert selected capabilities into a concrete installation and content plan.
- Present recommended tools, map collections, Wikipedia choices, and AI models.
- Persist drafts and support review before execution.

### Library And Content

- Provide bundled manifests for first-run curated content.
- Support local ZIM inventory and curated Wikipedia selection.
- Provide Kiwix-backed offline library serving.
- Support map collection visibility and acquisition workflows.

### AI And Knowledge Workflows

- Install and manage Ollama and Qdrant.
- Support local model catalog visibility and install tracking.
- Provide multi-session local chat.
- Allow users to upload local files and use them in retrieval-assisted chat.

### Documentation

- Provide a browsable `Field Guide` surface.
- Include product docs, use cases, setup help, and troubleshooting references.

### Benchmarks

- Support benchmark helper/runtime flows.
- Collect, store, and present benchmark results and comparisons.

### Extensibility

- Define a manifest contract for app packages.
- Support optional hooks for lifecycle customization.
- Provide app author documentation and testing guidance.

## 10. Non-Functional Requirements

- Local-first operation with host-backed storage
- Docker-first deployment model
- Clear operator messaging and understandable failure states
- Stable, documented `/api/*` contract for the rewrite
- Modular code boundaries across backend and frontend feature domains
- Testability through unit, contract, integration, smoke, and E2E layers
- Documentation that separates shipped behavior from planned behavior

## 11. Information Architecture

### Product Navigation

- `Bridge`: landing surface, summaries, launch surfaces, and high-priority actions
- `Atlas Maps`: map resources, downloads, and viewing workflows
- `AI Chat`: conversation workspace and Knowledge Base access
- `Field Guide`: product documentation and learning material
- `Control Room`: system operations, App Dock actions, downloads, settings, and runtime health

### Supporting Product Concepts

- `App Dock`: app install and runtime lifecycle management
- `Library Explorer`: remote and curated content discovery
- `Library Shelf`: installed content management
- `Releases`: product and app update awareness

## 12. App Framework Requirements

The app framework must support:

- app manifests with stable required sections
- catalog sync from disk
- dependency-aware installation order
- lifecycle hooks for specialized behavior
- per-app smoke tests
- app-specific docs and launch metadata

Every app definition must declare at least:

- identity and display metadata
- runtime image and ports
- mounts and storage requirements
- dependency list
- healthcheck contract
- update strategy
- permissions and capabilities
- docs and tests references

## 13. Release Acceptance

Atlas Haven should be considered release-ready for a given milestone only when:

- the documented features in that milestone are implemented or clearly labeled planned
- API behavior for the included domains is documented and test-backed
- user guides exist for each major operator workflow in the milestone
- developer docs exist for the affected architecture and extension points
- all core apps in scope are represented in the feature and developer docs

## 14. Open Product Constraints

- The platform remains single-operator and local-first unless explicitly re-scoped.
- Docker socket orchestration remains part of the runtime model.
- MySQL and Redis remain the base stateful services for the rewrite.
- Root repo planning docs remain historical and strategic; rewrite product docs live here.

## 15. Reference Inputs

This PRD is normalized from the following active inputs:

- rewrite architecture docs in `atlas-haven/docs/architecture/`
- module notes in `atlas-haven/docs/modules/`
- brand package in the root repo docs
- rebuild generation plans in the root repo docs
- the compatibility-first API draft
- current app manifests under `atlas-haven/apps/`
