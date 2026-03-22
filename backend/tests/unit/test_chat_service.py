import pytest

from app.modules.chat.service import ChatService
from app.modules.ollama.service import OllamaService

pytestmark = [pytest.mark.unit, pytest.mark.chat]


def test_first_user_message_generates_session_title() -> None:
    service = ChatService()

    created = service.create_session(title="New chat", model="llama3.2:1b-text-q2_K")
    message = service.add_message(
        created.id,
        role="user",
        content="How do I set up offline maps for the Pacific region?",
    )
    detail = service.get_session(created.id)

    assert message.role == "user"
    assert detail.title.startswith("How do I set up")
    assert len(detail.messages) == 1


def test_list_sessions_returns_latest_first_with_last_message() -> None:
    service = ChatService()

    first = service.create_session(title="First chat", model="llama3.2:1b-text-q2_K")
    service.add_message(first.id, role="user", content="First note")
    second = service.create_session(title="Second chat", model="llama3.2:1b-text-q2_K")
    service.add_message(second.id, role="user", content="Second note")

    sessions = service.list_sessions()

    assert [session.id for session in sessions] == [second.id, first.id]
    assert sessions[0].lastMessage == "Second note"


def test_local_ollama_chat_response_uses_installed_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(OllamaService, "_pull_ollama_model", lambda self, tag: None)
    monkeypatch.setattr(
        OllamaService,
        "_ollama_chat_or_fallback",
        lambda self, **kwargs: (
            "Survival checklist: shelter, water, food, fire, and signal. "
            "Plan for warmth and communication."
        ),
    )
    ollama = OllamaService()
    ollama.queue_model_download("llama3.2:1b-text-q2_K")

    response = ollama.send_chat(
        model="llama3.2:1b-text-q2_K",
        messages=[{"role": "user", "content": "Give me a quick survival checklist."}],
    )

    assert response.model == "llama3.2:1b-text-q2_K"
    assert response.done is True
    assert response.message.role == "assistant"
    assert "survival checklist" in response.message.content.lower()
