"""Instagram post details scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_POST_ACTOR_ID
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramPostDetailRequest(BaseModel):
    """Request to get details of specific posts."""

    post_urls: list[str] = Field(
        ...,
        alias="postUrls",
        description="List of Instagram post URLs",
        examples=[["https://www.instagram.com/p/ABC123/"]],
    )

    class Config:
        populate_by_name = True


def build_post_details_input(request: InstagramPostDetailRequest) -> dict:
    """Build the input payload for post details scraping."""
    return {
        "directUrls": request.post_urls,
        "resultsType": "details",
        "proxy": get_default_proxy(),
    }


def scrape_post_details(
    client: ApifyClient,
    request: InstagramPostDetailRequest,
) -> InstagramResponse:
    """
    Get detailed information about specific posts.

    Returns: full post metadata without comments.
    """
    actor_input = build_post_details_input(request)
    return run_actor(client, INSTAGRAM_POST_ACTOR_ID, actor_input)


def get_post_details(
    client: ApifyClient,
    post_url: str,
) -> InstagramResponse:
    """Get details of a single post."""
    request = InstagramPostDetailRequest(post_urls=[post_url])
    return scrape_post_details(client, request)
