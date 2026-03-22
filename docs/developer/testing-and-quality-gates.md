# Testing And Quality Gates

- Status: Current + Planned
- Audience: Maintainers, contributors
- Source of truth: Validation strategy for the rewrite
- Related modules/features: module gates, app smokes, contract testing

## Test Layers

- unit tests for service and validator logic
- contract tests for API route presence and schema expectations
- integration tests for API plus storage/runtime behavior
- app smoke tests for manifest packages
- frontend type checks and E2E navigation validation

## Current Common Commands

- `make lint`
- `make test-unit`
- `make test-contract`
- `make test-integration`
- `make test-module MODULE=Mxx`
- `make smoke MODULE=Mxx`

## Module Gate Principle

Every module should be independently testable and should not rely on ad hoc
manual validation alone. App-specific smoke tests are especially important for
manifest-driven packages.

## Quality Expectations

- documented public API surface
- clear current versus planned product labeling in docs
- no hidden cross-module dependencies
- predictable lifecycle behavior for app packages

## Planned Evolution

- deeper E2E coverage for operator workflows
- broader benchmark and parity regression suites
