from pathlib import Path

import pytest

from app.modules.knowledge_base.service import KnowledgeBaseService

pytestmark = [pytest.mark.unit, pytest.mark.knowledge_base]


def test_extracts_text_from_simple_pdf_literal_strings(tmp_path: Path) -> None:
    pdf_path = tmp_path / "field-guide.pdf"
    pdf_path.write_bytes(
        b"%PDF-1.4\n1 0 obj\n<<>>\nstream\nBT /F1 12 Tf 72 712 Td "
        b"(Atlas Haven Field Guide) Tj ET\nendstream\nendobj\n%%EOF"
    )

    text = KnowledgeBaseService().extract_text(pdf_path)

    assert "Atlas Haven Field Guide" in text


def test_indexes_text_file_and_returns_relevant_context(tmp_path: Path) -> None:
    source_path = tmp_path / "pacific-notes.txt"
    source_path.write_text(
        "Pacific maps should be cached locally. "
        "Medical references should be indexed for field search."
    )
    service = KnowledgeBaseService()

    service.index_path(source_path)
    context = service.assemble_context("How do I use pacific maps locally?")

    assert context is not None
    assert "pacific-notes.txt" in context
    assert "Pacific maps" in context
