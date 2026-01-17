"""
Threads Platform Module
Handles Threads-specific scraping operations via Apify.
"""

from pydantic import BaseModel, Field
from typing import Optional
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

THREADS_ACTOR_ID = "curious_coder/threads-scraper"

THREADS_MAX_RESULTS = 100
THREADS_DEFAULT_RESULTS = 20


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class ThreadsScrapeRequest(BaseModel):
    """Request schema for Threads scraping."""

    usernames: Optional[list[str]] = Field(
        default=None,
        description="List of Threads usernames to scrape (without @)",
        examples=[["zuck", "instagram"]],
    )
    thread_urls: Optional[list[str]] = Field(
        default=None,
        alias="threadUrls",
        description="Direct Threads post URLs to scrape",
        examples=[["https://www.threads.net/@zuck/post/123"]],
    )
    search_queries: Optional[list[str]] = Field(
        default=None,
        alias="searchQueries",
        description="Search terms to find threads/users",
        examples=[["technology", "AI"]],
    )
    hashtags: Optional[list[str]] = Field(
        default=None,
        description="Hashtags to search (without #)",
        examples=[["tech", "news"]],
    )
    results_limit: int = Field(
        default=THREADS_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=THREADS_MAX_RESULTS,
        description="Maximum number of results",
    )
    include_replies: bool = Field(
        default=False,
        alias="includeReplies",
        description="Include replies in results",
    )

    class Config:
        populate_by_name = True


class ThreadsScrapeResponse(BaseModel):
    """Response schema for Threads scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_threads_request(request: ThreadsScrapeRequest) -> tuple[bool, Optional[str]]:
    """Validate Threads scrape request."""
    if not any([request.usernames, request.thread_urls, request.search_queries, request.hashtags]):
        return False, "At least one of usernames, threadUrls, searchQueries, or hashtags must be provided"
    return True, None


# =============================================================================
# BUILDER FUNCTIONS
# =============================================================================

def build_threads_actor_input(request: ThreadsScrapeRequest) -> dict:
    """Build the input payload for the Threads Actor."""
    actor_input = {
        "maxItems": request.results_limit,
    }

    if request.usernames:
        actor_input["usernames"] = request.usernames

    if request.thread_urls:
        actor_input["threadUrls"] = request.thread_urls

    if request.search_queries:
        actor_input["searchQueries"] = request.search_queries

    if request.hashtags:
        # Convert hashtags to search queries with # prefix
        hashtag_queries = [f"#{tag}" for tag in request.hashtags]
        if "searchQueries" in actor_input:
            actor_input["searchQueries"].extend(hashtag_queries)
        else:
            actor_input["searchQueries"] = hashtag_queries

    if request.include_replies:
        actor_input["includeReplies"] = True

    return actor_input


# =============================================================================
# SERVICE CLASS
# =============================================================================

class ThreadsService:
    """Service for Threads scraping operations."""

    def __init__(self, client: ApifyClient):
        self.client = client

    async def scrape(self, request: ThreadsScrapeRequest) -> ThreadsScrapeResponse:
        """Execute Threads scraping based on request parameters."""
        is_valid, error = validate_threads_request(request)
        if not is_valid:
            raise ValueError(error)

        actor_input = build_threads_actor_input(request)
        run = self.client.actor(THREADS_ACTOR_ID).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return ThreadsScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    async def scrape_profile(self, username: str, limit: int = THREADS_DEFAULT_RESULTS) -> ThreadsScrapeResponse:
        """Scrape threads from a user profile."""
        request = ThreadsScrapeRequest(usernames=[username], results_limit=limit)
        return await self.scrape(request)

    async def scrape_hashtag(self, hashtag: str, limit: int = THREADS_DEFAULT_RESULTS) -> ThreadsScrapeResponse:
        """Scrape threads by hashtag."""
        request = ThreadsScrapeRequest(hashtags=[hashtag], results_limit=limit)
        return await self.scrape(request)

    async def search(self, query: str, limit: int = THREADS_DEFAULT_RESULTS) -> ThreadsScrapeResponse:
        """Search Threads."""
        request = ThreadsScrapeRequest(search_queries=[query], results_limit=limit)
        return await self.scrape(request)

    async def scrape_thread(self, thread_url: str, include_replies: bool = False) -> ThreadsScrapeResponse:
        """Scrape a specific thread."""
        request = ThreadsScrapeRequest(
            thread_urls=[thread_url],
            include_replies=include_replies
        )
        return await self.scrape(request)
