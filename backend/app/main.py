from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory
from app.modules.benchmark import models as benchmark_models  # noqa: F401
from app.modules.benchmark.routes import router as benchmark_router
from app.modules.catalog import models as catalog_models  # noqa: F401
from app.modules.catalog.service import CatalogSyncService
from app.modules.cognitive.routes import router as cognitive_router
from app.modules.chat import models as chat_models  # noqa: F401
from app.modules.chat.routes import router as chat_router
from app.modules.content_updates.routes import router as content_updates_router
from app.modules.docs.routes import router as docs_router
from app.modules.downloads import models as download_models  # noqa: F401
from app.modules.downloads.routes import router as downloads_router
from app.modules.easy_setup import models as easy_setup_models  # noqa: F401
from app.modules.easy_setup.routes import router as easy_setup_router
from app.modules.knowledge_base import models as knowledge_base_models  # noqa: F401
from app.modules.knowledge_base.routes import router as knowledge_base_router
from app.modules.maps.routes import router as maps_router
from app.modules.ollama.routes import router as ollama_router
from app.modules.platform_core.routes import router as platform_router
from app.modules.zim import models as zim_models  # noqa: F401
from app.modules.zim.routes import router as zim_router


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        initialize_session_factory(settings.database_url)
        Base.metadata.create_all(bind=get_engine())
        CatalogSyncService().sync_from_disk()
        yield

    openapi_tags = [
        {"name": "platform", "description": "Health checks, system info, service management, settings, and updates"},
        {"name": "chat", "description": "Chat sessions, messages, and conversation management"},
        {"name": "cognitive", "description": "AuraSDK cognitive memory — store, recall, maintenance, insights"},
        {"name": "ollama", "description": "Local LLM management — models, chat, and streaming"},
        {"name": "benchmark", "description": "System and AI benchmarking — run, results, comparison"},
        {"name": "knowledge-base", "description": "RAG document pipeline — upload, embed, sync"},
        {"name": "maps", "description": "Offline map regions, styles, collections, and tile serving"},
        {"name": "zim", "description": "ZIM/Wikipedia offline content management"},
        {"name": "easy-setup", "description": "Guided setup wizard — categories, drafts, and plans"},
        {"name": "content-updates", "description": "Manifest refresh and content update application"},
        {"name": "downloads", "description": "Download job tracking and progress"},
        {"name": "docs", "description": "Documentation listing"},
    ]

    app = FastAPI(
        title="Cairn API",
        version=settings.version,
        description="FastAPI control plane for Cairn — offline knowledge base with cognitive memory.",
        lifespan=lifespan,
        openapi_tags=openapi_tags,
    )
    register_error_handlers(app)
    app.include_router(platform_router, prefix="/api")
    app.include_router(chat_router, prefix="/api/chat")
    app.include_router(benchmark_router, prefix="/api/benchmark")
    app.include_router(downloads_router, prefix="/api/downloads")
    app.include_router(docs_router, prefix="/api/docs")
    app.include_router(easy_setup_router, prefix="/api/easy-setup")
    app.include_router(content_updates_router, prefix="/api")
    app.include_router(knowledge_base_router, prefix="/api/rag")
    app.include_router(maps_router, prefix="/api/maps")
    app.include_router(cognitive_router, prefix="/api/cognitive")
    app.include_router(ollama_router, prefix="/api/ollama")
    app.include_router(zim_router, prefix="/api/zim")
    return app


app = create_app()
