# Run Benchmarks

- Status: Current + Planned
- Audience: Operators, maintainers
- Source of truth: Guide for current benchmark workflows in Control Room
- Related modules/features: Benchmarks, Benchmark Helper

## Goal

Measure device capability for Atlas Haven workloads and compare results over time.

## Current Workflow

1. Open `Control Room`.
2. Find the `Benchmark Lane` panel.
3. Choose `Run Full`, `Run System`, or `Run AI`.
4. Wait for the page to refresh with the latest local benchmark result.
5. Review the saved score, hardware snapshot, and benchmark history count.

## Current Results

- persisted local benchmark result history
- latest benchmark type and score in the shell
- stored benchmark settings including anonymous submission preference

## Planned Improvements

- richer comparison views
- better interpretation guidance for maps, chat, and knowledge workloads
- deeper helper-runtime and long-running benchmark execution if needed

## Troubleshooting

- If the benchmark helper is unavailable, install or repair the package first.
- If results vary unexpectedly, re-run with fewer background workloads active.

## Related Docs

- [`../features/benchmarks.md`](../features/benchmarks.md)
