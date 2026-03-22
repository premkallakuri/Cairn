from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ATLAS_HAVEN_", extra="ignore")

    version: str = "0.1.0"
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = False
    database_url: str = "sqlite+pysqlite:///./atlas_haven.db"
    redis_url: str = "redis://localhost:6379/0"
    ollama_base_url: str = "http://127.0.0.1:11434"
    enqueue_download_worker_jobs: int = Field(default=1, ge=0, le=1)
    frontend_api_base_url: str = "http://127.0.0.1:8000"
    kiwix_catalog_url: str = "https://browse.library.kiwix.org/catalog/v2/entries"
    workspace_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[3])
    app_catalog_path: Path | None = None
    docs_path: Path | None = None
    collections_path: Path | None = None
    bundled_seed_zim_path: Path | None = None
    storage_path: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[4] / "storage"
    )

    @field_validator("database_url", "redis_url")
    @classmethod
    def validate_required_urls(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value

    @property
    def repo_root(self) -> Path:
        return self.workspace_root.parent

    @property
    def resolved_app_catalog_path(self) -> Path:
        return self.app_catalog_path or self.workspace_root / "apps"

    @property
    def resolved_docs_path(self) -> Path:
        return self.docs_path or self.workspace_root / "docs"

    @property
    def resolved_collections_path(self) -> Path:
        return self.collections_path or self.workspace_root / "collections"

    @property
    def resolved_bundled_seed_zim_path(self) -> Path:
        return self.bundled_seed_zim_path or (
            self.repo_root / "install" / "wikipedia_en_100_mini_2025-06.zim"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
