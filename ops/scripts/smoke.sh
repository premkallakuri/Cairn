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

docker compose -f compose.yaml config > /dev/null

case "$module" in
  M00)
    echo "M00 smoke passed"
    ;;
  M01|M02|M03|M04|all)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_health_api.py -q
    ;;
  M05)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_download_api.py -q
    ;;
  M06)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_easy_setup_api.py -q
    ;;
  M07)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_zim_api.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/kiwix/tests/test_smoke.py -q
    ;;
  M08)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_maps_api.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/maps/tests/test_smoke.py -q
    ;;
  M09)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_ollama_api.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/ollama/tests/test_smoke.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/qdrant/tests/test_smoke.py -q
    ;;
  M10)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_chat_api.py -q
    ;;
  M11)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_rag_api.py -q
    ;;
  M12)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_system_service_api.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/flatnotes/tests/test_smoke.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/cyberchef/tests/test_smoke.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/kolibri/tests/test_smoke.py -q
    ;;
  M13)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/integration/test_benchmark_api.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/benchmark-helper/tests/test_smoke.py -q
    ;;
  M14)
    cd backend
    UV_CACHE_DIR="$uv_cache_dir" uv run pytest tests/unit/test_manifest_catalog.py tests/unit/test_orchestration_service.py tests/unit/test_catalog_scaffold.py -q
    PYTHONPATH=. UV_CACHE_DIR="$uv_cache_dir" uv run pytest ../apps/sample-notes/tests/test_smoke.py -q
    ;;
  all-modules)
    for m in M00 M01 M02 M03 M04 M05 M06 M07 M08 M09 M10 M11 M12 M13 M14; do
      echo "smoke: $m"
      "$script_dir/smoke.sh" "$m"
    done
    ;;
  *)
    echo "Unknown module: $module" >&2
    exit 1
    ;;
esac
