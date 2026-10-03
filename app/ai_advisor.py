"""AI advisor: asks a local Ollama model for corrective actions on the biggest gaps.

Everything runs on this PC (http://localhost:11434), so no audit data leaves the site.
If Ollama is not running, the app falls back to the rule-based 'fix' hints so the
workflow still works offline.
"""

import os

import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
TOP_GAPS = 5


def ollama_available() -> bool:
    try:
        return requests.get(f"{OLLAMA_URL}/api/tags", timeout=2).ok
    except requests.RequestException:
        return False


def build_prompt(site_name: str, result: dict, top_n: int = TOP_GAPS) -> str:
    lines = [
        f"You are a food safety consultant helping the site '{site_name}' prepare for a BRCGS audit.",
        f"Its readiness score is {result['score']}% ({result['band']}).",
        "For each gap below, give a short, practical corrective action (2 sentences max), "
        "the evidence an auditor would expect, and a suggested owner role.",
        "Do not quote the BRCGS standard. Do not invent clause numbers. Keep it plain text.",
        "",
        "Gaps:",
    ]
    for g in result["gaps"][:top_n]:
        lines.append(f"- [{g['id']}] ({g['severity']}, {g['answer']}) {g['text']}")
    return "\n".join(lines)


def fallback_advice(result: dict, top_n: int = TOP_GAPS) -> str:
    return "\n".join(f"[{g['id']}] {g['fix']}" for g in result["gaps"][:top_n]) or "No gaps found."


def get_advice(site_name: str, result: dict) -> dict:
    if not result["gaps"]:
        return {"source": "none", "model": None, "advice": "No gaps found. Keep monitoring."}
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": build_prompt(site_name, result),
                  "stream": False, "options": {"temperature": 0.2}},
            timeout=180,
        )
        resp.raise_for_status()
        text = resp.json().get("response", "").strip()
        if text:
            return {"source": "ollama", "model": OLLAMA_MODEL, "advice": text}
    except (requests.RequestException, ValueError):
        pass
    return {"source": "fallback", "model": None, "advice": fallback_advice(result)}
