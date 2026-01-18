"""Threads search service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import THREADS_ACTOR_ID, THREADS_DEFAULT_RESULTS, THREADS_MAX_RESULTS
from .schemas import ThreadsResponse
from .utils import run_actor


class ThreadsSearchRequest(BaseModel):
    """Request to search Threads."""

    query: str = Field(description="Search query")
    limit: int = Field(
        default=THREADS_DEFAULT_RESULTS,
        ge=1,
        le=THREADS_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_search_input(request: ThreadsSearchRequest) -> dict:
    """Build the input payload for search."""
    return {
        "searchQueries": [request.query],
        "maxItems": request.limit,
    }


async def search(
    client: ApifyClient,
    query: str,
    limit: int = THREADS_DEFAULT_RESULTS,
) -> ThreadsResponse:
    """
    Search Threads.

    Args:
        client: Apify client instance
        query: Search query
        limit: Maximum number of results

    Returns:
        ThreadsResponse with search results
    """
    request = ThreadsSearchRequest(query=query, limit=limit)
    actor_input = build_search_input(request)
    return run_actor(client, THREADS_ACTOR_ID, actor_input)
