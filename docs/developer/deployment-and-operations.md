# Deployment And Operations

- Status: Current + Planned
- Audience: Maintainers, operators
- Source of truth: Deployment and day-two operations reference
- Related modules/features: compose stack, App Dock, Control Room

## Current Deployment Model

Atlas Haven is deployed locally through Docker Compose from inside the rewrite
workspace. The helper scripts are:

- `./ops/scripts/local-up.sh`
- `./ops/scripts/local-down.sh`

The compose file starts the core platform and provides the network and storage
base for sibling apps.

## Operational Responsibilities

- bootstrap dependencies
- validate compose configuration
- bring the stack up and down
- monitor app and job state from the UI
- preserve storage and infrastructure volumes

## Day-Two Operations

- use App Dock for app lifecycle actions
- use Control Room for download and runtime visibility
- use smoke and module test scripts to validate platform changes

## Planned Evolution

- more formal environment profiles
- release-aware upgrade flow
- restore and maintenance runbooks integrated with product workflows
