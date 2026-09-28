# EduGenie

Google Gemini Powered Learning Assistant.

## Features
- AI question answering
- Topic explanation
- AI quiz generation
- Study-note summarization
- Personalized learning paths
- Responsive web interface
- FastAPI backend
- Google Gemini integration

## Install

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\\Scripts\\activate
```

```bash
pip install -r requirements.txt
```

Create `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash
DEBUG=true
```

## Run

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/api/health

## Test

```bash
pytest
```

Never commit `.env` or expose the API key in frontend code.
