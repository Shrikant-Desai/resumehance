import google as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

EMBEDDING_MODEL = "gemini-embedding-2-preview"


def embed_skill(skill_name: str) -> list[float]:
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=skill_name,
        task_type="semantic_similarity",  # important — tells model what embeddings are used for
    )
    return response["embedding"]


def embed_skills_batch(skills: list[str]) -> dict[str, list[float]]:
    result = {}
    for skill in skills:
        try:
            result[skill] = embed_skill(skill)
        except Exception as e:
            # log and skip — don't let one bad skill kill the whole batch
            print(f"[embedder] Failed to embed skill '{skill}': {e}")
    return result
