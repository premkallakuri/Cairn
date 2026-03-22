# System Settings And Releases

- Status: Current + Planned
- Audience: Operators, maintainers
- Source of truth: Feature definition for runtime settings, release awareness, and maintenance
- Related modules/features: `platform_core`, `M01`, `M12`, planned parity work

## Purpose

This feature family covers machine and runtime information, system settings,
service update awareness, and future Atlas Haven release management flows.

## Current State

- system info is available through the API and Control Room
- app-level update checks exist through App Dock
- latest-version responses are local-first in the repo-wide local distribution work
- service versions and launch URLs are surfaced for current app packages
- internet reachability, system update status, update logs, and release-note subscription routes exist
- persisted system settings are available through `GET/PATCH /api/system/settings`
- Control Room now surfaces bundled-version and update-lane state

## Planned State

- backup, restore, and storage maintenance views
- deeper release/update workflows beyond the current local-first bundled distribution behavior
- richer settings UX beyond the current API and Control Room baseline

## API Surface

- `GET /api/system/info`
- `GET /api/system/internet-status`
- `GET /api/system/services`
- `POST /api/system/services/check-updates`
- `GET /api/system/latest-version`
- `POST /api/system/update`
- `GET /api/system/update/status`
- `GET /api/system/update/logs`
- `GET /api/system/settings`
- `PATCH /api/system/settings`
- `POST /api/system/subscribe-release-notes`

## Dependencies And Storage

- platform settings persistence under local storage
- service catalog and version metadata
- local update status and log persistence under storage/system

## Failure Modes

- mismatched version metadata can confuse update decisions
- partial settings persistence can create disagreement between UI and runtime behavior
- release status without logs or diagnostics can make recovery difficult

## Acceptance Criteria

- operators must have a clear runtime status and service-update view
- current settings and release behavior must align with the API contract and product terminology
- future parity work should deepen recovery, restore, and release automation without changing the local-first model unexpectedly
