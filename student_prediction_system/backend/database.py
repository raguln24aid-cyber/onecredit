"""SQLite helper. Creates database/database/students.db on first run."""
import sqlite3
from pathlib import Path

# backend/database.py -> project root / database / students.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "students.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            study_hours REAL NOT NULL,
            attendance REAL NOT NULL,
            internal_marks REAL NOT NULL,
            assignment_score REAL NOT NULL,
            previous_semester_score REAL NOT NULL,
            final_score REAL DEFAULT 0,
            cgpa REAL NOT NULL,
            aptitude_score REAL NOT NULL,
            technical_score REAL NOT NULL,
            communication_score REAL NOT NULL,
            internship INTEGER NOT NULL,
            projects INTEGER NOT NULL,
            placed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
