MODULE ?= all
UV_CACHE_DIR ?= $(CURDIR)/backend/.uv-cache

.PHONY: bootstrap bootstrap-backend bootstrap-frontend lint lint-backend lint-frontend test-unit test-contract test-integration test-module smoke smoke-all-modules docker-config

bootstrap: bootstrap-backend bootstrap-frontend

bootstrap-backend:
	cd backend && UV_CACHE_DIR=$(UV_CACHE_DIR) uv sync

bootstrap-frontend:
	cd frontend && pnpm install

lint: lint-backend lint-frontend

lint-backend:
	cd backend && UV_CACHE_DIR=$(UV_CACHE_DIR) uv run ruff check . && UV_CACHE_DIR=$(UV_CACHE_DIR) uv run ruff format --check .

lint-frontend:
	cd frontend && pnpm lint && pnpm typecheck

test-unit:
	cd backend && UV_CACHE_DIR=$(UV_CACHE_DIR) uv run pytest tests/unit -q

test-contract:
	cd backend && UV_CACHE_DIR=$(UV_CACHE_DIR) uv run pytest tests/contract -q

test-integration:
	cd backend && UV_CACHE_DIR=$(UV_CACHE_DIR) uv run pytest tests/integration -q

test-module:
	./ops/scripts/run-module-tests.sh $(MODULE)

smoke:
	./ops/scripts/smoke.sh $(MODULE)

smoke-all-modules:
	./ops/scripts/smoke.sh all-modules

docker-config:
	docker compose -f compose.yaml config > /dev/null
