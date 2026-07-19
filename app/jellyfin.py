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

        async def request(name: str, year: int | None) -> httpx.Response:
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
            return response

        raw_response = await request(name, year)
        if not raw_response and year is not None:
            logger.info("no results for %s (%s), retrying without year", name, year)
            raw_response = await request(name, None)

        results = []
        for raw_result in raw_response.json():
            try:
                result = MovieSearchResult.model_validate(raw_result)
            except Exception:
                logger.debug("skipping invalid search result: %s", raw_result)
                continue
            results.append(result)

        logger.info("jellyfin search %s: %d results", name, len(results))
        return results
