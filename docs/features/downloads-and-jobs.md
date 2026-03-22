# Downloads And Jobs

- Status: Current + Planned
- Audience: Operators, maintainers
- Source of truth: Feature definition for long-running file and model transfer visibility
- Related modules/features: `M05`, downloads, maps, ZIM, Ollama

## Purpose

Downloads And Jobs provide durable tracking for long-running pulls such as maps,
models, and future content packages. The goal is to make background work visible
and survivable across retries rather than hiding it inside transient processes.

## Current State

- download job records are persisted
- progress fields are exposed through API routes
- Control Room surfaces active download state
- the same subsystem is reused by model, map, and other content workflows

## Planned State

- richer job history
- pause/resume/cancel semantics where meaningful
- broader event streaming into the UI
- standardized retry and failure explanation states

## API Surface

- `GET /api/downloads/jobs`
- `GET /api/downloads/jobs/{filetype}`

## Dependencies And Storage

- download job table in the platform database
- destination files under app/content-specific storage roots
- worker infrastructure for asynchronous execution

## Failure Modes

- stalled progress can create false confidence if jobs are not actively refreshed
- destination path issues can fail late after long transfer times
- interruptions during partial downloads can leave inconsistent local state

## Acceptance Criteria

- operators must be able to see active download progress
- job state must survive beyond a single request lifecycle
- consuming features must be able to reuse the job system consistently
