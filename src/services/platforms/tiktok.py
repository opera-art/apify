"""
TikTok Platform Module
Handles TikTok-specific scraping operations via Apify.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

TIKTOK_ACTOR_ID = "clockworks/tiktok-scraper"

TIKTOK_MAX_RESULTS_PER_PAGE = 100
TIKTOK_DEFAULT_RESULTS = 10


# =============================================================================
# TYPES / ENUMS
# =============================================================================

class TikTokSearchType(str, Enum):
    VIDEO = "video"
    USER = "user"
    TOP = "top"


class TikTokSortType(str, Enum):
    LATEST = "latest"
    OLDEST = "oldest"
    POPULAR = "popular"


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class TikTokScrapeRequest(BaseModel):
    """Request schema for TikTok scraping."""

    hashtags: Optional[list[str]] = Field(
        default=None,
        description="List of TikTok hashtags to scrape (without #)",
        examples=[["dance", "funny"]],
    )
    profiles: Optional[list[str]] = Field(
        default=None,
        description="List of TikTok usernames to scrape",
        examples=[["tiktok", "charlidamelio"]],
    )
    search_queries: Optional[list[str]] = Field(
        default=None,
        alias="searchQueries",
        description="Search terms to find videos/users",
        examples=[["cooking recipes"]],
    )
    video_urls: Optional[list[str]] = Field(
        default=None,
        alias="videoUrls",
        description="Direct TikTok video URLs to scrape",
        examples=[["https://www.tiktok.com/@user/video/123456"]],
    )
    results_per_page: int = Field(
        default=TIKTOK_DEFAULT_RESULTS,
        alias="resultsPerPage",
        ge=1,
        le=TIKTOK_MAX_RESULTS_PER_PAGE,
        description="Number of results per hashtag/profile/search",
    )
    search_type: Optional[TikTokSearchType] = Field(
        default=TikTokSearchType.TOP,
        alias="searchType",
        description="Type of search results to return",
    )
    sort_type: Optional[TikTokSortType] = Field(
        default=None,
        alias="sortType",
        description="How to sort results",
    )

    class Config:
        populate_by_name = True


class TikTokScrapeResponse(BaseModel):
    """Response schema for TikTok scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_tiktok_request(request: TikTokScrapeRequest) -> tuple[bool, Optional[str]]:
    """Validate TikTok scrape request."""
    if not any([request.hashtags, request.profiles, request.search_queries, request.video_urls]):
        return False, "At least one of hashtags, profiles, searchQueries, or videoUrls must be provided"
    return True, None


# =============================================================================
# BUILDER FUNCTIONS
# =============================================================================

def build_tiktok_actor_input(request: TikTokScrapeRequest) -> dict:
    """Build the input payload for the TikTok Actor."""
    actor_input = {
        "resultsPerPage": request.results_per_page,
    }

    if request.hashtags:
        actor_input["hashtags"] = request.hashtags

    if request.profiles:
        actor_input["profiles"] = request.profiles

    if request.search_queries:
        actor_input["searchQueries"] = request.search_queries

    if request.video_urls:
        actor_input["postURLs"] = request.video_urls

    if request.search_type:
        actor_input["searchSection"] = request.search_type.value

    if request.sort_type:
        actor_input["oldestFirst"] = request.sort_type.value == "oldest"

    return actor_input


# =============================================================================
# SERVICE CLASS
# =============================================================================

class TikTokService:
    """Service for TikTok scraping operations."""

    def __init__(self, client: ApifyClient):
        self.client = client

    async def scrape(self, request: TikTokScrapeRequest) -> TikTokScrapeResponse:
        """Execute TikTok scraping based on request parameters."""
        is_valid, error = validate_tiktok_request(request)
        if not is_valid:
            raise ValueError(error)

        actor_input = build_tiktok_actor_input(request)
        run = self.client.actor(TIKTOK_ACTOR_ID).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return TikTokScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    async def scrape_hashtag(self, hashtag: str, limit: int = TIKTOK_DEFAULT_RESULTS) -> TikTokScrapeResponse:
        """Scrape videos by hashtag."""
        request = TikTokScrapeRequest(hashtags=[hashtag], results_per_page=limit)
        return await self.scrape(request)

    async def scrape_profile(self, username: str, limit: int = TIKTOK_DEFAULT_RESULTS) -> TikTokScrapeResponse:
        """Scrape profile and videos by username."""
        request = TikTokScrapeRequest(profiles=[username], results_per_page=limit)
        return await self.scrape(request)

    async def search(self, query: str, limit: int = TIKTOK_DEFAULT_RESULTS) -> TikTokScrapeResponse:
        """Search TikTok."""
        request = TikTokScrapeRequest(search_queries=[query], results_per_page=limit)
        return await self.scrape(request)
