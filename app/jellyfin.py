import httpx
from pydantic import BaseModel, Field


class MovieSearchResult(BaseModel):
    name: str | None = Field(default=None, alias="Name")
    production_year: int | None = Field(default=None, alias="ProductionYear")
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

    async def search_movie(self, query: str) -> list[MovieSearchResult]:
        response = await self._client.post(
            "/Items/RemoteSearch/Movie",
            json={"SearchInfo": {"Name": query}},
        )
        response.raise_for_status()
        return [MovieSearchResult.model_validate(item) for item in response.json()]
