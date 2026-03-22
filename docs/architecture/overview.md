# Atlas Haven Architecture Overview

Atlas Haven is a nested rewrite workspace that preserves the current local-first
Docker model while replacing the admin app with a modular Python + Next.js stack.

## First-Wave Boundaries

- `M00`: workspace bootstrap, compose, env templates, task runner
- `M01`: FastAPI platform core and health surface
- `M02`: manifest-driven catalog sync and service listing
- `M03`: orchestration service primitives and event model
- `M04`: Next.js shell with Bridge, Atlas Maps, AI Chat, Field Guide, and Control Room
- `M05`: durable download jobs, worker-facing runner, and Control Room visibility

## Runtime Model

- `api`: FastAPI control plane
- `worker`: ARQ-compatible background worker placeholder
- `web`: Next.js App Router shell
- `mysql`
- `redis`
- `disk-collector`

Sibling apps remain manifest-driven and continue to target the shared
`project-nomad_default` Docker network.
