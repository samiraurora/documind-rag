import logging

from fastapi import FastAPI

from documind_rag.core.config import get_settings
from documind_rag.core.logging_config import configure_logging
from documind_rag.core.middleware import request_logging_middleware

configure_logging()

settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=("Document question answering using retrieval-augmented generation."),
    version="0.1.0",
)

app.middleware("http")(request_logging_middleware)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
