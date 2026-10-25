import logging
from time import perf_counter
from uuid import uuid4

from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


async def request_logging_middleware(
    request: Request,
    call_next,
) -> Response:
    """Add a request ID and log HTTP request duration."""
    request_id = str(uuid4())
    request.state.request_id = request_id

    start_time = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round(
            (perf_counter() - start_time) * 1000,
            2,
        )

        logger.exception(
            "HTTP request failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
            },
        )
        raise

    duration_ms = round(
        (perf_counter() - start_time) * 1000,
        2,
    )

    response.headers["X-Request-ID"] = request_id

    if request.url.path != "/health":
        logger.info(
            "HTTP request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

    return response
