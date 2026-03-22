# Library Explorer

- Status: Current + Planned
- Audience: Operators, knowledge users
- Source of truth: Feature definition for curated and remote content discovery
- Related modules/features: `M06`, `M07`, `zim`, `easy_setup`, manifests

## Purpose

Library Explorer is the discovery surface for content that is not yet installed.
It helps users decide what to bring onto the device, especially ZIM-based
reference content and future curated datasets.

## Current State

- partially represented through Easy Setup curated categories
- partially represented through ZIM remote and Wikipedia selection APIs
- bundled manifests provide local-first curated discovery without requiring GitHub

## Planned State

- a clearer standalone discovery experience in the product UI
- richer metadata such as language, size, update age, and recommended use
- direct transition from discovery to install/download

## API Surface

- `GET /api/easy-setup/curated-categories`
- `GET /api/zim/curated-categories`
- `GET /api/zim/list-remote`
- `GET /api/zim/wikipedia`
- `POST /api/manifests/refresh`

## Dependencies And Storage

- bundled collection manifests
- remote catalog metadata when network access is available
- no primary storage ownership beyond cached metadata

## Failure Modes

- stale manifests can misrepresent availability
- remote source errors can make discovery incomplete
- confusing distinction between curated tiers and direct remote files can overwhelm new users

## Acceptance Criteria

- users must be able to discover not-yet-installed library resources from curated data
- bundled data must remain sufficient for first-run discovery
- explorer terminology must align with `Library Shelf`
