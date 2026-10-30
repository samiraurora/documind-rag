import pytest

from documind_rag.services.document_ingestion.exceptions import (
    TextExtractionError,
)
from documind_rag.services.document_ingestion.extractors.text_extractor import (
    TextExtractor,
)


def test_extracts_utf8_text() -> None:
    extractor = TextExtractor()

    result = extractor.extract(
        b"Hello, DocuMind RAG!",
        filename="sample.txt",
    )

    assert result.filename == "sample.txt"
    assert result.source_format == "txt"
    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1
    assert result.text == "Hello, DocuMind RAG!"


def test_extracts_unicode_text() -> None:
    extractor = TextExtractor()

    result = extractor.extract(
        "Hello, café!".encode(),
        filename="unicode.txt",
    )

    assert result.text == "Hello, café!"


def test_removes_utf8_bom() -> None:
    extractor = TextExtractor()

    result = extractor.extract(
        b"\xef\xbb\xbfHello",
        filename="bom.txt",
    )

    assert result.text == "Hello"


def test_extracts_empty_file() -> None:
    extractor = TextExtractor()

    result = extractor.extract(
        b"",
        filename="empty.txt",
    )

    assert result.text == ""
    assert len(result.pages) == 1


def test_extract_invalid_utf8() -> None:
    extractor = TextExtractor()

    with pytest.raises(
        TextExtractionError,
        match="valid UTF-8",
    ):
        extractor.extract(
            b"\xff\xfe\xfa",
            filename="invalid.txt",
        )
