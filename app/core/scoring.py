from app.models.vacancy import Vacancy
from app.models.candidate import Candidate
from app.core.normalizer import normalize_city, normalize_profession


def calculate_candidate_score(vacancy: Vacancy, candidate: Candidate) -> dict:
    score = 0
    reasons = []

    profession_score = 0
    city_score = 0
    experience_score = 0
    salary_score = 0
    schedule_score = 0

    vacancy_profession = normalize_profession(vacancy.title)
    candidate_profession = normalize_profession(candidate.profession)

    if vacancy_profession == candidate_profession:
        profession_score = 40
        reasons.append("Profession matches")
    elif vacancy_profession in candidate_profession or candidate_profession in vacancy_profession:
        profession_score = 25
        reasons.append("Profession partially matches")

    vacancy_city = normalize_city(vacancy.city)
    candidate_city = normalize_city(candidate.city)

    if vacancy_city == candidate_city:
        city_score = 20
        reasons.append("City matches")

    if candidate.experience_years >= vacancy.experience_min:
        experience_score = 20
        reasons.append("Experience meets requirements")
    elif candidate.experience_years >= max(vacancy.experience_min - 1, 0):
        experience_score = 10
        reasons.append("Experience is close to requirements")

    if vacancy.salary_max and candidate.salary_expectation:
        if candidate.salary_expectation <= vacancy.salary_max:
            salary_score = 10
            reasons.append("Salary expectation fits budget")
        elif candidate.salary_expectation <= vacancy.salary_max * 1.1:
            salary_score = 5
            reasons.append("Salary expectation is slightly above budget")

    if vacancy.schedule and candidate.schedule_preference:
        if vacancy.schedule.strip().lower() == candidate.schedule_preference.strip().lower():
            schedule_score = 10
            reasons.append("Work schedule matches")

    score = (
        profession_score
        + city_score
        + experience_score
        + salary_score
        + schedule_score
    )

    if score >= 80:
        status = "recommended"
    elif score >= 60:
        status = "possible"
    else:
        status = "rejected"

    return {
        "score": score,
        "profession_score": profession_score,
        "city_score": city_score,
        "experience_score": experience_score,
        "salary_score": salary_score,
        "schedule_score": schedule_score,
        "match_reasons": reasons,
        "status": status,
    }