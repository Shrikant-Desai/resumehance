from ai_engine import AIEngine
import json


def match_skills(extracted_skills: dict, required_skills: dict) -> dict:

    prompt = f"""
    Compare a candidate's skills with job requirements.

    Classify each requirement as: matched, partial, or missing.

    Rules:
    - Treat experience as a spectrum.
    - Less experience but relevant exposure → partial.
    - Related skills → partial.

    Return ONLY this dictionary:

    {{
    "matched": [],
    "partial": [
    {{"skill": "", "reason": ""}}
    ],
    "missing": []
    }}

    Candidate data:
    {json.dumps(extracted_skills, indent=2)}

    Job requirements:
    {json.dumps(required_skills, indent=2)}
    """

    ai = AIEngine()
    response = ai.ask(prompt)

    cleaned = response.strip()

    skill_match = json.loads(cleaned)

    return skill_match


def skill_gap_analyzer(missing_skills: dict, job_description: dict) -> dict:

    prompt = f"""
    Analyze the missing skills from a candidate-job comparison.

    For each skill determine:
    - priority: critical, important, good_to_have
    - critical → explicitly required in JD
    - important → mentioned but not mandatory
    - good_to_have → optional skill

    Also estimate:
    - learning_time_months

    Return ONLY JSON:
    {{
    "gaps": [
        {{
        "skill": "",
        "priority": "",
        "learning_time_months": "",
        "reason": ""
        }}
    ]
    }}

    Missing skills:
    {missing_skills}

    Job description:
    {job_description}
    """

    ai = AIEngine()
    response = ai.ask(prompt)

    cleaned = response.strip()

    skill_analysis = json.loads(cleaned)

    return skill_analysis
