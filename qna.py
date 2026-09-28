from app.ai.gemini_client import gemini

SYSTEM_PROMPT = """You are EduGenie, an educational AI assistant.
Help students understand academic topics clearly and accurately.
Use simple language, break difficult concepts into smaller parts, and give examples when useful.
Do not encourage cheating. For academic questions, teach the reasoning rather than giving unexplained answers."""


def ask_question(question: str, context: str | None = None) -> str:
    prompt = f"""Student question:\n{question}\n\nAdditional context:\n{context or "No additional context was provided."}\n\nAnswer clearly. When appropriate use: direct answer, explanation, example, and key points."""
    return gemini.generate(prompt=prompt, system_instruction=SYSTEM_PROMPT)
