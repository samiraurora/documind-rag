from pydantic import BaseModel


class ExtractedPageResponse(BaseModel):
    """Represent an extracted page in an API response."""

    page_number: int
    text: str


class DocumentUploadResponse(BaseModel):
    """Represent the result of a document upload."""

    filename: str
    source_format: str
    text: str
    pages: list[ExtractedPageResponse]
