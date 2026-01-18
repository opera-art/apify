"""Pinterest pin details service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import PINTEREST_ACTOR_ID
from .schemas import PinterestResponse
from .utils import run_actor, get_default_proxy


class PinterestPinRequest(BaseModel):
    """Request to get Pinterest pin details."""

    pin_url: str = Field(
        alias="pinUrl",
        description="Pinterest pin URL",
    )

    class Config:
        populate_by_name = True


def build_pin_input(request: PinterestPinRequest) -> dict:
    """Build the input payload for pin details."""
    return {
        "startUrls": [{"url": request.pin_url}],
        "maxItems": 1,
        "proxy": get_default_proxy(),
    }


async def get_pin(
    client: ApifyClient,
    pin_url: str,
) -> PinterestResponse:
    """
    Get Pinterest pin details.

    Args:
        client: Apify client instance
        pin_url: Pinterest pin URL

    Returns:
        PinterestResponse with pin details
    """
    request = PinterestPinRequest(pin_url=pin_url)
    actor_input = build_pin_input(request)
    return run_actor(client, PINTEREST_ACTOR_ID, actor_input)
