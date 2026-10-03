"""Tiny SQLite store so assessments survive restarts (no server, works offline)."""

import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.environ.get("BRCGS_DB", os.path.join("data", "brcgs.db"))


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS assessments (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   site_name TEXT NOT NULL,
                   created_at TEXT NOT NULL,
                   score REAL NOT NULL,
                   band TEXT NOT NULL,
                   result_json TEXT NOT NULL,
                   advice_json TEXT
               )"""
        )


def save_assessment(site_name: str, result: dict) -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO assessments (site_name, created_at, score, band, result_json) "
            "VALUES (?, ?, ?, ?, ?)",
            (site_name, datetime.now(timezone.utc).isoformat(timespec="seconds"),
             result["score"], result["band"], json.dumps(result)),
        )
        return cur.lastrowid


def get_assessment(assessment_id: int):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,)).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"], "site_name": row["site_name"], "created_at": row["created_at"],
        "score": row["score"], "band": row["band"],
        "result": json.loads(row["result_json"]),
        "advice": json.loads(row["advice_json"]) if row["advice_json"] else None,
    }


def list_assessments():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, site_name, created_at, score, band FROM assessments ORDER BY id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def save_advice(assessment_id: int, advice: dict) -> None:
    with _connect() as conn:
        conn.execute("UPDATE assessments SET advice_json = ? WHERE id = ?",
                     (json.dumps(advice), assessment_id))
