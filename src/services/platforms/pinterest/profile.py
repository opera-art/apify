"""Pinterest profile scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import PINTEREST_ACTOR_ID, PINTEREST_DEFAULT_RESULTS, PINTEREST_MAX_RESULTS
from .schemas import PinterestResponse
from .utils import run_actor, get_default_proxy


class PinterestProfileRequest(BaseModel):
    """Request to scrape Pinterest profile."""

    profile_url: str = Field(
        alias="profileUrl",
        description="Pinterest profile URL",
    )
    limit: int = Field(
        default=PINTEREST_DEFAULT_RESULTS,
        ge=1,
        le=PINTEREST_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_profile_input(request: PinterestProfileRequest) -> dict:
    """Build the input payload for profile scraping."""
    return {
        "startUrls": [{"url": request.profile_url}],
        "maxItems": request.limit,
        "proxy": get_default_proxy(),
    }


async def scrape_profile(
    client: ApifyClient,
    profile_url: str,
    limit: int = PINTEREST_DEFAULT_RESULTS,
) -> PinterestResponse:
    """
    Scrape pins from a Pinterest profile.

    Args:
        client: Apify client instance
        profile_url: Pinterest profile URL
        limit: Maximum number of pins

    Returns:
        PinterestResponse with profile pins
    """
    request = PinterestProfileRequest(profile_url=profile_url, limit=limit)
    actor_input = build_profile_input(request)
    return run_actor(client, PINTEREST_ACTOR_ID, actor_input)
