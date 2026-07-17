from fastapi import FastAPI

from app import config
from app.routes import router
from app.static import mount_frontend

app = FastAPI(
    openapi_url="/openapi.json" if config.environment.is_development() else None,
)
app.include_router(router)
mount_frontend(app)
