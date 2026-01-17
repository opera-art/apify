"""
LinkedIn Platform Module
Handles LinkedIn-specific scraping operations via Apify.
"""

from pydantic import BaseModel, Field
from typing import Optional
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

LINKEDIN_ACTOR_ID = "apimaestro/linkedin-profile-posts"

LINKEDIN_MAX_RESULTS = 100
LINKEDIN_DEFAULT_RESULTS = 20


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class LinkedInScrapeRequest(BaseModel):
    """Request schema for LinkedIn scraping."""

    profile_urls: Optional[list[str]] = Field(
        default=None,
        alias="profileUrls",
        description="LinkedIn profile URLs to scrape posts from",
        examples=[["https://www.linkedin.com/in/satyanadella/"]],
    )
    company_urls: Optional[list[str]] = Field(
        default=None,
        alias="companyUrls",
        description="LinkedIn company page URLs to scrape",
        examples=[["https://www.linkedin.com/company/microsoft/"]],
    )
    search_queries: Optional[list[str]] = Field(
        default=None,
        alias="searchQueries",
        description="Search terms to find posts",
        examples=[["artificial intelligence", "machine learning"]],
    )
    results_limit: int = Field(
        default=LINKEDIN_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=LINKEDIN_MAX_RESULTS,
        description="Maximum number of posts to scrape",
    )
    include_comments: bool = Field(
        default=False,
        alias="includeComments",
        description="Include comments on posts",
    )
    include_reactions: bool = Field(
        default=True,
        alias="includeReactions",
        description="Include reaction counts",
    )

    class Config:
        populate_by_name = True


class LinkedInScrapeResponse(BaseModel):
    """Response schema for LinkedIn scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_linkedin_request(request: LinkedInScrapeRequest) -> tuple[bool, Optional[str]]:
    """Validate LinkedIn scrape request."""
    if not any([request.profile_urls, request.company_urls, request.search_queries]):
        return False, "At least one of profileUrls, companyUrls, or searchQueries must be provided"
    return True, None


def is_valid_linkedin_url(url: str) -> bool:
    """Check if URL is a valid LinkedIn URL."""
    return "linkedin.com" in url.lower()


# =============================================================================
# BUILDER FUNCTIONS
# =============================================================================

def build_linkedin_actor_input(request: LinkedInScrapeRequest) -> dict:
    """Build the input payload for the LinkedIn Actor."""
    actor_input = {
        "maxPosts": request.results_limit,
    }

    urls = []

    if request.profile_urls:
        urls.extend(request.profile_urls)

    if request.company_urls:
        urls.extend(request.company_urls)

    if urls:
        actor_input["profileUrls"] = urls

    if request.search_queries:
        actor_input["searchQueries"] = request.search_queries

    if request.include_comments:
        actor_input["includeComments"] = True

    if request.include_reactions:
        actor_input["includeReactions"] = True

    return actor_input


# =============================================================================
# SERVICE CLASS
# =============================================================================

class LinkedInService:
    """Service for LinkedIn scraping operations."""

    def __init__(self, client: ApifyClient):
        self.client = client

    async def scrape(self, request: LinkedInScrapeRequest) -> LinkedInScrapeResponse:
        """Execute LinkedIn scraping based on request parameters."""
        is_valid, error = validate_linkedin_request(request)
        if not is_valid:
            raise ValueError(error)

        actor_input = build_linkedin_actor_input(request)
        run = self.client.actor(LINKEDIN_ACTOR_ID).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return LinkedInScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    async def scrape_profile_posts(self, profile_url: str, limit: int = LINKEDIN_DEFAULT_RESULTS) -> LinkedInScrapeResponse:
        """Scrape posts from a LinkedIn profile."""
        request = LinkedInScrapeRequest(profile_urls=[profile_url], results_limit=limit)
        return await self.scrape(request)

    async def scrape_company_posts(self, company_url: str, limit: int = LINKEDIN_DEFAULT_RESULTS) -> LinkedInScrapeResponse:
        """Scrape posts from a LinkedIn company page."""
        request = LinkedInScrapeRequest(company_urls=[company_url], results_limit=limit)
        return await self.scrape(request)

    async def search_posts(self, query: str, limit: int = LINKEDIN_DEFAULT_RESULTS) -> LinkedInScrapeResponse:
        """Search LinkedIn posts."""
        request = LinkedInScrapeRequest(search_queries=[query], results_limit=limit)
        return await self.scrape(request)
