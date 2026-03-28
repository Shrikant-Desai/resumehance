def calculate_score(match_result, gap_result, parsed_resume, parsed_job) -> dict:
    """
    Calculate job readiness score from structured schema objects.

    Called by analysis_service.run_analysis() after vector similarity matching.

    Weights:
      - Critical skills  → 40 pts
      - Important skills → 25 pts
      - Good-to-have     → 15 pts
      - Experience       → 20 pts
    Partial skill matches count at 50% of a full match.
    """

    weights = {
        "critical": 40,
        "important": 25,
        "good_to_have": 15,
        "experience": 20,
    }

    # Build fast lookup sets from match_result (list of SkillMatchItem objects)
    matched_skills = {item.skill.lower() for item in match_result.matched_skills}
    partial_skills = {item.skill.lower() for item in match_result.partial_skills}

    # Priority map from ParsedJob — normalise to lowercase keys
    priority_map = {k.lower(): v for k, v in parsed_job.skill_priority_map.items()}

    # Group by priority
    critical_skills = [s for s, p in priority_map.items() if p == "critical"]
    important_skills = [s for s, p in priority_map.items() if p == "important"]
    good_skills = [s for s, p in priority_map.items() if p == "good_to_have"]

    def score_bucket(skills: list[str], weight: float) -> float:
        """Score a bucket: full match = 1.0 credit, partial = 0.5 credit."""
        if not skills:
            return weight  # no skills required → full credit for this bucket
        credits = 0.0
        for s in skills:
            if s in matched_skills:
                credits += 1.0
            elif s in partial_skills:
                credits += 0.5
        return (credits / len(skills)) * weight

    critical_score = score_bucket(critical_skills, weights["critical"])
    important_score = score_bucket(important_skills, weights["important"])
    good_score = score_bucket(good_skills, weights["good_to_have"])

    # Experience score
    candidate_exp = parsed_resume.total_experience_years or 0.0
    min_exp = parsed_job.experience_required.minimum_years or 0.0

    if min_exp == 0:
        exp_score = weights["experience"]
    else:
        exp_score = min(candidate_exp / min_exp, 1.0) * weights["experience"]

    skill_score = round(critical_score + important_score + good_score, 2)
    experience_score = round(exp_score, 2)
    total_score = round(skill_score + experience_score, 2)

    # Verdict thresholds
    if total_score >= 75:
        verdict = "Strong"
    elif total_score >= 55:
        verdict = "Good"
    elif total_score >= 35:
        verdict = "Fair"
    else:
        verdict = "Needs Work"

    breakdown = {
        "critical_score": round(critical_score, 2),
        "important_score": round(important_score, 2),
        "good_to_have_score": round(good_score, 2),
        "experience_score": experience_score,
    }

    return {
        "score": total_score,
        "verdict": verdict,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "breakdown": breakdown,
    }
