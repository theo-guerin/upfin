from typing import Any, MutableMapping, override

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import ROOT_DIRECTORY

FRONTEND_DIRECTORY = ROOT_DIRECTORY / "frontend" / "dist"


class SPAStaticFiles(StaticFiles):
    @override
    async def get_response(
        self, path: str, scope: MutableMapping[str, Any]
    ) -> Response:
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exception:
            if exception.status_code != 404:
                raise

        return await super().get_response("index.html", scope)


def mount_frontend(app: FastAPI) -> None:
    app.mount("/", SPAStaticFiles(directory=FRONTEND_DIRECTORY, html=True))
