import jinja2
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.config import ROOT_DIRECTORY

TEMPLATE_DIRECTORY = ROOT_DIRECTORY / "app" / "templates"

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIRECTORY),
    )
    template = environment.get_template("index.j2")
    return template.render()
