from gemini_client import generate_text

SYSTEM = """
You are EduGenie's learning-path planner.
Create practical, progressive study paths from beginner to advanced.
Include resources types such as documentation, videos, articles, and books,
but do not fabricate specific URLs.
"""

def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = f"""
Create a personalized learning path for:

Topic: {topic}
Current level: {level}

Include:
1. Prerequisites
2. Beginner concepts
3. Intermediate concepts
4. Advanced concepts
5. A suggested weekly sequence
6. Practice/project ideas
7. Resource suggestions by type (official docs, tutorials, videos, books)
"""
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.35, max_output_tokens=1800)
