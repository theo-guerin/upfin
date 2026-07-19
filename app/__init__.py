import logging.config

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from app import config
from app.config import LOGGING_CONFIG
from app.middleware import AccessLogMiddleware, ExceptionLogMiddleware
from app.routes import router
from app.static import mount_frontend

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(
    openapi_url="/openapi.json" if config.environment.is_development() else None,
)

app.add_middleware(ExceptionLogMiddleware)
app.add_middleware(AccessLogMiddleware)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(router)
mount_frontend(app)
