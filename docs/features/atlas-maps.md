# Atlas Maps

- Status: Current + Planned
- Audience: Operators, map users, maintainers
- Source of truth: Feature definition for offline maps workflows
- Related modules/features: `M08`, `maps`, `downloads`, `nomad_maps`

## Purpose

Atlas Maps provides built-in offline map capability using local PMTiles data and
MapLibre-compatible style generation. It gives Atlas Haven a native geographic
workflow rather than outsourcing maps to a separate sibling app.

## Current State

- maps exist as a built-in core capability package
- the rewrite can enumerate region files and curated collections
- base styles can be generated for local rendering
- the frontend exposes an Atlas Maps route and collection visibility

## Planned State

- complete remote map acquisition flows
- base asset bootstrap and validation workflows
- richer regional search, coverage summaries, and install diagnostics
- stronger style customization and map-layer control

## API Surface

- `GET /api/maps/regions`
- `GET /api/maps/styles`
- `GET /api/maps/curated-collections`
- `POST /api/maps/fetch-latest-collections`
- `POST /api/maps/download-base-assets`
- `POST /api/maps/download-remote`
- `POST /api/maps/download-remote-preflight`
- `POST /api/maps/download-collection`
- `DELETE /api/maps/{filename}`

## Dependencies And Storage

- `storage/maps`
- `storage/maps/pmtiles`
- base style assets
- durable download job tracking for large map pulls

## Failure Modes

- missing base assets can prevent viewer initialization
- incomplete PMTiles downloads can create partially visible regions
- stale curated collection metadata can hide available resources

## Acceptance Criteria

- Atlas Maps must remain a first-class top-level destination
- local map files and curated collections must be discoverable
- the platform must clearly distinguish built-in map behavior from downloadable region data
