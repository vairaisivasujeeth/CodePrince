"""Pydantic request schemas used by the API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Credentials(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    registration_number: str | None = Field(default=None, max_length=64)


class TestIn(BaseModel):
    input: str = Field(max_length=10000)
    expected_output: str = Field(max_length=10000)
    is_hidden: bool = False


class QuestionIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    statement: str = Field(min_length=3)
    difficulty: Literal["Easy", "Medium", "Hard"] = "Easy"
    topic: str = "Arrays"
    tags: list[str] = []
    constraints: str = ""
    input_format: str = ""
    output_format: str = ""
    hints: str = ""
    editorial: str = ""
    starter_code: dict[str, str] = {}
    published: bool = False
    tests: list[TestIn] = []


class SheetIn(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str = ""
    is_public: bool = False
    target_date: str = ""


class ExecuteIn(BaseModel):
    question_id: int
    language: Literal["c", "cpp", "java", "python", "go"]
    source: str = Field(min_length=1, max_length=100000)
    input: str | None = None


class ProgressIn(BaseModel):
    bookmarked: bool | None = None
    notes: str | None = Field(default=None, max_length=10000)
    confidence: int | None = Field(default=None, ge=0, le=5)
    revision_due: datetime | None = None


class AccountIn(Credentials):
    role: Literal["admin", "faculty", "student"] = "student"


class CourseIn(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    code: str = Field(min_length=2, max_length=40)
    description: str = ""
    faculty_id: int | None = None


class AssessmentIn(BaseModel):
    course_id: int
    title: str = Field(min_length=2, max_length=160)
    description: str = ""
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    question_ids: list[int] = []
