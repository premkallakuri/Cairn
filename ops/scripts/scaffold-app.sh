#!/bin/sh
set -eu

uv_cache_dir="${UV_CACHE_DIR:-$(pwd)/backend/.uv-cache}"

cd backend
UV_CACHE_DIR="$uv_cache_dir" uv run python -m app.modules.catalog.scaffold "$@"
