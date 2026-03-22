# Coding standards

Conventions for the Cairn / Atlas Haven monorepo. **Tooling wins:** when this doc and an automated formatter or linter disagree, fix the code to satisfy the tool (or change the tool config in a dedicated PR).

## General principles

- **Scope:** Change only what the task requires. Avoid drive-by refactors, unrelated files, and scope creep.
- **Consistency:** Match surrounding code for naming, imports, types, error handling, and documentation density. If no local pattern exists, follow idioms for Python 3.13, FastAPI, and Next.js 15.
- **Reuse:** Extend existing services, repositories, and UI components instead of duplicating behavior.
- **Comments:** Prefer clear code over noise. Do not add obvious comments, long docstrings on trivial functions, or banner comments. Keep useful existing comments when editing a file.

## Python (backend)

- **Layout:** Source lives under `backend/app/`. Tests under `backend/tests/` mirror concerns (`unit`, `integration`, `contract`).
- **Version:** Target **Python 3.13** (`backend/.python-version`). Do not rely on features that break the pinned dependency set (e.g. native wheels).
- **Formatter / linter:** [Ruff](https://docs.astral.sh/ruff/) is the source of truth:
  - Line length **100**
  - Target **py313**
  - Enabled rule sets: **E**, **F**, **I**, **UP**, **B** (see `backend/pyproject.toml`)
- **Run checks:** From repo root, `make lint-backend` or:

  ```sh
  cd backend && UV_CACHE_DIR="$PWD/.uv-cache" uv run ruff check . && uv run ruff format --check .
  ```

- **Style:**
  - Use **type hints** on public functions and non-trivial internals where they clarify intent.
  - Prefer **Pydantic** models for request/response bodies and settings (`pydantic-settings` for env).
  - Keep FastAPI routers thin; put logic in services/modules.
  - Use **`from __future__ import annotations`** where the codebase already does for forward references.
  - **SQLAlchemy 2.x** style (mapped classes, session usage consistent with `app/db/`).
- **Settings:** All app configuration goes through `get_settings()` with the **`ATLAS_HAVEN_`** env prefix; do not read unrelated env vars ad hoc in feature code.
- **Errors:** Use shared error handling (`app/core/errors.py`) and predictable HTTP status codes for new routes.

## Tests (backend)

- **Framework:** `pytest`, with **`pytest-asyncio`** where async tests are used.
- **Markers:** Use the markers defined in `backend/pyproject.toml` (`unit`, `integration`, `contract`, and domain markers like `maps`, `zim`, etc.) so suites can be filtered.
- **Conventions:**
  - **Unit:** No real network or DB unless the test explicitly mocks; fast and isolated.
  - **Integration:** `TestClient` against the ASGI app; use `backend/tests/conftest.py` fixtures for DB/storage isolation.
  - **Contract:** OpenAPI path and schema expectations—keep them stable when changing public APIs.
- **Running:** `make test-unit`, `make test-contract`, `make test-integration`, or targeted `uv run pytest path -q`.

## TypeScript / React (frontend)

- **Stack:** Next.js **App Router** (`frontend/app/`), React 19, Tailwind CSS.
- **Package manager:** **pnpm** only (no alternate lockfiles committed for the main app).
- **Typecheck:** The project treats **`tsc --noEmit`** as the primary static check (`pnpm lint` and `pnpm typecheck` both run it—see `frontend/package.json`).
- **Imports:** Use the `@/` alias as established in `frontend/tsconfig.json` for app code.
- **Components:** Follow existing patterns (`"use client"` only where needed). Keep server components the default when possible.
- **Data:** Shared API types live under `frontend/lib/types/`; client helpers under `frontend/lib/api/`. Align field names with the backend/OpenAPI surface (often camelCase in JSON).
- **Styling:** Tailwind utility classes; follow existing spacing, typography, and component patterns in `frontend/components/` and `frontend/features/`.

## API design

- **Prefixes:** New HTTP surfaces stay under the existing `/api/...` layout and `app/main.py` router mounts.
- **OpenAPI:** Tag new routes with the appropriate `openapi_tags` group when adding modules.
- **Compatibility:** Prefer additive changes (new fields, optional parameters) over breaking renames without a version or migration plan.

## Background jobs

- **Downloads:** Schedule work through the shared download/job services and ARQ worker; do not run long blocking downloads inside request handlers.
- **Redis:** Jobs assume Redis availability when enqueue is enabled; document new job types in [`background-jobs-and-workers.md`](./background-jobs-and-workers.md).

## Documentation and manifests

- **Collections:** Curated JSON under `collections/` (or `ATLAS_HAVEN_COLLECTIONS_PATH`) must remain valid for loaders in `app/shared/collections.py` and related modules.
- **User-facing docs:** Update module or architecture docs when behavior or boundaries change in a way operators or integrators would notice.

## Security and configuration

- Never commit **secrets** (API keys, passwords, private URLs). Use environment variables and local `.env` files that are gitignored.
- Validate and sanitize user-controlled paths (file names, slugs) to avoid traversal and unsafe resolution—follow existing helpers in map/ZIM modules.

## Licensing

- New files should remain compatible with the repository **MIT** license (`LICENSE`). Do not commit third-party code without license compatibility and attribution per project policy.

## Where this is enforced

| Check | Command |
|--------|---------|
| Python format/lint | `make lint-backend` |
| Frontend typecheck | `make lint-frontend` (runs `pnpm lint` + `pnpm typecheck`) |
| Full lint | `make lint` |

For workflow and repo layout, see the [developer guide](./developer-guide.md).
