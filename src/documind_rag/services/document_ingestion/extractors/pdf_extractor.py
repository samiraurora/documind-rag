import pymupdf

from documind_rag.services.document_ingestion.exceptions import (
    PdfExtractionError,
)
from documind_rag.services.document_ingestion.models import (
    ExtractedDocument,
    ExtractedPage,
)


class PdfExtractor:
    """Extract text from PDF documents using PyMuPDF."""

    def extract(
        self,
        content: bytes,
        *,
        filename: str,
    ) -> ExtractedDocument:
        """Extract text from each PDF page."""
        try:
            with pymupdf.open(
                stream=content,
                filetype="pdf",
            ) as document:
                pages = tuple(
                    ExtractedPage(
                        page_number=page_number,
                        text=page.get_text("text"),
                    )
                    for page_number, page in enumerate(
                        document,
                        start=1,
                    )
                )
        except pymupdf.FileDataError as exc:
            raise PdfExtractionError(
                "The uploaded PDF is invalid or cannot be opened."
            ) from exc

        return ExtractedDocument(
            filename=filename,
            source_format="pdf",
            pages=pages,
        )
