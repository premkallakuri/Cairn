# First Run And Bootstrap

- Status: Current + Planned
- Audience: New operators
- Source of truth: Initial bring-up guide for the rewrite workspace
- Related modules/features: `M00`, `M01`, `M04`, Easy Setup, Control Room

## Goal

Bring Atlas Haven up locally, verify that the stack starts, and confirm the main
shell routes are reachable.

## Prerequisites

- Docker with Compose support
- `uv` available for backend bootstrap
- `pnpm` available for frontend bootstrap
- access to the repo root

## Current Steps

1. Change into the rewrite workspace:
   - `cd atlas-haven`
2. Install backend and frontend dependencies:
   - `make bootstrap`
3. Confirm the compose file is valid:
   - `make docker-config`
4. Start the local stack:
   - `./ops/scripts/local-up.sh`
5. Open the main surfaces:
   - `http://localhost:3000` for the Next.js shell
   - `http://localhost:8000/api/health` for API health
6. Verify the shell navigation shows:
   - `Bridge`
   - `Atlas Maps`
   - `AI Chat`
   - `Field Guide`
   - `Control Room`

## Expected Results

- Docker services for `api`, `worker`, `web`, `mysql`, `redis`, and `disk-collector` start
- `/api/health` returns an OK status
- the web shell loads without a blank or error page

## Planned Enhancements

- one-step bootstrap validation from inside the UI
- first-run success checklist and setup completion confirmation

## Troubleshooting

- If dependency installation fails, re-run `make bootstrap` and inspect backend/frontend toolchain availability.
- If compose validation fails, check `.env` values and Docker daemon availability.
- If the web UI loads but features are empty, verify the API is reachable from the frontend environment.

## Related Docs

- [`../features/easy-setup.md`](../features/easy-setup.md)
- [`../developer/docker-runtime-topology.md`](../developer/docker-runtime-topology.md)
