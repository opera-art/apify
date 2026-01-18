"""Pinterest platform module."""

from .constants import (
    PINTEREST_ACTOR_ID,
    PINTEREST_DEFAULT_RESULTS,
    PINTEREST_MAX_RESULTS,
)
from .schemas import PinterestResponse

# Board
from .board import (
    PinterestBoardRequest,
    scrape_board,
)

# Profile
from .profile import (
    PinterestProfileRequest,
    scrape_profile,
)

# Search
from .search import (
    PinterestSearchRequest,
    search,
)

# Pin
from .pin import (
    PinterestPinRequest,
    get_pin,
)

__all__ = [
    # Constants
    "PINTEREST_ACTOR_ID",
    "PINTEREST_DEFAULT_RESULTS",
    "PINTEREST_MAX_RESULTS",
    # Schemas
    "PinterestResponse",
    "PinterestBoardRequest",
    "PinterestProfileRequest",
    "PinterestSearchRequest",
    "PinterestPinRequest",
    # Functions
    "scrape_board",
    "scrape_profile",
    "search",
    "get_pin",
]
