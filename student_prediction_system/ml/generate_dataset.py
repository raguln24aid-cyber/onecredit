"""Generate a realistic students.csv with 500 records.

Run: python ml/generate_dataset.py
Output: data/students.csv
"""
import random
from pathlib import Path

import numpy as np
import pandas as pd

NUM_RECORDS = 500
RANDOM_SEED = 42

FIRST_NAMES = ["Aarav", "Diya", "Arjun", "Ananya", "Vikram", "Priya", "Rahul",
               "Sneha", "Karthik", "Meera", "Aditya", "Kavya", "Rohan", "Pooja",
               "Suresh", "Divya", "Manoj", "Lakshmi", "Nikhil", "Anitha"]
LAST_NAMES = ["Sharma", "Iyer", "Khan", "Patel", "Reddy", "Nair", "Gupta",
              "Singh", "Das", "Kumar", "Menon", "Rao", "Verma", "Joshi"]


def main():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    rows = []
    for i in range(1, NUM_RECORDS + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        age = int(np.random.randint(18, 24))
        gender = random.choice(["Male", "Female"])

        study_hours = round(float(np.clip(np.random.normal(5.5, 2.0), 1, 12)), 1)
        attendance = round(float(np.clip(np.random.normal(75, 12), 35, 100)), 1)
        internal_marks = round(float(np.clip(np.random.normal(65, 15), 0, 100)), 1)
        assignment_score = round(float(np.clip(np.random.normal(68, 14), 0, 100)), 1)
        previous_semester_score = round(float(np.clip(np.random.normal(66, 14), 0, 100)), 1)

        # Final score: weighted combination + noise (realistic correlation)
        final_score = (
            0.25 * internal_marks
            + 0.20 * assignment_score
            + 0.25 * previous_semester_score
            + 1.5 * study_hours
            + 0.15 * attendance
            + np.random.normal(0, 4)
        )
        final_score = round(float(np.clip(final_score, 0, 100)), 1)

        # CGPA correlated with academic scores
        cgpa = round(float(np.clip((final_score / 10) + np.random.normal(0, 0.4), 0, 10)), 2)

        aptitude_score = round(float(np.clip(np.random.normal(65, 15), 0, 100)), 1)
        technical_score = round(float(np.clip(np.random.normal(64, 16), 0, 100)), 1)
        communication_score = round(float(np.clip(np.random.normal(66, 14), 0, 100)), 1)
        internship = int(np.random.choice([0, 1], p=[0.55, 0.45]))
        projects = int(np.clip(np.random.poisson(2), 0, 5))

        # Placement probability: simple realistic scoring rule + noise
        score = (
            (cgpa / 10) * 0.30
            + (aptitude_score / 100) * 0.20
            + (technical_score / 100) * 0.25
            + (communication_score / 100) * 0.10
            + (attendance / 100) * 0.05
            + internship * 0.05
            + (projects / 5) * 0.05
            + np.random.normal(0, 0.05)
        )
        placed = 1 if score > 0.60 else 0

        rows.append({
            "id": i,
            "name": name,
            "age": age,
            "gender": gender,
            "study_hours": study_hours,
            "attendance": attendance,
            "internal_marks": internal_marks,
            "assignment_score": assignment_score,
            "previous_semester_score": previous_semester_score,
            "final_score": final_score,
            "cgpa": cgpa,
            "aptitude_score": aptitude_score,
            "technical_score": technical_score,
            "communication_score": communication_score,
            "internship": internship,
            "projects": projects,
            "placed": placed,
        })

    df = pd.DataFrame(rows)
    out_path = Path(__file__).resolve().parent.parent / "data" / "students.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} records to {out_path}")
    print(df.head(3).to_string(index=False))
    print(f"Placement rate: {df['placed'].mean():.2%}")


if __name__ == "__main__":
    main()
