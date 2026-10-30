from pathlib import PurePath

from documind_rag.services.document_ingestion.exceptions import (
    UnsupportedDocumentFormatError,
)
from documind_rag.services.document_ingestion.extractors.pdf_extractor import (
    PdfExtractor,
)
from documind_rag.services.document_ingestion.extractors.text_extractor import (
    TextExtractor,
)
from documind_rag.services.document_ingestion.models import (
    ExtractedDocument,
)


class DocumentIngestionService:
    """Coordinate document extraction using format-specific extractors."""

    def __init__(self) -> None:
        self._extractors = {
            ".txt": TextExtractor(),
            ".pdf": PdfExtractor(),
        }

    def extract(
        self,
        content: bytes,
        *,
        filename: str,
    ) -> ExtractedDocument:
        """Select an extractor based on the filename extension."""
        extension = PurePath(filename).suffix.lower()
        extractor = self._extractors.get(extension)

        if extractor is None:
            raise UnsupportedDocumentFormatError(
                f"Unsupported document format: {extension or 'unknown'}"
            )

        return extractor.extract(content, filename=filename)
