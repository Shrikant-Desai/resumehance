from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExperienceRequired(BaseModel):
    minimum_years: float = 0.0
    preferred_years: float = 0.0
    description: Optional[str] = None


class JobSkills(BaseModel):
    # technical
    technical_skills: list[str] = []
    tools_and_technologies: list[str] = []
    frameworks: list[str] = []
    databases: list[str] = []
    cloud_platforms: list[str] = []
    programming_languages: list[str] = []

    # non technical
    domain_skills: list[str] = []
    methodologies: list[str] = []
    soft_skills: list[str] = []

    # common
    certifications: list[str] = []
    tools: list[str] = []


class ParsedJob(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    domain: Optional[str] = None
    seniority_level: Optional[str] = None
    experience_required: ExperienceRequired = ExperienceRequired()
    required_skills: JobSkills = JobSkills()
    good_to_have_skills: JobSkills = JobSkills()
    key_responsibilities: list[str] = []
    skill_priority_map: dict[str, str] = {}  # skill -> critical/important/good_to_have


# --- Request / Response models ---


class JobCreateRequest(BaseModel):
    jd_text: str
    job_title: Optional[str] = None  # optional manual override
    company: Optional[str] = None


class JobCreateResponse(BaseModel):
    jd_id: int
    parsed_data: ParsedJob
    created_at: datetime
