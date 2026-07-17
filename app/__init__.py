from fastapi import FastAPI

from app import config
from app.routes import router

app = FastAPI(
    openapi_url="/openapi.json" if config.environment.is_development() else None,
)
app.include_router(router)
