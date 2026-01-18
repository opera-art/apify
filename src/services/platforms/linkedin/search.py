"""LinkedIn search service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import LINKEDIN_ACTOR_ID, LINKEDIN_DEFAULT_RESULTS, LINKEDIN_MAX_RESULTS
from .schemas import LinkedInResponse
from .utils import run_actor


class LinkedInSearchRequest(BaseModel):
    """Request to search LinkedIn posts."""

    query: str = Field(description="Search query")
    limit: int = Field(
        default=LINKEDIN_DEFAULT_RESULTS,
        ge=1,
        le=LINKEDIN_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_search_input(request: LinkedInSearchRequest) -> dict:
    """Build the input payload for search."""
    return {
        "searchQueries": [request.query],
        "maxPosts": request.limit,
    }


async def search_posts(
    client: ApifyClient,
    query: str,
    limit: int = LINKEDIN_DEFAULT_RESULTS,
) -> LinkedInResponse:
    """
    Search LinkedIn posts.

    Args:
        client: Apify client instance
        query: Search query
        limit: Maximum number of results

    Returns:
        LinkedInResponse with search results
    """
    request = LinkedInSearchRequest(query=query, limit=limit)
    actor_input = build_search_input(request)
    return run_actor(client, LINKEDIN_ACTOR_ID, actor_input)
