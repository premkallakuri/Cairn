from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SuggestionsResponse(BaseModel):
    suggestions: list[str]


class ChatSessionSummary(BaseModel):
    id: int
    title: str
    model: str | None = None
    timestamp: str | None = None
    lastMessage: str | None = None


class ChatMessage(BaseModel):
    id: int
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: str


class ChatSessionDetail(BaseModel):
    id: int
    title: str
    model: str | None = None
    timestamp: str | None = None
    messages: list[ChatMessage]


class CreateChatSessionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    model: str | None = None


class UpdateChatSessionRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    model: str | None = None


class ChatSessionCreateResponse(BaseModel):
    id: int
    title: str
    model: str | None = None
    timestamp: str | None = None


class AddChatMessageRequest(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)
