import pytest

from app.core.config import Settings

pytestmark = [pytest.mark.unit, pytest.mark.platform]


def test_settings_reject_blank_database_url() -> None:
    with pytest.raises(ValueError):
        Settings(database_url=" ")


def test_settings_resolve_workspace_relative_paths() -> None:
    settings = Settings()
    assert settings.resolved_app_catalog_path.name == "apps"
    assert settings.resolved_docs_path.name == "docs"
