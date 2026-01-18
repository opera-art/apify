"""
Jobs API Routes - Background job management

Endpoints for submitting and tracking background scraping jobs.
"""

from typing import Optional, Literal
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from celery.result import AsyncResult

from src.worker.celery_app import celery_app
from src.worker import tasks

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# =============================================================================
# SCHEMAS
# =============================================================================

class JobSubmitResponse(BaseModel):
    """Response when a job is submitted."""
    job_id: str
    status: str = "PENDING"
    message: str


class JobStatusResponse(BaseModel):
    """Response for job status check."""
    job_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None


class InstagramPostsJobRequest(BaseModel):
    """Request to submit Instagram posts scraping job."""
    usernames: list[str] = Field(..., description="List of Instagram usernames")
    limit: int = Field(default=20, ge=1, le=200)


class InstagramProfileJobRequest(BaseModel):
    """Request to submit Instagram profile scraping job."""
    usernames: list[str] = Field(..., description="List of Instagram usernames")


class InstagramHashtagJobRequest(BaseModel):
    """Request to submit Instagram hashtag scraping job."""
    hashtags: list[str] = Field(..., description="List of hashtags (without #)")
    limit: int = Field(default=20, ge=1, le=200)


class TikTokHashtagJobRequest(BaseModel):
    """Request to submit TikTok hashtag scraping job."""
    hashtag: str = Field(..., description="Hashtag to scrape")
    limit: int = Field(default=10, ge=1, le=100)


class YouTubeSearchJobRequest(BaseModel):
    """Request to submit YouTube search job."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=50)


# =============================================================================
# JOB STATUS ENDPOINT
# =============================================================================

@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Get job status",
    description="Check the status of a background job and get results when ready.",
)
def get_job_status(job_id: str) -> JobStatusResponse:
    """Get the status and result of a job."""
    result = AsyncResult(job_id, app=celery_app)

    response = JobStatusResponse(
        job_id=job_id,
        status=result.status,
    )

    if result.ready():
        if result.successful():
            response.result = result.get()
        else:
            response.error = str(result.result)

    return response


# =============================================================================
# INSTAGRAM JOB ENDPOINTS
# =============================================================================

@router.post(
    "/instagram/posts",
    response_model=JobSubmitResponse,
    summary="Submit Instagram posts job",
    description="Submit a background job to scrape Instagram posts. Returns immediately with job_id.",
)
def submit_instagram_posts_job(request: InstagramPostsJobRequest) -> JobSubmitResponse:
    """Submit Instagram posts scraping job."""
    task = tasks.instagram_scrape_posts.delay(
        usernames=request.usernames,
        limit=request.limit,
    )

    return JobSubmitResponse(
        job_id=task.id,
        status="PENDING",
        message=f"Job submitted. Check status at /api/v1/jobs/{task.id}",
    )


@router.post(
    "/instagram/profile",
    response_model=JobSubmitResponse,
    summary="Submit Instagram profile job",
    description="Submit a background job to scrape Instagram profiles.",
)
def submit_instagram_profile_job(request: InstagramProfileJobRequest) -> JobSubmitResponse:
    """Submit Instagram profile scraping job."""
    task = tasks.instagram_scrape_profile.delay(
        usernames=request.usernames,
    )

    return JobSubmitResponse(
        job_id=task.id,
        status="PENDING",
        message=f"Job submitted. Check status at /api/v1/jobs/{task.id}",
    )


@router.post(
    "/instagram/hashtag",
    response_model=JobSubmitResponse,
    summary="Submit Instagram hashtag job",
    description="Submit a background job to scrape Instagram hashtags.",
)
def submit_instagram_hashtag_job(request: InstagramHashtagJobRequest) -> JobSubmitResponse:
    """Submit Instagram hashtag scraping job."""
    task = tasks.instagram_scrape_hashtag.delay(
        hashtags=request.hashtags,
        limit=request.limit,
    )

    return JobSubmitResponse(
        job_id=task.id,
        status="PENDING",
        message=f"Job submitted. Check status at /api/v1/jobs/{task.id}",
    )


# =============================================================================
# TIKTOK JOB ENDPOINTS
# =============================================================================

@router.post(
    "/tiktok/hashtag",
    response_model=JobSubmitResponse,
    summary="Submit TikTok hashtag job",
    description="Submit a background job to scrape TikTok hashtag.",
)
def submit_tiktok_hashtag_job(request: TikTokHashtagJobRequest) -> JobSubmitResponse:
    """Submit TikTok hashtag scraping job."""
    task = tasks.tiktok_scrape_hashtag.delay(
        hashtag=request.hashtag,
        limit=request.limit,
    )

    return JobSubmitResponse(
        job_id=task.id,
        status="PENDING",
        message=f"Job submitted. Check status at /api/v1/jobs/{task.id}",
    )


# =============================================================================
# YOUTUBE JOB ENDPOINTS
# =============================================================================

@router.post(
    "/youtube/search",
    response_model=JobSubmitResponse,
    summary="Submit YouTube search job",
    description="Submit a background job to search YouTube.",
)
def submit_youtube_search_job(request: YouTubeSearchJobRequest) -> JobSubmitResponse:
    """Submit YouTube search job."""
    task = tasks.youtube_search.delay(
        query=request.query,
        limit=request.limit,
    )

    return JobSubmitResponse(
        job_id=task.id,
        status="PENDING",
        message=f"Job submitted. Check status at /api/v1/jobs/{task.id}",
    )
