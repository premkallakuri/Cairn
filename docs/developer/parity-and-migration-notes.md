# Parity And Migration Notes

- Status: Current + Planned
- Audience: Maintainers, product owners
- Source of truth: Legacy-to-rewrite context document
- Related modules/features: rebuild planning, current rewrite slices

## Why This Exists

Atlas Haven is a rewrite, not a greenfield invention. Maintainers need a concise
record of what is already preserved, what is partially preserved, and what still
needs explicit parity work.

## Already Preserved In The Rewrite

- local-first operating model
- Docker-managed sibling apps
- top-level shell destinations
- Kiwix, Ollama, Qdrant, FlatNotes, CyberChef, and Kolibri package definitions
- early maps, chat, and Knowledge Base workflows
- bundled content and seed-data orientation

## Partially Preserved

- richer release/update management
- full content update flows
- benchmark execution depth
- system settings breadth
- deeper docs and troubleshooting inside the product

## Migration Principle

The rewrite should preserve user-facing intent even when internal implementation
changes. Atlas Haven terminology becomes the new product language, while legacy
behavior remains relevant only where parity or migration context matters.

## Planned Closeout Areas

- benchmark parity
- app author scaffolding
- restore/backup maturity
- broader settings and release flows
