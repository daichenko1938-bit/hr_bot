from fastapi import APIRouter, HTTPException

from app.database.db import VACANCIES, CANDIDATES
from app.core.matcher import match_many_candidates_to_vacancy

router = APIRouter(prefix="/match", tags=["Match"])


@router.get("/{vacancy_id}")
def match_by_vacancy(vacancy_id: int):
    vacancy = next((item for item in VACANCIES if item.id == vacancy_id), None)

    if vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    results = match_many_candidates_to_vacancy(vacancy, CANDIDATES)

    response = []
    for item in results:
        row = item.dict()
        row["created_at"] = item.created_at.isoformat()
        response.append(row)

    return response