"""YouTube search service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import YOUTUBE_ACTOR_ID, YOUTUBE_DEFAULT_RESULTS, YOUTUBE_MAX_RESULTS
from .schemas import YouTubeResponse
from .utils import run_actor


class YouTubeSearchRequest(BaseModel):
    """Request to search YouTube videos."""

    query: str = Field(description="Search query")
    limit: int = Field(
        default=YOUTUBE_DEFAULT_RESULTS,
        ge=1,
        le=YOUTUBE_MAX_RESULTS,
    )
    include_shorts: bool = Field(
        default=True,
        alias="includeShorts",
    )

    class Config:
        populate_by_name = True


def build_search_input(request: YouTubeSearchRequest) -> dict:
    """Build the input payload for search."""
    return {
        "startUrls": [{"url": f"https://www.youtube.com/results?search_query={request.query}"}],
        "maxResults": request.limit,
        "maxResultsShorts": request.limit if request.include_shorts else 0,
    }


async def search(
    client: ApifyClient,
    query: str,
    limit: int = YOUTUBE_DEFAULT_RESULTS,
    include_shorts: bool = True,
) -> YouTubeResponse:
    """
    Search YouTube videos.

    Args:
        client: Apify client instance
        query: Search query
        limit: Maximum number of results
        include_shorts: Include YouTube Shorts

    Returns:
        YouTubeResponse with search results
    """
    request = YouTubeSearchRequest(
        query=query,
        limit=limit,
        include_shorts=include_shorts,
    )
    actor_input = build_search_input(request)
    return run_actor(client, YOUTUBE_ACTOR_ID, actor_input)
