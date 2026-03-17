from app.core.ai_engine import AIEngine
import json


def generate(
    target_role: str,
    seniority_level: str,
    missing_skills,
    partial_skills,
    total_experience_years: float = 0,
    candidate_level: str = "Fresher",
):
    """
    Generate a personalised week-by-week learning roadmap via Gemini.

    Args:
        target_role: Job title from the JD (e.g. "Software Engineer")
        seniority_level: Seniority expected by the job (e.g. "Mid-Level")
        missing_skills: list of SkillGapItem with gap_type == "missing"
        partial_skills: list of SkillGapItem with gap_type == "needs_strengthening"
        total_experience_years: Candidate's total years of experience
        candidate_level: Candidate's current seniority level (e.g. "Fresher", "Junior")
    """

    full_prompt = f"""Create a week-by-week learning roadmap and return ONLY a JSON object, no explanation:
    {{
    "target_role": "",
    "total_weeks": 0,
    "candidate_level": "",
    "roadmap": [
        {{
        "week": 1,
        "skill": "",
        "priority": "critical/important/good_to_have",
        "action": "learn from scratch / strengthen",
        "resource": "",
        "mini_project": "",
        "milestone": ""
        }}
    ]
    }}

    Target Role: {target_role}
    Target Seniority Level: {seniority_level}
    Candidate Current Level: {candidate_level}
    Candidate Total Experience: {total_experience_years} years

    Skills to learn (missing):
    {missing_skills}

    Skills to strengthen (partial matches):
    {partial_skills}

    Experience Adaptation Rules:
    - The roadmap must adapt based on the candidate's total experience AND current level.
    - A fresher should receive more foundational learning and longer time for basic concepts.
    - An experienced person should focus more on advanced topics, real-world projects, and system design.
    - Experienced developers should move faster through basics and spend more time on practical implementation.
    - Do not create the same roadmap for different experience levels.
    """

    ai = AIEngine()
    response = ai.ask(full_prompt)

    # Remove ```json ``` wrappers if Gemini returns markdown fences
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dictionary
    roadmap_dict = json.loads(cleaned)

    return roadmap_dict
