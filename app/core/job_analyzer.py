from app.core.ai_engine import AIEngine
import json


def analyze(job_description_text: str) -> dict:
    """
    Analyze a job description using Gemini and return a structured ParsedJob dict.

    Works for both technical (software/engineering) and non-technical (finance,
    healthcare, marketing, operations) roles by capturing domain-specific fields.

    Returns a dict matching the ParsedJob schema.
    """

    full_prompt = f"""Analyze this job description.
Return ONLY a valid JSON object matching the structure below. No explanation, no markdown fences.

{{
  "job_title": "",
  "company": "",
  "domain": "",
  "seniority_level": "",
  "experience_required": {{
    "minimum_years": 0.0,
    "preferred_years": 0.0,
    "description": ""
  }},
  "required_skills": {{
    "technical_skills": [],
    "tools_and_technologies": [],
    "frameworks": [],
    "databases": [],
    "cloud_platforms": [],
    "programming_languages": [],
    "domain_skills": [],
    "methodologies": [],
    "soft_skills": [],
    "certifications": [],
    "tools": []
  }},
  "good_to_have_skills": {{
    "technical_skills": [],
    "tools_and_technologies": [],
    "frameworks": [],
    "databases": [],
    "cloud_platforms": [],
    "programming_languages": [],
    "domain_skills": [],
    "methodologies": [],
    "soft_skills": [],
    "certifications": [],
    "tools": []
  }},
  "key_responsibilities": [],
  "skill_priority_map": {{
    "skill_name": "critical"
  }}
}}

Rules:
- "domain": overall job domain e.g. "Software Engineering", "Finance", "Healthcare", "Marketing"
- "seniority_level": e.g. "Fresher", "Junior", "Mid-Level", "Senior", "Lead/Principal"
- "skill_priority_map": classify EVERY skill mentioned — value must be "critical", "important", or "good_to_have"
  - critical → explicitly required / core to the role
  - important → mentioned but not blocking for hire
  - good_to_have → optional/preferred
- "domain_skills": non-technical competencies (e.g. financial modelling, patient care, risk management, supply chain)
- "methodologies": process frameworks (e.g. Agile, Scrum, Lean, Six Sigma, SDLC)
- "tools": general productivity/business tools (e.g. Excel, Salesforce, SAP, Figma, Tally)
- If a field has no data, use empty list [] or empty string "" — do NOT omit fields

Job Description:
{job_description_text}"""

    ai = AIEngine()
    response = ai.ask(full_prompt)

    # Remove ```json ``` wrappers if Gemini returns markdown fences
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dictionary
    job_dict = json.loads(cleaned)

    return job_dict
