# Kiwix And ZIM

- Status: Current + Planned
- Audience: Operators, knowledge users, maintainers
- Source of truth: Feature definition for offline reference serving and ZIM management
- Related modules/features: `M07`, `zim`, `nomad_kiwix_server`, library workflows

## Purpose

This feature family covers the end-to-end offline library workflow:

- discover content
- select curated Wikipedia bundles
- store local ZIM files
- serve them through Kiwix

## Current State

- bundled demo Wikipedia can be selected and seeded locally
- local ZIM inventory is supported
- Kiwix installs through the app framework and serves content from `storage/zim`
- curated categories and remote listing APIs exist for broader content workflows

## Planned State

- fuller remote explorer UX
- better replacement and upgrade workflows for library bundles
- richer local metadata and indexing
- stronger operator diagnostics for failed downloads or invalid ZIM files

## API Surface

- `GET /api/zim/list`
- `GET /api/zim/list-remote`
- `GET /api/zim/curated-categories`
- `POST /api/zim/download-remote`
- `POST /api/zim/download-category-tier`
- `GET /api/zim/wikipedia`
- `POST /api/zim/wikipedia/select`
- `DELETE /api/zim/{filename}`

## Dependencies And Storage

- `storage/zim`
- bundled `install/wikipedia_en_100_mini_2025-06.zim`
- Kiwix app package preinstall behavior

## Failure Modes

- invalid file placement prevents Kiwix from serving the library
- stale selection state can point at content that no longer exists
- large remote downloads can fail or stall without clear operator visibility

## Acceptance Criteria

- bundled demo Wikipedia must remain a reliable first-run path
- Kiwix must be able to serve local ZIM content from host-backed storage
- operators must be able to distinguish selection state, installed files, and remote availability
