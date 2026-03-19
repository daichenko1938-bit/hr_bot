from datetime import datetime
from typing import List

from app.models.match_result import MatchResult
from app.models.vacancy import Vacancy
from app.models.candidate import Candidate
from app.core.scoring import calculate_candidate_score


def match_candidate_to_vacancy(
    vacancy: Vacancy,
    candidate: Candidate,
    match_id: int = 1
) -> MatchResult:
    """
    Сопоставляет одного кандидата с одной вакансией
    и возвращает готовый MatchResult.
    """
    result = calculate_candidate_score(vacancy, candidate)

    return MatchResult(
        id=match_id,
        vacancy_id=vacancy.id,
        candidate_id=candidate.id,
        score=result["score"],
        profession_score=result["profession_score"],
        city_score=result["city_score"],
        experience_score=result["experience_score"],
        salary_score=result["salary_score"],
        schedule_score=result["schedule_score"],
        match_reasons=result["match_reasons"],
        status=result["status"],
        created_at=datetime.utcnow(),
    )


def match_many_candidates_to_vacancy(
    vacancy: Vacancy,
    candidates: List[Candidate]
) -> List[MatchResult]:
    """
    Сопоставляет одну вакансию со списком кандидатов,
    сортирует результаты по score от большего к меньшему.
    """
    results = []

    for index, candidate in enumerate(candidates, start=1):
        match_result = match_candidate_to_vacancy(
            vacancy=vacancy,
            candidate=candidate,
            match_id=index
        )
        results.append(match_result)

    results.sort(key=lambda item: item.score, reverse=True)
    return results