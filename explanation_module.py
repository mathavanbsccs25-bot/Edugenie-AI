from app.ai.gemini_client import gemini

SYSTEM_PROMPT = """You are EduGenie's concept explanation tutor.
Explain academic concepts according to the student's level using simple definitions, step-by-step explanations, real-world examples, important terminology, and a short recap."""


def explain_topic(topic: str, level: str = "beginner", language: str = "English") -> str:
    prompt = f"""Explain this topic for a student.\n\nTopic: {topic}\nStudent level: {level}\nPreferred language: {language}\n\nProvide: definition, basic explanation, how it works, example, important points, and short summary."""
    return gemini.generate(prompt=prompt, system_instruction=SYSTEM_PROMPT)
