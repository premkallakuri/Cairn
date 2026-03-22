import pytest

from app.main import create_app

pytestmark = [pytest.mark.contract]


def test_openapi_exposes_first_wave_routes() -> None:
    schema = create_app().openapi()
    paths = schema["paths"]

    assert "/api/health" in paths
    assert "/api/system/info" in paths
    assert "/api/system/internet-status" in paths
    assert "/api/system/subscribe-release-notes" in paths
    assert "/api/system/latest-version" in paths
    assert "/api/system/update" in paths
    assert "/api/system/update/status" in paths
    assert "/api/system/update/logs" in paths
    assert "/api/system/settings" in paths
    assert "/api/manifests/refresh" in paths
    assert "/api/content-updates/check" in paths
    assert "/api/content-updates/apply" in paths
    assert "/api/content-updates/apply-all" in paths
    assert "/api/system/services" in paths
    assert "/api/system/services/force-reinstall" in paths
    assert "/api/system/services/check-updates" in paths
    assert "/api/system/services/{name}/available-versions" in paths
    assert "/api/system/services/update" in paths
    assert "/api/downloads/jobs" in paths
    assert "/api/downloads/jobs/{filetype}" in paths
    assert "/api/benchmark/run" in paths
    assert "/api/benchmark/run/system" in paths
    assert "/api/benchmark/run/ai" in paths
    assert "/api/benchmark/results" in paths
    assert "/api/benchmark/results/latest" in paths
    assert "/api/benchmark/results/{id}" in paths
    assert "/api/benchmark/submit" in paths
    assert "/api/benchmark/builder-tag" in paths
    assert "/api/benchmark/comparison" in paths
    assert "/api/benchmark/status" in paths
    assert "/api/benchmark/settings" in paths
    assert "/api/ollama/models" in paths
    assert "/api/ollama/installed-models" in paths
    assert "/api/ollama/chat" in paths
    assert "/api/chat/suggestions" in paths
    assert "/api/chat/sessions" in paths
    assert "/api/chat/sessions/all" in paths
    assert "/api/chat/sessions/{id}" in paths
    assert "/api/chat/sessions/{id}/messages" in paths
    assert "/api/rag/upload" in paths
    assert "/api/rag/files" in paths
    assert "/api/rag/active-jobs" in paths
    assert "/api/rag/job-status" in paths
    assert "/api/rag/sync" in paths
    assert "/api/docs/list" in paths
    assert "/api/easy-setup/curated-categories" in paths
    assert "/api/easy-setup/bootstrap" in paths
    assert "/api/easy-setup/draft" in paths
    assert "/api/easy-setup/plan" in paths
    assert "/api/maps/regions" in paths
    assert "/api/maps/styles" in paths
    assert "/api/maps/curated-collections" in paths
    assert "/api/maps/fetch-latest-collections" in paths
    assert "/api/maps/download-base-assets" in paths
    assert "/api/maps/download-remote" in paths
    assert "/api/maps/download-remote-preflight" in paths
    assert "/api/maps/download-collection" in paths
    assert "/api/maps/{filename}" in paths
    assert "/api/zim/list" in paths
    assert "/api/zim/list-remote" in paths
    assert "/api/zim/curated-categories" in paths
    assert "/api/zim/download-remote" in paths
    assert "/api/zim/download-category-tier" in paths
    assert "/api/zim/wikipedia" in paths
    assert "/api/zim/wikipedia/select" in paths
    assert "/api/zim/{filename}" in paths
    assert "/api/system/services/affect" in paths
    assert "/api/system/services/install" in paths

    # Cognitive memory endpoints (AuraSDK)
    assert "/api/cognitive/status" in paths
    assert "/api/cognitive/store" in paths
    assert "/api/cognitive/recall" in paths
    assert "/api/cognitive/maintenance" in paths
    assert "/api/cognitive/insights" in paths
    assert "/api/cognitive/feedback" in paths


def test_openapi_title_matches_cairn_api() -> None:
    schema = create_app().openapi()

    assert schema["info"]["title"] == "Cairn API"


def test_openapi_tags_cover_all_modules() -> None:
    schema = create_app().openapi()
    tag_names = {tag["name"] for tag in schema.get("tags", [])}

    expected_tags = {
        "platform", "chat", "cognitive", "ollama", "benchmark",
        "knowledge-base", "maps", "zim", "easy-setup",
        "content-updates", "downloads", "docs",
    }
    assert expected_tags.issubset(tag_names), f"Missing tags: {expected_tags - tag_names}"
