# Use The Offline Library

- Status: Current + Planned
- Audience: Operators, knowledge users
- Source of truth: Guide for consuming local reference content
- Related modules/features: Library Shelf, Kiwix and ZIM, Field Guide

## Goal

Open Atlas Haven's local library content and use it as an offline reference
surface.

## Current Steps

1. Ensure `Information Library` is installed in App Dock.
2. Confirm at least one ZIM file exists in the library storage.
3. Open the `Field Guide` or the Kiwix launch URL from App Dock.
4. Use the installed library content as your local reference surface.

## Where Content Comes From

- bundled demo Wikipedia for first run
- curated category workflows
- future remote ZIM downloads

## Expected Results

- Kiwix opens in the browser
- the local library is available without depending on a cloud service
- installed content remains usable across restarts

## Planned Enhancements

- richer shelf browsing inside Atlas Haven
- clearer transitions between discoverable content and already installed content

## Troubleshooting

- If Kiwix opens but shows no useful content, verify that ZIM files are present in `storage/zim`.
- If a library file was removed manually, re-check the current Wikipedia selection and shelf state.

## Related Docs

- [`manage-zim-and-wikipedia.md`](./manage-zim-and-wikipedia.md)
- [`../features/library-shelf.md`](../features/library-shelf.md)
- [`../features/kiwix-and-zim.md`](../features/kiwix-and-zim.md)
