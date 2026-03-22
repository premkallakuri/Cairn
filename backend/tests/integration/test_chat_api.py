from unittest.mock import MagicMock, patch

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.chat]


def test_chat_suggestions_and_session_crud_flow(client) -> None:
    suggestions = client.get("/api/chat/suggestions")

    assert suggestions.status_code == 200
    assert len(suggestions.json()["suggestions"]) >= 3

    created = client.post(
        "/api/chat/sessions",
        json={"title": "New chat", "model": "llama3.2:1b-text-q2_K"},
    )
    assert created.status_code == 201
    session_id = created.json()["id"]

    added = client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"role": "user", "content": "How do I prepare maps for offline use?"},
    )
    assert added.status_code == 201

    detail = client.get(f"/api/chat/sessions/{session_id}")
    assert detail.status_code == 200
    assert detail.json()["title"].startswith("How do I prepare")
    assert len(detail.json()["messages"]) == 1

    updated = client.put(
        f"/api/chat/sessions/{session_id}",
        json={"title": "Offline maps", "model": "llama3.2:1b-text-q2_K"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Offline maps"

    sessions = client.get("/api/chat/sessions")
    assert sessions.status_code == 200
    assert sessions.json()[0]["lastMessage"] == "How do I prepare maps for offline use?"

    deleted = client.delete(f"/api/chat/sessions/{session_id}")
    assert deleted.status_code == 204
    assert client.get("/api/chat/sessions").json() == []


def test_delete_all_chat_sessions_clears_history(client) -> None:
    client.post("/api/chat/sessions", json={"title": "One", "model": "llama3.2:1b-text-q2_K"})
    client.post("/api/chat/sessions", json={"title": "Two", "model": "llama3.2:1b-text-q2_K"})

    response = client.request("DELETE", "/api/chat/sessions/all")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert client.get("/api/chat/sessions").json() == []


@patch("app.modules.ollama.service.httpx.post")
@patch("app.modules.ollama.service.subprocess.run", return_value=MagicMock(returncode=0))
@patch("app.modules.ollama.service.shutil.which", return_value="/fake/ollama")
def test_ollama_chat_supports_json_and_streaming_responses(
    mock_which, mock_run, mock_post, client,
) -> None:
    class _ChatResp:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "message": {
                    "role": "assistant",
                    "content": "Offline setup needs maps, wikipedia, and ollama.",
                }
            }

    mock_post.return_value = _ChatResp()

    client.post("/api/ollama/models", json={"model": "llama3.2:1b-text-q2_K"})

    payload = {
        "model": "llama3.2:1b-text-q2_K",
        "messages": [{"role": "user", "content": "Summarize offline setup in one paragraph."}],
    }

    response = client.post("/api/ollama/chat", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["done"] is True
    assert body["message"]["role"] == "assistant"
    assert "offline setup" in body["message"]["content"].lower()

    stream_response = client.post("/api/ollama/chat", json={**payload, "stream": True})

    assert stream_response.status_code == 200
    assert stream_response.headers["content-type"].startswith("text/event-stream")
    assert "data:" in stream_response.text
