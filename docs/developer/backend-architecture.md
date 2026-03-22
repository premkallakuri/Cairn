# Backend Architecture

- Status: Current + Planned
- Audience: Maintainers
- Source of truth: Backend structure and responsibility reference
- Related modules/features: FastAPI app, platform modules, worker

## Stack

- FastAPI
- Pydantic v2 and pydantic-settings
- SQLAlchemy 2.x
- ARQ
- MySQL in containerized runtime, SQLite in some local tests
- Redis for worker support

## Application Composition

The FastAPI app is created in `backend/app/main.py`. On startup it:

- loads settings
- configures logging
- initializes the DB session factory
- creates DB tables
- syncs the catalog from disk
- registers API routers

## Current Module Families

- `platform_core`: health, system info, service actions
- `catalog`: manifest parsing, sync, validation
- `orchestration`: app lifecycle orchestration and hooks
- `downloads`: durable download jobs and worker execution
- `easy_setup`: setup drafts and planning
- `zim`: local and remote library workflows
- `maps`: map metadata and styles
- `ollama`: model/runtime APIs
- `chat`: session and message workflows
- `knowledge_base`: uploads, indexing, retrieval
- `docs`: docs listing
- `benchmark`: planned parity area

## Design Rules

- keep domain logic inside module service layers
- expose behavior through typed schemas and routes
- avoid direct cross-module coupling except through public service boundaries
- make module behavior testable outside the full runtime

## Planned Evolution

- fuller benchmark module delivery
- stronger dashboard aggregation layer
- deeper settings and update domains
- more explicit migration strategy as parity closes
