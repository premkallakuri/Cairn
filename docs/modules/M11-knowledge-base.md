# M11 Knowledge Base

## Scope

- Add upload and indexing routes for local Knowledge Base files
- Extract text from text-like documents and simple PDF text streams
- Persist embedding-job state, indexed files, and searchable chunks
- Expose storage sync and file deletion through the `/rag/*` compatibility routes
- Feed matching local document context into the chat reply path

## Implemented

- `POST /api/rag/upload`
- `GET /api/rag/files`
- `DELETE /api/rag/files`
- `GET /api/rag/active-jobs`
- `GET /api/rag/job-status`
- `POST /api/rag/sync`
- SQL-backed knowledge file, embed job, and chunk tables
- Lexical chunk search and local context assembly
- Chat workspace Knowledge Base panel with upload, sync, and delete actions

## Notes

- This slice uses deterministic local indexing instead of a true vector store callout. It keeps the public contract in place while giving the chat path real local retrieval behavior.
- PDF support is intentionally lightweight and text-stream based for now. It is enough for simple embedded-text PDFs without introducing a heavier parser dependency.
- Qdrant-backed embeddings can replace the local scoring strategy in a later parity pass without changing the current `/rag/*` API shape.
