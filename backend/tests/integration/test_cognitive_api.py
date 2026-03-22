"""End-to-end integration tests for the cognitive memory API (/api/cognitive).

AuraSDK may or may not be installed in the test environment.  These tests
verify that every endpoint responds with valid JSON and correct HTTP status
regardless of whether the underlying Aura library is available.
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.cognitive]


# ── Status ───────────────────────────────────────────────────────────────


def test_cognitive_status_returns_availability_info(client) -> None:
    response = client.get("/api/cognitive/status")

    assert response.status_code == 200
    payload = response.json()
    assert "available" in payload
    assert isinstance(payload["available"], bool)
    assert "message" in payload


# ── Store ────────────────────────────────────────────────────────────────


def test_cognitive_store_accepts_valid_payload(client) -> None:
    response = client.post(
        "/api/cognitive/store",
        json={
            "content": "The capital of France is Paris.",
            "namespace": "test",
            "metadata": {"source": "unit-test"},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "success" in payload
    assert payload["namespace"] == "test"


def test_cognitive_store_rejects_empty_content(client) -> None:
    response = client.post(
        "/api/cognitive/store",
        json={"content": "", "namespace": "test"},
    )

    assert response.status_code == 422


def test_cognitive_store_uses_default_namespace(client) -> None:
    response = client.post(
        "/api/cognitive/store",
        json={"content": "Some memory to store."},
    )

    assert response.status_code == 200
    assert response.json()["namespace"] == "default"


# ── Recall ───────────────────────────────────────────────────────────────


def test_cognitive_recall_returns_memories_list(client) -> None:
    response = client.post(
        "/api/cognitive/recall",
        json={"query": "What is the capital of France?", "namespace": "test"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["memories"], list)
    assert payload["query"] == "What is the capital of France?"
    assert payload["namespace"] == "test"


def test_cognitive_recall_rejects_empty_query(client) -> None:
    response = client.post(
        "/api/cognitive/recall",
        json={"query": ""},
    )

    assert response.status_code == 422


def test_cognitive_recall_respects_top_k_bounds(client) -> None:
    response = client.post(
        "/api/cognitive/recall",
        json={"query": "test", "top_k": 0},
    )
    assert response.status_code == 422

    response = client.post(
        "/api/cognitive/recall",
        json={"query": "test", "top_k": 100},
    )
    assert response.status_code == 422


# ── Maintenance ──────────────────────────────────────────────────────────


def test_cognitive_maintenance_endpoint_responds(client) -> None:
    response = client.post("/api/cognitive/maintenance")

    assert response.status_code == 200
    payload = response.json()
    assert "success" in payload
    assert "message" in payload


def test_cognitive_maintenance_accepts_namespace_param(client) -> None:
    response = client.post("/api/cognitive/maintenance?namespace=custom")

    assert response.status_code == 200


# ── Insights ─────────────────────────────────────────────────────────────


def test_cognitive_insights_returns_list(client) -> None:
    response = client.get("/api/cognitive/insights")

    assert response.status_code == 200
    payload = response.json()
    assert "insights" in payload
    assert isinstance(payload["insights"], list)
    assert payload["namespace"] == "default"


def test_cognitive_insights_accepts_namespace_param(client) -> None:
    response = client.get("/api/cognitive/insights?namespace=research")

    assert response.status_code == 200
    assert response.json()["namespace"] == "research"


# ── Feedback ─────────────────────────────────────────────────────────────


def test_cognitive_feedback_reinforce(client) -> None:
    response = client.post(
        "/api/cognitive/feedback",
        json={
            "content": "The capital of France is Paris.",
            "namespace": "test",
            "positive": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "success" in payload
    assert "message" in payload


def test_cognitive_feedback_weaken(client) -> None:
    response = client.post(
        "/api/cognitive/feedback",
        json={
            "content": "Incorrect fact to weaken.",
            "namespace": "test",
            "positive": False,
        },
    )

    assert response.status_code == 200


def test_cognitive_feedback_rejects_empty_content(client) -> None:
    response = client.post(
        "/api/cognitive/feedback",
        json={"content": ""},
    )

    assert response.status_code == 422


# ── Full round-trip: store → recall → feedback ───────────────────────────


def test_cognitive_store_recall_feedback_roundtrip(client) -> None:
    """Walk through the full cognitive lifecycle via HTTP."""
    # 1. Store
    store_resp = client.post(
        "/api/cognitive/store",
        json={
            "content": "Cairn supports offline knowledge management.",
            "namespace": "roundtrip",
        },
    )
    assert store_resp.status_code == 200

    # 2. Recall
    recall_resp = client.post(
        "/api/cognitive/recall",
        json={"query": "offline knowledge", "namespace": "roundtrip", "top_k": 3},
    )
    assert recall_resp.status_code == 200
    assert isinstance(recall_resp.json()["memories"], list)

    # 3. Feedback
    feedback_resp = client.post(
        "/api/cognitive/feedback",
        json={
            "content": "Cairn supports offline knowledge management.",
            "namespace": "roundtrip",
            "positive": True,
        },
    )
    assert feedback_resp.status_code == 200

    # 4. Maintenance
    maint_resp = client.post("/api/cognitive/maintenance?namespace=roundtrip")
    assert maint_resp.status_code == 200

    # 5. Insights
    insights_resp = client.get("/api/cognitive/insights?namespace=roundtrip")
    assert insights_resp.status_code == 200
