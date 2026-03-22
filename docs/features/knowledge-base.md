# Knowledge Base

- Status: Current + Planned
- Audience: Operators, researchers, maintainers
- Source of truth: Feature definition for local file ingestion and retrieval
- Related modules/features: `M11`, `knowledge_base`, `chat`, `ollama`, `qdrant`

## Purpose

Knowledge Base allows Atlas Haven users to upload local files, process them into
searchable chunks, and reuse them as context inside AI Chat.

## Current State

- file upload is supported through the `/rag/upload` API
- indexed files can be listed, synced, and deleted
- chunk extraction and local retrieval are functional
- chat replies can incorporate relevant local file context

## Planned State

- stronger file-type support and extraction breadth
- deeper Qdrant-backed vector workflows where appropriate
- job history, indexing diagnostics, and reprocessing controls
- richer citations and source inspection in the chat UI

## API Surface

- `POST /api/rag/upload`
- `GET /api/rag/files`
- `DELETE /api/rag/files`
- `GET /api/rag/active-jobs`
- `GET /api/rag/job-status`
- `POST /api/rag/sync`
- `POST /api/ollama/chat`

## Dependencies And Storage

- `storage/rag`
- `storage/kb_uploads`
- platform DB tables for files, chunks, and jobs
- Ollama and Qdrant-related AI workflows

## Failure Modes

- invalid or unsupported files may upload but not produce useful retrieval chunks
- stale chunk state can misrepresent what the user expects the model to know
- missing model/runtime availability can break the end-to-end KB-to-chat loop

## Acceptance Criteria

- users must be able to upload, list, sync, and remove local knowledge files
- retrieval-assisted chat must visibly use local content when relevant
- KB workflows must remain local-first and operator-understandable
