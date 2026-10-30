from fastapi import Request, status
from fastapi.responses import JSONResponse

from documind_rag.services.document_ingestion.exceptions import (
    DocumentIngestionError,
    UnsupportedDocumentFormatError,
)


async def document_ingestion_exception_handler(
    request: Request,
    exc: DocumentIngestionError,
) -> JSONResponse:
    """Convert document ingestion exceptions into HTTP responses."""
    if isinstance(exc, UnsupportedDocumentFormatError):
        status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )
