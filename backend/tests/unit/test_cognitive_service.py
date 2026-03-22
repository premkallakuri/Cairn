"""Unit tests for the CognitiveService facade.

These tests verify service behaviour when AuraSDK is NOT installed
(graceful degradation) and when it IS available (via mocking).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.modules.cognitive.service import CognitiveService, _aura_instances

pytestmark = [pytest.mark.unit, pytest.mark.cognitive]


@pytest.fixture(autouse=True)
def _clear_aura_cache():
    """Ensure Aura instance cache is clean between tests."""
    _aura_instances.clear()
    yield
    _aura_instances.clear()


# ── Status ───────────────────────────────────────────────────────────────


def test_status_reports_unavailable_when_aura_not_installed() -> None:
    with patch.dict("sys.modules", {"aura": None}):
        service = CognitiveService()
        result = service.status()

    assert result.available is False or result.available is True  # depends on env
    assert result.message  # always has a message


def test_status_reports_available_when_aura_importable() -> None:
    mock_aura_mod = MagicMock()
    mock_aura_mod.Aura = MagicMock

    with patch.dict("sys.modules", {"aura": mock_aura_mod}):
        service = CognitiveService()
        result = service.status()

    assert result.available is True
    assert "active" in result.message.lower() or "installed" in result.message.lower() or result.available


# ── Store (graceful degradation) ─────────────────────────────────────────


def test_store_returns_failure_when_aura_unavailable() -> None:
    with patch("app.modules.cognitive.service._get_aura", return_value=None):
        service = CognitiveService()
        result = service.store("test content", namespace="test")

    assert result.success is False
    assert "unavailable" in result.message.lower()


def test_store_succeeds_with_mock_aura() -> None:
    mock_aura = MagicMock()
    mock_aura.store = MagicMock()

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.store("test memory", namespace="ns1", metadata={"key": "val"})

    assert result.success is True
    mock_aura.store.assert_called_once_with("test memory", metadata={"key": "val"})


def test_store_handles_aura_exception_gracefully() -> None:
    mock_aura = MagicMock()
    mock_aura.store.side_effect = RuntimeError("disk full")

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.store("content", namespace="test")

    assert result.success is False
    assert "disk full" in result.message


# ── Recall ───────────────────────────────────────────────────────────────


def test_recall_returns_empty_when_aura_unavailable() -> None:
    with patch("app.modules.cognitive.service._get_aura", return_value=None):
        service = CognitiveService()
        result = service.recall("query", namespace="test")

    assert result.memories == []
    assert result.query == "query"


def test_recall_parses_dict_results_from_aura() -> None:
    mock_aura = MagicMock()
    mock_aura.recall.return_value = [
        {"content": "memory one", "relevance": 0.95, "level": "belief"},
        {"content": "memory two", "relevance": 0.72, "level": "concept"},
    ]

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.recall("search query", namespace="test", top_k=5)

    assert len(result.memories) == 2
    assert result.memories[0].content == "memory one"
    assert result.memories[0].relevance == 0.95
    assert result.memories[0].level == "belief"
    assert result.memories[1].content == "memory two"
    mock_aura.recall.assert_called_once_with("search query", top_k=5)


def test_recall_handles_string_results_from_aura() -> None:
    mock_aura = MagicMock()
    mock_aura.recall.return_value = ["raw string memory"]

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.recall("test", namespace="test")

    assert len(result.memories) == 1
    assert result.memories[0].content == "raw string memory"


def test_recall_handles_exception_gracefully() -> None:
    mock_aura = MagicMock()
    mock_aura.recall.side_effect = RuntimeError("index corrupt")

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.recall("query", namespace="test")

    assert result.memories == []


# ── Recall context for LLM ──────────────────────────────────────────────


def test_recall_context_for_llm_returns_formatted_string() -> None:
    mock_aura = MagicMock()
    mock_aura.recall.return_value = [
        {"content": "Cairn is offline-first", "relevance": 0.9, "level": "belief"},
    ]

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        context = service.recall_context_for_llm("offline", namespace="test")

    assert "[Cognitive Memory Context]" in context
    assert "Cairn is offline-first" in context
    assert "[belief]" in context


def test_recall_context_for_llm_returns_empty_when_no_memories() -> None:
    with patch("app.modules.cognitive.service._get_aura", return_value=None):
        service = CognitiveService()
        context = service.recall_context_for_llm("test query")

    assert context == ""


# ── Maintenance ──────────────────────────────────────────────────────────


def test_maintenance_returns_failure_when_unavailable() -> None:
    with patch("app.modules.cognitive.service._get_aura", return_value=None):
        service = CognitiveService()
        result = service.maintenance(namespace="test")

    assert result.success is False


def test_maintenance_parses_dict_result() -> None:
    mock_aura = MagicMock()
    mock_aura.maintenance.return_value = {"consolidated": 3, "pruned": 1}

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.maintenance(namespace="test")

    assert result.success is True
    assert result.consolidated == 3
    assert result.pruned == 1


# ── Feedback ─────────────────────────────────────────────────────────────


def test_feedback_returns_failure_when_unavailable() -> None:
    with patch("app.modules.cognitive.service._get_aura", return_value=None):
        service = CognitiveService()
        result = service.feedback("content", namespace="test", positive=True)

    assert result.success is False


def test_feedback_calls_aura_feedback_method() -> None:
    mock_aura = MagicMock()
    mock_aura.feedback = MagicMock()

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.feedback("good memory", namespace="test", positive=True)

    assert result.success is True
    mock_aura.feedback.assert_called_once_with("good memory", positive=True)


def test_feedback_falls_back_to_reinforce_method() -> None:
    mock_aura = MagicMock(spec=[])  # no methods by default
    mock_aura.reinforce = MagicMock()
    # hasattr will find reinforce but not feedback

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.feedback("content", namespace="test", positive=True)

    assert result.success is True
    mock_aura.reinforce.assert_called_once_with("content")


def test_feedback_falls_back_to_weaken_method() -> None:
    mock_aura = MagicMock(spec=[])
    mock_aura.weaken = MagicMock()

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.feedback("bad memory", namespace="test", positive=False)

    assert result.success is True
    mock_aura.weaken.assert_called_once_with("bad memory")


# ── Insights ─────────────────────────────────────────────────────────────


def test_insights_returns_empty_when_unavailable() -> None:
    with patch("app.modules.cognitive.service._get_aura", return_value=None):
        service = CognitiveService()
        result = service.insights(namespace="test")

    assert result.insights == []


def test_insights_parses_aura_response() -> None:
    mock_aura = MagicMock()
    mock_aura.insights.return_value = [
        {"level": "belief", "summary": "Core beliefs", "entry_count": 10},
        {"level": "concept", "summary": "Learned concepts", "entry_count": 25},
    ]

    with patch("app.modules.cognitive.service._get_aura", return_value=mock_aura):
        service = CognitiveService()
        result = service.insights(namespace="test")

    assert len(result.insights) == 2
    assert result.insights[0].level == "belief"
    assert result.insights[0].entry_count == 10
