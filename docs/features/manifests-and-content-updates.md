# Manifests And Content Updates

- Status: Current + Planned
- Audience: Maintainers, operators, app authors
- Source of truth: Feature definition for bundled manifest data and content update workflows
- Related modules/features: `M02`, `M06`, `M07`, manifest sync, content updates

## Purpose

This feature family governs how Atlas Haven knows what content and app metadata
exist. It includes local-first manifest data, curated collection metadata, and
future update flows for content packages.

## Current State

- manifest and curated content data are bundled locally rather than pulled from GitHub
- catalog sync reads app package manifests from disk
- Easy Setup and library workflows consume local manifest data
- manifest refresh now copies bundled collection files into local content-manifest cache
- content update checks now compare installed map and ZIM versions against bundled manifests
- single and batch content update apply routes now queue download jobs

## Planned State

- better metadata normalization and source attribution
- clearer distinction between bundled, cached, and remote-only metadata
- richer UI messaging in maps and library pages
- stronger failure and retry behavior for queued content updates

## API Surface

- `POST /api/manifests/refresh`
- `POST /api/content-updates/check`
- `POST /api/content-updates/apply`
- `POST /api/content-updates/apply-all`

## Dependencies And Storage

- local manifest files under `collections/`
- app manifests under `apps/*/app.yaml`
- cached content metadata and update state under `storage/content-manifests`
- download job persistence under the shared downloads domain

## Failure Modes

- stale bundled metadata can hide new resources
- inconsistent metadata can produce incorrect storage estimates or availability states
- batch updates can partially succeed and require clear reporting
- installed filenames that do not follow expected version naming conventions may not produce update matches cleanly

## Acceptance Criteria

- first-run Atlas Haven must remain useful from bundled metadata alone
- update workflows are now documented and testable for the supported map and ZIM domains
- app framework docs must align with actual manifest requirements
