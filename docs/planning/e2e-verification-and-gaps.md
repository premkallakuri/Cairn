# E2E Verification And Feature Gaps

- Status: Verification run record
- Audience: Maintainers, QA, release planners
- Related: [`completed-features.md`](completed-features.md), [`../prd/atlas-haven-prd.md`](../prd/atlas-haven-prd.md), [`../prd/requirements-matrix.md`](../prd/requirements-matrix.md), [`next-wave-sequencing.md`](next-wave-sequencing.md)

## 1. Verification run (2026-03-20)

| Field | Value |
| --- | --- |
| Date | 2026-03-20 |
| Git commit | Not a git checkout in this workspace |
| OS | darwin (macOS), Docker Desktop |
| Parent layout | `project-nomad-2026/` contains `collections/`, `install/sidecar-disk-collector/`, `.docker/`, `storage/` — compose path assumptions satisfied |

### 1.1 Compose full stack (`docker compose up`)

- `make docker-config`: **passed**
- `docker compose -f compose.yaml up -d --build`: **mysql**, **redis**, and **disk-collector** started; **api**, **worker**, and **web** **exited**
- **api/worker failure**: bind-mounted `./backend` plus image `uv sync` recreating `.venv` hit `failed to remove file .../CACHEDIR.TAG` (host/container venv conflict on the same mount)
- **web** depended on healthy api and exited as a consequence

**Implication:** documented “full compose” E2E is currently fragile when the backend directory is bind-mounted with an existing host `.venv`. Mitigations to consider (future work): anonymous/named volume for `.venv` inside the api/worker image, or `.dockerignore`/mount excludes for `.venv`, or non-mounted backend in CI.

### 1.2 Alternate stack used for UI + API probes

To complete browser and HTTP checks without fixing compose in this pass:

- **MySQL** and **Redis** left running from compose (ports **3307** / **6380**)
- **API** on host: `uvicorn` with `ATLAS_HAVEN_DATABASE_URL=sqlite+pysqlite:////tmp/atlas_e2e.db`, `ATLAS_HAVEN_REDIS_URL=redis://127.0.0.1:6380/0`, storage and collections paths pointing at the parent repo
- **Next.js** on host: `pnpm dev` with `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`

This is **not** identical to production compose (SQLite vs MySQL) but validates API routes and the shell against a live backend.

### 1.3 Bootstrap note

- `make bootstrap` initially failed on **frozen lockfile** vs `package.json` (`lucide-react`). Ran `pnpm install --no-frozen-lockfile` in `frontend/`; **`pnpm-lock.yaml` updated** — commit with other changes when ready.

## 2. Automated test results

| Layer | Command | Result |
| --- | --- | --- |
| Unit | `make test-unit` | **53 passed** |
| Contract | `make test-contract` | **2 passed** |
| Integration | `make test-integration` | **34 passed** |
| Smoke M00–M14 | `make smoke MODULE=M00` … `M14` (after fix below) | **all passed** |
| Smoke all modules | `make smoke-all-modules` or `./ops/scripts/smoke.sh all-modules` | **available** (runs M00→M14 sequentially) |
| Playwright | `cd frontend && pnpm test:e2e` (with web on :3000) | **1 passed** |

### 2.1 Fixes applied during this verification

- [`../../apps/maps/tests/test_smoke.py`](../../apps/maps/tests/test_smoke.py): initialize SQLite session factory before `MapService.download_remote()` (was raising `Session factory has not been initialized`).
- [`../../frontend/tests/e2e/navigation.spec.ts`](../../frontend/tests/e2e/navigation.spec.ts): scope nav assertions to `getByRole("navigation")` to avoid strict-mode collisions with duplicate “Bridge” text on the page.

### 2.2 Playwright coverage gap

Only **top-level nav links** on `/` are asserted. There are **no** automated UI tests yet for Easy Setup, App Dock lifecycle, chat send, KB upload, Control Room lanes, or benchmark runs.

## 3. Manual / API spot checks (host stack)

Probed with **GET** where applicable (`http://127.0.0.1:8000/api`):

| Path | HTTP | Notes |
| --- | --- | --- |
| `/health` | 200 | |
| `/system/info` | 200 | |
| `/docs/list` | 200 | Field Guide backing |
| `/system/services` | 200 | Catalog / App Dock |
| `/easy-setup/draft` | 200 | Easy Setup |
| `/zim/list` | 200 | (not `/zim/files`) |
| `/maps/curated-collections` | 200 | (not `/maps/collections`) |
| `/ollama/installed-models` | 200 | |
| `/chat/sessions` | 200 | |
| `/rag/files` | 200 | Knowledge Base |
| `/downloads/jobs` | 200 | |
| `/benchmark/results/latest` | 200 | (not `/benchmark/latest`) |
| `/system/latest-version` | 200 | |

**Not exercised in browser here:** install/start/stop Docker apps, Ollama model pull, Kiwix reader UX, map viewer interactions, streaming chat UX — treat as **operator manual** follow-up on a healthy compose or host+Docker socket setup.

## 4. Requirement × status matrix (R-001–R-015)

Legend: **Shipped** = usable for the current wave per [`completed-features.md`](completed-features.md). **Partial** = delivered but parity/docs/tests still planned. **Gap** = PRD / next-wave items not yet primary focus.

| ID | Status | Completed / verified (this run + docs) | Missing or partial (product intent) |
| --- | --- | --- | --- |
| R-001 | Partial | Shell + nav; `/health`, `/system/info`, `/docs/list` OK | Fuller system settings, operational parity |
| R-002 | Shipped | `/system/services` OK; catalog sync in codebase | — |
| R-003 | Partial | Install/start/stop/update APIs + M12 coverage | Richer per-app detail, diagnostics, release parity |
| R-004 | Partial | Draft + plan APIs (M06) | **Full one-click plan execution** |
| R-005 | Shipped | Manifests, seed paths, zim/wikipedia in product | Content **update** parity (next wave) |
| R-006 | Partial | `/zim/list`, curated flows, demo seed | Remote explorer UX, replacement/update flows |
| R-007 | Partial | `/maps/curated-collections`, PMTiles, styles | **Remote acquisition**, viewer/base-asset maturity |
| R-008 | Shipped | `/ollama/installed-models`, M09 | Simplified runtime metadata vs full live parity |
| R-009 | Shipped | `/chat/sessions`, M10 | Richer streaming/citation UX |
| R-010 | Shipped | `/rag/files`, M11 | Broader formats, indexing diagnostics |
| R-011 | Partial | `/downloads/jobs` OK | History, richer event streaming |
| R-012 | Partial | `/system/latest-version` OK | **Settings persistence**, coherent update UX, troubleshooting |
| R-013 | Partial | `/benchmark/*`, M13, persisted results | Worker-driven long runs, comparison/interpretation UX |
| R-014 | Shipped | `/docs/list` OK | — |
| R-015 | Partial | M14 scaffold + hooks + sample app | App-author docs polish, runtime polish per app |

Canonical **module → capability** inventory remains [`completed-features.md`](completed-features.md) (M00–M14).

## 5. Completed feature map (summary)

Aligned with [`completed-features.md`](completed-features.md):

- **M00–M01:** Bootstrap, platform core, health
- **M02–M03:** Catalog, orchestration
- **M04:** Shell, dashboard, Field Guide route, docs routes
- **M05:** Downloads and jobs
- **M06:** Easy Setup planning (execution partial)
- **M07:** Kiwix / ZIM
- **M08:** Maps (partial — acquisition/viewer parity)
- **M09:** Ollama / Qdrant
- **M10:** Chat
- **M11:** Knowledge Base / RAG
- **M12:** App Dock day-one apps
- **M13:** Benchmarks (worker/UX partial)
- **M14:** Extensibility / scaffolder

**Apps (from completed-features app matrix):** Kiwix, Qdrant, Ollama, FlatNotes, CyberChef, Kolibri, Benchmark Helper, Sample Notes **shipped** for the wave; **Atlas Maps** **partial**.

## 6. Recommended next tests (priority)

1. **Compose CI job** with non-conflicting backend venv strategy so `api`/`web` smoke starts in Docker.
2. **Playwright:** Control Room loads jobs list; Easy Setup draft round-trip; App Dock list from `/system/services` reflected in UI; chat create session + send (mock Ollama if needed).
3. **Contract tests:** add explicit routes for `/zim/list`, `/maps/curated-collections`, `/benchmark/results/latest` if OpenAPI should document them verbatim (avoid wrong path assumptions).
4. **Makefile / CI:** call `make smoke-all-modules` on release candidates.

## 7. Doc / tooling updates in this pass

- [`../../ops/scripts/smoke.sh`](../../ops/scripts/smoke.sh): `all-modules` runs M00–M14 sequentially.
- [`../../Makefile`](../../Makefile): `smoke-all-modules` target.
- [`../../README.md`](../../README.md): documents `make smoke-all-modules`.
- [`../prd/requirements-matrix.md`](../prd/requirements-matrix.md): R-013/R-015 module column + coverage notes refreshed for M13/M14.
