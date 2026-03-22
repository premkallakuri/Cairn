# M06 Easy Setup

## Goal

Create a persisted setup wizard that can turn operator selections into a dependency-aware
install plan for apps, maps, offline libraries, and local AI models.

## Current Deliverables

- Default draft persistence in the backend database
- Bootstrap API for wizard options and local-first manifest data
- Plan API that expands required services and dependencies
- Next.js Easy Setup page with live draft sync and review summary
- Module test and smoke commands

## Gate

The module can save wizard state, regenerate the plan after each change, and produce a
stable summary of services, content payload, and estimated storage without executing any
installs yet.
