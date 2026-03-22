# Ollama Runtime

- Status: Current + Planned
- Audience: Operators, AI users, maintainers
- Source of truth: Feature definition for local model runtime management
- Related modules/features: `M09`, `ollama`, `downloads`, AI Chat, Knowledge Base

## Purpose

Ollama Runtime provides local model serving for chat and future embedding or AI
processing tasks. It is the core inference engine for Atlas Haven's private AI
workflows.

## Current State

- Ollama is a sibling app package managed through App Dock
- model catalog and installed-model APIs are available
- model downloads are tracked through the shared download job system
- Ollama installs with dependency-aware orchestration behavior

## Planned State

- richer model metadata, lifecycle controls, and storage accounting
- clearer support for embedding versus chat models
- stronger runtime readiness indicators
- deeper configuration of model defaults and AI workflow tuning

## API Surface

- `GET /api/ollama/models`
- `POST /api/ollama/models`
- `DELETE /api/ollama/models`
- `GET /api/ollama/installed-models`
- `POST /api/ollama/chat`

## Dependencies And Storage

- `storage/ollama`
- download job persistence
- dependency relationship with Qdrant for Knowledge Base workflows

## Failure Modes

- incomplete model downloads can leave confusing installed-model state
- runtime container health can diverge from model availability
- model selection can fail if no installed model is actually ready

## Acceptance Criteria

- operators must be able to see available and installed model state
- Ollama must support AI Chat entry from within Atlas Haven
- model download progress must be observable through the platform
