# Atlas Haven Developer Documentation

- Status: Current + Planned
- Audience: Maintainers and manifest-driven app authors
- Source of truth: Engineering handbook for the Atlas Haven rewrite
- Related modules/features: backend, frontend, apps, API, testing, deployment

This section explains how Atlas Haven is built, how its runtime is wired, how to
add new apps, and how to validate changes safely.

**Start here:** [Developer guide](./developer-guide.md) — local setup, running the API/worker/UI, env vars, and testing commands.

**Conventions:** [Coding standards](./coding-standards.md) — Python/Ruff, TypeScript, tests, API, and review expectations.

## Developer Reading Order

1. [`developer-guide.md`](./developer-guide.md)
2. [`coding-standards.md`](./coding-standards.md)
3. [`system-overview.md`](./system-overview.md)
4. [`repo-structure.md`](./repo-structure.md)
5. [`backend-architecture.md`](./backend-architecture.md)
6. [`frontend-architecture.md`](./frontend-architecture.md)
7. [`docker-runtime-topology.md`](./docker-runtime-topology.md)
8. [`manifest-and-app-framework.md`](./manifest-and-app-framework.md)
9. [`adding-a-new-app.md`](./adding-a-new-app.md)
10. [`testing-and-quality-gates.md`](./testing-and-quality-gates.md)

## Supporting References

- storage and persistence: [`data-model-and-storage.md`](./data-model-and-storage.md)
- workers and async jobs: [`background-jobs-and-workers.md`](./background-jobs-and-workers.md)
- deployment and operations: [`deployment-and-operations.md`](./deployment-and-operations.md)
- parity context: [`parity-and-migration-notes.md`](./parity-and-migration-notes.md)
- API reference: [`api/atlas-haven-api-overview.md`](./api/atlas-haven-api-overview.md)
