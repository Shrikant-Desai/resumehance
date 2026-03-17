from app.core.ai_engine import AIEngine
import json


def extract(resume_text):
    # full_prompt = f"Extract all skills from this resume. Return a JSON object with keys: technical_skills (list), soft_skills (list), tools (list), certifications (list). Return only JSON, nothing else.\n\nUser: {resume_text}"

    full_prompt = f"""Extract information from this resume and return ONLY a JSON object with this structure, no explanation:
    {{
    "total_experience_years": 0.0,
    "experience": [{{"company":"","role":"","start_date":"","end_date":"","duration_months":0}}],
    "skills": {{"technical_skills":[],"soft_skills":[],"tools_and_technologies":[],"frameworks":[],"databases":[],"certifications":[]}},
    "skill_experience_map": {{"skill_name": years_as_number}}
    }}

    Resume:
    {resume_text}"""
    ai = AIEngine()
    response = ai.ask(full_prompt)

    # Remove ```json ``` wrappers if present
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dictionary
    skills_dict = json.loads(cleaned)

    return skills_dict
