"""Instagram comments scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_ACTOR_ID
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramCommentsRequest(BaseModel):
    """Request to scrape comments from posts."""

    post_urls: list[str] = Field(
        ...,
        alias="postUrls",
        description="List of Instagram post URLs to get comments from",
        examples=[["https://www.instagram.com/p/ABC123/"]],
    )
    results_limit: int = Field(
        default=100,
        alias="resultsLimit",
        ge=1,
        le=1000,
        description="Maximum comments per post",
    )

    class Config:
        populate_by_name = True


def build_comments_input(request: InstagramCommentsRequest) -> dict:
    """Build the input payload for comments scraping."""
    return {
        "directUrls": request.post_urls,
        "resultsType": "comments",
        "resultsLimit": request.results_limit,
        "proxy": get_default_proxy(),
    }


def scrape_comments(
    client: ApifyClient,
    request: InstagramCommentsRequest,
) -> InstagramResponse:
    """
    Scrape comments from Instagram posts.

    Returns: comment text, author, likes, timestamp, etc.
    """
    actor_input = build_comments_input(request)
    return run_actor(client, INSTAGRAM_ACTOR_ID, actor_input)


def get_post_comments(
    client: ApifyClient,
    post_url: str,
    limit: int = 100,
) -> InstagramResponse:
    """Get comments from a single post."""
    request = InstagramCommentsRequest(post_urls=[post_url], results_limit=limit)
    return scrape_comments(client, request)
