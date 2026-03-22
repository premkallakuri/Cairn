from fastapi import APIRouter

from app.modules.docs.service import DocsService

router = APIRouter(tags=["docs"])


@router.get("/list")
def list_docs() -> list[dict[str, str]]:
    return DocsService().list_docs()
