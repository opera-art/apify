"""YouTube channel scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import YOUTUBE_ACTOR_ID, YOUTUBE_DEFAULT_RESULTS, YOUTUBE_MAX_RESULTS
from .schemas import YouTubeResponse
from .utils import run_actor


class YouTubeChannelRequest(BaseModel):
    """Request to scrape YouTube channel."""

    channel_url: str = Field(
        alias="channelUrl",
        description="YouTube channel URL",
    )
    limit: int = Field(
        default=YOUTUBE_DEFAULT_RESULTS,
        ge=1,
        le=YOUTUBE_MAX_RESULTS,
    )
    include_shorts: bool = Field(
        default=True,
        alias="includeShorts",
    )
    include_streams: bool = Field(
        default=True,
        alias="includeStreams",
    )

    class Config:
        populate_by_name = True


def build_channel_input(request: YouTubeChannelRequest) -> dict:
    """Build the input payload for channel scraping."""
    url = request.channel_url
    if "/videos" not in url:
        url = url.rstrip("/") + "/videos"

    return {
        "startUrls": [{"url": url}],
        "maxResults": request.limit,
        "maxResultsShorts": request.limit if request.include_shorts else 0,
        "maxResultStreams": request.limit if request.include_streams else 0,
    }


async def scrape_channel(
    client: ApifyClient,
    channel_url: str,
    limit: int = YOUTUBE_DEFAULT_RESULTS,
    include_shorts: bool = True,
    include_streams: bool = True,
) -> YouTubeResponse:
    """
    Scrape videos from a YouTube channel.

    Args:
        client: Apify client instance
        channel_url: YouTube channel URL
        limit: Maximum number of videos
        include_shorts: Include YouTube Shorts
        include_streams: Include live streams

    Returns:
        YouTubeResponse with channel videos
    """
    request = YouTubeChannelRequest(
        channel_url=channel_url,
        limit=limit,
        include_shorts=include_shorts,
        include_streams=include_streams,
    )
    actor_input = build_channel_input(request)
    return run_actor(client, YOUTUBE_ACTOR_ID, actor_input)
