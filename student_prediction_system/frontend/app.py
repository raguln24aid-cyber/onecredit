"""Streamlit frontend. Talks to FastAPI via requests.

Backend URL: env BACKEND_URL, default http://localhost:8000
(In Docker Compose it is http://backend:8000)
"""
import os

import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Smart Student Prediction System",
                   page_icon="🎓", layout="wide")
st.title("🎓 Smart Student Performance & Placement Prediction System")

page = st.sidebar.radio("Go to", ["Dashboard", "Student Management",
                                  "Final Score Prediction",
                                  "Placement Prediction", "About"])


def get(path):
    r = requests.get(f"{BACKEND_URL}{path}", timeout=10)
    r.raise_for_status()
    return r.json()


def post(path, payload):
    r = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.header("📊 Dashboard")
    try:
        students = get("/students")
    except Exception as e:
        st.error(f"Cannot reach backend at {BACKEND_URL}. "
                 f"Start FastAPI first. Error: {e}")
        students = []

    if students:
        df = pd.DataFrame(students)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Students", len(df))
        if "final_score" in df.columns:
            c2.metric("Avg Final Score",
                      f"{df['final_score'].mean():.1f}")
        if "placed" in df.columns:
            c3.metric("Placement Rate",
                      f"{df['placed'].mean():.1%}")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No students yet. Add students from Student Management page.")


# ---------------- Student Management ----------------
elif page == "Student Management":
    st.header("👨‍🎓 Student Management")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["View All", "Add", "Search by ID", "Update", "Delete"])

    with tab1:
        if st.button("Load all students"):
            try:
                st.dataframe(pd.DataFrame(get("/students")),
                             use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.subheader("Add student")
        with st.form("add_form"):
            name = st.text_input("Name", "Arjun Sharma")
            age = st.number_input("Age", 15, 40, 20)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            c1, c2 = st.columns(2)
            study_hours = c1.number_input("Study hours/day", 0.0, 24.0, 6.0)
            attendance = c2.number_input("Attendance %", 0.0, 100.0, 80.0)
            internal_marks = c1.number_input("Internal marks", 0.0, 100.0, 70.0)
            assignment_score = c2.number_input("Assignment score", 0.0, 100.0, 75.0)
            prev = c1.number_input("Previous sem score", 0.0, 100.0, 72.0)
            final = c2.number_input("Final score", 0.0, 100.0, 0.0)
            cgpa = c1.number_input("CGPA", 0.0, 10.0, 7.5)
            aptitude = c2.number_input("Aptitude score", 0.0, 100.0, 70.0)
            technical = c1.number_input("Technical score", 0.0, 100.0, 72.0)
            comm = c2.number_input("Communication score", 0.0, 100.0, 68.0)
            internship = c1.selectbox("Internship", [0, 1])
            projects = c2.number_input("Projects", 0, 20, 2)
            placed = st.selectbox("Placed", [0, 1])
            if st.form_submit_button("Add"):
                payload = dict(name=name, age=age, gender=gender,
                               study_hours=study_hours, attendance=attendance,
                               internal_marks=internal_marks,
                               assignment_score=assignment_score,
                               previous_semester_score=prev,
                               final_score=final, cgpa=cgpa,
                               aptitude_score=aptitude,
                               technical_score=technical,
                               communication_score=comm,
                               internship=internship, projects=projects,
                               placed=placed)
                try:
                    st.success(post("/students", payload))
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab3:
        sid = st.number_input("Student ID", min_value=1, value=1, key="s1")
        if st.button("Search"):
            try:
                st.json(get(f"/students/{sid}"))
            except Exception as e:
                st.error(f"Error: {e}")

    with tab4:
        st.subheader("Update student (fill all fields)")
        uid = st.number_input("Student ID", min_value=1, value=1, key="u1")
        with st.form("upd_form"):
            name = st.text_input("Name", "Arjun Sharma", key="u_name")
            age = st.number_input("Age", 15, 40, 20, key="u_age")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                  key="u_gender")
            study_hours = st.number_input("Study hours/day", 0.0, 24.0, 6.0,
                                          key="u_sh")
            attendance = st.number_input("Attendance %", 0.0, 100.0, 80.0,
                                         key="u_att")
            internal_marks = st.number_input("Internal marks", 0.0, 100.0,
                                             70.0, key="u_int")
            assignment_score = st.number_input("Assignment score", 0.0, 100.0,
                                               75.0, key="u_asg")
            prev = st.number_input("Previous sem score", 0.0, 100.0, 72.0,
                                   key="u_prev")
            final = st.number_input("Final score", 0.0, 100.0, 0.0,
                                    key="u_final")
            cgpa = st.number_input("CGPA", 0.0, 10.0, 7.5, key="u_cgpa")
            aptitude = st.number_input("Aptitude score", 0.0, 100.0, 70.0,
                                       key="u_apt")
            technical = st.number_input("Technical score", 0.0, 100.0, 72.0,
                                        key="u_tech")
            comm = st.number_input("Communication score", 0.0, 100.0, 68.0,
                                   key="u_comm")
            internship = st.selectbox("Internship", [0, 1], key="u_intern")
            projects = st.number_input("Projects", 0, 20, 2, key="u_proj")
            placed = st.selectbox("Placed", [0, 1], key="u_placed")
            if st.form_submit_button("Update"):
                payload = dict(name=name, age=age, gender=gender,
                               study_hours=study_hours, attendance=attendance,
                               internal_marks=internal_marks,
                               assignment_score=assignment_score,
                               previous_semester_score=prev,
                               final_score=final, cgpa=cgpa,
                               aptitude_score=aptitude,
                               technical_score=technical,
                               communication_score=comm,
                               internship=internship, projects=projects,
                               placed=placed)
                try:
                    r = requests.put(f"{BACKEND_URL}/students/{uid}",
                                     json=payload, timeout=10)
                    r.raise_for_status()
                    st.success(r.json())
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab5:
        did = st.number_input("Student ID", min_value=1, value=1, key="d1")
        if st.button("Delete"):
            try:
                r = requests.delete(f"{BACKEND_URL}/students/{did}",
                                    timeout=10)
                r.raise_for_status()
                st.success(r.json())
            except Exception as e:
                st.error(f"Error: {e}")


# ---------------- Final Score Prediction ----------------
elif page == "Final Score Prediction":
    st.header("📝 Final Score Prediction (RandomForestRegressor)")
    study_hours = st.number_input("Study hours/day", 0.0, 24.0, 6.0)
    attendance = st.number_input("Attendance %", 0.0, 100.0, 80.0)
    internal_marks = st.number_input("Internal marks", 0.0, 100.0, 70.0)
    assignment_score = st.number_input("Assignment score", 0.0, 100.0, 75.0)
    prev = st.number_input("Previous sem score", 0.0, 100.0, 72.0)
    if st.button("Predict Final Score"):
        try:
            res = post("/predict/final-score", dict(
                study_hours=study_hours, attendance=attendance,
                internal_marks=internal_marks,
                assignment_score=assignment_score,
                previous_semester_score=prev))
            st.success(f"Predicted Final Score: "
                       f"{res['predicted_final_score']}")
        except Exception as e:
            st.error(f"Error: {e}")


# ---------------- Placement Prediction ----------------
elif page == "Placement Prediction":
    st.header("💼 Placement Prediction (RandomForestClassifier)")
    cgpa = st.number_input("CGPA", 0.0, 10.0, 7.5)
    attendance = st.number_input("Attendance %", 0.0, 100.0, 80.0, key="p_att")
    aptitude = st.number_input("Aptitude score", 0.0, 100.0, 70.0)
    technical = st.number_input("Technical score", 0.0, 100.0, 72.0)
    comm = st.number_input("Communication score", 0.0, 100.0, 68.0)
    internship = st.selectbox("Internship (0=No, 1=Yes)", [0, 1])
    projects = st.number_input("Projects", 0, 20, 2)
    if st.button("Predict Placement"):
        try:
            res = post("/predict/placement", dict(
                cgpa=cgpa, attendance=attendance, aptitude_score=aptitude,
                technical_score=technical, communication_score=comm,
                internship=internship, projects=projects))
            st.success(f"{res['result']} "
                       f"(probability: {res['probability']})")
        except Exception as e:
            st.error(f"Error: {e}")


# ---------------- About ----------------
else:
    st.header("ℹ️ About")
    st.write("""
    **Smart Student Performance & Placement Prediction System**
    (1-credit college project)

    - **Backend:** FastAPI + SQLite (CRUD + predictions)
    - **ML Model 1:** RandomForestRegressor → predicts final score
      from study hours, attendance, internal marks, assignment score,
      previous semester score.
    - **ML Model 2:** RandomForestClassifier → predicts placement
      from CGPA, attendance, aptitude, technical, communication,
      internship, projects.
    - **Frontend:** Streamlit dashboard calling FastAPI with `requests`.
    - **Dataset:** 500 synthetic records in `data/students.csv`.
    - **Docker:** separate backend & frontend containers,
      frontend uses `http://backend:8000`.
    """)
