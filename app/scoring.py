"""Weighted readiness scoring engine (the deterministic, auditable half of the app)."""

from .questions import QUESTIONS, QUESTIONS_BY_ID, SECTIONS, SEVERITY_WEIGHTS

# How much credit each answer earns.
ANSWER_FACTORS = {"compliant": 1.0, "partial": 0.5, "non_compliant": 0.0}
VALID_ANSWERS = set(ANSWER_FACTORS) | {"na"}


def validate_answers(answers: dict) -> None:
    unknown = [k for k in answers if k not in QUESTIONS_BY_ID]
    if unknown:
        raise ValueError(f"Unknown question ids: {', '.join(sorted(unknown))}")
    bad = {k: v for k, v in answers.items() if v not in VALID_ANSWERS}
    if bad:
        raise ValueError(f"Invalid answer values: {bad}")


def band_for(score: float, fundamental_failures: int) -> str:
    """Readiness band. Any non-compliant fundamental item caps the band at 'At risk'."""
    if fundamental_failures > 0 or score < 75:
        return "At risk"
    if score < 90:
        return "Needs improvement"
    return "Audit ready"


def compute_score(answers: dict) -> dict:
    """Score a questionnaire. Unanswered questions count as non_compliant."""
    validate_answers(answers)
    earned = possible = 0.0
    sections = {s: {"earned": 0.0, "possible": 0.0} for s in SECTIONS}
    gaps = []
    fundamental_failures = 0

    for q in QUESTIONS:
        answer = answers.get(q["id"], "non_compliant")
        if answer == "na":
            continue
        weight = SEVERITY_WEIGHTS[q["severity"]]
        factor = ANSWER_FACTORS[answer]
        earned += weight * factor
        possible += weight
        sections[q["section"]]["earned"] += weight * factor
        sections[q["section"]]["possible"] += weight
        if factor < 1.0:
            gaps.append({
                "id": q["id"], "section": q["section"],
                "section_name": SECTIONS[q["section"]], "severity": q["severity"],
                "text": q["text"], "answer": answer,
                "lost_points": round(weight * (1 - factor), 1), "fix": q["fix"],
            })
        if q["severity"] == "fundamental" and answer == "non_compliant":
            fundamental_failures += 1

    score = round(100 * earned / possible, 1) if possible else 0.0
    gaps.sort(key=lambda g: (-g["lost_points"], g["id"]))
    section_scores = [
        {"section": s, "name": SECTIONS[s],
         "score": round(100 * v["earned"] / v["possible"], 1) if v["possible"] else None}
        for s, v in sections.items()
    ]
    return {
        "score": score,
        "band": band_for(score, fundamental_failures),
        "fundamental_failures": fundamental_failures,
        "sections": section_scores,
        "gaps": gaps,
    }
