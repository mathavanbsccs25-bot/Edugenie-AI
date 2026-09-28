# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A
- Concept explanations
- 3-question MCQ quizzes with 4 options each
- Concise summaries for revision
- Personalized learning paths with beginner/intermediate/advanced progression

## Architecture

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── README.txt
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

The source document explicitly describes FastAPI, a simple HTML/CSS frontend, the five learning functions/modules, and the `/quiz`, `/summarize`, and `/learn/recommendations` endpoints. This implementation keeps that architecture while making the frontend directly served by FastAPI for fewer moving parts.

## Important modernization

The source document refers to Gemini 1.5 Pro. That model is no longer the right dependency target for a new 2026 build. This implementation uses Google's current `google-genai` Python SDK and defaults to `gemini-3.8-flash`. You can change `GEMINI_MODEL` in `.env` if your Google AI account exposes another supported model.

## 1. Prerequisites

Install:

- Python 3.10 or newer
- VS Code
- Internet access for Gemini API calls
- A Gemini API key

## 2. Open the project

Open the `EduGenie` folder in VS Code.

## 3. Create a virtual environment

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Gemini

Copy `.env.example` to `.env`:

```text
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env` to Git. It is already excluded by `.gitignore`.

## 6. Run

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 7. Test without using the Gemini API

Run:

```bash
pytest -q
```

This verifies that the FastAPI app loads, the health endpoint works, and the frontend is served.

## 8. Test the AI endpoints

With the server running, use the web interface or `/docs`.

### Q&A

`POST /ask`

```json
{
  "question": "What is photosynthesis?",
  "context": ""
}
```

### Explanation

`POST /explain`

```json
{
  "text": "Explain inheritance in Java"
}
```

### Quiz

`POST /quiz`

```json
{
  "text": "The Earth revolves around the Sun and rotates on its axis."
}
```

### Summary

`POST /summarize`

```json
{
  "text": "Paste your study material here..."
}
```

### Learning path

`POST /learn/recommendations`

```json
{
  "topic": "Python programming",
  "level": "Beginner"
}
```

## Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure `.env` exists in the project root and contains a valid key.

### `ModuleNotFoundError`

Activate `.venv` and run:

```bash
pip install -r requirements.txt
```

### Model unavailable

Change `GEMINI_MODEL` to a model currently available to your API account. The Google Gemini model catalog changes over time.

### Port 8000 already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Project notes

The implementation intentionally avoids adding a database, authentication system, React build chain, or other infrastructure that is not required by the supplied documentation. The result is a small full-stack application: FastAPI backend + plain HTML/CSS/JavaScript frontend + Gemini API integration.
