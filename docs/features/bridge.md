# Bridge

- Status: Current + Planned
- Audience: Operators, product owners, designers
- Source of truth: Feature definition for the Atlas Haven landing surface
- Related modules/features: `M04`, `M12`, `BridgeDashboard`, `App Dock`

## Purpose

Bridge is the main launch surface for Atlas Haven. It gives operators a concise
view of the platform: what is installed, what content is available, where to go
next, and what actions matter most right now.

## Current State

- Implemented as the `/` route in the Next.js shell.
- Displays summary cards for catalog services, curated categories, docs count,
  and runtime version.
- Includes a direct CTA into Easy Setup.
- Embeds an `App Dock` panel preview showing app state, launch links, and basic actions.

## Planned State

- Add richer contextual alerts for storage, failed jobs, and pending updates.
- Add role-oriented quick starts such as research, education, or preparedness.
- Add recent activity, last-used content, and recommended next actions.

## Primary UX Flow

1. User opens Atlas Haven and lands on Bridge.
2. User understands the overall platform state in one screen.
3. User branches into Easy Setup, App Dock, Atlas Maps, AI Chat, or Field Guide.

## Entry Points

- top navigation `Bridge`
- first route after opening the web UI

## API Surface

- `GET /api/system/services`
- `GET /api/docs/list`
- `GET /api/easy-setup/curated-categories`
- `GET /api/system/info`

## Dependencies And Storage

- depends on catalog sync and service state
- depends on docs index visibility
- does not own storage directly

## Failure Modes

- if catalog sync fails, service summaries will be incomplete
- if docs indexing fails, the docs count or summaries will be stale
- if system info fails, runtime version visibility is reduced but the shell should still render

## Acceptance Criteria

- Bridge must render without requiring authentication
- Bridge must summarize current service, docs, and category state
- Bridge must provide a clear route to Easy Setup and App Dock operations
