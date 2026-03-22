# Background Jobs And Workers

- Status: Current + Planned
- Audience: Maintainers
- Source of truth: Async execution model reference
- Related modules/features: downloads, worker, planned benchmark/update jobs

## Current Worker Model

The worker entrypoint lives in `backend/app/shared/worker.py`. It:

- loads settings
- initializes the DB session factory
- creates DB tables
- runs ARQ worker settings from the downloads module

## Current Job Family

- download jobs for models, maps, and content-related transfers

## Why Jobs Exist

Jobs prevent long-running operations from living inside request handlers. They
also provide a stable progress model that the UI can inspect through Control
Room and related feature surfaces.

## Planned Job Families

- content update execution
- benchmark runs
- richer indexing or embedding work
- release/update operations

## Design Rules

- jobs must persist enough state to be operator-visible
- user-facing features should not require direct worker knowledge
- job-producing modules should use a consistent status vocabulary
