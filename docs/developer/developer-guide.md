# Developer guide

Hands-on setup and daily workflow for the Cairn / Atlas Haven monorepo (FastAPI backend, Next.js frontend, ARQ workers). For style and review expectations, see [coding standards](./coding-standards.md). For architecture deep-dives, use the [developer documentation index](./README.md).

## Prerequisites

| Tool | Role |
|------|------|
| [uv](https://docs.astral.sh/uv/) | Python deps and virtualenv for `backend/` |
| [pnpm](https://pnpm.io/) | Frontend package manager (`frontend/`) |
| Node.js 20+ | Next.js build and dev server |
| Redis | Required for download jobs (ARQ). Use Docker, Homebrew, or your OS package manager |
| [Ollama](https://ollama.com/) (optional) | Local LLM pull and chat when exercising `/api/ollama` |

The backend pins **Python 3.13** (see `backend/.python-version`) so native wheels such as `aura-memory` stay compatible.

## First-time setup

From the repository root:

```sh
make bootstrap
```

This runs `uv sync` in `backend/` (with `UV_CACHE_DIR` under `backend/.uv-cache`) and `pnpm install` in `frontend/`.

## Run the stack locally

You typically need **three processes**: API, ARQ worker (for downloads), and the Next.js dev server.

### 1. Redis

Downloads are queued to ARQ; the worker consumes Redis. Example:

```sh
docker run -d --name cairn-redis -p 6379:6379 redis:7.4-alpine
```

Default URL: `redis://127.0.0.1:6379/0` (`ATLAS_HAVEN_REDIS_URL`).

### 2. Backend API

```sh
cd backend
UV_CACHE_DIR="$PWD/.uv-cache" uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

SQLite is the default database (`ATLAS_HAVEN_DATABASE_URL`). The DB file is created relative to the process working directory unless you override the URL.

### 3. Download worker

```sh
cd backend
UV_CACHE_DIR="$PWD/.uv-cache" uv run python -m app.shared.worker
```

### 4. Frontend

```sh
cd frontend
pnpm dev --port 3000
```

The UI calls the API using `NEXT_PUBLIC_API_BASE_URL` when set; otherwise it defaults to `http://127.0.0.1:8000` (see `frontend/lib/api/client.ts`).

### Optional: seed demo content

`ops/setup-local-content.sh` queues Wikipedia ZIM selection, map base assets, and an Ollama model registration flow. Set `CAIRN_API_BASE` if the API is not on `http://127.0.0.1:8000`. For an extra PMTiles region, set `CAIRN_PMTILES_URL` to an HTTPS URL whose path ends in `.pmtiles`.

## Environment variables

All backend settings use the `ATLAS_HAVEN_` prefix. Common overrides:

| Variable | Purpose |
|----------|---------|
| `ATLAS_HAVEN_DATABASE_URL` | SQLAlchemy URL (default: SQLite in cwd) |
| `ATLAS_HAVEN_REDIS_URL` | Redis for ARQ |
| `ATLAS_HAVEN_STORAGE_PATH` | Root for ZIM, maps, RAG files, Ollama registry, etc. |
| `ATLAS_HAVEN_COLLECTIONS_PATH` | Directory containing `wikipedia.json`, `maps.json`, `kiwix-categories.json` (default: `collections/` under the repo root) |
| `ATLAS_HAVEN_FRONTEND_API_BASE_URL` | Base URL embedded in generated map style URLs |
| `ATLAS_HAVEN_OLLAMA_BASE_URL` | Ollama HTTP API (default `http://127.0.0.1:11434`) |
| `ATLAS_HAVEN_ENQUEUE_DOWNLOAD_WORKER_JOBS` | Set to `0` to skip ARQ enqueue (used in automated tests) |

Tests set additional variables via `backend/tests/conftest.py` (isolated DB and storage).

## Repository layout (short)

| Path | Contents |
|------|----------|
| `backend/` | FastAPI app, ARQ worker, pytest suites |
| `frontend/` | Next.js App Router UI |
| `collections/` | Curated manifests (Wikipedia options, map collections, Kiwix categories) |
| `ops/` | Scripts (e.g. local content setup) |
| `compose.yaml` | Docker Compose stack (API, worker, web, MySQL, Redis) |

More detail: [repo-structure.md](./repo-structure.md).

## Testing and quality

```sh
make lint
make test-unit
make test-contract
make test-integration
```

Module-scoped tests and smoke scripts: `make test-module MODULE=Mxx`, `make smoke MODULE=Mxx`.

See [testing-and-quality-gates.md](./testing-and-quality-gates.md) and [coding-standards.md](./coding-standards.md) (Ruff, TypeScript, pytest markers).

## Docker

Validate Compose configuration:

```sh
make docker-config
```

Full stack definition and volume mounts: [docker-runtime-topology.md](./docker-runtime-topology.md) and `compose.yaml`.

## Where to read next

1. [system-overview.md](./system-overview.md) — product and control-plane context  
2. [backend-architecture.md](./backend-architecture.md) / [frontend-architecture.md](./frontend-architecture.md)  
3. [background-jobs-and-workers.md](./background-jobs-and-workers.md) — ARQ and downloads  
4. [adding-a-new-app.md](./adding-a-new-app.md) — manifest-driven apps  

License: see `LICENSE` at the repository root.
