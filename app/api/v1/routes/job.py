from fastapi import APIRouter, HTTPException
from app.services import job_service
from app.schemas.job import JobCreateRequest, JobCreateResponse
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
