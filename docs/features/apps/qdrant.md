# Qdrant App Package

- Status: Current + Planned
- Audience: Maintainers, app authors, operators
- Source of truth: App package specification for `nomad_qdrant`
- Related modules/features: `M09`, Knowledge Base, AI workflows

## Why It Exists

Qdrant is the vector-store dependency for retrieval and semantic workflows in the
Atlas Haven AI stack.

## Current Package Contract

- Service ID: `nomad_qdrant`
- Kind: `dependency_app`
- Image: `qdrant/qdrant:v1.13.4`
- Port mapping: `6333 -> 6333`
- Mount: `${NOMAD_STORAGE_PATH}/qdrant -> /qdrant/storage`
- Healthcheck: `GET /healthz`

## Operator-Visible Behavior

- appears in App Dock as `Qdrant Vector Store`
- is installed automatically when needed by Ollama-dependent flows
- exposes launch URL `http://127.0.0.1:6333`

## Planned Evolution

- deeper diagnostics for vector state and collection visibility
- stronger KB-specific health reporting

## Acceptance Criteria

- dependency-aware installs must bring Qdrant up when required
- app status and version must be visible in App Dock
