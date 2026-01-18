"""Instagram hashtag scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_HASHTAG_ACTOR_ID, INSTAGRAM_DEFAULT_RESULTS, INSTAGRAM_MAX_RESULTS
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramHashtagRequest(BaseModel):
    """Request to scrape posts from hashtags."""

    hashtags: list[str] = Field(
        ...,
        description="List of hashtags (without #)",
        examples=[["travel", "photography"]],
    )
    results_limit: int = Field(
        default=INSTAGRAM_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=INSTAGRAM_MAX_RESULTS,
        description="Maximum posts per hashtag",
    )

    class Config:
        populate_by_name = True


def build_hashtag_input(request: InstagramHashtagRequest) -> dict:
    """Build the input payload for hashtag scraping."""
    return {
        "hashtags": request.hashtags,
        "resultsLimit": request.results_limit,
        "proxy": get_default_proxy(),
    }


def scrape_hashtag(
    client: ApifyClient,
    request: InstagramHashtagRequest,
) -> InstagramResponse:
    """
    Scrape posts from hashtags.

    Returns: posts containing the specified hashtags.
    """
    actor_input = build_hashtag_input(request)
    return run_actor(client, INSTAGRAM_HASHTAG_ACTOR_ID, actor_input)


def get_hashtag_posts(
    client: ApifyClient,
    hashtag: str,
    limit: int = INSTAGRAM_DEFAULT_RESULTS,
) -> InstagramResponse:
    """Get posts from a single hashtag."""
    request = InstagramHashtagRequest(hashtags=[hashtag], results_limit=limit)
    return scrape_hashtag(client, request)
