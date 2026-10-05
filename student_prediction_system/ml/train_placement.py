"""Train RandomForestClassifier for placement prediction.

Run: python ml/train_placement.py
Input: data/students.csv
Output: models/placement_model.pkl
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

FEATURES = ["cgpa", "attendance", "aptitude_score", "technical_score",
            "communication_score", "internship", "projects"]
TARGET = "placed"


def main():
    base = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base / "data" / "students.csv")

    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"Accuracy:  {accuracy_score(y_test, preds):.4f}")
    print(f"Precision: {precision_score(y_test, preds):.4f}")
    print(f"Recall:    {recall_score(y_test, preds):.4f}")
    print(f"F1-score:  {f1_score(y_test, preds):.4f}")

    out = base / "models" / "placement_model.pkl"
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out)
    print(f"Saved model to {out}")


if __name__ == "__main__":
    main()
