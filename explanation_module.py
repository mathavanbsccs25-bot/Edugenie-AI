from gemini_client import generate_text

SYSTEM = """
You are EduGenie, a patient educational tutor.
Explain concepts accurately and at a student-friendly level.
Use simple language, short sections, examples, and step-by-step reasoning.
Do not invent facts. If a topic is ambiguous, state the assumption briefly.
"""

def explain_concept(topic: str) -> str:
    prompt = f"""
Explain the following concept for a learner:

{topic}

Format:
1. Simple definition
2. Key idea
3. Step-by-step explanation
4. One simple example
5. Three quick points to remember
"""
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.25, max_output_tokens=1400)
