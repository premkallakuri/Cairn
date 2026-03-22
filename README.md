# Cairn

Offline AI essentials. Cairn is the Python + Next.js workspace for Project N.O.M.A.D. (Atlas Haven).

This nested monorepo preserves the current local-first Docker operating model while
moving the control plane to:

- FastAPI
- ARQ
- MySQL
- Redis
- Next.js App Router

## First Execution Wave

This initial workspace implements the first shipped rollout slice:

- `M00` Bootstrap
- `M01` Platform Core
- `M02` Catalog Core
- `M03` Orchestration Core
- `M04` Shell And Dashboard
- `M05` Downloads And Jobs
- `M06` Easy Setup
- `M07` Kiwix And ZIM
- `M08` Maps
- `M09` Ollama And Qdrant
- `M10` Chat
- `M11` Knowledge Base
- `M12` App Roundout
- `M13` Benchmark
- `M14` Extensibility

## Commands

```sh
make bootstrap
make test-unit
make test-contract
make test-integration
make smoke MODULE=M00
make smoke-all-modules
```

## Layout

See `docs/architecture/overview.md` for the workspace boundaries and
`docs/modules/` for the current module notes.

## Developer guide

Local setup, running the stack, environment variables, and tests:
[`docs/developer/developer-guide.md`](docs/developer/developer-guide.md).

Coding standards (Python/Ruff, TypeScript, tests, API conventions):
[`docs/developer/coding-standards.md`](docs/developer/coding-standards.md).
