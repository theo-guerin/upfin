import logging
import logging.config
import time

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint

from app import config
from app.config import LOGGING_CONFIG
from app.routes import router
from app.static import mount_frontend

logger = logging.getLogger(__name__)

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(
    openapi_url="/openapi.json" if config.environment.is_development() else None,
)


@app.middleware("http")
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


@app.middleware("http")
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


app.add_middleware(CorrelationIdMiddleware)

app.include_router(router)
mount_frontend(app)
