"""
YouTube Platform Module
Handles YouTube-specific scraping operations via Apify.
"""

from pydantic import BaseModel, Field
from typing import Optional
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

YOUTUBE_ACTOR_ID = "streamers/youtube-scraper"

YOUTUBE_MAX_RESULTS = 500
YOUTUBE_DEFAULT_RESULTS = 50


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class YouTubeScrapeRequest(BaseModel):
    """Request schema for YouTube scraping."""

    search_queries: Optional[list[str]] = Field(
        default=None,
        alias="searchQueries",
        description="Search terms to find videos",
        examples=[["python tutorial", "machine learning"]],
    )
    channel_urls: Optional[list[str]] = Field(
        default=None,
        alias="channelUrls",
        description="YouTube channel URLs to scrape",
        examples=[["https://www.youtube.com/@Google"]],
    )
    video_urls: Optional[list[str]] = Field(
        default=None,
        alias="videoUrls",
        description="Direct YouTube video URLs",
        examples=[["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]],
    )
    playlist_urls: Optional[list[str]] = Field(
        default=None,
        alias="playlistUrls",
        description="YouTube playlist URLs",
    )
    max_results: int = Field(
        default=YOUTUBE_DEFAULT_RESULTS,
        alias="maxResults",
        ge=1,
        le=YOUTUBE_MAX_RESULTS,
        description="Maximum number of results",
    )
    max_comments: Optional[int] = Field(
        default=0,
        alias="maxComments",
        ge=0,
        description="Maximum comments to scrape per video (0 = none)",
    )
    include_shorts: bool = Field(
        default=True,
        alias="includeShorts",
        description="Include YouTube Shorts in results",
    )
    include_streams: bool = Field(
        default=True,
        alias="includeStreams",
        description="Include live streams in results",
    )

    class Config:
        populate_by_name = True


class YouTubeScrapeResponse(BaseModel):
    """Response schema for YouTube scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_youtube_request(request: YouTubeScrapeRequest) -> tuple[bool, Optional[str]]:
    """Validate YouTube scrape request."""
    if not any([request.search_queries, request.channel_urls, request.video_urls, request.playlist_urls]):
        return False, "At least one of searchQueries, channelUrls, videoUrls, or playlistUrls must be provided"
    return True, None


# =============================================================================
# BUILDER FUNCTIONS
# =============================================================================

def build_youtube_actor_input(request: YouTubeScrapeRequest) -> dict:
    """Build the input payload for the YouTube Actor."""
    start_urls = []

    # Convert search queries to YouTube search URLs
    if request.search_queries:
        for query in request.search_queries:
            start_urls.append(f"https://www.youtube.com/results?search_query={query}")

    # Add channel URLs (ensure /videos path)
    if request.channel_urls:
        for url in request.channel_urls:
            if "/videos" not in url:
                url = url.rstrip("/") + "/videos"
            start_urls.append(url)

    # Add video URLs directly
    if request.video_urls:
        start_urls.extend(request.video_urls)

    # Add playlist URLs
    if request.playlist_urls:
        start_urls.extend(request.playlist_urls)

    actor_input = {
        "startUrls": [{"url": url} for url in start_urls],
        "maxResults": request.max_results,
        "maxResultsShorts": request.max_results if request.include_shorts else 0,
        "maxResultStreams": request.max_results if request.include_streams else 0,
        "maxComments": request.max_comments,
    }

    return actor_input


# =============================================================================
# SERVICE CLASS
# =============================================================================

class YouTubeService:
    """Service for YouTube scraping operations."""

    def __init__(self, client: ApifyClient):
        self.client = client

    async def scrape(self, request: YouTubeScrapeRequest) -> YouTubeScrapeResponse:
        """Execute YouTube scraping based on request parameters."""
        is_valid, error = validate_youtube_request(request)
        if not is_valid:
            raise ValueError(error)

        actor_input = build_youtube_actor_input(request)
        run = self.client.actor(YOUTUBE_ACTOR_ID).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return YouTubeScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    async def search(self, query: str, limit: int = YOUTUBE_DEFAULT_RESULTS) -> YouTubeScrapeResponse:
        """Search YouTube videos."""
        request = YouTubeScrapeRequest(search_queries=[query], max_results=limit)
        return await self.scrape(request)

    async def scrape_channel(self, channel_url: str, limit: int = YOUTUBE_DEFAULT_RESULTS) -> YouTubeScrapeResponse:
        """Scrape videos from a YouTube channel."""
        request = YouTubeScrapeRequest(channel_urls=[channel_url], max_results=limit)
        return await self.scrape(request)

    async def scrape_video(self, video_url: str, include_comments: bool = False) -> YouTubeScrapeResponse:
        """Scrape a specific YouTube video."""
        max_comments = 100 if include_comments else 0
        request = YouTubeScrapeRequest(video_urls=[video_url], max_comments=max_comments)
        return await self.scrape(request)

    async def scrape_playlist(self, playlist_url: str, limit: int = YOUTUBE_DEFAULT_RESULTS) -> YouTubeScrapeResponse:
        """Scrape videos from a YouTube playlist."""
        request = YouTubeScrapeRequest(playlist_urls=[playlist_url], max_results=limit)
        return await self.scrape(request)
