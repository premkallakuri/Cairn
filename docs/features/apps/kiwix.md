# Kiwix App Package

- Status: Current + Planned
- Audience: Operators, app authors, maintainers
- Source of truth: App package specification for `nomad_kiwix_server`
- Related modules/features: `M07`, Kiwix and ZIM, Library Shelf

## Why It Exists

Kiwix serves installed ZIM files as a browsable offline library. It is the
runtime behind Atlas Haven's local reference and encyclopedia workflows.

## Current Package Contract

- Service ID: `nomad_kiwix_server`
- Kind: `sibling_app`
- Image: `ghcr.io/kiwix/kiwix-serve:3.8.1`
- Port mapping: `8090 -> 8080`
- Mount: `${NOMAD_STORAGE_PATH}/zim -> /data`
- Healthcheck: HTTP on port `8080`
- Hook: `preinstall` seeds the bundled demo Wikipedia

## Operator-Visible Behavior

- appears in App Dock as `Information Library`
- launches at `http://127.0.0.1:8090`
- serves local `.zim` files from host-backed storage

## Planned Evolution

- version update visibility and richer content diagnostics
- clearer library-specific install validation

## Acceptance Criteria

- app install results in a running library server with mounted ZIM content
- bundled demo Wikipedia remains a valid first-run path
