# App Dock

- Status: Current + Planned
- Audience: Operators, maintainers, app authors
- Source of truth: Feature definition for app lifecycle management
- Related modules/features: `M02`, `M03`, `M12`, `platform_core`, `catalog`, `orchestration`

## Purpose

App Dock is the operator-facing surface for discovering, installing, launching,
updating, and repairing manifest-driven apps. It turns manifest metadata and
orchestration behavior into a plain-language management workflow.

## Current State

- Lists cataloged services with friendly name, description, type, status, and version.
- Shows launch URLs derived from manifest ports or built-in routes.
- Supports install, start, stop, restart, force reinstall, load versions, check updates, and apply update.
- Covers Kiwix, Qdrant, Ollama, FlatNotes, CyberChef, Kolibri, Atlas Maps, and Benchmark Helper.
- Available on Bridge as a preview and in Control Room as the primary operations surface.

## Planned State

- add per-service detail pages with logs, dependency graphs, and health history
- add clearer rollback and recovery messaging
- add storage impact previews before install/update
- add grouped filters by app type, status, and capability

## UX Model

Each app card should surface:

- what the app is
- whether it is available, running, stopped, or mid-operation
- where it launches
- whether an update is available
- what the operator can do next

## API Surface

- `GET /api/system/services`
- `POST /api/system/services/install`
- `POST /api/system/services/affect`
- `POST /api/system/services/force-reinstall`
- `POST /api/system/services/check-updates`
- `GET /api/system/services/{name}/available-versions`
- `POST /api/system/services/update`

## Dependencies And Storage

- catalog records in the database
- manifest files under `apps/*/app.yaml`
- host-backed storage declared by each app manifest
- orchestration layer that applies lifecycle state transitions

## Failure Modes

- invalid manifests can hide apps or block lifecycle actions
- dependency resolution failures prevent install completion
- bad image tags or update metadata can misrepresent version state
- storage or mount issues can make an app appear installed but unusable

## Acceptance Criteria

- every current app package must appear in App Dock
- lifecycle actions must match the supported app contract
- app cards must show launch information when a UI endpoint exists
- update and reinstall actions must be understandable without Docker CLI knowledge
