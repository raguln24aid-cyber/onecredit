# Smart Student Performance & Placement Prediction System

1-credit college project using **Python, FastAPI, Streamlit, Scikit-learn, SQLite, Docker**.

## Project Structure

```text
student_prediction_system/
├── backend/            # FastAPI app
│   ├── main.py         # CRUD + /predict/* endpoints
│   ├── database.py     # SQLite helper
│   ├── schemas.py      # Pydantic validation
│   └── requirements.txt
├── frontend/           # Streamlit app
│   ├── app.py          # Dashboard, CRUD, predictions, About (uses requests)
│   └── requirements.txt
├── ml/                 # Dataset + training scripts
│   ├── generate_dataset.py
│   ├── train_final_score.py
│   └── train_placement.py
├── data/students.csv   # 500 synthetic records
├── models/             # Saved .pkl models
│   ├── final_score_model.pkl
│   └── placement_model.pkl
├── database/           # SQLite file created at runtime (students.db)
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── .gitignore
└── README.md
```

## ML Algorithms

| Task | Model | Inputs | Output | Metrics (tested) |
|---|---|---|---|---|
| Final score | `RandomForestRegressor` (100 trees) | study_hours, attendance, internal_marks, assignment_score, previous_semester_score | predicted final score (0–100) | MAE 4.80, RMSE 5.73, R² 0.57 |
| Placement | `RandomForestClassifier` (100 trees) | cgpa, attendance, aptitude_score, technical_score, communication_score, internship, projects | Placed / Not Placed + probability | Accuracy 0.83, Precision 0.87, Recall 0.88, F1 0.87 |

## API Endpoints (http://localhost:8000)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/students` | Add student |
| GET | `/students` | View all students |
| GET | `/students/{id}` | Search by ID |
| PUT | `/students/{id}` | Update student |
| DELETE | `/students/{id}` | Delete student |
| POST | `/predict/final-score` | Predict final score |
| POST | `/predict/placement` | Predict placement + probability |

Swagger docs: http://localhost:8000/docs

## Run Commands (local, without Docker)

```bash
cd student_prediction_system

# 1. Install deps
pip install -r ml/requirements.txt
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 2. Generate dataset (500 records)
python ml/generate_dataset.py

# 3. Train models
python ml/train_final_score.py
python ml/train_placement.py

# 4. Run backend (terminal 1)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# 5. Run frontend (terminal 2)
streamlit run frontend/app.py
```

Open: backend http://localhost:8000/docs, frontend http://localhost:8501

## Docker Commands

```bash
cd student_prediction_system

# Build + start both containers
docker compose up --build -d

# Check status / logs
docker compose ps
docker compose logs backend
docker compose logs frontend

# Test
curl http://localhost:8000/health
# frontend -> backend via service name (inside frontend container):
docker compose exec frontend python -c "import requests,os; print(requests.get(os.getenv('BACKEND_URL')+'/health').json())"

# Stop
docker compose down
```

Frontend uses `BACKEND_URL=http://backend:8000` (Docker service name),
set in `docker-compose.yml`. Locally it defaults to `http://localhost:8000`.

## Viva Explanation (short)

> This system stores student academic records in SQLite and exposes
> them through FastAPI REST APIs with Pydantic validation.
> Two Random Forest models are trained on a 500-record synthetic dataset:
> a regressor predicts the final exam score from study habits and past
> marks, and a classifier predicts placement from CGPA, skills,
> internship and projects, with a probability.
> The Streamlit frontend calls the FastAPI backend using `requests`
> for the dashboard, CRUD, and both predictions.
> Everything runs in two Docker containers (backend:8000, frontend:8501)
> orchestrated by Docker Compose, with the frontend reaching the backend
> via the service name `http://backend:8000`.
