import errno
import logging
import shutil
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory

import pathvalidate
from fastapi import APIRouter, HTTPException, UploadFile

from app import config
from app.jellyfin import Jellyfin, MovieSearchResult

UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1 MB

logger = logging.getLogger(__name__)

jellyfin = Jellyfin(config.jellyfin_api_base_url, config.jellyfin_api_key)

router = APIRouter()


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
        HTTPStatus.CONFLICT: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Inception (2010) already exists.",
                    },
                },
            },
        },
        HTTPStatus.INSUFFICIENT_STORAGE: {
            "content": {
                "application/json": {
                    "examples": {
                        "DISK_FULL_TEMP": {
                            "summary": "Disk full while writing upload to temp.",
                            "value": {
                                "detail": "Disk full while writing upload to temp"
                            },
                        },
                        "DISK_FULL_LIBRARY": {
                            "summary": "Disk full while moving upload to library.",
                            "value": {
                                "detail": "Disk full while moving upload to library"
                            },
                        },
                    },
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

    movie_label = f"{name} ({year})"
    movie_label = pathvalidate.sanitize_filename(movie_label)

    destination = config.jellyfin_movie_library_path / movie_label
    if destination.exists():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"{movie_label} already exists.",
        )

    logger.info("receiving upload: %s (%s)", name, year)

    with TemporaryDirectory() as temporary_directory:
        temporary_directory = Path(temporary_directory)

        suffix = Path(movie.filename).suffix
        filename = f"{movie_label}{suffix}"

        destination_directory = temporary_directory / movie_label
        destination_directory.mkdir(parents=True, exist_ok=True)
        destination_path = destination_directory / filename

        logger.info("writing to temp file: %s", destination_path)

        try:
            with open(destination_path, "wb") as file:
                while chunk := await movie.read(UPLOAD_CHUNK_SIZE):
                    file.write(chunk)
        except OSError as exception:
            if exception.errno == errno.ENOSPC:
                logger.error("disk full while writing upload to temp")
                raise HTTPException(
                    status_code=HTTPStatus.INSUFFICIENT_STORAGE,
                    detail="Disk full while writing upload to temp",
                ) from None
            raise

        file_size = destination_path.stat().st_size
        logger.info("wrote %.1f MB to temp", file_size / (1024 * 1024))

        target = config.jellyfin_movie_library_path / movie_label

        logger.info("moving to library: %s -> %s", destination_directory, target)
        try:
            shutil.move(destination_directory, target)
        except FileExistsError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"{movie_label} already exists.",
            ) from None
        except shutil.Error as exception:
            logger.exception("shutil.move failed")
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=str(exception),
            ) from None
        except OSError as exception:
            if exception.errno == errno.ENOSPC:
                logger.error("disk full while moving upload to library")
                raise HTTPException(
                    status_code=HTTPStatus.INSUFFICIENT_STORAGE,
                    detail="Disk full while moving upload to library",
                ) from None
            raise

        logger.info("upload complete: %s -> %s", filename, target)


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
    name = Path(filename).stem
    logger.info("searching movie: %s", name)
    results = await jellyfin.search_movie(name)

    logger.info("search results for %s: %d found", name, len(results))
    return results
