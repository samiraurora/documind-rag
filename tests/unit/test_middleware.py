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
