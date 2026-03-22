from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from app.core.compat import UTC
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

from app.core.config import get_settings
from app.modules.ollama.schemas import (
    AvailableModelsResponse,
    NomadOllamaModel,
    NomadOllamaModelTag,
    OllamaChatMessage,
    OllamaChatResponse,
)
from app.modules.platform_core.schemas import SuccessMessageResponse

if TYPE_CHECKING:
    from app.modules.cognitive.service import CognitiveService

OLLAMA_TAG_BY_CATALOG_ID: dict[str, str] = {
    "llama3.2:1b-text-q2_K": "llama3.2:1b",
    "llama3.1:8b-text-q4_1": "llama3.1:8b",
    "qwen2.5:3b-instruct-q4_K_M": "qwen2.5:3b",
    "deepseek-r1:1.5b": "deepseek-r1:1.5b",
}


@dataclass(frozen=True, slots=True)
class ModelCatalogEntry:
    id: str
    name: str
    description: str
    estimated_pulls: str
    pulls_rank: int
    model_last_updated: str
    first_seen: str
    recommended: bool
    tags: tuple[NomadOllamaModelTag, ...]


MODEL_LIBRARY: tuple[ModelCatalogEntry, ...] = (
    ModelCatalogEntry(
        id="llama3.2:1b-text-q2_K",
        name="Llama 3.2 1B",
        description="Very small general text model for quick local setup and constrained hardware.",
        estimated_pulls="28M",
        pulls_rank=28_000_000,
        model_last_updated="2026-01-08",
        first_seen="2025-09-14",
        recommended=True,
        tags=(
            NomadOllamaModelTag(
                name="text",
                size="581 MB",
                context="8K",
                input="Text",
                cloud=False,
                thinking=False,
            ),
        ),
    ),
    ModelCatalogEntry(
        id="llama3.1:8b-text-q4_1",
        name="Llama 3.1 8B",
        description="Balanced assistant model for writing, Q&A, and grounded local tasks.",
        estimated_pulls="23M",
        pulls_rank=23_000_000,
        model_last_updated="2025-12-20",
        first_seen="2025-07-03",
        recommended=True,
        tags=(
            NomadOllamaModelTag(
                name="text",
                size="5.1 GB",
                context="128K",
                input="Text",
                cloud=False,
                thinking=False,
            ),
        ),
    ),
    ModelCatalogEntry(
        id="qwen2.5:3b-instruct-q4_K_M",
        name="Qwen 2.5 3B Instruct",
        description=(
            "Responsive multilingual assistant with good small-model quality for local devices."
        ),
        estimated_pulls="14M",
        pulls_rank=14_000_000,
        model_last_updated="2025-11-12",
        first_seen="2025-08-02",
        recommended=True,
        tags=(
            NomadOllamaModelTag(
                name="text",
                size="2.0 GB",
                context="32K",
                input="Text",
                cloud=False,
                thinking=False,
            ),
        ),
    ),
    ModelCatalogEntry(
        id="deepseek-r1:1.5b",
        name="DeepSeek R1 1.5B",
        description="Small reasoning-oriented model for lightweight structured problem solving.",
        estimated_pulls="11M",
        pulls_rank=11_000_000,
        model_last_updated="2025-10-19",
        first_seen="2025-08-28",
        recommended=False,
        tags=(
            NomadOllamaModelTag(
                name="reasoning",
                size="1.1 GB",
                context="32K",
                input="Text",
                cloud=False,
                thinking=True,
            ),
        ),
    ),
)


class OllamaService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._cognitive: CognitiveService | None = None

    @property
    def cognitive(self) -> CognitiveService:
        """Lazy-load the cognitive service so Aura init only happens on first use."""
        if self._cognitive is None:
            from app.modules.cognitive.service import CognitiveService

            self._cognitive = CognitiveService()
        return self._cognitive

    def list_available_models(
        self,
        *,
        sort: str | None = None,
        recommended_only: bool = False,
        query: str | None = None,
        limit: int | None = None,
        force: bool = False,  # noqa: ARG002 - reserved for later live refreshes
    ) -> AvailableModelsResponse:
        models = list(MODEL_LIBRARY)
        if recommended_only:
            models = [model for model in models if model.recommended]
        if query:
            needle = query.lower()
            models = [
                model
                for model in models
                if needle in model.id.lower()
                or needle in model.name.lower()
                or needle in model.description.lower()
            ]

        if sort == "name":
            models.sort(key=lambda model: model.name.lower())
        else:
            models.sort(key=lambda model: model.pulls_rank, reverse=True)

        has_more = limit is not None and len(models) > limit
        if limit is not None:
            models = models[:limit]

        return AvailableModelsResponse(
            models=[self._to_response_model(model) for model in models],
            hasMore=has_more,
        )

    def list_installed_models(self) -> list[dict[str, object]]:
        return self._read_registry()

    def queue_model_download(self, model_name: str) -> SuccessMessageResponse:
        ollama_tag = OLLAMA_TAG_BY_CATALOG_ID.get(model_name)
        if ollama_tag is None:
            return SuccessMessageResponse(
                success=False,
                message=f"Unknown catalog model id: {model_name}",
            )

        registry = self._read_registry()
        if any(item.get("name") == model_name for item in registry):
            return SuccessMessageResponse(
                success=True,
                message=f"Model already tracked: {model_name}",
            )

        catalog_entry = next((item for item in MODEL_LIBRARY if item.id == model_name), None)
        try:
            self._pull_ollama_model(ollama_tag)
        except (RuntimeError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            return SuccessMessageResponse(success=False, message=str(exc))

        registry.append(
            {
                "name": model_name,
                "model": model_name,
                "ollamaTag": ollama_tag,
                "status": "installed",
                "digest": None,
                "size": catalog_entry.tags[0].size if catalog_entry else "Unknown",
                "description": (
                    catalog_entry.description
                    if catalog_entry
                    else "Ollama model installed locally."
                ),
                "storagePath": "",
            }
        )
        self._write_registry(registry)
        return SuccessMessageResponse(
            success=True,
            message=f"Pulled and registered {ollama_tag} via the Ollama CLI.",
        )

    def delete_model(self, model_name: str) -> SuccessMessageResponse:
        ollama_tag = OLLAMA_TAG_BY_CATALOG_ID.get(model_name)
        if ollama_tag is not None:
            self._delete_ollama_model(ollama_tag)
        registry = self._read_registry()
        remaining = [item for item in registry if item.get("name") != model_name]
        self._write_registry(remaining)
        return SuccessMessageResponse(success=True, message=f"Removed local model {model_name}")

    def send_chat(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]] | list[OllamaChatMessage],
    ) -> OllamaChatResponse:
        if not any(item.get("name") == model for item in self._read_registry()):
            raise ValueError(f"Model is not installed locally: {model}")

        normalized_messages = [
            message if isinstance(message, OllamaChatMessage) else OllamaChatMessage(**message)
            for message in messages
        ]
        last_user_message = next(
            (
                message.content
                for message in reversed(normalized_messages)
                if message.role == "user"
            ),
            "Tell me what you need help with.",
        )

        # ── Cognitive recall: inject relevant memories before reply ──
        cognitive_context = self.cognitive.recall_context_for_llm(
            last_user_message, namespace="chat", top_k=3,
        )

        ollama_tag = OLLAMA_TAG_BY_CATALOG_ID.get(model)
        if ollama_tag is None:
            raise ValueError(f"Unknown catalog model id: {model}")

        reply = self._ollama_chat_or_fallback(
            ollama_tag=ollama_tag,
            catalog_id=model,
            messages=normalized_messages,
            cognitive_context=cognitive_context,
            last_user_message=last_user_message,
        )

        # ── Cognitive store: remember the exchange for future recall ──
        self.cognitive.store(
            f"User asked: {last_user_message}",
            namespace="chat",
            metadata={"model": model, "role": "user"},
        )
        self.cognitive.store(
            f"Assistant replied: {reply[:300]}",
            namespace="chat",
            metadata={"model": model, "role": "assistant"},
        )

        return OllamaChatResponse(
            model=model,
            created_at=datetime.now(UTC).isoformat(),
            message=OllamaChatMessage(role="assistant", content=reply),
            done=True,
        )

    def stream_chat(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]] | list[OllamaChatMessage],
    ) -> list[str]:
        response = self.send_chat(model=model, messages=messages)
        words = response.message.content.split()
        chunks = [" ".join(words[index : index + 4]) for index in range(0, len(words), 4)] or [
            response.message.content
        ]

        events: list[str] = []
        for chunk in chunks:
            payload = {
                "model": model,
                "created_at": response.created_at,
                "message": {"role": "assistant", "content": chunk},
                "done": False,
            }
            events.append(f"data: {json.dumps(payload)}\n\n")
        final_payload = response.model_dump(mode="json")
        events.append(f"data: {json.dumps(final_payload)}\n\n")
        return events

    def _registry_path(self) -> Path:
        return self.settings.storage_path / "ollama" / "installed-models.json"

    def _read_registry(self) -> list[dict[str, object]]:
        path = self._registry_path()
        if not path.exists():
            return []
        return json.loads(path.read_text())

    def _write_registry(self, payload: list[dict[str, object]]) -> None:
        path = self._registry_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2))

    def _pull_ollama_model(self, ollama_tag: str) -> None:
        if shutil.which("ollama") is None:
            raise RuntimeError(
                "The 'ollama' executable was not found on PATH. Install from https://ollama.com "
                "and ensure the CLI is available."
            )
        subprocess.run(
            ["ollama", "pull", ollama_tag],
            check=True,
            timeout=7200,
        )

    def _delete_ollama_model(self, ollama_tag: str) -> None:
        if shutil.which("ollama") is None:
            return
        subprocess.run(
            ["ollama", "rm", ollama_tag],
            check=False,
            timeout=300,
        )

    def _ollama_chat_or_fallback(
        self,
        *,
        ollama_tag: str,
        catalog_id: str,
        messages: list[OllamaChatMessage],
        cognitive_context: str,
        last_user_message: str,
    ) -> str:
        base = self.settings.ollama_base_url.rstrip("/")
        payload = {
            "model": ollama_tag,
            "messages": [message.model_dump() for message in messages],
            "stream": False,
        }
        try:
            response = httpx.post(f"{base}/api/chat", json=payload, timeout=300.0)
            response.raise_for_status()
            data = response.json()
            content = data.get("message", {}).get("content")
            if isinstance(content, str) and content.strip():
                return content
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            pass

        return self._build_local_reply(
            model=catalog_id,
            prompt=last_user_message,
            cognitive_context=cognitive_context,
        )

    def _build_local_reply(
        self, *, model: str, prompt: str, cognitive_context: str = "",
    ) -> str:
        prompt_excerpt = " ".join(prompt.strip().split()[:20]).rstrip(".")
        knowledge_context = self._build_knowledge_context(prompt)

        parts = [
            f"Cairn local response from {model}: {prompt_excerpt}.",
            "This compatibility path is wired through the local Ollama API surface and "
            "is ready for a live runtime adapter in a later module.",
        ]
        if cognitive_context:
            parts.append(f"Cognitive recall: {cognitive_context}")
        if knowledge_context:
            parts.append(knowledge_context)

        return " ".join(parts)

    def _build_knowledge_context(self, prompt: str) -> str:
        from app.modules.knowledge_base.service import KnowledgeBaseService

        context = KnowledgeBaseService().assemble_context(prompt)
        if not context:
            return ""
        return f" {context}"

    def _to_response_model(self, model: ModelCatalogEntry) -> NomadOllamaModel:
        return NomadOllamaModel(
            id=model.id,
            name=model.name,
            description=model.description,
            estimated_pulls=model.estimated_pulls,
            model_last_updated=model.model_last_updated,
            first_seen=model.first_seen,
            tags=list(model.tags),
        )
