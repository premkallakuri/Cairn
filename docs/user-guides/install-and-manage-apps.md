# Install And Manage Apps

- Status: Current + Planned
- Audience: Operators
- Source of truth: App Dock workflow guide
- Related modules/features: App Dock, Control Room, all app packages

## Goal

Install a supported app, launch it, and manage its lifecycle without using the
Docker CLI directly.

## Current Steps

1. Open `Bridge` or `Control Room`.
2. Find the app in `App Dock`.
3. Review the app card for:
   - app type
   - current status
   - current version
   - launch URL
4. If the app is not installed, select `Install`.
5. After install, use:
   - `Open` to launch the app
   - `Stop` to halt it
   - `Start` to bring it back
   - `Restart` to cycle the runtime
   - `Reinstall` to recover a broken app
6. If the card shows an available update, load versions and apply the target version.

## Good First Apps

- `Information Library` for offline reference
- `AI Assistant Runtime` for local chat
- `FlatNotes` for notes
- `CyberChef` for data tooling
- `Kolibri` for education workflows

## Expected Results

- App Dock updates the visible runtime state
- launch URLs become available for apps with browser interfaces
- the app remains represented even after restart or reinstall

## Planned Enhancements

- per-app logs and health history
- rollback actions with clearer operator guidance
- storage impact preview before large installs

## Troubleshooting

- If install does nothing, check Control Room for active download or job state.
- If an app installs but does not launch, confirm the launch URL and app-specific mount requirements.
- If update options are missing, the app may not yet have multiple tracked versions in the current metadata.

## Related Docs

- [`../features/app-dock.md`](../features/app-dock.md)
- [`../features/control-room.md`](../features/control-room.md)
