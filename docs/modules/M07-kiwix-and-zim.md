# M07 Kiwix And ZIM

## Goal

Create the local library domain for ZIM files, Wikipedia state, remote catalog discovery, and
the bundled Kiwix seed path that future install flows can rely on.

## Current Deliverables

- Local ZIM storage listing and safe deletion
- Remote Kiwix catalog parsing for the content explorer
- Curated category tier download planning through the shared download job system
- Wikipedia state and selection APIs with bundled demo seeding for `top-mini`
- Kiwix app preinstall hook that copies the bundled demo ZIM into storage
- Field Guide surface showing local library status
- Module test and smoke commands

## Gate

The module can safely manage local ZIM files, expose curated and remote content state, and prepare
the Kiwix package with a bundled demo Wikipedia file without requiring internet access for the first
run path.
