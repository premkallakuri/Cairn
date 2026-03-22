# Atlas Maps Capability Package

- Status: Current + Planned
- Audience: Maintainers, app authors, operators
- Source of truth: App package specification for `nomad_maps`
- Related modules/features: `M08`, Atlas Maps

## Why It Exists

Atlas Maps is treated as a core capability package so it can participate in the
same catalog and App Dock vocabulary while remaining a built-in platform feature.

## Current Package Contract

- Service ID: `nomad_maps`
- Kind: `core_capability`
- Image: `builtin://atlas-haven/maps`
- Built-in runtime rather than a sibling image-backed container
- Mount: `${NOMAD_STORAGE_PATH}/maps -> /workspace/storage/maps`
- Health target: `atlas-haven://maps`

## Operator-Visible Behavior

- appears in App Dock and Bridge-oriented surfaces
- launches at `http://127.0.0.1:3000/maps`
- uses the same install/status vocabulary as other capabilities

## Planned Evolution

- tighter integration between capability state and actual map asset readiness

## Acceptance Criteria

- Atlas Maps must remain manageable through the same catalog-driven framework
- built-in capability semantics must stay understandable to operators
