from fastapi.testclient import TestClient

from documind_rag.main import app

client = TestClient(app)


def test_request_returns_correlation_id() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_each_request_gets_a_unique_correlation_id() -> None:
    first_response = client.get("/health")
    second_response = client.get("/health")

    first_request_id = first_response.headers["X-Request-ID"]
    second_request_id = second_response.headers["X-Request-ID"]

    assert first_request_id != second_request_id


def test_non_health_request_returns_correlation_id() -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_not_found_response_includes_correlation_id() -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert "X-Request-ID" in response.headers


def test_non_health_request_logs_structured_fields(caplog) -> None:
    import logging

    with caplog.at_level(
        logging.INFO,
        logger="documind_rag.core.middleware",
    ):
        response = client.get("/docs")

    assert response.status_code == 200

    log_record = next(
        record
        for record in caplog.records
        if record.name == "documind_rag.core.middleware"
        and record.getMessage() == "HTTP request completed"
    )

    assert log_record.request_id == response.headers["X-Request-ID"]
    assert log_record.method == "GET"
    assert log_record.path == "/docs"
    assert log_record.status_code == 200
    assert log_record.duration_ms >= 0
