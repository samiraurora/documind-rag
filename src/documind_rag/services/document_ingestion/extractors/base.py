from typing import Protocol

from documind_rag.services.document_ingestion.models import (
    ExtractedDocument,
)


class DocumentExtractor(Protocol):
    """Define the contract for document text extractors."""

    def extract(
        self,
        content: bytes,
        *,
        filename: str,
    ) -> ExtractedDocument:
        """Extract text from document bytes."""
        ...
