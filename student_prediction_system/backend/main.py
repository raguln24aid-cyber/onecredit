"""FastAPI backend: Student CRUD + 2 ML prediction endpoints."""
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException

from .database import get_connection, init_db
from .schemas import FinalScoreInput, PlacementInput, StudentCreate, StudentUpdate

app = FastAPI(title="Smart Student Performance & Placement Prediction System")

BASE_DIR = Path(__file__).resolve().parent.parent
FINAL_SCORE_MODEL_PATH = BASE_DIR / "models" / "final_score_model.pkl"
PLACEMENT_MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"

final_score_model = None
placement_model = None


def row_to_dict(row):
    return dict(row) if row else None


@app.on_event("startup")
def startup():
    init_db()
    global final_score_model, placement_model
    if FINAL_SCORE_MODEL_PATH.exists():
        final_score_model = joblib.load(FINAL_SCORE_MODEL_PATH)
    if PLACEMENT_MODEL_PATH.exists():
        placement_model = joblib.load(PLACEMENT_MODEL_PATH)


@app.get("/")
def root():
    return {"message": "Student Prediction API is running. See /docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- CRUD ----------------

@app.post("/students", status_code=201)
def add_student(student: StudentCreate):
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO students
        (name, age, gender, study_hours, attendance, internal_marks,
         assignment_score, previous_semester_score, final_score, cgpa,
         aptitude_score, technical_score, communication_score,
         internship, projects, placed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (student.name, student.age, student.gender, student.study_hours,
         student.attendance, student.internal_marks, student.assignment_score,
         student.previous_semester_score, student.final_score, student.cgpa,
         student.aptitude_score, student.technical_score,
         student.communication_score, student.internship,
         student.projects, student.placed),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, **student.model_dump()}


@app.get("/students")
def view_all_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


@app.get("/students/{student_id}")
def search_student(student_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?",
                       (student_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return row_to_dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?",
                       (student_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.execute(
        """UPDATE students SET name=?, age=?, gender=?, study_hours=?,
        attendance=?, internal_marks=?, assignment_score=?,
        previous_semester_score=?, final_score=?, cgpa=?, aptitude_score=?,
        technical_score=?, communication_score=?, internship=?, projects=?,
        placed=? WHERE id=?""",
        (student.name, student.age, student.gender, student.study_hours,
         student.attendance, student.internal_marks, student.assignment_score,
         student.previous_semester_score, student.final_score, student.cgpa,
         student.aptitude_score, student.technical_score,
         student.communication_score, student.internship,
         student.projects, student.placed, student_id),
    )
    conn.commit()
    conn.close()
    return {"id": student_id, **student.model_dump()}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?",
                       (student_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"message": f"Student {student_id} deleted"}


# ---------------- ML predictions ----------------

@app.post("/predict/final-score")
def predict_final_score(data: FinalScoreInput):
    global final_score_model
    if final_score_model is None:
        if FINAL_SCORE_MODEL_PATH.exists():
            final_score_model = joblib.load(FINAL_SCORE_MODEL_PATH)
        else:
            raise HTTPException(status_code=500,
                                detail="Final score model not found")
    features = [[data.study_hours, data.attendance, data.internal_marks,
                 data.assignment_score, data.previous_semester_score]]
    pred = float(final_score_model.predict(features)[0])
    return {"predicted_final_score": round(pred, 2)}


@app.post("/predict/placement")
def predict_placement(data: PlacementInput):
    global placement_model
    if placement_model is None:
        if PLACEMENT_MODEL_PATH.exists():
            placement_model = joblib.load(PLACEMENT_MODEL_PATH)
        else:
            raise HTTPException(status_code=500,
                                detail="Placement model not found")
    features = [[data.cgpa, data.attendance, data.aptitude_score,
                 data.technical_score, data.communication_score,
                 data.internship, data.projects]]
    pred = int(placement_model.predict(features)[0])
    proba = float(placement_model.predict_proba(features)[0][1])
    return {
        "placed": pred,
        "result": "Placed" if pred == 1 else "Not Placed",
        "probability": round(proba, 4),
    }
