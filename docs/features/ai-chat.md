# AI Chat

- Status: Current + Planned
- Audience: Operators, knowledge users
- Source of truth: Feature definition for local chat workflows
- Related modules/features: `M10`, `chat`, `ollama`, Knowledge Base

## Purpose

AI Chat is the conversational workspace of Atlas Haven. It provides multi-session
local chat against installed models and serves as the primary front door for
retrieval-assisted knowledge workflows.

## Current State

- multiple local sessions can be created, updated, deleted, and reopened
- session messages persist in the platform database
- title generation occurs from early user input
- chat sends prompts through the Ollama-compatible API layer
- the frontend exposes a complete session deck and active conversation pane

## Planned State

- streaming-first UX refinement
- richer citations and context controls
- better model selection defaults and conversation tools
- tighter integration with library content and maps workflows

## API Surface

- `GET /api/chat/suggestions`
- `GET /api/chat/sessions`
- `POST /api/chat/sessions`
- `DELETE /api/chat/sessions/all`
- `GET /api/chat/sessions/{id}`
- `PUT /api/chat/sessions/{id}`
- `DELETE /api/chat/sessions/{id}`
- `POST /api/chat/sessions/{id}/messages`
- `POST /api/ollama/chat`

## Dependencies And Storage

- session and message tables in the platform database
- Ollama runtime and installed models
- optional Knowledge Base context assembly

## Failure Modes

- chat can fail if no usable local model is installed
- stale active-session state can confuse users after destructive actions
- assistant replies can degrade if retrieval context or model state is inconsistent

## Acceptance Criteria

- users must be able to maintain multiple local conversations
- chat history must persist across page reloads
- AI Chat must remain functional without cloud services
