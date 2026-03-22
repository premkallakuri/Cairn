# Benchmarks

- Status: Current + Planned
- Audience: Operators, maintainers, performance evaluators
- Source of truth: Feature definition for system and AI benchmark workflows
- Related modules/features: `M13`, `benchmark`, `nomad_benchmark_helper`, `Control Room`

## Purpose

Benchmarks measure how capable the local device is for Atlas Haven workloads.
This includes system-level performance and current AI workload comparisons.

## Current State

- benchmark runs can now be started from the rewrite API and Control Room
- local benchmark results, settings, status, builder tags, and submission metadata are persisted
- latest-result, list, comparison, and submit flows are implemented in the backend
- the benchmark helper remains the package-level runtime marker in the app framework

## Planned State

- richer UI comparison views and interpretation guidance
- more realistic long-running execution through a worker-backed runtime
- stronger benchmark helper integration if helper-side runtime behavior becomes necessary
- clearer recommendations tied to maps, chat, and retrieval workloads

## API Surface

- `POST /api/benchmark/run`
- `POST /api/benchmark/run/system`
- `POST /api/benchmark/run/ai`
- `GET /api/benchmark/results`
- `GET /api/benchmark/results/latest`
- `GET /api/benchmark/results/{id}`
- `POST /api/benchmark/submit`
- `POST /api/benchmark/builder-tag`
- `GET /api/benchmark/comparison`
- `GET /api/benchmark/status`
- `GET /api/benchmark/settings`
- `POST /api/benchmark/settings`

## Dependencies And Storage

- benchmark helper runtime marker
- persistent benchmark result storage
- future worker orchestration for long-running tests

## Failure Modes

- deterministic local execution can differ from future worker-backed real-world runs
- benchmark results can be misleading if system state or active loads are not captured
- AI benchmark comparability depends on model/runtime normalization

## Acceptance Criteria

- users can run and review baseline benchmark workflows without leaving Atlas Haven
- benchmark results are stored and repeatable enough for local comparison
- deeper comparison and interpretation workflows remain part of the next maturity wave
