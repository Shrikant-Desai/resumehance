import json
from datetime import datetime

from app.core import pdf_parser, skill_extractor
from app.core.exceptions import (
    PDFParsingFailedException,
    GeminiCallFailedException,
    EmbeddingFailedException,
)
from app.db import repositories
from app.embeddings.embedder import embed_skills_batch
from app.schemas.resume import ResumeUploadResponse, ParsedResume, ResumeSkills


def _flatten_skills(skills: ResumeSkills) -> list[str]:
    """
    Merge all skill fields into one flat list for embedding.
    Removes duplicates and empty strings.
    """
    all_skills = (
        skills.technical_skills
        + skills.tools_and_technologies
        + skills.frameworks
        + skills.databases
        + skills.cloud_platforms
        + skills.programming_languages
        + skills.domain_skills
        + skills.methodologies
        + skills.soft_skills
        + skills.certifications
        + skills.tools
        + skills.languages_spoken
    )
    # deduplicate while preserving order
    seen = set()
    flat = []
    for skill in all_skills:
        skill = skill.strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            flat.append(skill)
    return flat


async def process_resume(file_bytes: bytes, file_name: str) -> ResumeUploadResponse:

    # step 1 — parse PDF to raw text
    try:
        raw_text = pdf_parser.extract_pdf_text(file_bytes)
    except Exception as e:
        raise PDFParsingFailedException(reason=str(e))

    if not raw_text or len(raw_text.strip()) < 50:
        raise PDFParsingFailedException(
            reason="Extracted text is too short. PDF may be scanned or image-based."
        )

    # step 2 — extract structured data from Gemini
    try:
        parsed_dict = skill_extractor.extract(raw_text)
    except Exception as e:
        raise GeminiCallFailedException(step="skill_extraction", reason=str(e))

    # step 3 — validate parsed data through schema
    try:
        parsed_resume = ParsedResume(**parsed_dict)
    except Exception as e:
        raise GeminiCallFailedException(step="skill_extraction_parsing", reason=str(e))

    # step 4 — save resume to DB
    resume_record = repositories.save_resume(
        raw_text=raw_text, parsed_json=parsed_resume.model_dump(), file_name=file_name
    )

    # step 5 — flatten all skills and embed them
    all_skills = _flatten_skills(parsed_resume.skills)

    try:
        skill_vectors = embed_skills_batch(all_skills)
    except Exception as e:
        raise EmbeddingFailedException(skill="batch", reason=str(e))

    # step 6 — save each skill vector to DB
    for skill_name, vector in skill_vectors.items():
        try:
            repositories.save_skill_vector(
                skill_name=skill_name,
                source="resume",
                source_id=resume_record.id,
                vector=vector,
            )
        except Exception as e:
            raise EmbeddingFailedException(skill=skill_name, reason=str(e))

    return ResumeUploadResponse(
        resume_id=resume_record.id,
        file_name=file_name,
        parsed_data=parsed_resume,
        uploaded_at=resume_record.uploaded_at,
    )
