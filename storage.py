import sqlite3
from pathlib import Path
from models import JobPosting

DB_PATH = Path(__file__).parent / "data" / "jobs.db"


def init_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS seen_jobs (
            id TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            company TEXT,
            url TEXT,
            score INTEGER,
            seen_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn


def filter_new(conn: sqlite3.Connection, postings: list[JobPosting]) -> list[JobPosting]:
    new = []
    for p in postings:
        row = conn.execute("SELECT 1 FROM seen_jobs WHERE id = ?", (p.id,)).fetchone()
        if row is None:
            new.append(p)
    return new


def mark_seen(conn: sqlite3.Connection, posting: JobPosting, score: int) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO seen_jobs (id, source, title, company, url, score) VALUES (?, ?, ?, ?, ?, ?)",
        (posting.id, posting.source, posting.title, posting.company, posting.url, score),
    )
    conn.commit()
