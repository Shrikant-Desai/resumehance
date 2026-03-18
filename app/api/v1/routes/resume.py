from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services import resume_service
from app.schemas.resume import ResumeUploadResponse, ResumeListResponse
from app.core.exceptions import (
    PDFParsingFailedException,
    GeminiCallFailedException,
    EmbeddingFailedException,
)

router = APIRouter(
    prefix="/resume",
)


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):

    # validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # validate file size — reject anything above 5MB
    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 5MB.")

    try:
        return await resume_service.process_resume(
            file_bytes=file_bytes, file_name=file.filename
        )
    except PDFParsingFailedException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except GeminiCallFailedException as e:
        raise HTTPException(status_code=502, detail=e.message)
    except EmbeddingFailedException as e:
        raise HTTPException(status_code=502, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=ResumeListResponse)
def list_resumes(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Max records to return"),
):
    """List all uploaded resumes with lightweight summary info."""
    try:
        return resume_service.list_resumes(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
