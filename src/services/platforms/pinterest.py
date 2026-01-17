"""
Pinterest Platform Module
Handles Pinterest-specific scraping operations via Apify.
"""

from pydantic import BaseModel, Field
from typing import Optional
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

PINTEREST_ACTOR_ID = "epctex/pinterest-scraper"

PINTEREST_MAX_RESULTS = 200
PINTEREST_DEFAULT_RESULTS = 20


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class PinterestScrapeRequest(BaseModel):
    """Request schema for Pinterest scraping."""

    pin_urls: Optional[list[str]] = Field(
        default=None,
        alias="pinUrls",
        description="Direct Pinterest pin URLs to scrape",
        examples=[["https://www.pinterest.com/pin/123456789/"]],
    )
    board_urls: Optional[list[str]] = Field(
        default=None,
        alias="boardUrls",
        description="Pinterest board URLs to scrape",
        examples=[["https://www.pinterest.com/user/board-name/"]],
    )
    profile_urls: Optional[list[str]] = Field(
        default=None,
        alias="profileUrls",
        description="Pinterest profile URLs to scrape",
        examples=[["https://www.pinterest.com/username/"]],
    )
    search_queries: Optional[list[str]] = Field(
        default=None,
        alias="searchQueries",
        description="Search terms to find pins",
        examples=[["home decor", "recipes"]],
    )
    max_items: int = Field(
        default=PINTEREST_DEFAULT_RESULTS,
        alias="maxItems",
        ge=1,
        le=PINTEREST_MAX_RESULTS,
        description="Maximum number of pins to scrape",
    )
    end_page: int = Field(
        default=1,
        alias="endPage",
        ge=1,
        le=10,
        description="Last page to scrape",
    )

    class Config:
        populate_by_name = True


class PinterestScrapeResponse(BaseModel):
    """Response schema for Pinterest scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_pinterest_request(request: PinterestScrapeRequest) -> tuple[bool, Optional[str]]:
    """Validate Pinterest scrape request."""
    if not any([request.pin_urls, request.board_urls, request.profile_urls, request.search_queries]):
        return False, "At least one of pinUrls, boardUrls, profileUrls, or searchQueries must be provided"
    return True, None


# =============================================================================
# BUILDER FUNCTIONS
# =============================================================================

def build_pinterest_actor_input(request: PinterestScrapeRequest) -> dict:
    """Build the input payload for the Pinterest Actor."""
    start_urls = []

    if request.pin_urls:
        start_urls.extend(request.pin_urls)

    if request.board_urls:
        start_urls.extend(request.board_urls)

    if request.profile_urls:
        start_urls.extend(request.profile_urls)

    if request.search_queries:
        for query in request.search_queries:
            search_url = f"https://www.pinterest.com/search/pins/?q={query}"
            start_urls.append(search_url)

    actor_input = {
        "startUrls": [{"url": url} for url in start_urls],
        "maxItems": request.max_items,
        "endPage": request.end_page,
        "proxy": {
            "useApifyProxy": True
        }
    }

    return actor_input


# =============================================================================
# SERVICE CLASS
# =============================================================================

class PinterestService:
    """Service for Pinterest scraping operations."""

    def __init__(self, client: ApifyClient):
        self.client = client

    async def scrape(self, request: PinterestScrapeRequest) -> PinterestScrapeResponse:
        """Execute Pinterest scraping based on request parameters."""
        is_valid, error = validate_pinterest_request(request)
        if not is_valid:
            raise ValueError(error)

        actor_input = build_pinterest_actor_input(request)
        run = self.client.actor(PINTEREST_ACTOR_ID).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return PinterestScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    async def scrape_board(self, board_url: str, limit: int = PINTEREST_DEFAULT_RESULTS) -> PinterestScrapeResponse:
        """Scrape pins from a Pinterest board."""
        request = PinterestScrapeRequest(board_urls=[board_url], max_items=limit)
        return await self.scrape(request)

    async def scrape_profile(self, profile_url: str, limit: int = PINTEREST_DEFAULT_RESULTS) -> PinterestScrapeResponse:
        """Scrape pins from a Pinterest profile."""
        request = PinterestScrapeRequest(profile_urls=[profile_url], max_items=limit)
        return await self.scrape(request)

    async def search(self, query: str, limit: int = PINTEREST_DEFAULT_RESULTS) -> PinterestScrapeResponse:
        """Search Pinterest pins."""
        request = PinterestScrapeRequest(search_queries=[query], max_items=limit)
        return await self.scrape(request)

    async def scrape_pin(self, pin_url: str) -> PinterestScrapeResponse:
        """Scrape a specific Pinterest pin."""
        request = PinterestScrapeRequest(pin_urls=[pin_url])
        return await self.scrape(request)
