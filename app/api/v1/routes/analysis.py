from fastapi import APIRouter, HTTPException
from app.services import analysis_service
from app.schemas.analysis import (
    AnalysisRunRequest,
    AnalysisRunResponse,
    AnalysisSummaryResponse,
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
