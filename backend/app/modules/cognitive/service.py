"""Cognitive memory service wrapping AuraSDK.

AuraSDK provides a five-layer cognitive stack (Belief, Concept, Causal, Policy,
Advisory) with sub-millisecond recall, namespace isolation, and fully local
operation.  This service exposes a thin application layer that the rest of the
Cairn backend can import without coupling to Aura internals.
"""

from __future__ import annotations

import logging
from typing import Any

from app.modules.cognitive.schemas import (
    CognitiveInsight,
    CognitiveStatusResponse,
    FeedbackResponse,
    InsightsResponse,
    MaintenanceResponse,
    MemoryEntry,
    MemoryRecallResponse,
    MemoryStoreResponse,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy import for Aura so the backend can still start when the package
# is not yet installed (e.g., during early CI or migration runs).
# ---------------------------------------------------------------------------
_aura_instances: dict[str, Any] = {}


def _get_aura(namespace: str = "default") -> Any:
    """Return a cached Aura instance for the given namespace."""
    if namespace not in _aura_instances:
        try:
            from aura import Aura  # type: ignore[import-untyped]

            _aura_instances[namespace] = Aura(namespace=namespace)
            logger.info("AuraSDK initialised for namespace '%s'", namespace)
        except ImportError:
            logger.warning(
                "aura-memory is not installed – cognitive features are disabled. "
                "Install with: pip install aura-memory"
            )
            return None
        except Exception:
            logger.exception("Failed to initialise AuraSDK for namespace '%s'", namespace)
            return None
    return _aura_instances[namespace]


def _is_available() -> bool:
    try:
        from aura import Aura  # type: ignore[import-untyped]  # noqa: F401

        return True
    except ImportError:
        return False


def _get_version() -> str | None:
    try:
        import importlib.metadata

        return importlib.metadata.version("aura-memory")
    except Exception:
        return None


class CognitiveService:
    """Application-level facade over AuraSDK."""

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------
    def status(self) -> CognitiveStatusResponse:
        available = _is_available()
        return CognitiveStatusResponse(
            available=available,
            version=_get_version() if available else None,
            namespaces=list(_aura_instances.keys()),
            message="Cognitive layer is active." if available else "aura-memory not installed.",
        )

    # ------------------------------------------------------------------
    # Store
    # ------------------------------------------------------------------
    def store(
        self,
        content: str,
        *,
        namespace: str = "default",
        metadata: dict[str, str] | None = None,
    ) -> MemoryStoreResponse:
        aura = _get_aura(namespace)
        if aura is None:
            return MemoryStoreResponse(
                success=False,
                message="Cognitive layer unavailable – aura-memory not installed.",
                namespace=namespace,
            )
        try:
            aura.store(content, metadata=metadata or {})
            return MemoryStoreResponse(
                success=True,
                message="Memory stored successfully.",
                namespace=namespace,
            )
        except Exception as exc:
            logger.exception("Cognitive store failed in namespace '%s'", namespace)
            return MemoryStoreResponse(
                success=False,
                message=f"Store failed: {exc}",
                namespace=namespace,
            )

    # ------------------------------------------------------------------
    # Recall
    # ------------------------------------------------------------------
    def recall(
        self,
        query: str,
        *,
        namespace: str = "default",
        top_k: int = 5,
    ) -> MemoryRecallResponse:
        aura = _get_aura(namespace)
        if aura is None:
            return MemoryRecallResponse(memories=[], query=query, namespace=namespace)
        try:
            results = aura.recall(query, top_k=top_k)
            memories = [
                MemoryEntry(
                    content=entry.get("content", str(entry)),
                    relevance=float(entry.get("relevance", 0.0)),
                    level=entry.get("level", "unknown"),
                    namespace=namespace,
                )
                if isinstance(entry, dict)
                else MemoryEntry(
                    content=str(entry),
                    relevance=0.0,
                    level="unknown",
                    namespace=namespace,
                )
                for entry in (results if isinstance(results, list) else [results])
            ]
            return MemoryRecallResponse(memories=memories, query=query, namespace=namespace)
        except Exception:
            logger.exception("Cognitive recall failed in namespace '%s'", namespace)
            return MemoryRecallResponse(memories=[], query=query, namespace=namespace)

    # ------------------------------------------------------------------
    # Maintenance (consolidation & pruning)
    # ------------------------------------------------------------------
    def maintenance(self, *, namespace: str = "default") -> MaintenanceResponse:
        aura = _get_aura(namespace)
        if aura is None:
            return MaintenanceResponse(
                success=False,
                message="Cognitive layer unavailable.",
            )
        try:
            result = aura.maintenance()
            consolidated = result.get("consolidated", 0) if isinstance(result, dict) else 0
            pruned = result.get("pruned", 0) if isinstance(result, dict) else 0
            return MaintenanceResponse(
                success=True,
                message="Maintenance cycle completed.",
                consolidated=consolidated,
                pruned=pruned,
            )
        except Exception as exc:
            logger.exception("Cognitive maintenance failed in namespace '%s'", namespace)
            return MaintenanceResponse(success=False, message=f"Maintenance failed: {exc}")

    # ------------------------------------------------------------------
    # Insights
    # ------------------------------------------------------------------
    def insights(self, *, namespace: str = "default") -> InsightsResponse:
        aura = _get_aura(namespace)
        if aura is None:
            return InsightsResponse(namespace=namespace, insights=[])
        try:
            raw = aura.insights() if hasattr(aura, "insights") else []
            insights = [
                CognitiveInsight(
                    level=item.get("level", "unknown"),
                    summary=item.get("summary", ""),
                    entry_count=item.get("entry_count", 0),
                )
                for item in (raw if isinstance(raw, list) else [])
            ]
            return InsightsResponse(namespace=namespace, insights=insights)
        except Exception:
            logger.exception("Cognitive insights failed in namespace '%s'", namespace)
            return InsightsResponse(namespace=namespace, insights=[])

    # ------------------------------------------------------------------
    # Feedback (reinforce / weaken)
    # ------------------------------------------------------------------
    def feedback(
        self,
        content: str,
        *,
        namespace: str = "default",
        positive: bool = True,
    ) -> FeedbackResponse:
        aura = _get_aura(namespace)
        if aura is None:
            return FeedbackResponse(
                success=False, message="Cognitive layer unavailable."
            )
        try:
            if hasattr(aura, "feedback"):
                aura.feedback(content, positive=positive)
            elif positive and hasattr(aura, "reinforce"):
                aura.reinforce(content)
            elif not positive and hasattr(aura, "weaken"):
                aura.weaken(content)
            else:
                return FeedbackResponse(
                    success=False,
                    message="Feedback API not supported by installed aura-memory version.",
                )
            action = "reinforced" if positive else "weakened"
            return FeedbackResponse(success=True, message=f"Memory {action} successfully.")
        except Exception as exc:
            logger.exception("Cognitive feedback failed in namespace '%s'", namespace)
            return FeedbackResponse(success=False, message=f"Feedback failed: {exc}")

    # ------------------------------------------------------------------
    # Convenience: recall context string for LLM injection
    # ------------------------------------------------------------------
    def recall_context_for_llm(
        self,
        query: str,
        *,
        namespace: str = "default",
        top_k: int = 3,
    ) -> str:
        """Return a formatted string of recalled memories suitable for LLM context injection."""
        result = self.recall(query, namespace=namespace, top_k=top_k)
        if not result.memories:
            return ""
        lines = [
            f"- [{m.level}] {m.content}" for m in result.memories if m.content.strip()
        ]
        if not lines:
            return ""
        return "[Cognitive Memory Context]\n" + "\n".join(lines)
