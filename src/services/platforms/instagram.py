"""
Instagram Platform Module
Handles Instagram-specific scraping operations via Apify.

Each function has a single responsibility:
- Profile scraping
- Posts scraping
- Comments scraping
- Hashtag scraping
- Reels scraping
- Stories scraping
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from apify_client import ApifyClient

# =============================================================================
# CONSTANTS
# =============================================================================

INSTAGRAM_ACTOR_ID = "apify/instagram-scraper"
INSTAGRAM_PROFILE_ACTOR_ID = "apify/instagram-profile-scraper"
INSTAGRAM_POST_ACTOR_ID = "apify/instagram-post-scraper"
INSTAGRAM_COMMENT_ACTOR_ID = "apify/instagram-comment-scraper"
INSTAGRAM_HASHTAG_ACTOR_ID = "apify/instagram-hashtag-scraper"

INSTAGRAM_MAX_RESULTS = 200
INSTAGRAM_DEFAULT_RESULTS = 20


# =============================================================================
# TYPES / ENUMS
# =============================================================================

class InstagramSearchType(str, Enum):
    USER = "user"
    HASHTAG = "hashtag"
    PLACE = "place"


class InstagramResultsType(str, Enum):
    POSTS = "posts"
    DETAILS = "details"
    COMMENTS = "comments"


# =============================================================================
# REQUEST SCHEMAS - Separados por funcionalidade
# =============================================================================

class InstagramProfileRequest(BaseModel):
    """Request to scrape Instagram profile data."""
    usernames: list[str] = Field(
        ...,
        description="List of Instagram usernames to scrape",
        examples=[["natgeo", "instagram"]],
    )

    class Config:
        populate_by_name = True


class InstagramPostsRequest(BaseModel):
    """Request to scrape posts from profiles."""
    usernames: Optional[list[str]] = Field(
        default=None,
        description="List of Instagram usernames",
        examples=[["natgeo"]],
    )
    profile_urls: Optional[list[str]] = Field(
        default=None,
        alias="profileUrls",
        description="Direct profile URLs",
    )
    results_limit: int = Field(
        default=INSTAGRAM_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=INSTAGRAM_MAX_RESULTS,
        description="Maximum posts per profile",
    )

    class Config:
        populate_by_name = True


class InstagramCommentsRequest(BaseModel):
    """Request to scrape comments from posts."""
    post_urls: list[str] = Field(
        ...,
        alias="postUrls",
        description="List of Instagram post URLs to get comments from",
        examples=[["https://www.instagram.com/p/ABC123/"]],
    )
    results_limit: int = Field(
        default=100,
        alias="resultsLimit",
        ge=1,
        le=1000,
        description="Maximum comments per post",
    )

    class Config:
        populate_by_name = True


class InstagramHashtagRequest(BaseModel):
    """Request to scrape posts from hashtags."""
    hashtags: list[str] = Field(
        ...,
        description="List of hashtags (without #)",
        examples=[["travel", "photography"]],
    )
    results_limit: int = Field(
        default=INSTAGRAM_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=INSTAGRAM_MAX_RESULTS,
        description="Maximum posts per hashtag",
    )

    class Config:
        populate_by_name = True


class InstagramReelsRequest(BaseModel):
    """Request to scrape reels from profiles."""
    usernames: Optional[list[str]] = Field(
        default=None,
        description="List of Instagram usernames",
    )
    profile_urls: Optional[list[str]] = Field(
        default=None,
        alias="profileUrls",
        description="Direct profile URLs",
    )
    results_limit: int = Field(
        default=INSTAGRAM_DEFAULT_RESULTS,
        alias="resultsLimit",
        ge=1,
        le=INSTAGRAM_MAX_RESULTS,
        description="Maximum reels per profile",
    )

    class Config:
        populate_by_name = True


class InstagramSearchRequest(BaseModel):
    """Request to search Instagram."""
    query: str = Field(
        ...,
        description="Search query",
    )
    search_type: InstagramSearchType = Field(
        default=InstagramSearchType.USER,
        alias="searchType",
        description="Type of search: user, hashtag, or place",
    )
    results_limit: int = Field(
        default=10,
        alias="resultsLimit",
        ge=1,
        le=100,
        description="Maximum search results",
    )

    class Config:
        populate_by_name = True


class InstagramPostDetailRequest(BaseModel):
    """Request to get details of specific posts."""
    post_urls: list[str] = Field(
        ...,
        alias="postUrls",
        description="List of Instagram post URLs",
        examples=[["https://www.instagram.com/p/ABC123/"]],
    )

    class Config:
        populate_by_name = True


# =============================================================================
# RESPONSE SCHEMA
# =============================================================================

class InstagramScrapeResponse(BaseModel):
    """Generic response schema for Instagram scraping results."""
    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True


# =============================================================================
# SERVICE CLASS - Métodos separados por responsabilidade
# =============================================================================

class InstagramService:
    """
    Service for Instagram scraping operations.

    Each method has a single responsibility:
    - scrape_profiles: Get profile metadata
    - scrape_posts: Get posts from profiles
    - scrape_comments: Get comments from posts
    - scrape_hashtag: Get posts from hashtags
    - scrape_reels: Get reels from profiles
    - scrape_post_details: Get details of specific posts
    - search: Search users/hashtags/places
    """

    def __init__(self, client: ApifyClient):
        self.client = client

    def _run_actor(self, actor_id: str, actor_input: dict) -> InstagramScrapeResponse:
        """Execute an Apify actor and return results."""
        run = self.client.actor(actor_id).call(run_input=actor_input)

        dataset_id = run.get("defaultDatasetId")
        items = []

        if dataset_id:
            dataset_items = self.client.dataset(dataset_id).list_items()
            items = dataset_items.items

        return InstagramScrapeResponse(
            success=True,
            data=items,
            total_results=len(items),
            run_id=run.get("id"),
        )

    # =========================================================================
    # PROFILE SCRAPING
    # =========================================================================

    async def scrape_profiles(self, request: InstagramProfileRequest) -> InstagramScrapeResponse:
        """
        Scrape Instagram profile metadata.

        Returns: bio, followers, following, posts count, etc.
        """
        actor_input = {
            "usernames": request.usernames,
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_PROFILE_ACTOR_ID, actor_input)

    async def get_profile(self, username: str) -> InstagramScrapeResponse:
        """Get a single profile's metadata."""
        request = InstagramProfileRequest(usernames=[username])
        return await self.scrape_profiles(request)

    # =========================================================================
    # POSTS SCRAPING
    # =========================================================================

    async def scrape_posts(self, request: InstagramPostsRequest) -> InstagramScrapeResponse:
        """
        Scrape posts from Instagram profiles.

        Returns: post images, captions, likes, comments count, etc.
        """
        direct_urls = []

        if request.usernames:
            direct_urls.extend([f"https://www.instagram.com/{u}/" for u in request.usernames])

        if request.profile_urls:
            direct_urls.extend(request.profile_urls)

        if not direct_urls:
            raise ValueError("Either usernames or profileUrls must be provided")

        actor_input = {
            "directUrls": direct_urls,
            "resultsType": "posts",
            "resultsLimit": request.results_limit,
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_ACTOR_ID, actor_input)

    async def get_user_posts(self, username: str, limit: int = INSTAGRAM_DEFAULT_RESULTS) -> InstagramScrapeResponse:
        """Get posts from a single user."""
        request = InstagramPostsRequest(usernames=[username], results_limit=limit)
        return await self.scrape_posts(request)

    # =========================================================================
    # COMMENTS SCRAPING
    # =========================================================================

    async def scrape_comments(self, request: InstagramCommentsRequest) -> InstagramScrapeResponse:
        """
        Scrape comments from Instagram posts.

        Returns: comment text, author, likes, timestamp, etc.
        """
        actor_input = {
            "directUrls": request.post_urls,
            "resultsType": "comments",
            "resultsLimit": request.results_limit,
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_ACTOR_ID, actor_input)

    async def get_post_comments(self, post_url: str, limit: int = 100) -> InstagramScrapeResponse:
        """Get comments from a single post."""
        request = InstagramCommentsRequest(post_urls=[post_url], results_limit=limit)
        return await self.scrape_comments(request)

    # =========================================================================
    # HASHTAG SCRAPING
    # =========================================================================

    async def scrape_hashtag(self, request: InstagramHashtagRequest) -> InstagramScrapeResponse:
        """
        Scrape posts from hashtags.

        Returns: posts containing the specified hashtags.
        """
        actor_input = {
            "hashtags": request.hashtags,
            "resultsLimit": request.results_limit,
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_HASHTAG_ACTOR_ID, actor_input)

    async def get_hashtag_posts(self, hashtag: str, limit: int = INSTAGRAM_DEFAULT_RESULTS) -> InstagramScrapeResponse:
        """Get posts from a single hashtag."""
        request = InstagramHashtagRequest(hashtags=[hashtag], results_limit=limit)
        return await self.scrape_hashtag(request)

    # =========================================================================
    # REELS SCRAPING
    # =========================================================================

    async def scrape_reels(self, request: InstagramReelsRequest) -> InstagramScrapeResponse:
        """
        Scrape reels from Instagram profiles.

        Returns: reel videos, views, likes, etc.
        """
        direct_urls = []

        if request.usernames:
            direct_urls.extend([f"https://www.instagram.com/{u}/reels/" for u in request.usernames])

        if request.profile_urls:
            for url in request.profile_urls:
                if "/reels" not in url:
                    url = url.rstrip("/") + "/reels/"
                direct_urls.append(url)

        if not direct_urls:
            raise ValueError("Either usernames or profileUrls must be provided")

        actor_input = {
            "directUrls": direct_urls,
            "resultsType": "posts",
            "resultsLimit": request.results_limit,
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_ACTOR_ID, actor_input)

    async def get_user_reels(self, username: str, limit: int = INSTAGRAM_DEFAULT_RESULTS) -> InstagramScrapeResponse:
        """Get reels from a single user."""
        request = InstagramReelsRequest(usernames=[username], results_limit=limit)
        return await self.scrape_reels(request)

    # =========================================================================
    # POST DETAILS SCRAPING
    # =========================================================================

    async def scrape_post_details(self, request: InstagramPostDetailRequest) -> InstagramScrapeResponse:
        """
        Get detailed information about specific posts.

        Returns: full post metadata without comments.
        """
        actor_input = {
            "directUrls": request.post_urls,
            "resultsType": "details",
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_POST_ACTOR_ID, actor_input)

    async def get_post_details(self, post_url: str) -> InstagramScrapeResponse:
        """Get details of a single post."""
        request = InstagramPostDetailRequest(post_urls=[post_url])
        return await self.scrape_post_details(request)

    # =========================================================================
    # SEARCH
    # =========================================================================

    async def search(self, request: InstagramSearchRequest) -> InstagramScrapeResponse:
        """
        Search Instagram for users, hashtags, or places.

        Returns: search results based on type.
        """
        actor_input = {
            "search": request.query,
            "searchType": request.search_type.value,
            "searchLimit": request.results_limit,
            "resultsType": "details",
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
        }
        return self._run_actor(INSTAGRAM_ACTOR_ID, actor_input)

    async def search_users(self, query: str, limit: int = 10) -> InstagramScrapeResponse:
        """Search for Instagram users."""
        request = InstagramSearchRequest(
            query=query,
            search_type=InstagramSearchType.USER,
            results_limit=limit
        )
        return await self.search(request)

    async def search_hashtags(self, query: str, limit: int = 10) -> InstagramScrapeResponse:
        """Search for Instagram hashtags."""
        request = InstagramSearchRequest(
            query=query,
            search_type=InstagramSearchType.HASHTAG,
            results_limit=limit
        )
        return await self.search(request)

    async def search_places(self, query: str, limit: int = 10) -> InstagramScrapeResponse:
        """Search for Instagram places/locations."""
        request = InstagramSearchRequest(
            query=query,
            search_type=InstagramSearchType.PLACE,
            results_limit=limit
        )
        return await self.search(request)
