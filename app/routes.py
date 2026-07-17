import jinja2
from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse

from app.config import ROOT_DIRECTORY

TEMPLATE_DIRECTORY = ROOT_DIRECTORY / "app" / "templates"
UPLOAD_DIRECTORY = ROOT_DIRECTORY / "uploads"

environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIRECTORY),
)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return environment.get_template("index.j2").render()


@router.post("/", response_class=HTMLResponse)
async def upload(file: UploadFile):
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    template = environment.get_template("index.j2")

    if not file.filename:
        return template.render(
            message="No file selected.",
            message_type="error",
        )

    file_path = UPLOAD_DIRECTORY / file.filename

    try:
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

        return template.render(
            message=f"Successfully uploaded {file.filename}",
            message_type="success",
        )
    except Exception:
        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass

        return template.render(
            message="Upload failed. Please try again.",
            message_type="error",
        )
