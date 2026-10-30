import pymupdf
import pytest

from documind_rag.services.document_ingestion.exceptions import (
    UnsupportedDocumentFormatError,
)
from documind_rag.services.document_ingestion.service import (
    DocumentIngestionService,
)


def create_pdf(text: str) -> bytes:
    """Create a single-page PDF containing the supplied text."""
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), text)
        return document.tobytes()


def test_extracts_text_file() -> None:
    service = DocumentIngestionService()

    result = service.extract(
        b"Hello from a text file.",
        filename="notes.txt",
    )

    assert result.filename == "notes.txt"
    assert result.source_format == "txt"
    assert result.text == "Hello from a text file."


def test_extracts_pdf_file() -> None:
    service = DocumentIngestionService()

    result = service.extract(
        create_pdf("Hello from a PDF file."),
        filename="report.pdf",
    )

    assert result.filename == "report.pdf"
    assert result.source_format == "pdf"
    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1
    assert "Hello from a PDF file." in result.text


def test_rejects_unsupported_format() -> None:
    service = DocumentIngestionService()

    with pytest.raises(
        UnsupportedDocumentFormatError,
        match="Unsupported document format: .docx",
    ):
        service.extract(
            b"Some content",
            filename="notes.docx",
        )


def test_rejects_filename_without_extension() -> None:
    service = DocumentIngestionService()

    with pytest.raises(
        UnsupportedDocumentFormatError,
        match="Unsupported document format: unknown",
    ):
        service.extract(
            b"Some content",
            filename="notes",
        )


def test_accepts_uppercase_extension() -> None:
    service = DocumentIngestionService()

    result = service.extract(
        b"Uppercase extension works.",
        filename="NOTES.TXT",
    )

    assert result.source_format == "txt"
    assert result.text == "Uppercase extension works."
