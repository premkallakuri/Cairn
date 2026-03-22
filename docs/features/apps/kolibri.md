# Kolibri App Package

- Status: Current + Planned
- Audience: Operators, educators, app authors
- Source of truth: App package specification for `nomad_kolibri`
- Related modules/features: `M12`, education use cases

## Why It Exists

Kolibri brings an offline education platform into the Atlas Haven catalog for
classroom, lab, and study-oriented deployments.

## Current Package Contract

- Service ID: `nomad_kolibri`
- Kind: `sibling_app`
- Image: `learningequality/kolibri:latest`
- Port mapping: `8085 -> 8080`
- Mount: `${NOMAD_STORAGE_PATH}/kolibri -> /kolibrihome`
- Healthcheck: HTTP on port `8080`

## Operator-Visible Behavior

- appears in App Dock and Bridge-oriented application surfaces
- exposes launch URL `http://127.0.0.1:8085`
- persists data in host-backed storage

## Planned Evolution

- richer education-focused onboarding and content guidance

## Acceptance Criteria

- Kolibri must install, launch, and survive restart/reinstall through App Dock
