"""Pinterest request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional


class PinterestResponse(BaseModel):
    """Response schema for Pinterest scraping results."""

    success: bool
    data: list[dict]
    total_results: int = Field(alias="totalResults")
    run_id: Optional[str] = Field(default=None, alias="runId")

    class Config:
        populate_by_name = True
