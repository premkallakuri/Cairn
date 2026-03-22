#!/bin/sh
set -eu

module="${1:-all}"
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
project_root="$(CDPATH= cd -- "$script_dir/../.." && pwd)"
project_root="${PROJECT_ROOT:-$project_root}"
export PROJECT_ROOT="$project_root"
export NOMAD_STORAGE_PATH="${NOMAD_STORAGE_PATH:-$project_root/storage}"
uv_cache_dir="${UV_CACHE_DIR:-$project_root/backend/.uv-cache}"

cd "$project_root"

case "$module" in
  M00)
    docker compose -f compose.yaml config > /dev/null
    ;;
  M01)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_settings.py tests/integration/test_health_api.py -q
    ;;
  M02)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_manifest_catalog.py tests/contract/test_openapi_contract.py -q
    ;;
  M03)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_orchestration_service.py -q
    ;;
  M04)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_health_api.py tests/contract/test_openapi_contract.py -q
    ;;
  M05)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_download_jobs.py tests/integration/test_download_api.py tests/contract/test_openapi_contract.py -q
    ;;
  M06)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_easy_setup_service.py tests/integration/test_easy_setup_api.py tests/contract/test_openapi_contract.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M07)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_zim_service.py tests/unit/test_kiwix_hook.py tests/integration/test_zim_api.py tests/contract/test_openapi_contract.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/kiwix/tests/test_smoke.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M08)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_map_service.py tests/integration/test_maps_api.py tests/contract/test_openapi_contract.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/maps/tests/test_smoke.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M09)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_ollama_service.py tests/integration/test_ollama_api.py tests/contract/test_openapi_contract.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/ollama/tests/test_smoke.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/qdrant/tests/test_smoke.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M10)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_chat_service.py tests/integration/test_chat_api.py tests/contract/test_openapi_contract.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M11)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_knowledge_base_service.py tests/integration/test_rag_api.py tests/contract/test_openapi_contract.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M12)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_system_service_manager.py tests/integration/test_system_service_api.py tests/contract/test_openapi_contract.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/flatnotes/tests/test_smoke.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/cyberchef/tests/test_smoke.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/kolibri/tests/test_smoke.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M13)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_benchmark_service.py tests/integration/test_benchmark_api.py tests/contract/test_openapi_contract.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/benchmark-helper/tests/test_smoke.py -q
    cd ../frontend
    pnpm typecheck
    ;;
  M14)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_manifest_catalog.py tests/unit/test_orchestration_service.py tests/unit/test_catalog_scaffold.py tests/contract/test_openapi_contract.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/sample-notes/tests/test_smoke.py -q
    ;;
  all)
    make test-unit
    make test-contract
    make test-integration
    ;;
  *)
    echo "Unknown module: $module" >&2
    exit 1
    ;;
esac
