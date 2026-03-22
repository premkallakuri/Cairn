# Benchmark Helper App Package

- Status: Planned
- Audience: Maintainers, app authors
- Source of truth: App package specification for `nomad_benchmark_helper`
- Related modules/features: planned `M13`, Benchmarks

## Why It Exists

Benchmark Helper is the auxiliary runtime used to execute or support benchmark
workloads without overloading the core control plane service.

## Current Package Contract

- Service ID: `nomad_benchmark_helper`
- Kind: `dependency_app`
- Image: `alpine:3.20`
- Command: `sleep infinity`
- No persistent mount required
- Health target: process-based check on `sleep`

## Operator-Visible Behavior

- appears as a dependency-oriented runtime in App Dock
- is not yet a fully realized user-facing workflow in the rewrite

## Planned Evolution

- execute sysbench-like operations and future AI benchmark support
- integrate with benchmark settings, results, and comparison views

## Acceptance Criteria

- benchmark workflows must eventually be able to rely on this helper package or its successor contract
