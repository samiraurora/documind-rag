import pymupdf

from documind_rag.services.document_ingestion.extractors.pdf_extractor import (
    PdfExtractor,
)


def create_pdf(*page_texts: str) -> bytes:
    """Create a PDF containing the supplied page text."""
    with pymupdf.open() as document:
        for page_text in page_texts:
            page = document.new_page()

            if page_text:
                page.insert_text(
                    (72, 72),
                    page_text,
                )

        return document.tobytes()


def test_extracts_text_from_single_page_pdf() -> None:
    extractor = PdfExtractor()
    pdf_content = create_pdf("Hello, DocuMind RAG!")

    result = extractor.extract(
        pdf_content,
        filename="sample.pdf",
    )

    assert result.filename == "sample.pdf"
    assert result.source_format == "pdf"
    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1
    assert "Hello, DocuMind RAG!" in result.text


def test_extracts_text_and_preserves_page_numbers() -> None:
    extractor = PdfExtractor()
    pdf_content = create_pdf(
        "Content on page one.",
        "Content on page two.",
    )

    result = extractor.extract(
        pdf_content,
        filename="report.pdf",
    )

    assert len(result.pages) == 2
    assert result.pages[0].page_number == 1
    assert result.pages[1].page_number == 2
    assert "Content on page one." in result.pages[0].text
    assert "Content on page two." in result.pages[1].text


def test_extracts_blank_pdf_page() -> None:
    extractor = PdfExtractor()
    pdf_content = create_pdf("")

    result = extractor.extract(
        pdf_content,
        filename="blank.pdf",
    )

    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1
    assert result.pages[0].text == ""
    assert result.text == ""
