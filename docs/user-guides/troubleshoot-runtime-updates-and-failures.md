# Troubleshoot Runtime Updates And Failures

- Status: Current + Planned
- Audience: Operators, maintainers
- Source of truth: Operational troubleshooting guide for runtime issues
- Related modules/features: Control Room, App Dock, Downloads And Jobs, system releases

## Goal

Diagnose and recover when app installs, updates, launches, or runtime workflows
do not behave as expected.

## Quick Triage Checklist

1. Open `Control Room`.
2. Check whether the affected app is present in `App Dock`.
3. Review the app status, current version, and available update state.
4. Check the `Download Activity` area for blocked or incomplete jobs.
5. Try `Restart` first for transient runtime issues.
6. Try `Reinstall` if the app appears corrupted or partially installed.

## Common Failure Classes

### App Will Not Install

- possible cause: dependency or manifest issue
- action: verify the app is present in the catalog and retry install from App Dock

### App Installs But Does Not Open

- possible cause: port, health, or mount problem
- action: verify the launch URL and app-specific storage requirements

### Update State Looks Wrong

- possible cause: stale version metadata
- action: run `Check Updates` again and confirm the listed available versions

### AI Or Content Workflows Stall

- possible cause: background job not completed
- action: inspect Control Room download activity and confirm destination content exists

## Planned Enhancements

- built-in log viewers
- richer error explanations and recovery tips
- stronger rollback flows for version changes

## Related Docs

- [`install-and-manage-apps.md`](./install-and-manage-apps.md)
- [`../features/system-settings-and-releases.md`](../features/system-settings-and-releases.md)
- [`../features/downloads-and-jobs.md`](../features/downloads-and-jobs.md)
