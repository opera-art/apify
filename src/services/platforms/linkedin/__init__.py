"""LinkedIn platform module."""

from .constants import (
    LINKEDIN_ACTOR_ID,
    LINKEDIN_DEFAULT_RESULTS,
    LINKEDIN_MAX_RESULTS,
)
from .schemas import LinkedInResponse

# Profile
from .profile import (
    LinkedInProfileRequest,
    scrape_profile_posts,
)

# Company
from .company import (
    LinkedInCompanyRequest,
    scrape_company_posts,
)

# Search
from .search import (
    LinkedInSearchRequest,
    search_posts,
)

__all__ = [
    # Constants
    "LINKEDIN_ACTOR_ID",
    "LINKEDIN_DEFAULT_RESULTS",
    "LINKEDIN_MAX_RESULTS",
    # Schemas
    "LinkedInResponse",
    "LinkedInProfileRequest",
    "LinkedInCompanyRequest",
    "LinkedInSearchRequest",
    # Functions
    "scrape_profile_posts",
    "scrape_company_posts",
    "search_posts",
]
