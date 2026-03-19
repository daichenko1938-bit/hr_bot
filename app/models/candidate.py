from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Candidate(BaseModel):
    id: int
    full_name: str
    phone: str
    city: str
    profession: str
    category: str
    experience_years: float
    skills: List[str] = Field(default_factory=list)
    salary_expectation: Optional[int] = None
    employment_type: Optional[str] = None
    schedule_preference: Optional[str] = None
    resume_text: Optional[str] = None
    source: str = "manual"
    created_at: datetime


class CandidateCreate(BaseModel):
    full_name: str
    phone: str
    city: str
    profession: str
    category: str
    experience_years: float
    skills: List[str] = Field(default_factory=list)
    salary_expectation: Optional[int] = None
    employment_type: Optional[str] = None
    schedule_preference: Optional[str] = None
    resume_text: Optional[str] = None
    source: str = "manual"