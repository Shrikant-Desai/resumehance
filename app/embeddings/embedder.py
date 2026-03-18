from google import genai
from google.genai import types
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

EMBEDDING_MODEL = "gemini-embedding-2-preview"


def embed_skill(skill_name: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=skill_name,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY", output_dimensionality=768
        ),  # important — tells model what embeddings are used for
    )
    # response.embeddings is a list of Embedding objects; .values is the list[float]
    return response.embeddings[0].values


def embed_skills_batch(skills: list[str]) -> dict[str, list[float]]:
    result = {}
    for skill in skills:
        try:
            result[skill] = embed_skill(skill)
        except Exception as e:
            # log and skip — don't let one bad skill kill the whole batch
            print(f"[embedder] Failed to embed skill '{skill}': {e}")
    return result
