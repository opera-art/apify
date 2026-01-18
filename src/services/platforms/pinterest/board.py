"""Pinterest board scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import PINTEREST_ACTOR_ID, PINTEREST_DEFAULT_RESULTS, PINTEREST_MAX_RESULTS
from .schemas import PinterestResponse
from .utils import run_actor, get_default_proxy


class PinterestBoardRequest(BaseModel):
    """Request to scrape Pinterest board."""

    board_url: str = Field(
        alias="boardUrl",
        description="Pinterest board URL",
    )
    limit: int = Field(
        default=PINTEREST_DEFAULT_RESULTS,
        ge=1,
        le=PINTEREST_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_board_input(request: PinterestBoardRequest) -> dict:
    """Build the input payload for board scraping."""
    return {
        "startUrls": [{"url": request.board_url}],
        "maxItems": request.limit,
        "proxy": get_default_proxy(),
    }


async def scrape_board(
    client: ApifyClient,
    board_url: str,
    limit: int = PINTEREST_DEFAULT_RESULTS,
) -> PinterestResponse:
    """
    Scrape pins from a Pinterest board.

    Args:
        client: Apify client instance
        board_url: Pinterest board URL
        limit: Maximum number of pins

    Returns:
        PinterestResponse with board pins
    """
    request = PinterestBoardRequest(board_url=board_url, limit=limit)
    actor_input = build_board_input(request)
    return run_actor(client, PINTEREST_ACTOR_ID, actor_input)
