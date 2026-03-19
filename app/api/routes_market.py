from fastapi import APIRouter, Query

from app.core.trudvsem_client import TrudvsemClient

router = APIRouter(prefix="/market", tags=["market"])
client = TrudvsemClient()


@router.get("/vacancies")
async def market_vacancies(
    text: str = Query(..., description="Поисковый текст"),
    region_code: str | None = Query(None, description="Код региона"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    vacancies = await client.search_vacancies(
        text=text,
        region_code=region_code,
        limit=limit,
        offset=offset,
    )
    return {
        "count": len(vacancies),
        "items": vacancies,
    }