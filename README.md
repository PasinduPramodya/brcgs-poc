# BRCGS Readiness Scorer (proof of concept)

An offline desktop tool that helps a food-manufacturing QA team prepare for a BRCGS
Global Standard for Food Safety audit. Built for IT6070 Assignment 02.

**Two connected features**

1. **Weighted scoring engine** – staff answer a questionnaire (Compliant / Partial /
   Non-compliant / N/A); the app calculates an overall and per-section readiness score and a
   readiness band. Any non-compliant *fundamental* item caps the band at "At risk".
2. **AI corrective-action advisor** – the biggest gaps from the score are sent to a local
   language model running in [Ollama](https://ollama.com), which writes practical corrective
   actions. If Ollama is not running, rule-based hints are used so the workflow still works.

Everything runs on one PC (FastAPI + SQLite + Ollama on `localhost`), so no audit data leaves the site.

> The questions in `app/questions.py` are short paraphrased examples, **not** the licensed BRCGS text,
> and the weights (fundamental 10, major 5, minor 2) and bands are this project's own assumptions, not an
> official BRCGS grade. Replace the list with the site's licensed clause list (~300 clauses) and have a
> QA specialist review AI advice before acting on it.

## Project layout

```
brcgs-poc/
├── app/
│   ├── main.py        # FastAPI routes + server start (python -m app.main)
│   ├── scoring.py     # weighted scoring engine
│   ├── questions.py   # sample questionnaire, sections, weights
│   ├── ai_advisor.py  # Ollama client + offline fallback
│   ├── database.py    # SQLite storage (data/brcgs.db)
│   └── static/index.html   # simple browser UI
├── tests/test_scoring.py
├── requirements.txt
└── .gitignore
```

## Run it (Windows, PowerShell, from the project folder, e.g. `e:\brcgs-poc`)

```powershell
# 1. Python environment (Python 3.10+)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Local AI (one-time): install Ollama from https://ollama.com, then
ollama pull llama3.2

# 3. Start the app (run as a module from the project root)
python -m app.main
```

Open **http://127.0.0.1:8000** in a browser, fill in the questionnaire, press
**Calculate score**, then **Get AI corrective-action advice**.

API docs are at http://127.0.0.1:8000/docs.

Use a different model or Ollama address:

```powershell
$env:OLLAMA_MODEL = "mistral"
$env:OLLAMA_URL   = "http://localhost:11434"
python -m app.main
```

Run the tests: `python -m pytest -q`

If PowerShell blocks the activate script, run
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

## Put it on GitHub

1. Install Git for Windows and set your identity once:
   ```powershell
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
2. On github.com click **New repository**, name it `brcgs-poc`, choose Private or Public, and
   leave "Add a README / .gitignore / licence" **unticked** (this project already has them). Click **Create repository**.
3. In the project folder:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: BRCGS readiness scorer proof of concept"
   git branch -M main
   git remote add origin https://github.com/<your-username>/brcgs-poc.git
   git push -u origin main
   ```
   GitHub asks you to sign in in the browser the first time (use a personal access token if it asks for a password).
4. Later changes: `git add .` → `git commit -m "message"` → `git push`.

`.gitignore` already keeps the virtual environment and the local database (`data/*.db`) out of the repository.
