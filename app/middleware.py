import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger(__name__)


async def log_exceptions(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    try:
        return await call_next(request)
    except Exception:
        logger.exception(
            "Unhandled exception for %s %s", request.method, request.url.path
        )
        raise


async def log_access(request: Request, call_next: RequestResponseEndpoint) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    response_time = time.perf_counter() - start_time
    logger.info(
        "%s %s %s %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        response_time,
    )
    return response
