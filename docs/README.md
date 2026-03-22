# Atlas Haven Documentation

- Status: Current + Planned
- Audience: Operators, maintainers, app authors, product owners
- Source of truth: Authoritative rewrite documentation for Atlas Haven
- Related modules/features: `M00-M12`, product planning, API contract, app framework

Atlas Haven is the Python + Next.js rewrite workspace for Project N.O.M.A.D. This
documentation set is the primary source of truth for the rewrite. It explains
what Atlas Haven is today, what it is intended to become, and how to operate,
extend, and maintain it.

The root repo `docs/` folder remains the home for brand, rebuild, and strategy
artifacts. This `atlas-haven/docs/` tree is the operational and engineering
documentation set for the product itself.

## How To Use This Docs Set

- Start with [`prd/atlas-haven-prd.md`](./prd/atlas-haven-prd.md) for the product contract.
- Use [`features/README.md`](./features/README.md) for detailed feature behavior and feature-to-API mapping.
- Use [`user-guides/README.md`](./user-guides/README.md) for operator workflows.
- Use [`developer/README.md`](./developer/README.md) for system architecture, app authoring, and engineering workflows.
- Keep using [`architecture/overview.md`](./architecture/overview.md) and [`modules/`](./modules/) for delivery-slice notes and implementation progress.

## Documentation Conventions

- Every page declares whether it documents `Current`, `Planned`, or `Current + Planned` behavior.
- `Current` means behavior implemented in the active Atlas Haven workspace.
- `Planned` means behavior required by the product contract but not fully implemented yet.
- `Current + Planned` means the page intentionally covers both the delivered slice and the expected end-state platform.
- Atlas Haven product terminology is canonical:
  - `Bridge`
  - `App Dock`
  - `Atlas Maps`
  - `AI Chat`
  - `Field Guide`
  - `Control Room`
  - `Library Explorer`
  - `Library Shelf`

## Documentation Map

### Product Definition

- [`prd/atlas-haven-prd.md`](./prd/atlas-haven-prd.md)
- [`prd/personas-and-use-cases.md`](./prd/personas-and-use-cases.md)
- [`prd/requirements-matrix.md`](./prd/requirements-matrix.md)
- [`prd/release-phasing.md`](./prd/release-phasing.md)

### Planning

- [`planning/README.md`](./planning/README.md)
- [`planning/completed-features.md`](./planning/completed-features.md)
- [`planning/roadmap-next-wave.md`](./planning/roadmap-next-wave.md)
- [`planning/next-wave-sequencing.md`](./planning/next-wave-sequencing.md)

### Feature Specifications

- [`features/README.md`](./features/README.md)
- Primary shell and workflows:
  - [`features/bridge.md`](./features/bridge.md)
  - [`features/app-dock.md`](./features/app-dock.md)
  - [`features/control-room.md`](./features/control-room.md)
  - [`features/easy-setup.md`](./features/easy-setup.md)
  - [`features/atlas-maps.md`](./features/atlas-maps.md)
  - [`features/field-guide.md`](./features/field-guide.md)
  - [`features/library-explorer.md`](./features/library-explorer.md)
  - [`features/library-shelf.md`](./features/library-shelf.md)
  - [`features/kiwix-and-zim.md`](./features/kiwix-and-zim.md)
  - [`features/ollama-runtime.md`](./features/ollama-runtime.md)
  - [`features/ai-chat.md`](./features/ai-chat.md)
  - [`features/knowledge-base.md`](./features/knowledge-base.md)
  - [`features/downloads-and-jobs.md`](./features/downloads-and-jobs.md)
  - [`features/manifests-and-content-updates.md`](./features/manifests-and-content-updates.md)
  - [`features/benchmarks.md`](./features/benchmarks.md)
  - [`features/system-settings-and-releases.md`](./features/system-settings-and-releases.md)
- App package specs:
  - [`features/apps/kiwix.md`](./features/apps/kiwix.md)
  - [`features/apps/qdrant.md`](./features/apps/qdrant.md)
  - [`features/apps/ollama.md`](./features/apps/ollama.md)
  - [`features/apps/flatnotes.md`](./features/apps/flatnotes.md)
  - [`features/apps/cyberchef.md`](./features/apps/cyberchef.md)
  - [`features/apps/kolibri.md`](./features/apps/kolibri.md)
  - [`features/apps/maps.md`](./features/apps/maps.md)
  - [`features/apps/benchmark-helper.md`](./features/apps/benchmark-helper.md)

### User Guides

- [`user-guides/README.md`](./user-guides/README.md)
- [`user-guides/first-run-and-bootstrap.md`](./user-guides/first-run-and-bootstrap.md)
- [`user-guides/install-and-manage-apps.md`](./user-guides/install-and-manage-apps.md)
- [`user-guides/use-the-offline-library.md`](./user-guides/use-the-offline-library.md)
- [`user-guides/manage-zim-and-wikipedia.md`](./user-guides/manage-zim-and-wikipedia.md)
- [`user-guides/download-and-use-maps.md`](./user-guides/download-and-use-maps.md)
- [`user-guides/run-local-ai-chat.md`](./user-guides/run-local-ai-chat.md)
- [`user-guides/build-and-search-the-knowledge-base.md`](./user-guides/build-and-search-the-knowledge-base.md)
- [`user-guides/run-benchmarks.md`](./user-guides/run-benchmarks.md)
- [`user-guides/manage-storage-backups-and-restores.md`](./user-guides/manage-storage-backups-and-restores.md)
- [`user-guides/troubleshoot-runtime-updates-and-failures.md`](./user-guides/troubleshoot-runtime-updates-and-failures.md)

### Developer Documentation

- [`developer/README.md`](./developer/README.md)
- [`developer/system-overview.md`](./developer/system-overview.md)
- [`developer/repo-structure.md`](./developer/repo-structure.md)
- [`developer/backend-architecture.md`](./developer/backend-architecture.md)
- [`developer/frontend-architecture.md`](./developer/frontend-architecture.md)
- [`developer/data-model-and-storage.md`](./developer/data-model-and-storage.md)
- [`developer/background-jobs-and-workers.md`](./developer/background-jobs-and-workers.md)
- [`developer/docker-runtime-topology.md`](./developer/docker-runtime-topology.md)
- [`developer/manifest-and-app-framework.md`](./developer/manifest-and-app-framework.md)
- [`developer/adding-a-new-app.md`](./developer/adding-a-new-app.md)
- [`developer/testing-and-quality-gates.md`](./developer/testing-and-quality-gates.md)
- [`developer/deployment-and-operations.md`](./developer/deployment-and-operations.md)
- [`developer/parity-and-migration-notes.md`](./developer/parity-and-migration-notes.md)
- API references:
  - [`developer/api/atlas-haven-api-overview.md`](./developer/api/atlas-haven-api-overview.md)
  - [`developer/api/atlas-haven-api.yaml`](./developer/api/atlas-haven-api.yaml)
  - [`developer/api/endpoint-domain-map.md`](./developer/api/endpoint-domain-map.md)

## Existing Implementation Notes

These documents remain valid and are intentionally preserved:

- [`architecture/overview.md`](./architecture/overview.md): high-level rewrite topology
- [`modules/`](./modules/): implementation notes for delivered slices `M00-M12`

The feature and developer docs should reference those module notes when they need
delivery history or slice-specific implementation detail.
