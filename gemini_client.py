import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Copy .env.example to .env and add your Gemini API key."
        )
    return genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
) -> str:
    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def clean_json_block(text: str) -> str:
    text = text.strip()
    match = __import__("re").search(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
    return match.group(1).strip() if match else text


def generate_json(prompt: str, *, system_instruction: str | None = None) -> object:
    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=2200,
        system_instruction=system_instruction,
        response_mime_type="application/json",
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")

    try:
        return __import__("json").loads(text)
    except Exception:
        return __import__("json").loads(clean_json_block(text))
