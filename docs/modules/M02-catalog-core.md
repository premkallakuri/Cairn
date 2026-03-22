# M02 Catalog Core

## Goal

Load app manifests from disk, validate them, resolve dependencies, detect port
collisions, and expose a seeded service catalog.

## Current Deliverables

- Manifest schema
- Manifest scanner
- Dependency resolver
- Port conflict validator
- Catalog database sync
- `/api/system/services`

## Gate

All bundled apps are listed through the catalog and invalid manifests fail fast.
