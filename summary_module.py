from gemini_client import generate_text

SYSTEM = """
You are EduGenie's revision summarizer.
Preserve the important meaning and facts while removing repetition.
Write a concise, easy-to-revise summary.
"""

def summarize_text(text: str) -> str:
    prompt = f"""
Summarize this material for quick student revision:

{text}

Return:
- A short overview
- 5 to 8 key points
- Important terms or formulas if present
"""
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.2, max_output_tokens=1200)
