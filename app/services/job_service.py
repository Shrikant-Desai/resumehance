from app.core import job_analyzer
from app.core.exceptions import GeminiCallFailedException, EmbeddingFailedException
from app.db import repositories
from app.embeddings.embedder import embed_skills_batch
from app.schemas.job import JobCreateRequest, JobCreateResponse, ParsedJob, JobSkills, JobListItem, JobListResponse


def _flatten_job_skills(required: JobSkills, good_to_have: JobSkills) -> list[str]:
    """
    Flatten both required and good_to_have skills into one list.
    We embed everything — similarity search handles priority separately.
    """
    all_skills = (
        required.technical_skills
        + required.tools_and_technologies
        + required.frameworks
        + required.databases
        + required.cloud_platforms
        + required.programming_languages
        + required.domain_skills
        + required.methodologies
        + required.soft_skills
        + required.certifications
        + required.tools
        + good_to_have.technical_skills
        + good_to_have.tools_and_technologies
        + good_to_have.frameworks
        + good_to_have.domain_skills
        + good_to_have.methodologies
        + good_to_have.tools
    )
    seen = set()
    flat = []
    for skill in all_skills:
        skill = skill.strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            flat.append(skill)
    return flat


async def process_job(request: JobCreateRequest) -> JobCreateResponse:

    # step 1 — analyze JD with Gemini
    try:
        parsed_dict = job_analyzer.analyze(request.jd_text)
    except Exception as e:
        raise GeminiCallFailedException(step="job_analysis", reason=str(e))

    # step 2 — override title and company if manually provided
    if request.job_title:
        parsed_dict["job_title"] = request.job_title
    if request.company:
        parsed_dict["company"] = request.company

    # step 3 — validate through schema
    try:
        parsed_job = ParsedJob(**parsed_dict)
    except Exception as e:
        raise GeminiCallFailedException(step="job_analysis_parsing", reason=str(e))

    # step 4 — save JD to DB
    jd_record = repositories.save_jd(
        raw_text=request.jd_text,
        parsed_json=parsed_job.model_dump(),
        job_title=parsed_job.job_title,
        company=parsed_job.company,
    )

    # step 5 — flatten and embed all skills
    all_skills = _flatten_job_skills(
        parsed_job.required_skills, parsed_job.good_to_have_skills
    )

    try:
        skill_vectors = embed_skills_batch(all_skills)
    except Exception as e:
        raise EmbeddingFailedException(skill="batch", reason=str(e))

    # step 6 — save skill vectors to DB
    for skill_name, vector in skill_vectors.items():
        try:
            repositories.save_skill_vector(
                skill_name=skill_name,
                source="jd",
                source_id=jd_record.id,
                vector=vector,
            )
        except Exception as e:
            raise EmbeddingFailedException(skill=skill_name, reason=str(e))

    return JobCreateResponse(
        jd_id=jd_record.id, parsed_data=parsed_job, created_at=jd_record.created_at
    )


def list_jobs(skip: int = 0, limit: int = 20) -> JobListResponse:
    total = repositories.count_jds()
    records = repositories.get_all_jds(skip=skip, limit=limit)

    items = []
    for r in records:
        pj = r.parsed_json or {}
        exp = pj.get("experience_required", {})
        minimum_years = exp.get("minimum_years", 0.0) if isinstance(exp, dict) else 0.0
        items.append(
            JobListItem(
                jd_id=r.id,
                job_title=r.job_title,
                company=r.company,
                domain=pj.get("domain"),
                seniority_level=pj.get("seniority_level"),
                minimum_years_required=minimum_years,
                created_at=r.created_at,
            )
        )

    return JobListResponse(total=total, skip=skip, limit=limit, items=items)
