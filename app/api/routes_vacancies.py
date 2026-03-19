from datetime import datetime
from fastapi import APIRouter

from app.database.db import VACANCIES
from app.models.vacancy import Vacancy, VacancyCreate

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.post("/")
def create_vacancy(data: VacancyCreate):
    vacancy = Vacancy(
        id=len(VACANCIES) + 1,
        employer_id=data.employer_id,
        title=data.title,
        category=data.category,
        city=data.city,
        experience_min=data.experience_min,
        schedule=data.schedule,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        employment_type=data.employment_type,
        description=data.description,
        status="open",
        created_at=datetime.utcnow(),
    )

    VACANCIES.append(vacancy)

    result = vacancy.dict()
    result["created_at"] = vacancy.created_at.isoformat()
    return result


@router.get("/")
def list_vacancies():
    response = []
    for vacancy in VACANCIES:
        item = vacancy.dict()
        item["created_at"] = vacancy.created_at.isoformat()
        response.append(item)
    return response