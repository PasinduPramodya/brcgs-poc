import pytest
from fastapi.testclient import TestClient

from app import main
from app.questions import QUESTIONS
from app.scoring import compute_score


def all_answers(value):
    return {q["id"]: value for q in QUESTIONS}


def test_all_compliant_is_audit_ready():
    r = compute_score(all_answers("compliant"))
    assert r["score"] == 100.0 and r["band"] == "Audit ready" and r["gaps"] == []


def test_fundamental_failure_caps_band():
    answers = all_answers("compliant")
    answers["1.1"] = "non_compliant"  # fundamental item
    r = compute_score(answers)
    assert r["fundamental_failures"] == 1 and r["band"] == "At risk"
    assert r["gaps"][0]["id"] == "1.1"  # biggest loss listed first


def test_partial_earns_half_credit_and_na_is_excluded():
    answers = all_answers("compliant")
    answers["1.4"] = "na"
    answers["1.2"] = "partial"
    r = compute_score(answers)
    assert 0 < r["score"] < 100


def test_unknown_question_rejected():
    with pytest.raises(ValueError):
        compute_score({"9.9": "compliant"})


def test_api_flow_with_fallback_advice(tmp_path, monkeypatch):
    from app import ai_advisor, database
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setattr(ai_advisor, "OLLAMA_URL", "http://127.0.0.1:9")  # nothing listening
    with TestClient(main.app) as client:
        answers = all_answers("compliant")
        answers["3.4"] = "non_compliant"
        created = client.post("/api/assessments", json={"site_name": "T", "answers": answers}).json()
        assert created["band"] == "At risk"
        advice = client.post(f"/api/assessments/{created['id']}/advice").json()
        assert advice["source"] == "fallback" and "3.4" in advice["advice"]
