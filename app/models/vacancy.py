from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Vacancy(BaseModel):
    id: int
    employer_id: int
    title: str
    category: str
    city: str
    experience_min: float
    schedule: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    status: str = "open"
    created_at: datetime


class VacancyCreate(BaseModel):
    employer_id: int
    title: str
    category: str
    city: str
    experience_min: float
    schedule: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None