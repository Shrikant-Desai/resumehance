from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None


class ExperienceItem(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_months: Optional[int] = None
    responsibilities: list[str] = []


class EducationItem(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None


class ResumeSkills(BaseModel):
    # technical folks
    technical_skills: list[str] = []
    tools_and_technologies: list[str] = []
    frameworks: list[str] = []
    databases: list[str] = []
    cloud_platforms: list[str] = []
    programming_languages: list[str] = []

    # non technical folks
    domain_skills: list[str] = []  # e.g. financial modeling, patient care, supply chain
    methodologies: list[str] = []  # e.g. agile, six sigma, lean, design thinking
    soft_skills: list[str] = []
    languages_spoken: list[str] = []

    # common for all
    certifications: list[str] = []
    tools: list[str] = []  # generic tools — excel, figma, salesforce, tally etc.


class ParsedResume(BaseModel):
    personal_info: PersonalInfo
    total_experience_years: float = 0.0
    experience: list[ExperienceItem] = []
    education: list[EducationItem] = []
    skills: ResumeSkills
    skill_experience_map: dict[str, float] = {}  # skill -> years
    resume_domain: Optional[str] = (
        None  # e.g. "software engineering", "finance", "healthcare", "marketing"
    )
    seniority_level: Optional[str] = None  # inferred from experience


# --- Request / Response models ---


class ResumeUploadResponse(BaseModel):
    resume_id: int
    file_name: str
    parsed_data: ParsedResume
    uploaded_at: datetime
