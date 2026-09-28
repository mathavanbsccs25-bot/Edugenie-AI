from pathlib import Path
import ast

ROOT = Path(__file__).parent
required = [
    "main.py", "gemini_client.py", "explanation_module.py", "qna_module.py",
    "quiz_module.py", "summary_module.py", "learning_path.py",
    "requirements.txt", ".env.example", "README.md",
    "static/index.html", "static/style.css", "static/app.js",
    "tests/test_app.py"
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit(f"Missing files: {missing}")

for py in ROOT.glob("*.py"):
    ast.parse(py.read_text(encoding="utf-8"))

ast.parse((ROOT / "tests/test_app.py").read_text(encoding="utf-8"))
print("EduGenie project structure and Python syntax checks passed.")
