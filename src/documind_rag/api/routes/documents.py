from fastapi import APIRouter, File, HTTPException, UploadFile, status

from documind_rag.api.schemas.documents import (
    DocumentUploadResponse,
    ExtractedPageResponse,
)
from documind_rag.services.document_ingestion.service import (
    DocumentIngestionService,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024

UPLOAD_FILE = File(...)

document_ingestion_service = DocumentIngestionService()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_200_OK,
)
async def upload_document(
    file: UploadFile = UPLOAD_FILE,
) -> DocumentUploadResponse:
    """Upload a TXT or PDF file and extract its text."""
    filename = file.filename or ""

    try:
        content = await file.read(MAX_UPLOAD_SIZE_BYTES + 1)
    finally:
        await file.close()

    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the maximum allowed size of 10 MB.",
        )

    extracted_document = document_ingestion_service.extract(
        content,
        filename=filename,
    )

    return DocumentUploadResponse(
        filename=extracted_document.filename,
        source_format=extracted_document.source_format,
        text=extracted_document.text,
        pages=[
            ExtractedPageResponse(
                page_number=page.page_number,
                text=page.text,
            )
            for page in extracted_document.pages
        ],
    )
