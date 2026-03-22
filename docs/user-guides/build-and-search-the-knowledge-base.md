# Build And Search The Knowledge Base

- Status: Current + Planned
- Audience: Operators, researchers
- Source of truth: Guide for file ingestion and retrieval-assisted chat
- Related modules/features: Knowledge Base, AI Chat

## Goal

Upload local files, sync the knowledge store, and use those files as context in
AI Chat.

## Current Steps

1. Open `AI Chat`.
2. Use the `Knowledge Base` panel to select a local file.
3. Upload the file.
4. Run a sync if needed to refresh indexed state.
5. Confirm the file appears in the indexed-file list.
6. Ask a question in chat that should use the uploaded material.

## What Works Today

- upload
- sync
- list indexed files
- delete indexed files
- retrieval-assisted response composition

## Planned Enhancements

- broader file format support
- deeper indexing diagnostics
- stronger per-file status and reprocessing flows

## Expected Results

- the file remains visible after refresh
- chat can reference relevant local material

## Troubleshooting

- If upload succeeds but retrieval is poor, confirm the file contains extractable text.
- If a file seems stuck, use sync and re-check indexed state.
- If KB workflows look healthy but chat fails, inspect the local model runtime.

## Related Docs

- [`run-local-ai-chat.md`](./run-local-ai-chat.md)
- [`../features/knowledge-base.md`](../features/knowledge-base.md)
