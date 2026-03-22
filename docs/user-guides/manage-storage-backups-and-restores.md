# Manage Storage, Backups, And Restores

- Status: Current + Planned
- Audience: Operators, maintainers
- Source of truth: Guide for storage awareness and future recovery workflows
- Related modules/features: Control Room, app storage, data model

## Goal

Understand where Atlas Haven stores data today and prepare for safe backup and
restore workflows as the platform matures.

## Current Storage Areas

- `../storage/zim`
- `../storage/maps`
- `../storage/ollama`
- `../storage/qdrant`
- `../storage/flatnotes`
- `../storage/kolibri`
- `../storage/rag`
- `../.docker/mysql`
- `../.docker/redis`

## Current Best Practices

1. Stop the stack before taking a full filesystem-level backup.
2. Preserve both service data directories and database volumes.
3. Keep app-specific storage together with database state when possible.
4. After restore, start the stack and validate services from Control Room.

## Planned Enhancements

- explicit backup and restore runbooks in the product
- storage health and disk summaries
- safer operator-facing restore validation

## Expected Results

- critical application data survives restart and reinstall
- operators understand that app storage and platform database state are both important

## Troubleshooting

- If an app comes back empty after restore, verify its mounted storage path was backed up.
- If platform metadata is missing, inspect MySQL and Redis volume state in addition to app-specific directories.

## Related Docs

- [`../developer/data-model-and-storage.md`](../developer/data-model-and-storage.md)
- [`../developer/deployment-and-operations.md`](../developer/deployment-and-operations.md)
