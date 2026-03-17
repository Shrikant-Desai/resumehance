from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SkillMatchItem(BaseModel):
    skill: str
    matched_with: Optional[str] = None  # what it matched to on resume side
    similarity_score: float = 0.0
    match_type: str  # "full" / "partial" / "missing"


class ExperienceGap(BaseModel):
    required_years: float
    candidate_years: float
    gap_years: float
    verdict: str  # "meets", "close", "below"


class SkillGapItem(BaseModel):
    skill: str
    priority: str  # "critical" / "important" / "good_to_have"
    gap_type: str  # "missing" / "needs_strengthening"
    estimated_learning_weeks: Optional[int] = None


class MatchResult(BaseModel):
    matched_skills: list[SkillMatchItem] = []
    partial_skills: list[SkillMatchItem] = []
    missing_skills: list[SkillMatchItem] = []
    match_percentage: float = 0.0


class GapResult(BaseModel):
    experience_gap: ExperienceGap
    skill_gaps: list[SkillGapItem] = []
    total_critical_gaps: int = 0
    total_important_gaps: int = 0


class RoadmapWeek(BaseModel):
    week: int
    skill: str
    priority: str
    action: str  # "learn from scratch" / "strengthen"
    resource: str
    mini_project: str
    milestone: str


class Roadmap(BaseModel):
    target_role: str
    total_weeks: int
    candidate_level: str
    roadmap: list[RoadmapWeek] = []


class ReadinessScore(BaseModel):
    score: float  # 0 to 100
    verdict: str  # "Strong" / "Good" / "Fair" / "Needs Work"
    skill_score: float  # contribution from skills
    experience_score: float  # contribution from experience
    breakdown: dict[str, float] = {}  # optional detailed breakdown


# --- Request / Response models ---


class AnalysisRunRequest(BaseModel):
    resume_id: int
    jd_id: int


class AnalysisRunResponse(BaseModel):
    analysis_id: int
    resume_id: int
    jd_id: int
    match_result: MatchResult
    gap_result: GapResult
    readiness_score: ReadinessScore
    roadmap: Roadmap
    created_at: datetime


class AnalysisSummaryResponse(BaseModel):
    analysis_id: int
    resume_id: int
    jd_id: int
    readiness_score: float
    verdict: str
    total_matched: int
    total_gaps: int
    created_at: datetime


class AnalysisListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[AnalysisSummaryResponse]
