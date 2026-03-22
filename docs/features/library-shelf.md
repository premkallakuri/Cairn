# Library Shelf

- Status: Current + Planned
- Audience: Operators, knowledge users
- Source of truth: Feature definition for installed content management
- Related modules/features: `M07`, `zim`, Kiwix, local content storage

## Purpose

Library Shelf is the installed-content view of Atlas Haven. It answers the
operator question: what local reference material is already on this machine, and
what can I do with it?

## Current State

- represented through local ZIM listing and Wikipedia selection state
- surfaced in the Field Guide library view
- compatible with the Kiwix app package and bundled demo Wikipedia flow

## Planned State

- broader installed-content management beyond ZIM files
- better metadata display, filtering, and source attribution
- tighter transitions from shelf items into launch actions or deletion flows

## API Surface

- `GET /api/zim/list`
- `GET /api/zim/wikipedia`
- `DELETE /api/zim/{filename}`

## Dependencies And Storage

- `storage/zim`
- ZIM metadata extraction and listing
- Kiwix mount and library-serving behavior

## Failure Modes

- damaged or incomplete ZIM files can appear installed but fail at serve time
- deletion mistakes can remove needed content if metadata is unclear
- Kiwix can be healthy while content state is stale or mismatched

## Acceptance Criteria

- users must be able to see what local library files exist
- current Wikipedia selection state must be obvious
- installed content must be clearly separated from discoverable but not-yet-installed content
