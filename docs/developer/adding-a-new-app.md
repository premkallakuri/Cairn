# Adding A New App

- Status: Current + Planned
- Audience: App authors, maintainers
- Source of truth: App author workflow guide
- Related modules/features: app framework, catalog, App Dock

## Goal

Add a new Atlas Haven app without editing core orchestration behavior unless the
new app introduces a genuinely new capability class.

## Current Workflow

1. Create `apps/<app-id>/`.
2. Add `app.yaml` with the required manifest fields.
3. Add `docs/overview.md` describing the package.
4. Add `tests/test_smoke.py` to validate install behavior.
5. Add `hooks.py` only if lifecycle customization is necessary.
6. Start the backend so catalog sync can discover the package.
7. Confirm the app appears in `App Dock`.

## Authoring Rules

- choose a stable `id` using the `nomad_` naming pattern already in use
- declare all mounts and ports explicitly
- keep app storage under the shared Atlas Haven storage root
- document whether the app is a sibling app, dependency app, or built-in capability
- make smoke tests assert installability and, when possible, launch URL behavior

## When Core Changes Are Acceptable

Core framework changes should only be required when:

- a new app kind is introduced
- orchestration needs a new lifecycle semantic
- the app requires framework-level capability that cannot be expressed by current hooks

## Planned Evolution

- scaffold CLI support
- stronger app manifest linting
- generated docs/test templates
