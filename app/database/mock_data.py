from datetime import datetime

from app.models.vacancy import Vacancy
from app.models.candidate import Candidate


def get_test_vacancy() -> Vacancy:
    return Vacancy(
        id=1,
        employer_id=101,
        title="Продавец",
        category="sales",
        city="Орёл",
        experience_min=1,
        schedule="2/2",
        salary_min=40000,
        salary_max=50000,
        employment_type="full_time",
        description="Нужен продавец в магазин",
        status="open",
        created_at=datetime.utcnow(),
    )


def get_test_candidates() -> list[Candidate]:
    return [
        Candidate(
            id=501,
            full_name="Иван Петров",
            phone="+79990000000",
            city="Орел",
            profession="Продавец-консультант",
            category="sales",
            experience_years=3,
            skills=["касса", "консультирование", "продажи"],
            salary_expectation=45000,
            employment_type="full_time",
            schedule_preference="2/2",
            resume_text="Опыт работы продавцом 3 года",
            source="manual",
            created_at=datetime.utcnow(),
        ),
        Candidate(
            id=502,
            full_name="Анна Смирнова",
            phone="+79990000001",
            city="Орёл",
            profession="Продавец",
            category="sales",
            experience_years=1,
            skills=["продажи", "касса"],
            salary_expectation=50000,
            employment_type="full_time",
            schedule_preference="2/2",
            resume_text="Опыт работы продавцом 1 год",
            source="manual",
            created_at=datetime.utcnow(),
        ),
        Candidate(
            id=503,
            full_name="Сергей Волков",
            phone="+79990000002",
            city="Брянск",
            profession="Кладовщик",
            category="warehouse",
            experience_years=2,
            skills=["склад", "приемка товара"],
            salary_expectation=48000,
            employment_type="full_time",
            schedule_preference="5/2",
            resume_text="Опыт работы кладовщиком 2 года",
            source="manual",
            created_at=datetime.utcnow(),
        ),
    ]