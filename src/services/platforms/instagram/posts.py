"""Instagram posts scraping service."""

from typing import Optional
from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_ACTOR_ID, INSTAGRAM_DEFAULT_RESULTS, INSTAGRAM_MAX_RESULTS
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramPostsRequest(BaseModel):
    """Request to scrape posts from profiles."""

    usernames: Optional[list[str]] = Field(
        default=None,
        description="List of Instagram usernames",
        examples=[["natgeo"]],
    )
    profile_urls: Optional[list[str]] = Field(
        default=None,
        alias="profileUrls",
        description="Direct profile URLs",
    )
    results_limit: int = Field(
        default=INSTAGRAM_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=INSTAGRAM_MAX_RESULTS,
        description="Maximum posts per profile",
    )

    class Config:
        populate_by_name = True


def build_posts_input(request: InstagramPostsRequest) -> dict:
    """Build the input payload for posts scraping."""
    direct_urls = []

    if request.usernames:
        direct_urls.extend([f"https://www.instagram.com/{u}/" for u in request.usernames])

    if request.profile_urls:
        direct_urls.extend(request.profile_urls)

    if not direct_urls:
        raise ValueError("Either usernames or profileUrls must be provided")

    return {
        "directUrls": direct_urls,
        "resultsType": "posts",
        "resultsLimit": request.results_limit,
        "proxy": get_default_proxy(),
    }


async def scrape_posts(
    client: ApifyClient,
    request: InstagramPostsRequest,
) -> InstagramResponse:
    """
    Scrape posts from Instagram profiles.

    Returns: post images, captions, likes, comments count, etc.
    """
    actor_input = build_posts_input(request)
    return run_actor(client, INSTAGRAM_ACTOR_ID, actor_input)


async def get_user_posts(
    client: ApifyClient,
    username: str,
    limit: int = INSTAGRAM_DEFAULT_RESULTS,
) -> InstagramResponse:
    """Get posts from a single user."""
    request = InstagramPostsRequest(usernames=[username], results_limit=limit)
    return await scrape_posts(client, request)
