from gemini_client import generate_text

SYSTEM = """
You are EduGenie, an educational question-answering assistant.
Answer directly, accurately, and at an appropriate student level.
Prefer concise explanations and examples. If the supplied context is insufficient,
say what is missing instead of pretending to know it.
"""

def answer_question(question: str, context: str = "") -> str:
    prompt = f"""
Question:
{question}

Optional study context:
{context or "(none supplied)"}

Give a clear answer. If useful, include a short example or analogy.
"""
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.2, max_output_tokens=1200)
