# Atlas Haven API Overview

- Status: Current + Planned
- Audience: Maintainers, integrators, QA
- Source of truth: Rewrite API reference overview
- Related modules/features: all backend modules, OpenAPI contract

## Purpose

The Atlas Haven API is the backend contract for the rewrite. It preserves the
existing `/api/*` shape where practical while normalizing the product language
around Atlas Haven.

## API Design Goals

- local-first compatibility
- stable operator workflows
- explicit domain boundaries
- straightforward mapping between frontend features and backend routes

## Current Domain Groups

- Health
- Easy Setup
- Content Updates
- Maps
- Docs
- Downloads
- Ollama
- Chat Sessions
- Knowledge Base
- System
- ZIM
- Benchmark

## Main References

- canonical YAML: [`atlas-haven-api.yaml`](./atlas-haven-api.yaml)
- domain map: [`endpoint-domain-map.md`](./endpoint-domain-map.md)

## Current Implementation Note

The rewrite has active implementations for many domains but not yet all end-state
parity routes. The YAML remains the broader contract the product is moving
toward.
