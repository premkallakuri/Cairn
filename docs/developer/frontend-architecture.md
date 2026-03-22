# Frontend Architecture

- Status: Current + Planned
- Audience: Maintainers, frontend contributors
- Source of truth: Frontend shell and feature composition reference
- Related modules/features: AppShell, feature modules, API client

## Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- React 19 client/server component mix
- Playwright for E2E validation

## Shell Model

The frontend uses one shared shell with top-level destinations:

- `Bridge`
- `Atlas Maps`
- `AI Chat`
- `Field Guide`
- `Control Room`

## Feature Organization

Each feature lives under `frontend/features/<feature>/` and should export through
its own `index.tsx` surface. Current features include:

- `bridge`
- `app_dock`
- `control_room`
- `easy_setup`
- `maps`
- `chat`
- `field_guide`
- `benchmark`

## Data Flow

- route entrypoints load initial server data through `frontend/lib/api/client.ts`
- feature modules render current state and client interactions
- typed API shapes live under `frontend/lib/types`

## Design Rules

- keep feature UI isolated by domain
- keep route files thin and data-loading focused
- prefer API-client abstractions over raw fetches in feature code
- preserve Atlas Haven brand language in UI labels and docs

## Planned Evolution

- richer server/client boundary optimization
- stronger live event handling for jobs and long-running operations
- deeper component library reuse as the shell grows
