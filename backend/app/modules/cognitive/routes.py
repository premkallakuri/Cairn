"""Cognitive memory API routes.

Exposes AuraSDK's five-layer cognitive stack through REST endpoints.
All operations are local and require no external API keys.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.modules.cognitive.schemas import (
    CognitiveStatusResponse,
    FeedbackRequest,
    FeedbackResponse,
    InsightsResponse,
    MaintenanceResponse,
    MemoryRecallRequest,
    MemoryRecallResponse,
    MemoryStoreRequest,
    MemoryStoreResponse,
)
from app.modules.cognitive.service import CognitiveService

router = APIRouter(tags=["cognitive"])

_service = CognitiveService()


@router.get("/status", response_model=CognitiveStatusResponse)
def get_cognitive_status() -> CognitiveStatusResponse:
    """Check whether the cognitive layer (AuraSDK) is available."""
    return _service.status()


@router.post("/store", response_model=MemoryStoreResponse)
def store_memory(body: MemoryStoreRequest) -> MemoryStoreResponse:
    """Commit content to cognitive memory within a namespace."""
    return _service.store(body.content, namespace=body.namespace, metadata=body.metadata)


@router.post("/recall", response_model=MemoryRecallResponse)
def recall_memories(body: MemoryRecallRequest) -> MemoryRecallResponse:
    """Recall memories relevant to a query from the cognitive stack."""
    return _service.recall(body.query, namespace=body.namespace, top_k=body.top_k)


@router.post("/maintenance", response_model=MaintenanceResponse)
def run_maintenance(namespace: str = "default") -> MaintenanceResponse:
    """Run a consolidation and pruning cycle on the cognitive memory."""
    return _service.maintenance(namespace=namespace)


@router.get("/insights", response_model=InsightsResponse)
def get_insights(namespace: str = "default") -> InsightsResponse:
    """Get a summary of cognitive insights across memory levels."""
    return _service.insights(namespace=namespace)


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(body: FeedbackRequest) -> FeedbackResponse:
    """Reinforce or weaken a memory entry via feedback."""
    return _service.feedback(body.content, namespace=body.namespace, positive=body.positive)
