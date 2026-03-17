from fastapi import APIRouter, HTTPException, Query
from app.services import job_service
from app.schemas.job import JobCreateRequest, JobCreateResponse, JobListResponse
from app.core.exceptions import GeminiCallFailedException, EmbeddingFailedException

router = APIRouter(prefix="/job", tags=["Job Description"])


@router.post("/create", response_model=JobCreateResponse)
async def create_job(request: JobCreateRequest):

    if not request.jd_text or len(request.jd_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description is too short.")

    try:
        return await job_service.process_job(request)
    except GeminiCallFailedException as e:
        raise HTTPException(status_code=502, detail=e.message)
    except EmbeddingFailedException as e:
        raise HTTPException(status_code=502, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=JobListResponse)
def list_jobs(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
):
    """List all submitted job descriptions with lightweight summary info."""
    try:
        return job_service.list_jobs(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
