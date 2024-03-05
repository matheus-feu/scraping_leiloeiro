from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator


class ScrapyResponse(BaseModel):
    state: str = Field('sp')
    order_by: str = Field('padrao')
    headless: Optional[bool] = Field(True)
    selenoid: Optional[bool] = Field(False)
    host: Optional[str] = Field('localhost')

    class Config:
        from_attributes = True

    @validator('state', always=True, pre=True)
    def validate_state(cls, state: str) -> str:
        """
        Valida se o estado fornecido é válido na lista de estados aceitos.
        """
        valid_states = ["ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe",
                        "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to"]
        if state.lower() in valid_states:
            return state.lower()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Estado inválido')

    @validator('order_by', always=True, pre=True)
    def validate_order_by(cls, order_by: str) -> str:
        """
        Valida se o order_by fornecido é válido na lista de order_by aceitos.
        """
        valid_order_by = ["padrao", "menor_preco", "maior_preco", "popularidade"]
        if order_by.lower() in valid_order_by:
            return order_by.lower()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Order_by inválido')

    @validator('selenoid', always=True, pre=True)
    def validate_selenoid(cls, selenoid: bool) -> bool:
        """
        Valida se for selenoid, solicitar o host.
        """
        if selenoid:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Selenoid requer host')
        return selenoid
