import json
import re
from typing import Any, Dict, Optional

from google import genai
from google.genai import types

from app.config import settings


class GeminiClient:
    def __init__(self):
        self.client = None
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def is_configured(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        if not self.client:
            raise RuntimeError(
                "Gemini API key is not configured. Add GEMINI_API_KEY to the .env file."
            )

        config = None
        if system_instruction:
            config = types.GenerateContentConfig(system_instruction=system_instruction)

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        return response.text.strip()

    def generate_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        text = self.generate(prompt, system_instruction)
        cleaned = self._clean_json(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Gemini returned invalid JSON: {exc}") from exc

    @staticmethod
    def _clean_json(text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        return text.strip()


gemini = GeminiClient()
