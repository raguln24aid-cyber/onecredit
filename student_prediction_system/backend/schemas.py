"""Pydantic schemas for validation."""
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, examples=["Arjun Sharma"])
    age: int = Field(..., ge=15, le=40, examples=[20])
    gender: str = Field(..., examples=["Male"])
    study_hours: float = Field(..., ge=0, le=24, examples=[6.0])
    attendance: float = Field(..., ge=0, le=100, examples=[80.0])
    internal_marks: float = Field(..., ge=0, le=100, examples=[70.0])
    assignment_score: float = Field(..., ge=0, le=100, examples=[75.0])
    previous_semester_score: float = Field(..., ge=0, le=100, examples=[72.0])
    final_score: float = Field(default=0, ge=0, le=100)
    cgpa: float = Field(..., ge=0, le=10, examples=[7.5])
    aptitude_score: float = Field(..., ge=0, le=100, examples=[70.0])
    technical_score: float = Field(..., ge=0, le=100, examples=[72.0])
    communication_score: float = Field(..., ge=0, le=100, examples=[68.0])
    internship: int = Field(..., ge=0, le=1, examples=[1])
    projects: int = Field(..., ge=0, le=20, examples=[2])
    placed: int = Field(default=0, ge=0, le=1)


class StudentUpdate(StudentCreate):
    pass


class FinalScoreInput(BaseModel):
    study_hours: float = Field(..., ge=0, le=24)
    attendance: float = Field(..., ge=0, le=100)
    internal_marks: float = Field(..., ge=0, le=100)
    assignment_score: float = Field(..., ge=0, le=100)
    previous_semester_score: float = Field(..., ge=0, le=100)


class PlacementInput(BaseModel):
    cgpa: float = Field(..., ge=0, le=10)
    attendance: float = Field(..., ge=0, le=100)
    aptitude_score: float = Field(..., ge=0, le=100)
    technical_score: float = Field(..., ge=0, le=100)
    communication_score: float = Field(..., ge=0, le=100)
    internship: int = Field(..., ge=0, le=1)
    projects: int = Field(..., ge=0, le=20)
