"""Threads profile scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import THREADS_ACTOR_ID, THREADS_DEFAULT_RESULTS, THREADS_MAX_RESULTS
from .schemas import ThreadsResponse
from .utils import run_actor


class ThreadsProfileRequest(BaseModel):
    """Request to scrape Threads profile."""

    username: str = Field(description="Threads username (without @)")
    limit: int = Field(
        default=THREADS_DEFAULT_RESULTS,
        ge=1,
        le=THREADS_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_profile_input(request: ThreadsProfileRequest) -> dict:
    """Build the input payload for profile scraping."""
    return {
        "usernames": [request.username],
        "maxItems": request.limit,
    }


async def scrape_profile(
    client: ApifyClient,
    username: str,
    limit: int = THREADS_DEFAULT_RESULTS,
) -> ThreadsResponse:
    """
    Scrape threads from a user profile.

    Args:
        client: Apify client instance
        username: Threads username (without @)
        limit: Maximum number of threads

    Returns:
        ThreadsResponse with profile threads
    """
    request = ThreadsProfileRequest(username=username, limit=limit)
    actor_input = build_profile_input(request)
    return run_actor(client, THREADS_ACTOR_ID, actor_input)
