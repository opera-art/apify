"""LinkedIn company posts scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import LINKEDIN_ACTOR_ID, LINKEDIN_DEFAULT_RESULTS, LINKEDIN_MAX_RESULTS
from .schemas import LinkedInResponse
from .utils import run_actor


class LinkedInCompanyRequest(BaseModel):
    """Request to scrape LinkedIn company posts."""

    company_url: str = Field(
        alias="companyUrl",
        description="LinkedIn company page URL",
    )
    limit: int = Field(
        default=LINKEDIN_DEFAULT_RESULTS,
        ge=1,
        le=LINKEDIN_MAX_RESULTS,
    )
    include_comments: bool = Field(
        default=False,
        alias="includeComments",
    )
    include_reactions: bool = Field(
        default=True,
        alias="includeReactions",
    )

    class Config:
        populate_by_name = True


def build_company_input(request: LinkedInCompanyRequest) -> dict:
    """Build the input payload for company posts scraping."""
    actor_input = {
        "profileUrls": [request.company_url],
        "maxPosts": request.limit,
    }

    if request.include_comments:
        actor_input["includeComments"] = True

    if request.include_reactions:
        actor_input["includeReactions"] = True

    return actor_input


async def scrape_company_posts(
    client: ApifyClient,
    company_url: str,
    limit: int = LINKEDIN_DEFAULT_RESULTS,
    include_comments: bool = False,
    include_reactions: bool = True,
) -> LinkedInResponse:
    """
    Scrape posts from a LinkedIn company page.

    Args:
        client: Apify client instance
        company_url: LinkedIn company page URL
        limit: Maximum number of posts
        include_comments: Include comments
        include_reactions: Include reactions

    Returns:
        LinkedInResponse with company posts
    """
    request = LinkedInCompanyRequest(
        company_url=company_url,
        limit=limit,
        include_comments=include_comments,
        include_reactions=include_reactions,
    )
    actor_input = build_company_input(request)
    return run_actor(client, LINKEDIN_ACTOR_ID, actor_input)
