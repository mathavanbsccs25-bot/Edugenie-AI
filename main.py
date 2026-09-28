from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.schemas import AskRequest, ExplainRequest, QuizRequest, SummarizeRequest, LearningPathRequest, AIResponse, QuizResponse
from app.ai.gemini_client import gemini
from app.modules.qna import ask_question
from app.modules.explanation_module import explain_topic
from app.modules.quiz_module import generate_quiz
from app.modules.summarizer_module import summarize
from app.modules.learning_path_module import generate_learning_path

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, description="Google Gemini powered educational learning assistant.")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/health")
async def health():
    return {"status": "ok", "application": settings.APP_NAME, "version": settings.APP_VERSION, "gemini_configured": gemini.is_configured()}

@app.post("/api/ask", response_model=AIResponse)
async def ask(request: AskRequest):
    try:
        return AIResponse(success=True, response=ask_question(request.question, request.context))
    except Exception as exc:
        return AIResponse(success=False, response="", error=str(exc))

@app.post("/api/explain", response_model=AIResponse)
async def explain(request: ExplainRequest):
    try:
        return AIResponse(success=True, response=explain_topic(request.topic, request.level, request.language))
    except Exception as exc:
        return AIResponse(success=False, response="", error=str(exc))

@app.post("/api/summarize", response_model=AIResponse)
async def summarize_content(request: SummarizeRequest):
    try:
        return AIResponse(success=True, response=summarize(request.content, request.length))
    except Exception as exc:
        return AIResponse(success=False, response="", error=str(exc))

@app.post("/api/quiz", response_model=QuizResponse)
async def quiz(request: QuizRequest):
    try:
        return QuizResponse(success=True, topic=request.topic, questions=generate_quiz(request.topic, request.number_of_questions, request.difficulty))
    except Exception as exc:
        return QuizResponse(success=False, topic=request.topic, questions=[], error=str(exc))

@app.post("/api/learn/recommendations", response_model=AIResponse)
async def learning_recommendations(request: LearningPathRequest):
    try:
        return AIResponse(success=True, response=generate_learning_path(request.subject, request.current_level, request.goal))
    except Exception as exc:
        return AIResponse(success=False, response="", error=str(exc))
