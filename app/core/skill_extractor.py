from app.core.ai_engine import AIEngine
import json


def extract(resume_text: str) -> dict:
    """
    Extract structured information from a resume using Gemini.

    Works for both technical (software engineer) and non-technical (finance,
    healthcare, marketing) resumes by capturing domain-specific skill fields.

    Returns a dict matching the ParsedResume schema.
    """

    full_prompt = f"""Extract structured information from this resume.
Return ONLY a valid JSON object matching the structure below. No explanation, no markdown fences.

{{
  "personal_info": {{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "portfolio": ""
  }},
  "total_experience_years": 0.0,
  "experience": [
    {{
      "company": "",
      "role": "",
      "start_date": "",
      "end_date": "",
      "duration_months": 0,
      "responsibilities": []
    }}
  ],
  "education": [
    {{
      "degree": "",
      "field": "",
      "institution": "",
      "year": ""
    }}
  ],
  "skills": {{
    "technical_skills": [],
    "tools_and_technologies": [],
    "frameworks": [],
    "databases": [],
    "cloud_platforms": [],
    "programming_languages": [],
    "domain_skills": [],
    "methodologies": [],
    "soft_skills": [],
    "languages_spoken": [],
    "certifications": [],
    "tools": []
  }},
  "skill_experience_map": {{"skill_name": 0.0}},
  "resume_domain": "",
  "seniority_level": ""
}}

Rules:
- "resume_domain": overall domain of the resume e.g. "Software Engineering", "Finance", "Healthcare", "Marketing", "Operations"
- "seniority_level": infer from experience — "Fresher", "Junior", "Mid-Level", "Senior", "Lead/Principal"
- "technical_skills": core domain-specific skills (e.g. Python, financial modelling, patient care)
- "domain_skills": non-technical domain competencies (e.g. supply chain, patient care, risk analysis)
- "methodologies": process methodologies (e.g. Agile, Lean, Six Sigma, Design Thinking, Scrum)
- "tools": general productivity/business tools (e.g. Excel, Tally, Salesforce, Figma, SAP)
- "skill_experience_map": map key skills to years of professional exposure (float)
- If a field has no data, use empty list [] or empty string "" — do NOT omit fields

Resume:
{resume_text}"""

    ai = AIEngine()
    response = ai.ask(full_prompt)

    # Remove ```json ``` wrappers if Gemini returns markdown fences
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dictionary
    skills_dict = json.loads(cleaned)

    return skills_dict
