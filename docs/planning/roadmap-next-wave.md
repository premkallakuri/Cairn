# Atlas Haven Roadmap: Next Wave

- Status: Current + Planned
- Audience: Product owners, maintainers, release planners
- Source of truth: Canonical near-term roadmap for the next implementation wave after `M14`
- Related modules/features: settings/update parity, content parity, ops hardening, AI maturity, app diagnostics

This roadmap now covers the immediate build wave after `M14`. `M13 Benchmark`
and `M14 Extensibility` have moved into the shipped-state inventory in
[`completed-features.md`](./completed-features.md). The focus now shifts to the
next operator-visible outcomes that close parity and maturity gaps.

## Roadmap Item 1: System Settings And Release/Update Parity

Why it matters:

- Atlas Haven needs a fuller system operations story than the current early-wave service controls

User-facing outcome:

- operators can inspect and manage product/runtime settings, release state, and update workflows from the shell

Main work involved:

- backend settings persistence and read/update APIs
- latest-version and system update parity alignment
- frontend release/update and settings surfaces in Control Room
- clearer operational diagnostics and user messaging

Depends on:

- platform core
- App Dock update patterns
- Control Room shell

Docs that must ship with it:

- update [`../features/system-settings-and-releases.md`](../features/system-settings-and-releases.md)
- update [`../user-guides/troubleshoot-runtime-updates-and-failures.md`](../user-guides/troubleshoot-runtime-updates-and-failures.md)
- update operations and deployment developer docs

## Roadmap Item 2: Content Update Parity

Why it matters:

- Atlas Haven already has local-first content foundations, but it still needs a
  clearer story for checking and applying content updates over time

User-facing outcome:

- operators can see when maps or library content are out of date and apply updates through documented workflows

Main work involved:

- content update check/apply execution
- consistent update state for maps and ZIM-related assets
- better integration with download jobs and content metadata
- clearer UI language around bundled, installed, and updatable content

Depends on:

- manifests/content foundations
- downloads/jobs
- maps and Kiwix/ZIM domains

Docs that must ship with it:

- update [`../features/manifests-and-content-updates.md`](../features/manifests-and-content-updates.md)
- update map and library user guides
- update API domain mapping if route behavior changes

## Roadmap Item 3: Operations Hardening And Recovery Workflows

Why it matters:

- the rewrite is now useful, but operators still need stronger recovery,
  troubleshooting, storage, and backup/restore guidance and product affordances

User-facing outcome:

- operators can diagnose failures more confidently and maintain Atlas Haven as a durable local platform

Main work involved:

- richer operational diagnostics
- stronger download/update failure visibility
- backup and restore workflow maturity
- storage and runtime health improvements
- better per-app troubleshooting surfaces

Depends on:

- Control Room
- App Dock
- settings/update parity
- content/job visibility

Docs that must ship with it:

- update [`../user-guides/manage-storage-backups-and-restores.md`](../user-guides/manage-storage-backups-and-restores.md)
- update [`../user-guides/troubleshoot-runtime-updates-and-failures.md`](../user-guides/troubleshoot-runtime-updates-and-failures.md)
- update deployment and operations developer docs

## Roadmap Item 4: AI And Product Maturity

Why it matters:

- the product now has core AI and benchmark surfaces, but the remaining maturity work needs to tie chat, knowledge retrieval, maps, library content, and app diagnostics together more cleanly

User-facing outcome:

- operators get a more trustworthy, better integrated platform for local AI, content stewardship, and app lifecycle diagnostics

Main work involved:

- richer citations and retrieval maturity
- clearer model/runtime readiness state
- stronger benchmark interpretation and comparison UX
- deeper app detail and troubleshooting surfaces
- better cross-feature messaging between content, AI, and system operations

Depends on:

- benchmark workflows
- chat and knowledge base foundations
- content update parity
- App Dock diagnostics

Docs that must ship with it:

- update [`../features/ai-chat.md`](../features/ai-chat.md)
- update [`../features/knowledge-base.md`](../features/knowledge-base.md)
- update [`../features/benchmarks.md`](../features/benchmarks.md)
- update relevant user and developer guides

## Summary Of The Next Wave

The next wave should produce:

- fuller settings and release/update parity
- stronger content update behavior
- better day-two operations and recovery
- deeper AI, benchmark, and app-diagnostic maturity

These are the most important steps to move Atlas Haven from a strong
`M14`-level rewrite into a broader, maintainable, operator-ready platform.
