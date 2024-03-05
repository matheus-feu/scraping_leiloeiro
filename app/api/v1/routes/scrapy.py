from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from app.schemas.scrapy_schema import ScrapyResponse
from app.services.scraping_service import ScrapingService

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, summary="Retorna JSON com todos os leiões de acordo com o estado")
async def scrapy(state: ScrapyResponse):
    """
    Retorna JSON com todos os leiões de acordo com o estado
    :param state:
    :return: Lista de dicionários com os dados dos leilões
    """
    if not state:
        raise HTTPException(status_code=400, detail="State is required")

    data = ScrapingService(
        state=state.state,
        order_by=state.order_by,
        headless=state.headless,
        selenoid=state.selenoid,
        host=state.host).run()

    print(data)
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    return data, status.HTTP_200_OK
