from fastapi import APIRouter, HTTPException, Query
from app.services import analysis_service
from app.schemas.analysis import (
    AnalysisRunRequest,
    AnalysisRunResponse,
    AnalysisSummaryResponse,
    AnalysisListResponse,
)
from app.core.exceptions import (
    ResumeNotFoundException,
    JobNotFoundException,
    AnalysisNotFoundException,
    GeminiCallFailedException,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/run", response_model=AnalysisRunResponse)
async def run_analysis(request: AnalysisRunRequest):
    try:
        return await analysis_service.run_analysis(request)
    except ResumeNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except JobNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except GeminiCallFailedException as e:
        raise HTTPException(status_code=502, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/{analysis_id}", response_model=AnalysisRunResponse)
async def get_analysis(analysis_id: int):
    try:
        return await analysis_service.get_analysis(analysis_id)
    except AnalysisNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/{analysis_id}/summary", response_model=AnalysisSummaryResponse)
async def get_analysis_summary(analysis_id: int):
    try:
        return await analysis_service.get_analysis_summary(analysis_id)
    except AnalysisNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=AnalysisListResponse)
def list_analyses(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
):
    """List all analyses (paginated) ordered by most recent first."""
    try:
        return analysis_service.list_analyses(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/by-resume/{resume_id}", response_model=AnalysisListResponse)
def list_analyses_by_resume(resume_id: int):
    """All analyses that were run for a specific resume."""
    try:
        return analysis_service.list_analyses_by_resume(resume_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/by-jd/{jd_id}", response_model=AnalysisListResponse)
def list_analyses_by_jd(jd_id: int):
    """All analyses that were run for a specific job description."""
    try:
        return analysis_service.list_analyses_by_jd(jd_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
