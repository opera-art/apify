"""LinkedIn API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.linkedin import (
    LinkedInResponse,
    scrape_profile_posts,
    scrape_company_posts,
    search_posts,
)

router = APIRouter(prefix="/linkedin", tags=["LinkedIn"])


@router.get(
    "/profile",
    response_model=LinkedInResponse,
    summary="Scrape profile posts",
)
async def get_profile_posts(
    url: str = Query(..., description="LinkedIn profile URL"),
    limit: int = Query(default=20, ge=1, le=100),
    include_comments: bool = Query(default=False, alias="includeComments"),
    include_reactions: bool = Query(default=True, alias="includeReactions"),
    client: ApifyClient = Depends(get_apify_client),
) -> LinkedInResponse:
    """Get posts from a LinkedIn profile."""
    try:
        return await scrape_profile_posts(client, url, limit, include_comments, include_reactions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/company",
    response_model=LinkedInResponse,
    summary="Scrape company posts",
)
async def get_company_posts(
    url: str = Query(..., description="LinkedIn company URL"),
    limit: int = Query(default=20, ge=1, le=100),
    include_comments: bool = Query(default=False, alias="includeComments"),
    include_reactions: bool = Query(default=True, alias="includeReactions"),
    client: ApifyClient = Depends(get_apify_client),
) -> LinkedInResponse:
    """Get posts from a LinkedIn company page."""
    try:
        return await scrape_company_posts(client, url, limit, include_comments, include_reactions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search",
    response_model=LinkedInResponse,
    summary="Search LinkedIn posts",
)
async def search_linkedin_posts(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> LinkedInResponse:
    """Search LinkedIn posts."""
    try:
        return await search_posts(client, q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
