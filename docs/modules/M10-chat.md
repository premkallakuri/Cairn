# M10 Chat

## Scope

- Add chat session persistence with multiple local threads
- Add CRUD APIs for sessions and messages
- Add starter prompt suggestions and automatic title generation from the first user turn
- Add `POST /api/ollama/chat` with JSON and SSE-compatible streaming responses
- Replace the placeholder `AI Chat` page with a working local session workspace

## Implemented

- `GET /api/chat/suggestions`
- `GET /api/chat/sessions`
- `POST /api/chat/sessions`
- `DELETE /api/chat/sessions/all`
- `GET /api/chat/sessions/{id}`
- `PUT /api/chat/sessions/{id}`
- `DELETE /api/chat/sessions/{id}`
- `POST /api/chat/sessions/{id}/messages`
- `POST /api/ollama/chat`
- SQL-backed `chat_sessions` and `chat_messages` tables
- Local title generation for sessions created as `New chat`
- Multi-session chat workspace in the frontend

## Notes

- The current chat reply path is deterministic and local-first. It validates that a model is tracked locally, then returns an Ollama-compatible response shape.
- SSE streaming is implemented at the compatibility layer even though the frontend currently uses the JSON response path.
- This module intentionally stops at local conversations. Knowledge Base retrieval and cited context stay in the next modules.
