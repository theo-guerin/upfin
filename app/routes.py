import jinja2
from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse

from app import config
from app.config import ROOT_DIRECTORY
from app.jellyfin import Jellyfin

TEMPLATE_DIRECTORY = ROOT_DIRECTORY / "app" / "templates"
UPLOAD_DIRECTORY = ROOT_DIRECTORY / "uploads"

UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1 MB

UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIRECTORY),
)
jellyfin = Jellyfin(config.jellyfin_api_base_url, config.jellyfin_api_key)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return jinja_environment.get_template("index.j2").render()


@router.post("/", response_class=HTMLResponse)
async def upload(file: UploadFile):
    template = jinja_environment.get_template("index.j2")

    if not file.filename:
        return template.render(
            error="No file selected.",
        )

    search_results = await jellyfin.search_movie(file.filename)
    if not search_results:
        return template.render(
            error=f"No movie found for {file.filename}.",
        )
    print(f"Found {len(search_results)} search results for {file.filename}.")

    file_path = UPLOAD_DIRECTORY / file.filename

    try:
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(UPLOAD_CHUNK_SIZE):
                buffer.write(chunk)
    except Exception:
        file_path.unlink(missing_ok=True)

        return template.render(
            error="Upload failed. Please try again.",
        )
