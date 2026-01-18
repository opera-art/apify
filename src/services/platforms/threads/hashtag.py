"""Threads hashtag scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import THREADS_ACTOR_ID, THREADS_DEFAULT_RESULTS, THREADS_MAX_RESULTS
from .schemas import ThreadsResponse
from .utils import run_actor


class ThreadsHashtagRequest(BaseModel):
    """Request to scrape Threads by hashtag."""

    hashtag: str = Field(description="Hashtag (without #)")
    limit: int = Field(
        default=THREADS_DEFAULT_RESULTS,
        ge=1,
        le=THREADS_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_hashtag_input(request: ThreadsHashtagRequest) -> dict:
    """Build the input payload for hashtag scraping."""
    return {
        "searchQueries": [f"#{request.hashtag}"],
        "maxItems": request.limit,
    }


async def scrape_hashtag(
    client: ApifyClient,
    hashtag: str,
    limit: int = THREADS_DEFAULT_RESULTS,
) -> ThreadsResponse:
    """
    Scrape threads by hashtag.

    Args:
        client: Apify client instance
        hashtag: Hashtag (without #)
        limit: Maximum number of threads

    Returns:
        ThreadsResponse with hashtag threads
    """
    request = ThreadsHashtagRequest(hashtag=hashtag, limit=limit)
    actor_input = build_hashtag_input(request)
    return run_actor(client, THREADS_ACTOR_ID, actor_input)
