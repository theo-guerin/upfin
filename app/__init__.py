from fastapi import FastAPI

from app import config



app = FastAPI(
    openapi_url="/openapi.json" if config.environment.is_development() else None,
)
