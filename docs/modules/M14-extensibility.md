# M14 Extensibility

## Scope

- Strengthen manifest validation so catalog scans fail early on malformed app packages
- Add a scaffolding workflow for creating new app packages from the existing manifest framework
- Prove the framework with a sample app package that can be catalog-scanned without touching core plumbing
- Extend orchestration hooks so app lifecycle stages can support preflight, install, start, update, rollback, and uninstall behavior

## Implemented

- Manifest shape validation for ids, docs slugs, smoke tests, hook references, storage references, and runtime ports
- Catalog scaffolder service for generating app package skeletons under `apps/`
- Shell wrapper for scaffold generation from the workspace root
- `sample-notes` example package with manifest, docs, and smoke test coverage
- Orchestration hook sequencing for `preflight`, `preinstall`, `postinstall`, `prestart`, `poststart`, `preupdate`, `rollback`, `preuninstall`, and `postuninstall`

## Notes

- The scaffold flow is intentionally opinionated: it produces a catalog-valid package first, then leaves room for app-specific details.
- The sample package is deliberately lightweight so it can act as a reference template for future app authors without adding runtime complexity.
