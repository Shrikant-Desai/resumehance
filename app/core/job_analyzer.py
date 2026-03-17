from app.core.ai_engine import AIEngine
import json


def analyze(job_description_text):

    full_prompt = f"""Analyze this job description and return ONLY a JSON object with this structure, no explanation:
    {{
    "job_title": "",
    "seniority_level": "",
    "domain": "",
    "experience_required": {{"minimum_years": 0, "preferred_years": 0}},
    "required_skills": {{"technical_skills":[],"soft_skills":[],"tools_and_technologies":[],"frameworks":[],"databases":[]}},
    "good_to_have_skills": {{"technical_skills":[],"tools_and_technologies":[],"frameworks":[]}},
    "skill_priority_map": {{"skill_name": "critical/important/good_to_have"}}
    }}

    Job Description:
    {job_description_text}"""
    ai = AIEngine()
    response = ai.ask(full_prompt)

    # Remove ```json ``` wrappers if present
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dictionary
    skills_dict = json.loads(cleaned)

    return skills_dict
