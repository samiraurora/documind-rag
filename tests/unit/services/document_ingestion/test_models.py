from documind_rag.services.document_ingestion.models import (
    ExtractedDocument,
    ExtractedPage,
)


def test_extracted_document_combines_page_text() -> None:
    document = ExtractedDocument(
        filename="report.pdf",
        source_format="pdf",
        pages=(
            ExtractedPage(
                page_number=1,
                text="First page content.",
            ),
            ExtractedPage(
                page_number=2,
                text="Second page content.",
            ),
        ),
    )

    assert document.text == ("First page content.\n\nSecond page content.")


def test_extracted_document_preserves_page_numbers() -> None:
    pages = (
        ExtractedPage(page_number=1, text="Page one."),
        ExtractedPage(page_number=3, text="Page three."),
    )

    document = ExtractedDocument(
        filename="report.pdf",
        source_format="pdf",
        pages=pages,
    )

    assert document.pages == pages
    assert document.pages[1].page_number == 3


def test_empty_document_returns_empty_text() -> None:
    document = ExtractedDocument(
        filename="empty.txt",
        source_format="txt",
        pages=(),
    )

    assert document.text == ""
