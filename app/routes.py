from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import APIRouter, HTTPException, UploadFile
from guessit import guessit
from pydantic import BaseModel

from app import config
from app.jellyfin import Jellyfin, MovieSearchResult

UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1 MB

jellyfin = Jellyfin(config.jellyfin_api_base_url, config.jellyfin_api_key)

router = APIRouter()


class UploadRequest(BaseModel):
    name: str
    year: int


@router.post(
    "/submit",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {"detail": "No file attached to the upload."},
                },
            },
        },
    },
)
async def post_submit(movie: UploadFile, name: str, year: int):
    if not movie.filename:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="No file attached to the upload."
        )

    with TemporaryDirectory() as temporary_directory:
        temporary_directory = Path(temporary_directory)

        movie_directory = temporary_directory / name
        movie_directory.mkdir(parents=True, exist_ok=True)

        suffix = Path(movie.filename).suffix
        movie_filename = f"{name} ({year}){suffix}"
        movie_file = movie_directory / movie_filename

        with open(movie_file, "wb") as file:
            while chunk := await movie.read(UPLOAD_CHUNK_SIZE):
                file.write(chunk)


@router.get(
    "/search_movie",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": {
                        "NO_TITLE": {
                            "summary": "No title found in filename.",
                            "value": {
                                "detail": "Could not detect a movie title in the filename"
                            },
                        },
                    },
                },
            },
        },
    },
    response_model=list[MovieSearchResult],
)
async def get_search_movie(filename: str):
    guess = guessit(filename, {"type": "movie"})

    name = guess.get("title")
    if not name:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Could not detect a movie title in the filename",
        )

    return await jellyfin.search_movie(name, guess.get("year"))
