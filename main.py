import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from qna_module import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("edugenie")

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: str = Field(default="Beginner", max_length=50)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
    context: str = Field(default="", max_length=20000)


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


@app.post("/explain")
async def explain(request: TextRequest):
    try:
        return {"result": explain_concept(request.text)}
    except Exception as exc:
        logger.exception("Explain failed")
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/ask")
async def ask(request: QuestionRequest):
    try:
        return {"result": answer_question(request.question, request.context)}
    except Exception as exc:
        logger.exception("Q&A failed")
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/quiz")
async def quiz(request: TextRequest):
    try:
        return {"quiz": generate_quiz(request.text)}
    except Exception as exc:
        logger.exception("Quiz failed")
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        return {"result": summarize_text(request.text)}
    except Exception as exc:
        logger.exception("Summary failed")
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/learn/recommendations")
async def learning_recommendations(request: TopicRequest):
    try:
        return {"result": get_learning_recommendations(request.topic, request.level)}
    except Exception as exc:
        logger.exception("Learning path failed")
        raise HTTPException(status_code=502, detail=str(exc))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
