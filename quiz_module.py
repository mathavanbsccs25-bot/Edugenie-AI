from gemini_client import generate_json

SYSTEM = """
You create educational multiple-choice quizzes.
Return valid JSON only.
Each quiz contains exactly 3 questions.
Each question has exactly 4 options and exactly one correct answer.
The correct_answer must exactly match one option.
Keep questions grounded in the supplied passage/topic.
"""

def _validate_quiz(data):
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Gemini did not return exactly 3 questions.")

    normalized = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Invalid quiz question.")
        question = str(item.get("question", "")).strip()
        options = item.get("options")
        correct = str(item.get("correct_answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError("Each question must contain 4 options.")
        options = [str(x).strip() for x in options]
        if correct not in options:
            raise ValueError("Correct answer must match an option.")

        normalized.append({
            "question": question,
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
        })
    return normalized


def generate_quiz(content: str):
    prompt = f"""
Create a 3-question MCQ quiz from this learning material:

{content}

Return JSON in exactly this shape:
[
  {{
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "explanation": "Why this is correct"
  }}
]
"""
    return _validate_quiz(generate_json(prompt, system_instruction=SYSTEM))
