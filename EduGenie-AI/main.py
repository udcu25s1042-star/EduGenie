from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description=(
        "Google Gemini powered AI learning assistant."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# Static files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# --------------------------------------------------
# Request models
# --------------------------------------------------

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=30000,
    )


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class ExplanationRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced",
    ] = "beginner"


# --------------------------------------------------
# Frontend
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie"
    }


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post("/qa")
async def qa(
    payload: QuestionRequest
):

    try:

        answer = await answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# --------------------------------------------------
# Explanation
# --------------------------------------------------

@app.post("/explain")
async def explain(
    payload: ExplanationRequest
):

    try:

        explanation = await explain_concept(
            payload.topic
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# --------------------------------------------------
# Quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(
    payload: TextRequest
):

    try:

        quiz_data = await generate_quiz(
            payload.text
        )

        return {
            "quiz": quiz_data
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# --------------------------------------------------
# Summary
# --------------------------------------------------

@app.post("/summarize")
async def summarize(
    payload: TextRequest
):

    try:

        summary = await summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


# --------------------------------------------------
# Learning recommendations
# --------------------------------------------------

@app.post(
    "/learn/recommendations"
)
async def recommendations(
    payload: LearningPathRequest
):

    try:

        recommendations = (
            await get_learning_recommendations(
                payload.topic,
                payload.level
            )
        )

        return {
            "recommendations": recommendations
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc