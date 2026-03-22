import pytest

pytestmark = [pytest.mark.integration, pytest.mark.benchmark]


def test_benchmark_run_results_and_status_endpoints(client) -> None:
    response = client.post("/api/benchmark/run?sync=true", json={"benchmark_type": "full"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    benchmark_id = payload["benchmark_id"]

    results = client.get("/api/benchmark/results")
    assert results.status_code == 200
    assert results.json()["total"] == 1

    latest = client.get("/api/benchmark/results/latest")
    assert latest.status_code == 200
    assert latest.json()["result"]["benchmark_id"] == benchmark_id

    status = client.get("/api/benchmark/status")
    assert status.status_code == 200
    assert status.json()["status"] == "completed"


def test_benchmark_submit_builder_tag_and_settings_endpoints(client) -> None:
    created = client.post("/api/benchmark/run?sync=true", json={"benchmark_type": "ai"}).json()
    benchmark_id = created["benchmark_id"]

    submitted = client.post("/api/benchmark/submit", json={"benchmark_id": benchmark_id})
    assert submitted.status_code == 200
    assert submitted.json()["repository_id"].startswith("repo-")

    builder = client.post(
        "/api/benchmark/builder-tag",
        json={"benchmark_id": benchmark_id, "builder_tag": "Atlas-Haven-2026"},
    )
    assert builder.status_code == 200
    assert builder.json()["builder_tag"] == "Atlas-Haven-2026"

    settings = client.get("/api/benchmark/settings")
    assert settings.status_code == 200
    assert "installation_id" in settings.json()

    updated = client.post("/api/benchmark/settings", json={"allow_anonymous_submission": True})
    assert updated.status_code == 200
    assert updated.json()["settings"]["allow_anonymous_submission"] is True


def test_benchmark_run_system_and_ai_endpoints(client) -> None:
    system = client.post("/api/benchmark/run/system")
    ai = client.post("/api/benchmark/run/ai")

    assert system.status_code == 200
    assert ai.status_code == 200
    assert system.json()["message"] == "System benchmark queued"
    assert ai.json()["message"] == "AI benchmark queued"


def test_benchmark_comparison_endpoint_returns_stats(client) -> None:
    client.post("/api/benchmark/run?sync=true", json={"benchmark_type": "full"})

    comparison = client.get("/api/benchmark/comparison")
    assert comparison.status_code == 200
    assert comparison.json()["stats"]["total_submissions"] == 1
