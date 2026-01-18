"""YouTube video details service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import YOUTUBE_ACTOR_ID
from .schemas import YouTubeResponse
from .utils import run_actor


class YouTubeVideoRequest(BaseModel):
    """Request to get YouTube video details."""

    video_url: str = Field(
        alias="videoUrl",
        description="YouTube video URL",
    )
    include_comments: bool = Field(
        default=False,
        alias="includeComments",
    )
    max_comments: int = Field(
        default=100,
        alias="maxComments",
        ge=0,
    )

    class Config:
        populate_by_name = True


def build_video_input(request: YouTubeVideoRequest) -> dict:
    """Build the input payload for video details."""
    return {
        "startUrls": [{"url": request.video_url}],
        "maxResults": 1,
        "maxComments": request.max_comments if request.include_comments else 0,
    }


async def get_video(
    client: ApifyClient,
    video_url: str,
    include_comments: bool = False,
    max_comments: int = 100,
) -> YouTubeResponse:
    """
    Get YouTube video details.

    Args:
        client: Apify client instance
        video_url: YouTube video URL
        include_comments: Include video comments
        max_comments: Maximum comments to fetch

    Returns:
        YouTubeResponse with video details
    """
    request = YouTubeVideoRequest(
        video_url=video_url,
        include_comments=include_comments,
        max_comments=max_comments,
    )
    actor_input = build_video_input(request)
    return run_actor(client, YOUTUBE_ACTOR_ID, actor_input)
