#!/usr/bin/env bash
# Fetch Wikipedia (ZIM), map base assets + optional PMTiles, and pull a small Ollama model.
# Prerequisites: Redis on localhost:6379, API on 127.0.0.1:8000, ARQ worker running,
# and Ollama installed (https://ollama.com) for the LLM step.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API="${CAIRN_API_BASE:-http://127.0.0.1:8000}"

echo "==> Map base assets (local style template + sprites)"
curl -fsS -X POST "$API/api/maps/download-base-assets" \
  -H 'Content-Type: application/json' \
  -d '{}' | cat

echo
echo "==> Wikipedia ZIM (English 100 mini from Kiwix mirror, ~4.5MB+)"
curl -fsS -X POST "$API/api/zim/wikipedia/select" \
  -H 'Content-Type: application/json' \
  -d '{"optionId":"en-100-mini-remote"}' | cat

echo
if [[ -n "${CAIRN_PMTILES_URL:-}" ]]; then
  echo "==> Map region from CAIRN_PMTILES_URL"
  curl -fsS -X POST "$API/api/maps/download-remote" \
    -H 'Content-Type: application/json' \
    -d "{\"url\":\"$CAIRN_PMTILES_URL\"}" | cat
  echo
else
  echo "==> Skipping extra PMTiles (set CAIRN_PMTILES_URL to a .pmtiles HTTPS URL to queue one)"
fi

echo
echo "==> LLM: pull Llama 3.2 1B via Ollama (also registers it in Cairn)"
curl -fsS -X POST "$API/api/ollama/models" \
  -H 'Content-Type: application/json' \
  -d '{"model":"llama3.2:1b-text-q2_K"}' | cat

echo
echo "Done. Ensure Redis + 'uv run python -m app.shared.worker' are running so downloads complete."
