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
    InstagramResponse,
    # Profile
    InstagramProfileRequest,
    scrape_profiles,
    get_profile,
    # Posts
    InstagramPostsRequest,
    scrape_posts,
    get_user_posts,
    # Comments
    InstagramCommentsRequest,
    scrape_comments,
    get_post_comments,
    # Hashtag
    InstagramHashtagRequest,
    scrape_hashtag,
    get_hashtag_posts,
    # Reels
    InstagramReelsRequest,
    scrape_reels,
    get_user_reels,
    # Post Details
    InstagramPostDetailRequest,
    scrape_post_details,
    get_post_details,
    # Search
    InstagramSearchRequest,
    search,
    search_users,
    search_hashtags,
    search_places,
)

router = APIRouter(prefix="/instagram", tags=["Instagram"])


# =============================================================================
# PROFILE ROUTES
# =============================================================================

@router.get(
    "/profile/{username}",
    response_model=InstagramResponse,
    summary="Get profile metadata",
    description="Get Instagram profile metadata: bio, followers, following, posts count, etc.",
)
def get_profile_route(
    username: str,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return get_profile(client, username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/profiles",
    response_model=InstagramResponse,
    summary="Get multiple profiles metadata",
    description="Get metadata for multiple Instagram profiles at once.",
)
def scrape_profiles_route(
    request: InstagramProfileRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return scrape_profiles(client, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# POSTS ROUTES
# =============================================================================

@router.get(
    "/posts/{username}",
    response_model=InstagramResponse,
    summary="Get user posts",
    description="Get posts from a specific Instagram user.",
)
def get_user_posts_route(
    username: str,
    limit: int = Query(default=20, ge=1, le=200),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return get_user_posts(client, username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/posts",
    response_model=InstagramResponse,
    summary="Get posts from multiple profiles",
    description="Get posts from multiple Instagram profiles at once.",
)
def scrape_posts_route(
    request: InstagramPostsRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return scrape_posts(client, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# COMMENTS ROUTES
# =============================================================================

@router.get(
    "/comments",
    response_model=InstagramResponse,
    summary="Get post comments",
    description="Get comments from a specific Instagram post.",
)
def get_post_comments_route(
    url: str = Query(..., description="Instagram post URL"),
    limit: int = Query(default=100, ge=1, le=1000),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return get_post_comments(client, url, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/comments",
    response_model=InstagramResponse,
    summary="Get comments from multiple posts",
    description="Get comments from multiple Instagram posts at once.",
)
def scrape_comments_route(
    request: InstagramCommentsRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return scrape_comments(client, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# HASHTAG ROUTES
# =============================================================================

@router.get(
    "/hashtag/{hashtag}",
    response_model=InstagramResponse,
    summary="Get hashtag posts",
    description="Get posts from a specific hashtag.",
)
def get_hashtag_posts_route(
    hashtag: str,
    limit: int = Query(default=20, ge=1, le=200),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return get_hashtag_posts(client, hashtag, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/hashtags",
    response_model=InstagramResponse,
    summary="Get posts from multiple hashtags",
    description="Get posts from multiple hashtags at once.",
)
def scrape_hashtags_route(
    request: InstagramHashtagRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return scrape_hashtag(client, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# REELS ROUTES
# =============================================================================

@router.get(
    "/reels/{username}",
    response_model=InstagramResponse,
    summary="Get user reels",
    description="Get reels from a specific Instagram user.",
)
def get_user_reels_route(
    username: str,
    limit: int = Query(default=20, ge=1, le=200),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return get_user_reels(client, username, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/reels",
    response_model=InstagramResponse,
    summary="Get reels from multiple profiles",
    description="Get reels from multiple Instagram profiles at once.",
)
def scrape_reels_route(
    request: InstagramReelsRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return scrape_reels(client, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# POST DETAILS ROUTES
# =============================================================================

@router.get(
    "/post-details",
    response_model=InstagramResponse,
    summary="Get post details",
    description="Get detailed information about a specific Instagram post.",
)
def get_post_details_route(
    url: str = Query(..., description="Instagram post URL"),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return get_post_details(client, url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/post-details",
    response_model=InstagramResponse,
    summary="Get details from multiple posts",
    description="Get detailed information about multiple Instagram posts at once.",
)
def scrape_post_details_route(
    request: InstagramPostDetailRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return scrape_post_details(client, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# SEARCH ROUTES
# =============================================================================

@router.get(
    "/search/users",
    response_model=InstagramResponse,
    summary="Search users",
    description="Search for Instagram users by name/username.",
)
def search_users_route(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return search_users(client, q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search/hashtags",
    response_model=InstagramResponse,
    summary="Search hashtags",
    description="Search for Instagram hashtags.",
)
def search_hashtags_route(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return search_hashtags(client, q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/search/places",
    response_model=InstagramResponse,
    summary="Search places",
    description="Search for Instagram places/locations.",
)
def search_places_route(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=100),
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return search_places(client, q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/search",
    response_model=InstagramResponse,
    summary="Search Instagram",
    description="Search Instagram for users, hashtags, or places.",
)
def search_route(
    request: InstagramSearchRequest,
    client: ApifyClient = Depends(get_apify_client),
) -> InstagramResponse:
    try:
        return search(client, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
