def calculate_score(extracted_skills, required_skills, skills_match):

    weights = {
        "critical": 40,
        "important": 25,
        "good_to_have": 15,
        "experience": 20,
    }

    matched = set(skills_match.get("matched", []))

    priority_map = required_skills.get("skill_priority_map", {})

    # categorize skills dynamically
    critical_skills = [s for s, p in priority_map.items() if p == "critical"]
    important_skills = [s for s, p in priority_map.items() if p == "important"]
    good_skills = [s for s, p in priority_map.items() if p == "good_to_have"]

    # scoring helper
    def score(skills, weight):
        if not skills:
            return 0
        matched_count = len([s for s in skills if s in matched])
        return (matched_count / len(skills)) * weight

    critical_score = score(critical_skills, weights["critical"])
    important_score = score(important_skills, weights["important"])
    good_score = score(good_skills, weights["good_to_have"])

    # Experience score
    candidate_exp = extracted_skills.get("total_experience_years", 0)
    min_exp = required_skills.get("experience_required", {}).get("minimum_years", 0)

    if min_exp == 0:
        exp_score = weights["experience"]
    else:
        exp_score = min(candidate_exp / min_exp, 1) * weights["experience"]

    total_score = critical_score + important_score + good_score + exp_score

    return round(total_score, 2)
