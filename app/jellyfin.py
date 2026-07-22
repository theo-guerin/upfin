import logging

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MovieSearchResult(BaseModel):
    name: str = Field(alias="Name")
    production_year: int = Field(alias="ProductionYear")
    image_url: str | None = Field(default=None, alias="ImageUrl")
    overview: str | None = Field(default=None, alias="Overview")


class Jellyfin:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f'MediaBrowser Token="{api_key}"',
            },
        )

    async def search_movie(
        self, name: str, year: int | None = None
    ) -> list[MovieSearchResult]:
        """raises:
        httpx.HTTPStatusError: If the request to the Jellyfin API fails.
        """

        response = await self._client.post(
            "/Items/RemoteSearch/Movie",
            json={
                "SearchInfo": {
                    "Name": name,
                    "Year": year,
                },
                "SearchProviderName": "TheMovieDb",
            },
        )
        response.raise_for_status()

        results = []
        for raw_result in response.json():
            try:
                result = MovieSearchResult.model_validate(raw_result)
            except Exception:
                logger.debug("skipping invalid search result: %s", raw_result)
                continue
            results.append(result)

        logger.info("jellyfin search %s: %d results", name, len(results))
        return results
