from app.ai.gemini_client import gemini

SYSTEM_PROMPT = """You are EduGenie's quiz generation engine.
Generate educational multiple-choice questions. Every question must have a question, exactly four options, answer, and explanation. The answer must exactly match one option. Return only valid JSON."""


def generate_quiz(topic: str, number_of_questions: int = 5, difficulty: str = "medium"):
    prompt = f"""Create a multiple-choice quiz.\nTopic: {topic}\nNumber of questions: {number_of_questions}\nDifficulty: {difficulty}\n\nReturn exactly this JSON structure:\n{{"questions":[{{"question":"Question text","options":["Option A","Option B","Option C","Option D"],"answer":"Correct option","explanation":"Why this answer is correct"}}]}}\nDo not include Markdown or code fences. Return only JSON."""
    data = gemini.generate_json(prompt=prompt, system_instruction=SYSTEM_PROMPT)
    questions = data.get("questions", [])
    if not questions:
        raise RuntimeError("Gemini did not return any quiz questions.")
    return questions
