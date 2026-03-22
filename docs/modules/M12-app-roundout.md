# M12 App Roundout

## Scope

- Round out the day-one sibling apps with FlatNotes, CyberChef, and Kolibri coverage
- Expose install, start, stop, restart, reinstall, and update actions through the rewrite shell
- Add service launch URLs and image-tag version metadata to the platform service list
- Replace the placeholder App Dock card with a real operator-facing control surface

## Implemented

- `POST /api/system/services/force-reinstall`
- `POST /api/system/services/check-updates`
- `GET /api/system/services/{name}/available-versions`
- `POST /api/system/services/update`
- Launch URL derivation for sibling apps from manifest ports
- Current-version extraction from container image tags
- Static version catalog for the current day-one app set
- App Dock operations panel on Bridge and Control Room
- App smoke coverage for FlatNotes, CyberChef, and Kolibri

## Notes

- Version discovery is intentionally deterministic for now. The version catalog keeps the update flow testable without introducing registry access into the early rewrite slices.
- The App Dock is the current service-detail surface. It lets us exercise the orchestration paths and user flows now, while leaving room for a richer dedicated service detail page later.
- FlatNotes, CyberChef, and Kolibri are wired through the same manifest-driven orchestration contract as the earlier Kiwix, Maps, Ollama, and Qdrant packages.
