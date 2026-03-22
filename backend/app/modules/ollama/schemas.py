from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class NomadOllamaModelTag(BaseModel):
    name: str
    size: str
    context: str
    input: str
    cloud: bool
    thinking: bool


class NomadOllamaModel(BaseModel):
    id: str
    name: str
    description: str
    estimated_pulls: str
    model_last_updated: str
    first_seen: str
    tags: list[NomadOllamaModelTag]


class AvailableModelsResponse(BaseModel):
    models: list[NomadOllamaModel]
    hasMore: bool


class ModelNameRequest(BaseModel):
    model: str


class OllamaChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    thinking: str | None = None


class OllamaChatRequest(BaseModel):
    model: str
    messages: list[OllamaChatMessage]
    stream: bool = False
    sessionId: int | None = None


class OllamaChatResponse(BaseModel):
    model: str
    created_at: str
    message: OllamaChatMessage
    done: bool
