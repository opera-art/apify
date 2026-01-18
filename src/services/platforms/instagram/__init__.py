"""Instagram platform module."""

from .constants import (
    INSTAGRAM_ACTOR_ID,
    INSTAGRAM_PROFILE_ACTOR_ID,
    INSTAGRAM_POST_ACTOR_ID,
    INSTAGRAM_COMMENT_ACTOR_ID,
    INSTAGRAM_HASHTAG_ACTOR_ID,
    INSTAGRAM_DEFAULT_RESULTS,
    INSTAGRAM_MAX_RESULTS,
)
from .types import InstagramSearchType, InstagramResultsType
from .schemas import InstagramResponse

# Profile
from .profile import (
    InstagramProfileRequest,
    scrape_profiles,
    get_profile,
)

# Posts
from .posts import (
    InstagramPostsRequest,
    scrape_posts,
    get_user_posts,
)

# Comments
from .comments import (
    InstagramCommentsRequest,
    scrape_comments,
    get_post_comments,
)

# Hashtag
from .hashtag import (
    InstagramHashtagRequest,
    scrape_hashtag,
    get_hashtag_posts,
)

# Reels
from .reels import (
    InstagramReelsRequest,
    scrape_reels,
    get_user_reels,
)

# Post Details
from .post_details import (
    InstagramPostDetailRequest,
    scrape_post_details,
    get_post_details,
)

# Search
from .search import (
    InstagramSearchRequest,
    search,
    search_users,
    search_hashtags,
    search_places,
)

__all__ = [
    # Constants
    "INSTAGRAM_ACTOR_ID",
    "INSTAGRAM_PROFILE_ACTOR_ID",
    "INSTAGRAM_POST_ACTOR_ID",
    "INSTAGRAM_COMMENT_ACTOR_ID",
    "INSTAGRAM_HASHTAG_ACTOR_ID",
    "INSTAGRAM_DEFAULT_RESULTS",
    "INSTAGRAM_MAX_RESULTS",
    # Types
    "InstagramSearchType",
    "InstagramResultsType",
    # Schemas
    "InstagramResponse",
    "InstagramProfileRequest",
    "InstagramPostsRequest",
    "InstagramCommentsRequest",
    "InstagramHashtagRequest",
    "InstagramReelsRequest",
    "InstagramPostDetailRequest",
    "InstagramSearchRequest",
    # Profile functions
    "scrape_profiles",
    "get_profile",
    # Posts functions
    "scrape_posts",
    "get_user_posts",
    # Comments functions
    "scrape_comments",
    "get_post_comments",
    # Hashtag functions
    "scrape_hashtag",
    "get_hashtag_posts",
    # Reels functions
    "scrape_reels",
    "get_user_reels",
    # Post Details functions
    "scrape_post_details",
    "get_post_details",
    # Search functions
    "search",
    "search_users",
    "search_hashtags",
    "search_places",
]
