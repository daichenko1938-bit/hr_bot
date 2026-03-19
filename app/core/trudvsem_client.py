import httpx
from typing import Any


TRUDVSEM_API = "http://opendata.trudvsem.ru/api/v1"


class TrudvsemClient:
    async def search_vacancies(
        self,
        text: str,
        limit: int = 20,
        offset: int = 0,
        region_code: str | None = None,
    ) -> list[dict[str, Any]]:
        if region_code:
            url = f"{TRUDVSEM_API}/vacancies/region/{region_code}"
        else:
            url = f"{TRUDVSEM_API}/vacancies"

        params = {
            "text": text,
            "limit": limit,
            "offset": offset,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        results = data.get("results", {})
        vacancies = results.get("vacancies", [])
        return vacancies