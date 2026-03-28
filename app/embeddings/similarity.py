import math
from app.db.models import SkillVector
from app.schemas.analysis import SkillMatchItem

FULL_MATCH_THRESHOLD = 0.85
PARTIAL_MATCH_THRESHOLD = 0.65


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a**2 for a in vec_a))
    mag_b = math.sqrt(sum(b**2 for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def find_matching_skills(
    resume_skill_vectors: list[SkillVector], jd_skill_vectors: list[SkillVector]
) -> tuple[list[SkillMatchItem], list[SkillMatchItem], list[SkillMatchItem]]:

    matched = []
    partial = []
    missing = []

    for jd_skill in jd_skill_vectors:
        best_score = 0.0
        best_match = None

        # find the closest resume skill for this JD skill
        for resume_skill in resume_skill_vectors:
            score = _cosine_similarity(jd_skill.vector, resume_skill.vector)
            if score > best_score:
                best_score = score
                best_match = resume_skill.skill_name

        score_rounded = round(best_score, 4)

        if best_score >= FULL_MATCH_THRESHOLD:
            matched.append(
                SkillMatchItem(
                    skill=jd_skill.skill_name,
                    matched_with=best_match,
                    similarity_score=score_rounded,
                    match_type="full",
                )
            )
        elif best_score >= PARTIAL_MATCH_THRESHOLD:
            partial.append(
                SkillMatchItem(
                    skill=jd_skill.skill_name,
                    matched_with=best_match,
                    similarity_score=score_rounded,
                    match_type="partial",
                )
            )
        else:
            missing.append(
                SkillMatchItem(
                    skill=jd_skill.skill_name,
                    matched_with=None,
                    similarity_score=score_rounded,
                    match_type="missing",
                )
            )

    return matched, partial, missing
