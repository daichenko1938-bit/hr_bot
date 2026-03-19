from datetime import datetime
from fastapi import APIRouter

from app.database.db import CANDIDATES
from app.models.candidate import Candidate, CandidateCreate

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post("/")
def create_candidate(data: CandidateCreate):
    candidate = Candidate(
        id=len(CANDIDATES) + 1,
        full_name=data.full_name,
        phone=data.phone,
        city=data.city,
        profession=data.profession,
        category=data.category,
        experience_years=data.experience_years,
        skills=data.skills,
        salary_expectation=data.salary_expectation,
        employment_type=data.employment_type,
        schedule_preference=data.schedule_preference,
        resume_text=data.resume_text,
        source=data.source,
        created_at=datetime.utcnow(),
    )

    CANDIDATES.append(candidate)

    result = candidate.dict()
    result["created_at"] = candidate.created_at.isoformat()
    return result


@router.get("/")
def list_candidates():
    response = []
    for candidate in CANDIDATES:
        item = candidate.dict()
        item["created_at"] = candidate.created_at.isoformat()
        response.append(item)
    return response