# M08 Maps

## Goal

Create the offline maps domain for PMTiles storage, curated collection planning, base-asset
preparation, and generated map styles that later viewer work can build on.

## Current Deliverables

- Local PMTiles listing and safe deletion
- Curated map collection status based on bundled manifests and local files
- PMTiles download queuing and remote preflight checks
- Generated base-assets scaffold and style document creation
- File and asset routes for local map files and generated viewer assets
- Atlas Maps page with readiness, collection, and local-region visibility
- Module test and smoke commands

## Gate

The module can prepare base assets, queue PMTiles downloads, expose collection status, and
generate a stable style document from local map files without depending on the legacy app.
