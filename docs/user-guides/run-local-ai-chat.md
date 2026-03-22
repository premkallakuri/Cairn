# Run Local AI Chat

- Status: Current + Planned
- Audience: Operators, knowledge users
- Source of truth: Guide for chat session workflows
- Related modules/features: AI Chat, Ollama Runtime, Knowledge Base

## Goal

Install or verify a local model runtime, create a chat session, and run
conversations entirely on local infrastructure.

## Current Steps

1. Open `AI Chat`.
2. Check whether an installed local model is available.
3. If not, install the `AI Assistant Runtime` and queue a model through the supported runtime flows.
4. Create a new session.
5. Choose the active model.
6. Send a prompt and review the persisted conversation.
7. Reopen the session later from the session deck.

## Expected Results

- session history persists
- replies come from the local model runtime
- the workflow remains usable without cloud dependencies

## Planned Enhancements

- better streaming-first conversation UX
- clearer model defaults and model capability labels
- richer source citations when Knowledge Base context is active

## Troubleshooting

- If no model is selectable, install or queue one first.
- If the session exists but replies fail, confirm the Ollama runtime is healthy in App Dock.
- If responses ignore local files, verify that the Knowledge Base has indexed relevant content.

## Related Docs

- [`build-and-search-the-knowledge-base.md`](./build-and-search-the-knowledge-base.md)
- [`../features/ai-chat.md`](../features/ai-chat.md)
- [`../features/ollama-runtime.md`](../features/ollama-runtime.md)
