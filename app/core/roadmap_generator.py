from ai_engine import AIEngine
import json


def generate(
    target_role,
    seniority_level,
    missing_skills,
    partial_skills,
    total_experience_years=0,
):

    full_prompt = f"""Create a week-by-week learning roadmap and return ONLY a JSON object, no explanation:
    {{
    "target_role": "",
    "total_weeks": 0,
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
    Seniority Level: {seniority_level}
    Candidate Total Experience: {total_experience_years} years

    Skills to learn (missing):
    {missing_skills}

    Skills to strengthen (partial matches):
    {partial_skills}

    Experience Adaptation Rules:
    - The roadmap must adapt based on the candidate's total experience.
    - A fresher should receive more foundational learning and longer time for basic concepts.
    - An experienced person should focus more on advanced topics, real-world projects, and system design.
    - Experienced developers should move faster through basics and spend more time on practical implementation.
    - Do not create the same roadmap for different experience levels.
    """

    ai = AIEngine()
    response = ai.ask(full_prompt)

    # Convert JSON string to Python dictionary
    skills_dict = json.loads(response)

    return skills_dict
