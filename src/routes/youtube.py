"""YouTube API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.youtube import (
    YouTubeResponse,
    search,
    scrape_channel,
    get_video,
    scrape_playlist,
)

router = APIRouter(prefix="/youtube", tags=["YouTube"])


@router.get(
    "/search",
    response_model=YouTubeResponse,
    summary="Search YouTube",
)
async def search_youtube(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=50, ge=1, le=500),
    include_shorts: bool = Query(default=True, alias="includeShorts"),
    client: ApifyClient = Depends(get_apify_client),
) -> YouTubeResponse:
    """Search YouTube videos."""
    try:
        return await search(client, q, limit, include_shorts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/channel",
    response_model=YouTubeResponse,
    summary="Scrape channel videos",
)
async def get_channel_videos(
    url: str = Query(..., description="YouTube channel URL"),
    limit: int = Query(default=50, ge=1, le=500),
    include_shorts: bool = Query(default=True, alias="includeShorts"),
    include_streams: bool = Query(default=True, alias="includeStreams"),
    client: ApifyClient = Depends(get_apify_client),
) -> YouTubeResponse:
    """Get videos from a YouTube channel."""
    try:
        return await scrape_channel(client, url, limit, include_shorts, include_streams)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/video",
    response_model=YouTubeResponse,
    summary="Get video details",
)
async def get_video_details(
    url: str = Query(..., description="YouTube video URL"),
    include_comments: bool = Query(default=False, alias="includeComments"),
    max_comments: int = Query(default=100, alias="maxComments", ge=0),
    client: ApifyClient = Depends(get_apify_client),
) -> YouTubeResponse:
    """Get YouTube video details."""
    try:
        return await get_video(client, url, include_comments, max_comments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/playlist",
    response_model=YouTubeResponse,
    summary="Scrape playlist videos",
)
async def get_playlist_videos(
    url: str = Query(..., description="YouTube playlist URL"),
    limit: int = Query(default=50, ge=1, le=500),
    client: ApifyClient = Depends(get_apify_client),
) -> YouTubeResponse:
    """Get videos from a YouTube playlist."""
    try:
        return await scrape_playlist(client, url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
