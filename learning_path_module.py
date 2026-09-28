from app.ai.gemini_client import gemini

SYSTEM_PROMPT = """You are EduGenie's learning-path advisor. Create practical educational learning paths that start with prerequisites, progress from fundamentals to advanced topics, include practice and projects, and provide checkpoints."""


def generate_learning_path(subject: str, current_level: str, goal: str) -> str:
    prompt = f"""Create a personalized learning path.\nSubject: {subject}\nCurrent level: {current_level}\nGoal: {goal}\n\nCreate: prerequisites, fundamentals, core concepts, practical skills, advanced concepts, practice projects, revision strategy, and final skills checklist."""
    return gemini.generate(prompt=prompt, system_instruction=SYSTEM_PROMPT)
