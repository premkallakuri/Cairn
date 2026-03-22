# M13 Benchmark

- Status: Current
- Audience: Engineers, operators, and app authors
- Source of truth: Atlas Haven benchmark backend slice
- Related modules/features: `backend/app/modules/benchmark`, `Control Room`, `Benchmark Helper`

## Summary

M13 adds the first full benchmark backend slice for Atlas Haven. It introduces a persistent benchmark result store, benchmark settings, benchmark status, run/list/latest/result flows, submission metadata, builder-tag updates, and a local repository-comparison baseline.

## Implemented

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

## Behavior

- Benchmark runs are persisted locally in SQLite/MySQL through SQLAlchemy models.
- `sync=true` returns a completed benchmark payload immediately.
- Asynchronous runs are still completed locally for now, which keeps the contract useful before a real worker is introduced.
- Settings and status are persisted so the slice survives process restarts.
- Submission and builder-tag updates are validated and stored on the result record.

## Notes

- This slice is intentionally self-contained so it can be expanded later without changing the top-level navigation.
- The benchmark-helper app package remains a dependency/runtime marker and does not require user-facing UI changes for this milestone.
