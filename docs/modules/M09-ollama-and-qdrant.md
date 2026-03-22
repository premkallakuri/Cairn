# M09 Ollama And Qdrant

## Scope

- Add a first compatible Ollama API surface for available models, local inventory, queue, and delete
- Add dependency-aware service installation so `nomad_ollama` installs `nomad_qdrant` first
- Expose service start and stop actions through the system routes
- Surface the new model state on the `AI Chat` page without pulling full session CRUD in early

## Implemented

- `GET /api/ollama/models`
- `POST /api/ollama/models`
- `DELETE /api/ollama/models`
- `GET /api/ollama/installed-models`
- `POST /api/system/services/install`
- `POST /api/system/services/affect`
- Local Ollama inventory persisted under `storage/ollama/installed-models.json`
- Model pull jobs queued through the shared downloads module as `filetype=model`
- `AI Chat` now shows recommended models and tracked local pulls

## Notes

- This module intentionally uses a local model registry file instead of a live Ollama runtime query.
- The system service adapter still updates catalog state, not Docker containers. Real container execution stays for later orchestration slices.
- The next module will build on this runtime shelf instead of reintroducing model catalog logic elsewhere.
