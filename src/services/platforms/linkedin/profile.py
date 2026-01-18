"""LinkedIn profile posts scraping service."""

from pydantic import BaseModel, Field
from apify_client import ApifyClient

from .constants import LINKEDIN_ACTOR_ID, LINKEDIN_DEFAULT_RESULTS, LINKEDIN_MAX_RESULTS
from .schemas import LinkedInResponse
from .utils import run_actor


class LinkedInProfileRequest(BaseModel):
    """Request to scrape LinkedIn profile posts."""

    profile_url: str = Field(
        alias="profileUrl",
        description="LinkedIn profile URL",
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


def build_profile_input(request: LinkedInProfileRequest) -> dict:
    """Build the input payload for profile posts scraping."""
    actor_input = {
        "profileUrls": [request.profile_url],
        "maxPosts": request.limit,
    }

    if request.include_comments:
        actor_input["includeComments"] = True

    if request.include_reactions:
        actor_input["includeReactions"] = True

    return actor_input


async def scrape_profile_posts(
    client: ApifyClient,
    profile_url: str,
    limit: int = LINKEDIN_DEFAULT_RESULTS,
    include_comments: bool = False,
    include_reactions: bool = True,
) -> LinkedInResponse:
    """
    Scrape posts from a LinkedIn profile.

    Args:
        client: Apify client instance
        profile_url: LinkedIn profile URL
        limit: Maximum number of posts
        include_comments: Include comments
        include_reactions: Include reactions

    Returns:
        LinkedInResponse with profile posts
    """
    request = LinkedInProfileRequest(
        profile_url=profile_url,
        limit=limit,
        include_comments=include_comments,
        include_reactions=include_reactions,
    )
    actor_input = build_profile_input(request)
    return run_actor(client, LINKEDIN_ACTOR_ID, actor_input)
