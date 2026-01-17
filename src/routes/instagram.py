"""
Instagram API Routes

Each route has a single responsibility:
- /profile - Get profile metadata
- /posts - Get posts from profiles
- /comments - Get comments from posts
- /hashtag - Get posts from hashtags
- /reels - Get reels from profiles
- /post-details - Get details of specific posts
- /search - Search users/hashtags/places
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from apify_client import ApifyClient

from src.services.apify_client import get_apify_client
from src.services.platforms.instagram import (
    InstagramService,
    InstagramScrapeResponse,
    InstagramSearchType,
    InstagramProfileRequest,
    InstagramPostsRequest,
    InstagramCommentsRequest,
    InstagramHashtagRequest,
    InstagramReelsRequest,
    InstagramSearchRequest,
    InstagramPostDetailRequest,
)

router = APIRouter(prefix="/instagram", tags=["Instagram"])


def get_service(client: ApifyClient = Depends(get_apify_client)) -> InstagramService:
    return InstagramService(client)


# =============================================================================
# PROFILE ROUTES
# =============================================================================

@router.get(
    "/profile/{username}",
    response_model=InstagramScrapeResponse,
    summary="Get profile metadata",
    description="Get Instagram profile metadata: bio, followers, following, posts count, etc.",
)
async def get_profile(
    username: str,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.get_profile(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/profiles",
    response_model=InstagramScrapeResponse,
    summary="Get multiple profiles metadata",
    description="Get metadata for multiple Instagram profiles at once.",
)
async def scrape_profiles(
    request: InstagramProfileRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.scrape_profiles(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# POSTS ROUTES
# =============================================================================

@router.get(
    "/posts/{username}",
    response_model=InstagramScrapeResponse,
    summary="Get user posts",
    description="Get posts from a specific Instagram user.",
)
async def get_user_posts(
    username: str,
    limit: int = Query(default=20, ge=1, le=200),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.get_user_posts(username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/posts",
    response_model=InstagramScrapeResponse,
    summary="Get posts from multiple profiles",
    description="Get posts from multiple Instagram profiles at once.",
)
async def scrape_posts(
    request: InstagramPostsRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.scrape_posts(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# COMMENTS ROUTES
# =============================================================================

@router.get(
    "/comments",
    response_model=InstagramScrapeResponse,
    summary="Get post comments",
    description="Get comments from a specific Instagram post.",
)
async def get_post_comments(
    url: str = Query(..., description="Instagram post URL"),
    limit: int = Query(default=100, ge=1, le=1000),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.get_post_comments(url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/comments",
    response_model=InstagramScrapeResponse,
    summary="Get comments from multiple posts",
    description="Get comments from multiple Instagram posts at once.",
)
async def scrape_comments(
    request: InstagramCommentsRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.scrape_comments(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# HASHTAG ROUTES
# =============================================================================

@router.get(
    "/hashtag/{hashtag}",
    response_model=InstagramScrapeResponse,
    summary="Get hashtag posts",
    description="Get posts from a specific hashtag.",
)
async def get_hashtag_posts(
    hashtag: str,
    limit: int = Query(default=20, ge=1, le=200),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.get_hashtag_posts(hashtag, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/hashtags",
    response_model=InstagramScrapeResponse,
    summary="Get posts from multiple hashtags",
    description="Get posts from multiple hashtags at once.",
)
async def scrape_hashtags(
    request: InstagramHashtagRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.scrape_hashtag(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# REELS ROUTES
# =============================================================================

@router.get(
    "/reels/{username}",
    response_model=InstagramScrapeResponse,
    summary="Get user reels",
    description="Get reels from a specific Instagram user.",
)
async def get_user_reels(
    username: str,
    limit: int = Query(default=20, ge=1, le=200),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.get_user_reels(username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/reels",
    response_model=InstagramScrapeResponse,
    summary="Get reels from multiple profiles",
    description="Get reels from multiple Instagram profiles at once.",
)
async def scrape_reels(
    request: InstagramReelsRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.scrape_reels(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# POST DETAILS ROUTES
# =============================================================================

@router.get(
    "/post-details",
    response_model=InstagramScrapeResponse,
    summary="Get post details",
    description="Get detailed information about a specific Instagram post.",
)
async def get_post_details(
    url: str = Query(..., description="Instagram post URL"),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.get_post_details(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/post-details",
    response_model=InstagramScrapeResponse,
    summary="Get details from multiple posts",
    description="Get detailed information about multiple Instagram posts at once.",
)
async def scrape_post_details(
    request: InstagramPostDetailRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.scrape_post_details(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# SEARCH ROUTES
# =============================================================================

@router.get(
    "/search/users",
    response_model=InstagramScrapeResponse,
    summary="Search users",
    description="Search for Instagram users by name/username.",
)
async def search_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.search_users(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search/hashtags",
    response_model=InstagramScrapeResponse,
    summary="Search hashtags",
    description="Search for Instagram hashtags.",
)
async def search_hashtags(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.search_hashtags(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search/places",
    response_model=InstagramScrapeResponse,
    summary="Search places",
    description="Search for Instagram places/locations.",
)
async def search_places(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.search_places(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/search",
    response_model=InstagramScrapeResponse,
    summary="Search Instagram",
    description="Search Instagram for users, hashtags, or places.",
)
async def search(
    request: InstagramSearchRequest,
    service: InstagramService = Depends(get_service),
) -> InstagramScrapeResponse:
    try:
        return await service.search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
