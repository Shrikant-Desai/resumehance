from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.db.models import Resume, JobDescription, SkillVector, Analysis


# --- Resume ---


def save_resume(raw_text: str, parsed_json: dict, file_name: str) -> Resume:
    with SessionLocal() as db:
        record = Resume(raw_text=raw_text, parsed_json=parsed_json, file_name=file_name)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record


def get_resume_by_id(resume_id: int) -> Resume | None:
    with SessionLocal() as db:
        return db.get(Resume, resume_id)


def get_all_resumes(skip: int = 0, limit: int = 20) -> list[Resume]:
    with SessionLocal() as db:
        return db.query(Resume).order_by(Resume.uploaded_at.desc()).offset(skip).limit(limit).all()


def count_resumes() -> int:
    with SessionLocal() as db:
        return db.query(Resume).count()


# --- Job Description ---


def save_jd(
    raw_text: str, parsed_json: dict, job_title: str, company: str
) -> JobDescription:
    with SessionLocal() as db:
        record = JobDescription(
            raw_text=raw_text,
            parsed_json=parsed_json,
            job_title=job_title,
            company=company,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record


def get_jd_by_id(jd_id: int) -> JobDescription | None:
    with SessionLocal() as db:
        return db.get(JobDescription, jd_id)


def get_all_jds(skip: int = 0, limit: int = 20) -> list[JobDescription]:
    with SessionLocal() as db:
        return (
            db.query(JobDescription)
            .order_by(JobDescription.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


def count_jds() -> int:
    with SessionLocal() as db:
        return db.query(JobDescription).count()


# --- Skill Vectors ---


def save_skill_vector(
    skill_name: str, source: str, source_id: int, vector: list
) -> SkillVector:
    with SessionLocal() as db:
        record = SkillVector(
            skill_name=skill_name,
            source=source,
            resume_id=source_id if source == "resume" else None,
            jd_id=source_id if source == "jd" else None,
            vector=vector,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record


def get_skill_vectors(source: str, source_id: int) -> list[SkillVector]:
    with SessionLocal() as db:
        if source == "resume":
            return (
                db.query(SkillVector)
                .filter(
                    SkillVector.source == "resume", SkillVector.resume_id == source_id
                )
                .all()
            )
        else:
            return (
                db.query(SkillVector)
                .filter(SkillVector.source == "jd", SkillVector.jd_id == source_id)
                .all()
            )


# --- Analysis ---


def save_analysis(
    resume_id: int,
    jd_id: int,
    match_result: dict,
    gap_result: dict,
    score: float,
    roadmap: dict,
    result_json: dict,
) -> Analysis:
    with SessionLocal() as db:
        record = Analysis(
            resume_id=resume_id,
            jd_id=jd_id,
            match_result=match_result,
            gap_result=gap_result,
            readiness_score=score,
            roadmap=roadmap,
            result_json=result_json,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record


def get_analysis_by_id(analysis_id: int) -> Analysis | None:
    with SessionLocal() as db:
        return db.get(Analysis, analysis_id)


def get_analysis_by_resume_and_jd(resume_id: int, jd_id: int) -> Analysis | None:
    with SessionLocal() as db:
        return (
            db.query(Analysis)
            .filter(Analysis.resume_id == resume_id, Analysis.jd_id == jd_id)
            .first()
        )


def get_all_analyses(skip: int = 0, limit: int = 20) -> list[Analysis]:
    with SessionLocal() as db:
        return (
            db.query(Analysis)
            .order_by(Analysis.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


def count_analyses() -> int:
    with SessionLocal() as db:
        return db.query(Analysis).count()


def get_analyses_by_resume(resume_id: int) -> list[Analysis]:
    """All analyses that used a given resume — useful for resume detail views."""
    with SessionLocal() as db:
        return (
            db.query(Analysis)
            .filter(Analysis.resume_id == resume_id)
            .order_by(Analysis.created_at.desc())
            .all()
        )


def get_analyses_by_jd(jd_id: int) -> list[Analysis]:
    """All analyses that used a given JD — useful for JD detail views."""
    with SessionLocal() as db:
        return (
            db.query(Analysis)
            .filter(Analysis.jd_id == jd_id)
            .order_by(Analysis.created_at.desc())
            .all()
        )
