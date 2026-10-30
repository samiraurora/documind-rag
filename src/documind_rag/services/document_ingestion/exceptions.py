class DocumentIngestionError(Exception):
    """Base exception for document ingestion failures."""


class UnsupportedDocumentFormatError(DocumentIngestionError):
    """Raised when a document format is not supported."""


class TextExtractionError(DocumentIngestionError):
    """Raised when text extraction fails."""


class PdfExtractionError(DocumentIngestionError):
    """Raised when PDF extraction fails."""
