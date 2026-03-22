# FlatNotes App Package

- Status: Current + Planned
- Audience: Operators, app authors, maintainers
- Source of truth: App package specification for `nomad_flatnotes`
- Related modules/features: `M12`, App Dock

## Why It Exists

FlatNotes provides a lightweight notes capability inside the Atlas Haven app
catalog for local knowledge capture.

## Current Package Contract

- Service ID: `nomad_flatnotes`
- Kind: `sibling_app`
- Image: `dullage/flatnotes:latest`
- Port mapping: `8081 -> 8080`
- Mount: `${NOMAD_STORAGE_PATH}/flatnotes -> /data`
- Healthcheck: HTTP on port `8080`

## Operator-Visible Behavior

- appears in App Dock and Bridge-facing app surfaces
- exposes launch URL `http://127.0.0.1:8081`
- supports install, restart, reinstall, and update flows

## Planned Evolution

- app detail views and stronger data-location visibility

## Acceptance Criteria

- FlatNotes installs cleanly and launches from App Dock
- app state remains visible after reinstall and restart
