# M03 Orchestration Core

## Goal

Provide generic install, reinstall, and update orchestration primitives with
event ordering that can later be backed by the Docker SDK.

## Current Deliverables

- Container adapter protocol
- Operation event model
- Generic install/reinstall/update service
- Unit tests for event ordering and rollback

## Gate

The orchestration service produces deterministic lifecycle events under test.
