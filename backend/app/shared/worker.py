from arq import run_worker

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_engine, initialize_session_factory
from app.modules.downloads.worker import DownloadWorkerSettings


def main() -> None:
    settings = get_settings()
    initialize_session_factory(settings.database_url)
    Base.metadata.create_all(bind=get_engine())
    run_worker(DownloadWorkerSettings)


if __name__ == "__main__":
    main()
