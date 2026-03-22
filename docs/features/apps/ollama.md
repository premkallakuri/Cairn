# Ollama App Package

- Status: Current + Planned
- Audience: Operators, maintainers, app authors
- Source of truth: App package specification for `nomad_ollama`
- Related modules/features: `M09`, AI Chat, Knowledge Base

## Why It Exists

Ollama is the local model runtime that powers chat and future AI processing
flows in Atlas Haven.

## Current Package Contract

- Service ID: `nomad_ollama`
- Kind: `sibling_app`
- Image: `ollama/ollama:0.11.0`
- Port mapping: `11434 -> 11434`
- Mount: `${NOMAD_STORAGE_PATH}/ollama -> /root/.ollama`
- Dependency: `nomad_qdrant`
- Healthcheck: `GET /api/tags`

## Operator-Visible Behavior

- appears in App Dock as `AI Assistant Runtime`
- exposes launch URL `http://127.0.0.1:11434`
- supports model acquisition through the platform

## Planned Evolution

- richer model/runtime configuration
- stronger diagnostics for chat versus embedding use

## Acceptance Criteria

- install flow must honor dependencies
- runtime state must support local AI Chat workflows
