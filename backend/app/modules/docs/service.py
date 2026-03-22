from app.core.config import get_settings


class DocsService:
    def list_docs(self) -> list[dict[str, str]]:
        settings = get_settings()
        docs_root = settings.resolved_docs_path
        items: list[dict[str, str]] = []
        for path in sorted(docs_root.rglob("*.md")):
            slug = str(path.relative_to(docs_root)).replace(".md", "")
            title = path.stem.replace("-", " ").replace("_", " ").title()
            items.append({"title": title, "slug": slug})
        return items
