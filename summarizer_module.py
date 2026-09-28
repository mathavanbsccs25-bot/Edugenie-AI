from app.ai.gemini_client import gemini

SYSTEM_PROMPT = """You are EduGenie's summarization assistant. Summarize educational material accurately. Preserve important concepts, definitions, facts, and relationships. Do not introduce information that is not present in the source."""


def summarize(content: str, length: str = "medium") -> str:
    prompt = f"""Summarize the following educational content.\nDesired summary length: {length}\n\nContent:\n{content}\n\nUse clear headings and bullet points where appropriate."""
    return gemini.generate(prompt=prompt, system_instruction=SYSTEM_PROMPT)
