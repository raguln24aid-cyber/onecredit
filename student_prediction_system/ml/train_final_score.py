"""Train RandomForestRegressor for final score prediction.

Run: python ml/train_final_score.py
Input: data/students.csv
Output: models/final_score_model.pkl
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

FEATURES = ["study_hours", "attendance", "internal_marks",
            "assignment_score", "previous_semester_score"]
TARGET = "final_score"


def main():
    base = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base / "data" / "students.csv")

    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds) ** 0.5
    r2 = r2_score(y_test, preds)

    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.4f}")

    out = base / "models" / "final_score_model.pkl"
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out)
    print(f"Saved model to {out}")


if __name__ == "__main__":
    main()
