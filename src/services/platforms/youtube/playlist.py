"""YouTube playlist scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import YOUTUBE_ACTOR_ID, YOUTUBE_DEFAULT_RESULTS, YOUTUBE_MAX_RESULTS
from .schemas import YouTubeResponse
from .utils import run_actor


class YouTubePlaylistRequest(BaseModel):
    """Request to scrape YouTube playlist."""

    playlist_url: str = Field(
        alias="playlistUrl",
        description="YouTube playlist URL",
    )
    limit: int = Field(
        default=YOUTUBE_DEFAULT_RESULTS,
        ge=1,
        le=YOUTUBE_MAX_RESULTS,
    )

    class Config:
        populate_by_name = True


def build_playlist_input(request: YouTubePlaylistRequest) -> dict:
    """Build the input payload for playlist scraping."""
    return {
        "startUrls": [{"url": request.playlist_url}],
        "maxResults": request.limit,
    }


async def scrape_playlist(
    client: ApifyClient,
    playlist_url: str,
    limit: int = YOUTUBE_DEFAULT_RESULTS,
) -> YouTubeResponse:
    """
    Scrape videos from a YouTube playlist.

    Args:
        client: Apify client instance
        playlist_url: YouTube playlist URL
        limit: Maximum number of videos

    Returns:
        YouTubeResponse with playlist videos
    """
    request = YouTubePlaylistRequest(
        playlist_url=playlist_url,
        limit=limit,
    )
    actor_input = build_playlist_input(request)
    return run_actor(client, YOUTUBE_ACTOR_ID, actor_input)
