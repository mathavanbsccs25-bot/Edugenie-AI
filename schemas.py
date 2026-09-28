from typing import List, Optional
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    context: Optional[str] = None


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"
    language: str = "English"


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    number_of_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str = "medium"


class SummarizeRequest(BaseModel):
    content: str = Field(..., min_length=1)
    length: str = "medium"


class LearningPathRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    current_level: str = "beginner"
    goal: str = Field(..., min_length=1)


class AIResponse(BaseModel):
    success: bool
    response: str
    error: Optional[str] = None


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str


class QuizResponse(BaseModel):
    success: bool
    topic: str
    questions: List[QuizQuestion]
    error: Optional[str] = None
