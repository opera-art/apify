"""Instagram request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional

from .constants import INSTAGRAM_DEFAULT_RESULTS, INSTAGRAM_MAX_RESULTS
from .types import InstagramSearchType


class InstagramResponse(BaseModel):
    """Generic response schema for Instagram scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True
