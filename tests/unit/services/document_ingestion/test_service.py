import pytest

from documind_rag.services.document_ingestion.service import (
    DocumentIngestionService,
    UnsupportedDocumentFormatError,
)


def test_extracts_text_file() -> None:
    service = DocumentIngestionService()

    result = service.extract(
        b"Hello from a text file.",
        filename="notes.txt",
    )

    assert result.filename == "notes.txt"
    assert result.source_format == "txt"
    assert result.text == "Hello from a text file."


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
