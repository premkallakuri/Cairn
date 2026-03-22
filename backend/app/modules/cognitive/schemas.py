from __future__ import annotations

from pydantic import BaseModel, Field


class MemoryStoreRequest(BaseModel):
    """Store a cognitive memory entry."""

    content: str = Field(..., min_length=1, description="The content to commit to cognitive memory.")
    namespace: str = Field(
        default="default",
        description="Namespace to isolate memory domains (e.g., per-user, per-topic).",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Optional metadata tags for the memory entry.",
    )


class MemoryStoreResponse(BaseModel):
    success: bool = True
    message: str
    namespace: str


class MemoryRecallRequest(BaseModel):
    """Recall memories relevant to a query."""

    query: str = Field(..., min_length=1, description="The query to recall memories for.")
    namespace: str = Field(default="default")
    top_k: int = Field(default=5, ge=1, le=50, description="Max number of memories to return.")


class MemoryEntry(BaseModel):
    content: str
    relevance: float = Field(ge=0.0, le=1.0)
    level: str
    namespace: str


class MemoryRecallResponse(BaseModel):
    memories: list[MemoryEntry]
    query: str
    namespace: str


class MaintenanceResponse(BaseModel):
    success: bool = True
    message: str
    consolidated: int = 0
    pruned: int = 0


class CognitiveInsight(BaseModel):
    level: str
    summary: str
    entry_count: int


class InsightsResponse(BaseModel):
    namespace: str
    insights: list[CognitiveInsight]


class FeedbackRequest(BaseModel):
    """Provide feedback to reinforce or weaken a memory."""

    content: str = Field(..., min_length=1)
    namespace: str = Field(default="default")
    positive: bool = Field(default=True, description="True to reinforce, False to weaken.")


class FeedbackResponse(BaseModel):
    success: bool = True
    message: str


class CognitiveStatusResponse(BaseModel):
    available: bool
    version: str | None = None
    namespaces: list[str] = []
    message: str
