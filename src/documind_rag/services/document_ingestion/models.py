from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class ExtractedPage:
    """Represent text extracted from a single document page."""

    page_number: int
    text: str


@dataclass(frozen=True, slots=True)
class ExtractedDocument:
    """Represent the text extracted from a document."""

    filename: str
    source_format: Literal["txt", "pdf"]
    pages: tuple[ExtractedPage, ...]

    @property
    def text(self) -> str:
        """Return the combined text from all pages."""
        return "\n\n".join(page.text for page in self.pages)
