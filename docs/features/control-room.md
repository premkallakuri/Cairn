# Control Room

- Status: Current + Planned
- Audience: Operators, maintainers
- Source of truth: Feature definition for system operations and runtime management
- Related modules/features: `M04`, `M05`, `M12`, `platform_core`, `downloads`

## Purpose

Control Room is the operations console for Atlas Haven. It centralizes system
state, app operations, download activity, and future release and maintenance
workflows.

## Current State

- Displays environment, catalog entry count, and workspace root.
- Hosts the full `App Dock` operations panel.
- Shows download activity cards with progress state from the downloads module.
- Acts as the closest current equivalent to a system management center.

## Planned State

- add system settings editors
- add release and update status panels
- add richer storage, disk, and maintenance views
- add repair flows, job history, and benchmark visibility

## Entry Points

- top navigation `Control Room`
- links from Bridge and future system warning banners

## API Surface

- `GET /api/system/info`
- `GET /api/system/services`
- `GET /api/downloads/jobs`
- future parity paths under `/api/system/*`, `/api/benchmark/*`, and update/status routes

## Dependencies And Storage

- depends on system info and service catalog state
- depends on durable download job storage
- planned future dependence on settings and benchmark persistence

## Failure Modes

- stale download state can mislead operators during long-running content pulls
- incomplete system info reduces confidence in runtime status
- partial app lifecycle state can cause apparent disagreement between App Dock and actual container state

## Acceptance Criteria

- Control Room must render even if no jobs are active
- App Dock operations must be accessible from this page
- system summary information must be readable without developer knowledge
