# Download And Use Maps

- Status: Current + Planned
- Audience: Operators, map users
- Source of truth: Guide for Atlas Maps workflows
- Related modules/features: Atlas Maps, Downloads And Jobs

## Goal

Prepare local maps, verify map assets are present, and use the Atlas Maps
surface for offline geographic workflows.

## Current Steps

1. Open `Atlas Maps` from the main navigation.
2. Review visible curated map collections and installed region files.
3. Confirm that base assets and PMTiles data needed for your intended view are present.
4. Use the map viewer to render local map data.
5. Open `Control Room` to monitor active map downloads when applicable.

## Current Limits

- the rewrite already exposes maps as a first-class destination
- complete end-to-end remote acquisition is still part of the broader planned platform

## Planned Enhancements

- direct collection download from the UI
- clearer preflight checks for remote map pulls
- coverage summaries and storage impact previews

## Expected Results

- installed map regions are visible to the platform
- the map route opens without requiring an external map service

## Troubleshooting

- If the map viewer does not render, verify base assets exist and the styles endpoint is healthy.
- If a region is expected but missing, inspect the local map storage and download job state.

## Related Docs

- [`../features/atlas-maps.md`](../features/atlas-maps.md)
- [`../features/downloads-and-jobs.md`](../features/downloads-and-jobs.md)
