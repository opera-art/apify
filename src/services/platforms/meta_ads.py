"""
Meta Ads (Facebook Ads) Platform Module
Handles Meta Ads Library scraping operations via Apify.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

META_ADS_ACTOR_ID = "apify/facebook-ads-scraper"

META_ADS_MAX_RESULTS = 500
META_ADS_DEFAULT_RESULTS = 50

META_ADS_COUNTRIES = [
    "ALL", "US", "GB", "CA", "AU", "DE", "FR", "ES", "IT", "BR", "MX", "IN", "JP"
]

META_ADS_TYPES = [
    "all",
    "political_and_issue_ads",
    "housing",
    "employment",
    "credit"
]


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class MetaAdsScrapeRequest(BaseModel):
    """Request schema for Meta (Facebook) Ads scraping."""

    page_urls: Optional[list[str]] = Field(
        default=None,
        alias="pageUrls",
        description="Facebook Page URLs to scrape ads from",
        examples=[["https://www.facebook.com/Meta"]],
    )
    ad_urls: Optional[list[str]] = Field(
        default=None,
        alias="adUrls",
        description="Direct ad URLs from Facebook Ad Library",
    )
    search_terms: Optional[list[str]] = Field(
        default=None,
        alias="searchTerms",
        description="Keywords to search in Ad Library",
        examples=[["technology", "software"]],
    )
    country: str = Field(
        default="ALL",
        description="Country code for ad targeting (e.g., US, BR, ALL)",
    )
    ad_type: str = Field(
        default="all",
        alias="adType",
        description="Type of ads: all, political_and_issue_ads, housing, employment, credit",
    )
    results_limit: int = Field(
        default=META_ADS_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=META_ADS_MAX_RESULTS,
        description="Maximum number of ads to scrape",
    )
    start_date: Optional[date] = Field(
        default=None,
        alias="startDate",
        description="Filter ads from this date",
    )
    end_date: Optional[date] = Field(
        default=None,
        alias="endDate",
        description="Filter ads until this date",
    )

    class Config:
        populate_by_name = True


class MetaAdsScrapeResponse(BaseModel):
    """Response schema for Meta Ads scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_meta_ads_request(request: MetaAdsScrapeRequest) -> tuple[bool, Optional[str]]:
    """Validate Meta Ads scrape request."""
    if not any([request.page_urls, request.ad_urls, request.search_terms]):
        return False, "At least one of pageUrls, adUrls, or searchTerms must be provided"

    if request.country not in META_ADS_COUNTRIES:
        return False, f"Invalid country. Must be one of: {', '.join(META_ADS_COUNTRIES)}"

    if request.ad_type not in META_ADS_TYPES:
        return False, f"Invalid adType. Must be one of: {', '.join(META_ADS_TYPES)}"

    return True, None


# =============================================================================
# BUILDER FUNCTIONS
# =============================================================================

def build_meta_ads_actor_input(request: MetaAdsScrapeRequest) -> dict:
    """Build the input payload for the Meta Ads Actor."""
    start_urls = []

    if request.page_urls:
        start_urls.extend(request.page_urls)

    if request.ad_urls:
        start_urls.extend(request.ad_urls)

    actor_input = {
        "startUrls": [{"url": url} for url in start_urls] if start_urls else [],
        "maxAds": request.results_limit,
        "country": request.country,
        "adType": request.ad_type,
    }

    if request.search_terms:
        actor_input["searchTerms"] = request.search_terms

    if request.start_date:
        actor_input["startDate"] = request.start_date.isoformat()

    if request.end_date:
        actor_input["endDate"] = request.end_date.isoformat()

    return actor_input


# =============================================================================
# SERVICE CLASS
# =============================================================================

class MetaAdsService:
    """Service for Meta Ads scraping operations."""

    def __init__(self, client: ApifyClient):
        self.client = client

    async def scrape(self, request: MetaAdsScrapeRequest) -> MetaAdsScrapeResponse:
        """Execute Meta Ads scraping based on request parameters."""
        is_valid, error = validate_meta_ads_request(request)
        if not is_valid:
            raise ValueError(error)

        actor_input = build_meta_ads_actor_input(request)
        run = self.client.actor(META_ADS_ACTOR_ID).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return MetaAdsScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    async def scrape_page_ads(self, page_url: str, limit: int = META_ADS_DEFAULT_RESULTS, country: str = "ALL") -> MetaAdsScrapeResponse:
        """Scrape ads from a Facebook Page."""
        request = MetaAdsScrapeRequest(
            page_urls=[page_url],
            results_limit=limit,
            country=country
        )
        return await self.scrape(request)

    async def search_ads(self, query: str, limit: int = META_ADS_DEFAULT_RESULTS, country: str = "ALL") -> MetaAdsScrapeResponse:
        """Search ads in the Ad Library."""
        request = MetaAdsScrapeRequest(
            search_terms=[query],
            results_limit=limit,
            country=country
        )
        return await self.scrape(request)

    async def scrape_political_ads(self, country: str = "US", limit: int = META_ADS_DEFAULT_RESULTS) -> MetaAdsScrapeResponse:
        """Scrape political and issue ads."""
        request = MetaAdsScrapeRequest(
            search_terms=["*"],
            ad_type="political_and_issue_ads",
            country=country,
            results_limit=limit
        )
        return await self.scrape(request)
