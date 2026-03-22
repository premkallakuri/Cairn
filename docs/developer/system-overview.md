# Atlas Haven System Overview

- Status: Current + Planned
- Audience: Maintainers
- Source of truth: High-level system explanation for the rewrite
- Related modules/features: architecture overview, platform core, shell, app framework

## What Atlas Haven Is

Atlas Haven is a modular monolith with a manifest-driven app framework. It is
not a collection of unrelated microservices. The core platform owns the control
plane, while sibling application containers extend capability in a consistent
way.

## Core Runtime Components

- `api`: FastAPI control plane
- `worker`: ARQ-based background worker entrypoint
- `web`: Next.js App Router frontend
- `mysql`: primary relational state
- `redis`: queue/cache/event support
- `disk-collector`: sidecar for host storage inventory

## Core Architectural Ideas

- local-first storage and operation
- Docker-first deployment
- manifest-driven app discovery and lifecycle management
- stable `/api/*` contract for the rewrite
- task-oriented shell for operators
- explicit distinction between delivered and planned parity

## Current Delivered Feature Slices

- bootstrap and health
- catalog sync
- app lifecycle primitives
- shell and dashboard
- downloads and jobs
- Easy Setup
- Kiwix and ZIM
- maps
- Ollama and Qdrant
- chat
- Knowledge Base
- app roundout for FlatNotes, CyberChef, and Kolibri

## Planned Growth Areas

- richer benchmark workflows
- extension scaffolding
- deeper system settings and release/update parity
- stronger restore, diagnostics, and failure recovery tooling
