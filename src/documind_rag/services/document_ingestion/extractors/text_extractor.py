from documind_rag.services.document_ingestion.models import (
    ExtractedDocument,
    ExtractedPage,
)


class TextExtractor:
    """Extract text from plain-text documents."""

    def extract(
        self,
        content: bytes,
        *,
        filename: str,
    ) -> ExtractedDocument:
        """Decode UTF-8 content and return an extracted document."""
        text = content.decode("utf-8-sig")

        return ExtractedDocument(
            filename=filename,
            source_format="txt",
            pages=(
                ExtractedPage(
                    page_number=1,
                    text=text,
                ),
            ),
        )
