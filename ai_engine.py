from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


class AIEngine:
    """Wrapper around the Gemini generative AI client."""

    def __init__(self, model: str = "gemini-3.1-flash-lite-preview"):
        # API Keys
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def ask(
        self,
        prompt: str,
    ) -> str:
        """Send a prompt to Gemini and return the response text."""
        try:
            # full_prompt = f"{AI_SYSTEM_PROMPT}\n\nUser: {user_input}"
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            answer = response.text.strip()
            return answer

        except Exception as e:
            return f"Sorry, I ran into an error. Please try again. {e}"
