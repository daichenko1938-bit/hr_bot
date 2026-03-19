from fastapi import FastAPI

from app.api.routes_vacancies import router as vacancies_router
from app.api.routes_candidates import router as candidates_router
from app.api.routes_match import router as match_router
from app.api.routes_market import router as market_router


app = FastAPI(
    title="HR Core",
    description="MVP HR-бота для подбора сотрудников",
    version="0.5.0"
)


@app.get("/")
def root():
    return {"message": "HR Core MVP is running"}


app.include_router(vacancies_router)
app.include_router(candidates_router)
app.include_router(match_router)
app.include_router(market_router)