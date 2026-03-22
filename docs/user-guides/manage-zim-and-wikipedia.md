# Manage ZIM And Wikipedia

- Status: Current + Planned
- Audience: Operators
- Source of truth: Guide for local library content selection and maintenance
- Related modules/features: Kiwix and ZIM, Library Explorer, Library Shelf

## Goal

Choose a Wikipedia package, review local ZIM files, and maintain the installed
offline reference set.

## Current Steps

1. Open the relevant library or setup workflow.
2. Review available Wikipedia options from the bundled list.
3. Select the bundled `top-mini` or another supported option.
4. Verify the selection state shows installed or ready.
5. Review local files through the shelf/listing workflows.
6. Remove outdated files only after confirming they are not the active selection.

## What Exists Today

- bundled demo Wikipedia selection
- local ZIM file inventory
- curated categories and remote-listing APIs

## Planned Enhancements

- richer remote explorer UI
- one-click replacement and upgrade workflows
- metadata-rich browsing and filtering of local files

## Expected Results

- current selection is visible
- local files are discoverable
- the library runtime can use the selected content

## Troubleshooting

- If a selection looks active but content is missing, inspect `storage/zim`.
- If downloaded content does not appear in the library, verify Kiwix is mounted against the correct storage path.
- If you are unsure whether to remove a file, compare the active selection state first.

## Related Docs

- [`../features/library-explorer.md`](../features/library-explorer.md)
- [`../features/kiwix-and-zim.md`](../features/kiwix-and-zim.md)
