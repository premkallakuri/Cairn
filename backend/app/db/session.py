from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def initialize_session_factory(database_url: str) -> None:
    global _engine, _session_factory

    engine_kwargs: dict[str, object] = {"future": True}
    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
        if database_url.endswith(":memory:"):
            engine_kwargs["poolclass"] = StaticPool

    _engine = create_engine(database_url, **engine_kwargs)
    _session_factory = sessionmaker(bind=_engine, autocommit=False, autoflush=False, future=True)


def get_engine() -> Engine:
    if _engine is None:
        raise RuntimeError("Database engine has not been initialized")
    return _engine


def get_session() -> Generator[Session]:
    if _session_factory is None:
        raise RuntimeError("Session factory has not been initialized")
    session = _session_factory()
    try:
        yield session
    finally:
        session.close()


def reset_session_factory() -> None:
    global _engine, _session_factory
    _engine = None
    _session_factory = None
