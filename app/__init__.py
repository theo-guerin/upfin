import logging
import logging.config

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from app import config, middleware
from app.config import LOGGING_CONFIG
from app.routes import router
from app.static import mount_frontend

logging.config.dictConfig(LOGGING_CONFIG)


app = FastAPI(
    openapi_url="/openapi.json" if config.environment.is_development() else None,
)

app.middleware("http")(middleware.log_exceptions)
app.middleware("http")(middleware.log_access)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(router)
mount_frontend(app)
