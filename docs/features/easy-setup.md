# Easy Setup

- Status: Current + Planned
- Audience: First-time operators, product owners
- Source of truth: Feature definition for guided bootstrap and installation planning
- Related modules/features: `M06`, `easy_setup`, `catalog`, `maps`, `zim`, `ollama`

## Purpose

Easy Setup translates user goals into a concrete install-and-content plan. It is
the preferred starting point for new operators who want Atlas Haven to be useful
quickly without manually choosing every service and dataset.

## Current State

- supports draft persistence
- exposes capabilities, additional tools, map collections, category tiers, AI models, and Wikipedia options
- generates a typed plan with service count and total storage estimates
- can recommend Kiwix, Ollama, Qdrant, maps, and content packages based on selected goals

## Planned State

- one-click execution of the full generated plan
- more explicit dependency explanations and storage previews
- profile presets such as education, research, and field library
- post-setup verification and completion checklists

## Primary UX Flow

1. User chooses capabilities.
2. User chooses supporting content and tools.
3. User reviews storage impact and selected services.
4. User accepts the plan and proceeds to installation workflows.

## API Surface

- `GET /api/easy-setup/bootstrap`
- `GET /api/easy-setup/draft`
- `PUT /api/easy-setup/draft`
- `POST /api/easy-setup/plan`
- `GET /api/easy-setup/curated-categories`

## Dependencies And Storage

- catalog metadata
- maps collections
- Wikipedia/ZIM options
- model catalog data
- easy setup draft persistence in the platform database

## Failure Modes

- stale manifest data can generate incomplete plans
- storage estimates may drift from real downloaded sizes
- missing downstream services can block plan execution even if planning succeeds

## Acceptance Criteria

- a new user can generate a coherent installation plan without touching raw manifests
- the plan must explain which services and content will be installed
- plan output must be stable and reviewable
