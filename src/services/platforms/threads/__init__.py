"""Threads platform module."""

from .constants import (
    THREADS_ACTOR_ID,
    THREADS_DEFAULT_RESULTS,
    THREADS_MAX_RESULTS,
)
from .schemas import ThreadsResponse

# Profile
from .profile import (
    ThreadsProfileRequest,
    scrape_profile,
)

# Hashtag
from .hashtag import (
    ThreadsHashtagRequest,
    scrape_hashtag,
)

# Search
from .search import (
    ThreadsSearchRequest,
    search,
)

# Thread
from .thread import (
    ThreadsThreadRequest,
    get_thread,
)

__all__ = [
    # Constants
    "THREADS_ACTOR_ID",
    "THREADS_DEFAULT_RESULTS",
    "THREADS_MAX_RESULTS",
    # Schemas
    "ThreadsResponse",
    "ThreadsProfileRequest",
    "ThreadsHashtagRequest",
    "ThreadsSearchRequest",
    "ThreadsThreadRequest",
    # Functions
    "scrape_profile",
    "scrape_hashtag",
    "search",
    "get_thread",
]
