# Field Guide

- Status: Current + Planned
- Audience: Operators, new users, maintainers
- Source of truth: Feature definition for the in-product documentation surface
- Related modules/features: `M04`, `docs`, product documentation corpus

## Purpose

Field Guide is the documentation surface inside Atlas Haven. It provides product
learning, workflow help, onboarding, troubleshooting, and future release notes.

## Current State

- exposed as the `/docs` route in the shell
- backed by docs indexing and listing APIs
- currently supports basic documentation surfacing and acts as a lightweight docs shell

## Planned State

- deeper browsing and search
- category-based documentation navigation
- better mapping between features, user guides, and troubleshooting entries
- tighter integration with release notes and use-case documentation

## API Surface

- `GET /api/docs/list`

## Dependencies And Storage

- markdown documentation content in the repo
- docs indexing logic in the backend

## Failure Modes

- incomplete docs indexing can hide available documentation
- stale content can confuse users if product behavior changes faster than docs

## Acceptance Criteria

- users must be able to reach documentation from the top-level shell
- docs visibility must not depend on external network access
- product terminology in the Field Guide must match the rest of the shell
