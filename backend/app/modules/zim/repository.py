from sqlalchemy.orm import Session

from app.db.session import get_session
from app.modules.zim.models import WikipediaSelectionModel


class WikipediaSelectionRepository:
    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    def get_selection(self) -> WikipediaSelectionModel | None:
        if self._session is not None:
            return self._session.get(WikipediaSelectionModel, 1)

        session = next(get_session())
        try:
            return session.get(WikipediaSelectionModel, 1)
        finally:
            session.close()

    def save_selection(
        self,
        *,
        option_id: str,
        status: str,
        filename: str | None,
        url: str | None,
    ) -> WikipediaSelectionModel:
        if self._session is not None:
            return self._save_selection(
                self._session,
                option_id=option_id,
                status=status,
                filename=filename,
                url=url,
            )

        session = next(get_session())
        try:
            return self._save_selection(
                session,
                option_id=option_id,
                status=status,
                filename=filename,
                url=url,
            )
        finally:
            session.close()

    def _save_selection(
        self,
        session: Session,
        *,
        option_id: str,
        status: str,
        filename: str | None,
        url: str | None,
    ) -> WikipediaSelectionModel:
        selection = session.get(WikipediaSelectionModel, 1)
        if selection is None:
            selection = WikipediaSelectionModel(id=1)
            session.add(selection)

        selection.option_id = option_id
        selection.status = status
        selection.filename = filename
        selection.url = url
        session.commit()
        session.refresh(selection)
        return selection
