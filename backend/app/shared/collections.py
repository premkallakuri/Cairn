import json
import logging
from pathlib import Path
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_collection_manifest(
    filename: str, *, default: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Load a collection manifest JSON file, returning *default* when the file is missing."""
    settings = get_settings()
    path = settings.resolved_collections_path / filename
    try:
        return load_json_file(path)
    except (FileNotFoundError, NotADirectoryError):
        if default is not None:
            logger.warning("Collection manifest not found: %s – using default", path)
            return default
        raise
