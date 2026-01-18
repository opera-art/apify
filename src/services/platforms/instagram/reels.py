"""Instagram reels scraping service."""

from typing import Optional
from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_ACTOR_ID, INSTAGRAM_DEFAULT_RESULTS, INSTAGRAM_MAX_RESULTS
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramReelsRequest(BaseModel):
    """Request to scrape reels from profiles."""

    usernames: Optional[list[str]] = Field(
        default=None,
        description="List of Instagram usernames",
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
        description="Maximum reels per profile",
    )

    class Config:
        populate_by_name = True


def build_reels_input(request: InstagramReelsRequest) -> dict:
    """Build the input payload for reels scraping."""
    direct_urls = []

    if request.usernames:
        direct_urls.extend([f"https://www.instagram.com/{u}/reels/" for u in request.usernames])

    if request.profile_urls:
        for url in request.profile_urls:
            if "/reels" not in url:
                url = url.rstrip("/") + "/reels/"
            direct_urls.append(url)

    if not direct_urls:
        raise ValueError("Either usernames or profileUrls must be provided")

    return {
        "directUrls": direct_urls,
        "resultsType": "posts",
        "resultsLimit": request.results_limit,
        "proxy": get_default_proxy(),
    }


async def scrape_reels(
    client: ApifyClient,
    request: InstagramReelsRequest,
) -> InstagramResponse:
    """
    Scrape reels from Instagram profiles.

    Returns: reel videos, views, likes, etc.
    """
    actor_input = build_reels_input(request)
    return run_actor(client, INSTAGRAM_ACTOR_ID, actor_input)


async def get_user_reels(
    client: ApifyClient,
    username: str,
    limit: int = INSTAGRAM_DEFAULT_RESULTS,
) -> InstagramResponse:
    """Get reels from a single user."""
    request = InstagramReelsRequest(usernames=[username], results_limit=limit)
    return await scrape_reels(client, request)
