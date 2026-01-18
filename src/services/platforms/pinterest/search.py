"""Pinterest search service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import PINTEREST_ACTOR_ID, PINTEREST_DEFAULT_RESULTS, PINTEREST_MAX_RESULTS
from .schemas import PinterestResponse
from .utils import run_actor, get_default_proxy


class PinterestSearchRequest(BaseModel):
    """Request to search Pinterest pins."""

    query: str = Field(description="Search query")
    limit: int = Field(
        default=PINTEREST_DEFAULT_RESULTS,
        ge=1,
        le=PINTEREST_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_search_input(request: PinterestSearchRequest) -> dict:
    """Build the input payload for search."""
    search_url = f"https://www.pinterest.com/search/pins/?q={request.query}"
    return {
        "startUrls": [{"url": search_url}],
        "maxItems": request.limit,
        "proxy": get_default_proxy(),
    }


async def search(
    client: ApifyClient,
    query: str,
    limit: int = PINTEREST_DEFAULT_RESULTS,
) -> PinterestResponse:
    """
    Search Pinterest pins.

    Args:
        client: Apify client instance
        query: Search query
        limit: Maximum number of results

    Returns:
        PinterestResponse with search results
    """
    request = PinterestSearchRequest(query=query, limit=limit)
    actor_input = build_search_input(request)
    return run_actor(client, PINTEREST_ACTOR_ID, actor_input)
