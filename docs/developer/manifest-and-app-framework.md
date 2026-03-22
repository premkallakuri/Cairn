# Manifest And App Framework

- Status: Current + Planned
- Audience: Maintainers, app authors
- Source of truth: App package contract and framework rules
- Related modules/features: catalog, orchestration, App Dock, planned `M14`

## Purpose

The manifest-and-app framework lets Atlas Haven add capabilities by declaring
packages rather than hard-coding each app into the control plane.

## Required Manifest Sections

- `id`
- `kind`
- `display`
- `runtime`
- `network`
- `storage`
- `dependencies`
- `healthcheck`
- `hooks`
- `updates`
- `permissions`
- `capabilities`
- `docs`
- `tests`

## Current Kind Values

- `sibling_app`
- `dependency_app`
- `core_capability`

## Runtime Responsibilities

The manifest must describe:

- image or built-in runtime identity
- ports
- mounts
- restart behavior
- dependency ordering
- health target
- update strategy

## Hooks

Hook entrypoints may expose:

- `preflight`
- `preinstall`
- `postinstall`
- `prestart`
- `poststart`
- `preupdate`
- `rollback`
- `preuninstall`
- `postuninstall`

## Current Framework Behavior

- catalog sync reads app manifests from disk
- App Dock renders app metadata from the catalog
- install order honors dependencies
- Kiwix already uses a specialized `preinstall` hook

## Planned Evolution

- new-app scaffolding
- richer validation feedback
- stronger docs/test generation expectations
