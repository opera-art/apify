"""Instagram profile scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import INSTAGRAM_PROFILE_ACTOR_ID
from .schemas import InstagramResponse
from .utils import run_actor, get_default_proxy


class InstagramProfileRequest(BaseModel):
    """Request to scrape Instagram profile data."""

    usernames: list[str] = Field(
        ...,
        description="List of Instagram usernames to scrape",
        examples=[["natgeo", "instagram"]],
    )

    class Config:
        populate_by_name = True


def build_profile_input(request: InstagramProfileRequest) -> dict:
    """Build the input payload for profile scraping."""
    return {
        "usernames": request.usernames,
        "proxy": get_default_proxy(),
    }


async def scrape_profiles(
    client: ApifyClient,
    request: InstagramProfileRequest,
) -> InstagramResponse:
    """
    Scrape Instagram profile metadata.

    Returns: bio, followers, following, posts count, etc.
    """
    actor_input = build_profile_input(request)
    return run_actor(client, INSTAGRAM_PROFILE_ACTOR_ID, actor_input)


async def get_profile(
    client: ApifyClient,
    username: str,
) -> InstagramResponse:
    """Get a single profile's metadata."""
    request = InstagramProfileRequest(usernames=[username])
    return await scrape_profiles(client, request)
