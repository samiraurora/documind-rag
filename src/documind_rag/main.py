from fastapi import FastAPI

app = FastAPI(
    title="DocuMind RAG API",
    description=("Document question answering using retrieval-augmented generation."),
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

