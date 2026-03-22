# Docker Runtime Topology

- Status: Current + Planned
- Audience: Maintainers, operators
- Source of truth: Container topology and network model reference
- Related modules/features: compose stack, sibling apps, App Dock

## Base Compose Services

The rewrite compose stack currently defines:

- `api`
- `worker`
- `web`
- `mysql`
- `redis`
- `disk-collector`

## Shared Network Model

The default compose network is named `project-nomad_default`. Sibling app
containers are expected to join that same network so that Atlas Haven can manage
them coherently.

## Important Mounts

- backend container mounts the rewrite `backend/`, `apps/`, and `docs/`
- backend and worker see the root `collections/` directory
- backend owns access to `/var/run/docker.sock`
- sibling apps mount host-backed paths under the shared storage root

## Runtime Principle

Atlas Haven is not only a web app. It is a control plane that manages other
application runtimes as part of the same local system.

## Planned Evolution

- more explicit disk inventory reporting
- richer runtime introspection and health visibility
- deeper restore and repair guidance
