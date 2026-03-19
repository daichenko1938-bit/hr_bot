from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class MatchResult(BaseModel):
    id: int
    vacancy_id: int
    candidate_id: int
    score: int
    profession_score: int = 0
    city_score: int = 0
    experience_score: int = 0
    salary_score: int = 0
    schedule_score: int = 0
    match_reasons: List[str] = Field(default_factory=list)
    status: str
    created_at: datetime