"""FastAPI app: questionnaire in -> weighted score -> AI corrective-action advice out.

Run from the project root:  python -m app.main
"""

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import ai_advisor, database
from .questions import QUESTIONS, SECTIONS
from .scoring import compute_score

@asynccontextmanager
async def lifespan(_app):
    database.init_db()
    yield


app = FastAPI(title="BRCGS Readiness Scorer (proof of concept)", lifespan=lifespan)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class AssessmentIn(BaseModel):
    site_name: str
    answers: dict[str, str]  # question id -> compliant | partial | non_compliant | na


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/health")
def health():
    return {"status": "ok", "ollama": ai_advisor.ollama_available(), "model": ai_advisor.OLLAMA_MODEL}


@app.get("/api/questions")
def questions():
    return {"sections": SECTIONS, "questions": QUESTIONS}


@app.post("/api/assessments")
def create_assessment(body: AssessmentIn):
    try:
        result = compute_score(body.answers)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    assessment_id = database.save_assessment(body.site_name, result)
    return {"id": assessment_id, "site_name": body.site_name, **result}


@app.get("/api/assessments")
def list_assessments():
    return database.list_assessments()


@app.get("/api/assessments/{assessment_id}")
def get_assessment(assessment_id: int):
    record = database.get_assessment(assessment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return record


@app.post("/api/assessments/{assessment_id}/advice")
def advice(assessment_id: int):
    record = database.get_assessment(assessment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    result = ai_advisor.get_advice(record["site_name"], record["result"])
    database.save_advice(assessment_id, result)
    return result


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
