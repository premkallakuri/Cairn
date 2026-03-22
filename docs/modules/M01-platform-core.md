# M01 Platform Core

## Goal

Stand up the FastAPI control plane with health, system info, shared settings, logging,
error handling, and DB initialization.

## Current Deliverables

- FastAPI app factory
- Settings model
- Logging configuration
- Error handlers
- `/api/health`
- `/api/system/info`

## Gate

The API boots with a valid config and health checks pass in tests.
