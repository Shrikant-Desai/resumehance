from app.core import readiness_score as score_calculator
from app.core import roadmap_generator
from app.core.exceptions import (
    ResumeNotFoundException,
    JobNotFoundException,
    AnalysisNotFoundException,
    GeminiCallFailedException,
)
from app.db import repositories
from app.embeddings.similarity import find_matching_skills
from app.schemas.analysis import (
    AnalysisRunRequest,
    AnalysisRunResponse,
    AnalysisSummaryResponse,
    MatchResult,
    GapResult,
    SkillGapItem,
    ExperienceGap,
    ReadinessScore,
    Roadmap,
)
from app.schemas.job import ParsedJob
from app.schemas.resume import ParsedResume


def _build_experience_gap(
    parsed_resume: ParsedResume, parsed_job: ParsedJob
) -> ExperienceGap:
    candidate_years = parsed_resume.total_experience_years or 0.0
    required_years = parsed_job.experience_required.minimum_years or 0.0
    gap = max(0.0, required_years - candidate_years)

    if candidate_years >= required_years:
        verdict = "meets"
    elif gap <= 1.0:
        verdict = "close"
    else:
        verdict = "below"

    return ExperienceGap(
        required_years=required_years,
        candidate_years=candidate_years,
        gap_years=round(gap, 1),
        verdict=verdict,
    )


def _build_skill_gaps(
    missing_skills, partial_skills, priority_map: dict
) -> list[SkillGapItem]:
    gaps = []

    for item in missing_skills:
        gaps.append(
            SkillGapItem(
                skill=item.skill,
                priority=priority_map.get(item.skill.lower(), "important"),
                gap_type="missing",
                estimated_learning_weeks=None,  # roadmap generator will handle this
            )
        )

    for item in partial_skills:
        gaps.append(
            SkillGapItem(
                skill=item.skill,
                priority=priority_map.get(item.skill.lower(), "important"),
                gap_type="needs_strengthening",
                estimated_learning_weeks=None,
            )
        )

    # sort by priority — critical first
    priority_order = {"critical": 0, "important": 1, "good_to_have": 2}
    gaps.sort(key=lambda x: priority_order.get(x.priority, 1))

    return gaps


async def run_analysis(request: AnalysisRunRequest) -> AnalysisRunResponse:

    # step 1 — check if analysis already exists for this pair
    existing = repositories.get_analysis_by_resume_and_jd(
        resume_id=request.resume_id, jd_id=request.jd_id
    )
    if existing:
        return AnalysisRunResponse(**existing.result_json)

    # step 2 — fetch resume and JD from DB
    resume_record = repositories.get_resume_by_id(request.resume_id)
    if not resume_record:
        raise ResumeNotFoundException(request.resume_id)

    jd_record = repositories.get_jd_by_id(request.jd_id)
    if not jd_record:
        raise JobNotFoundException(request.jd_id)

    # step 3 — reconstruct schema objects from stored JSON
    parsed_resume = ParsedResume(**resume_record.parsed_json)
    parsed_job = ParsedJob(**jd_record.parsed_json)

    # step 4 — fetch skill vectors from DB
    resume_vectors = repositories.get_skill_vectors(
        source="resume", source_id=request.resume_id
    )
    jd_vectors = repositories.get_skill_vectors(source="jd", source_id=request.jd_id)

    # step 5 — run vector similarity matching
    matched, partial, missing = find_matching_skills(
        resume_skill_vectors=resume_vectors, jd_skill_vectors=jd_vectors
    )

    match_result = MatchResult(
        matched_skills=matched,
        partial_skills=partial,
        missing_skills=missing,
        match_percentage=round(
            len(matched) / max(len(matched) + len(partial) + len(missing), 1) * 100, 1
        ),
    )

    # step 6 — build experience gap
    experience_gap = _build_experience_gap(parsed_resume, parsed_job)

    # step 7 — build skill gaps list
    # normalize priority map keys to lowercase for safe lookup
    priority_map = {k.lower(): v for k, v in parsed_job.skill_priority_map.items()}
    skill_gaps = _build_skill_gaps(missing, partial, priority_map)

    gap_result = GapResult(
        experience_gap=experience_gap,
        skill_gaps=skill_gaps,
        total_critical_gaps=sum(1 for g in skill_gaps if g.priority == "critical"),
        total_important_gaps=sum(1 for g in skill_gaps if g.priority == "important"),
    )

    # step 8 — calculate readiness score (your pure logic function)
    readiness = score_calculator.calculate_score(
        match_result=match_result,
        gap_result=gap_result,
        parsed_resume=parsed_resume,
        parsed_job=parsed_job,
    )

    readiness_score = ReadinessScore(
        score=readiness["score"],
        verdict=readiness["verdict"],
        skill_score=readiness["skill_score"],
        experience_score=readiness["experience_score"],
        breakdown=readiness.get("breakdown", {}),
    )

    # step 9 — generate roadmap via Gemini
    try:
        roadmap_dict = roadmap_generator.generate(
            target_role=parsed_job.job_title,
            seniority_level=parsed_job.seniority_level,
            candidate_level=parsed_resume.seniority_level,
            total_experience_years=parsed_resume.total_experience_years,
            missing_skills=[g for g in skill_gaps if g.gap_type == "missing"],
            partial_skills=[
                g for g in skill_gaps if g.gap_type == "needs_strengthening"
            ],
        )
        roadmap = Roadmap(**roadmap_dict)
    except Exception as e:
        raise GeminiCallFailedException(step="roadmap_generation", reason=str(e))

    # step 10 — build final response
    response = AnalysisRunResponse(
        analysis_id=0,  # will be updated after save
        resume_id=request.resume_id,
        jd_id=request.jd_id,
        match_result=match_result,
        gap_result=gap_result,
        readiness_score=readiness_score,
        roadmap=roadmap,
        created_at=None,  # will be updated after save
    )

    # step 11 — save to DB
    analysis_record = repositories.save_analysis(
        resume_id=request.resume_id,
        jd_id=request.jd_id,
        match_result=match_result.model_dump(),
        gap_result=gap_result.model_dump(),
        score=readiness_score.score,
        roadmap=roadmap.model_dump(),
        result_json=response.model_dump(),
    )

    response.analysis_id = analysis_record.id
    response.created_at = analysis_record.created_at

    return response


async def get_analysis(analysis_id: int) -> AnalysisRunResponse:
    record = repositories.get_analysis_by_id(analysis_id)
    if not record:
        raise AnalysisNotFoundException(analysis_id)
    return AnalysisRunResponse(**record.result_json)


async def get_analysis_summary(analysis_id: int) -> AnalysisSummaryResponse:
    record = repositories.get_analysis_by_id(analysis_id)
    if not record:
        raise AnalysisNotFoundException(analysis_id)

    match = MatchResult(**record.result_json["match_result"])
    gap = GapResult(**record.result_json["gap_result"])

    return AnalysisSummaryResponse(
        analysis_id=record.id,
        resume_id=record.resume_id,
        jd_id=record.jd_id,
        readiness_score=record.readiness_score,
        verdict=record.result_json["readiness_score"]["verdict"],
        total_matched=len(match.matched_skills),
        total_gaps=len(gap.skill_gaps),
        created_at=record.created_at,
    )
