# Atlas Haven Repo Structure

- Status: Current + Planned
- Audience: Maintainers, app authors
- Source of truth: Workspace layout reference
- Related modules/features: backend, frontend, apps, docs, ops

## Rewrite Workspace Layout

```text
atlas-haven/
  backend/      FastAPI app, DB models, tests, worker
  frontend/     Next.js shell, features, API client, e2e tests
  apps/         Manifest-driven app packages
  docs/         Product, feature, user, and developer docs
  ops/          Compose helpers and test scripts
  tests/        Higher-level smoke and shared fixtures
```

## Backend Layout

- `app/core`: config, logging, errors
- `app/db`: engine/session/base
- `app/modules`: feature domains
- `app/shared`: shared worker and collection helpers
- `tests/unit`, `tests/contract`, `tests/integration`: test layers

## Frontend Layout

- `app/`: route entrypoints
- `components/`: shared shell components
- `features/`: feature-isolated UI modules
- `lib/api`: client wrappers for backend APIs
- `lib/types`: shared API shape definitions
- `tests/e2e`: browser tests

## App Package Layout

Each app package should contain:

- `app.yaml`
- optional `hooks.py`
- `docs/overview.md`
- `tests/test_smoke.py`

## Documentation Layout

- `architecture/`: short rewrite topology references
- `modules/`: implementation slice notes
- `prd/`, `features/`, `user-guides/`, `developer/`: authoritative product docs
