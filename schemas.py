from datetime import date
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

class SpentBase(BaseModel):
    name: str
    content: str
    category: str
    recurring: bool = False
    installment_debt: Optional[int] = None
    purchase_date: date = Field(default_factory=date.today)  # Data da compra, padrão: hoje
    amount: float = Field(gt=0, description="Valor da compra")  # Valor da compra, deve ser maior que 0
    model_config = ConfigDict(from_attributes=True)

class NumberBase(BaseModel):
    name: str
    number: str
    status: bool = True
    model_config = ConfigDict(from_attributes=True)

class SpentRequest(SpentBase):
    ...

class SpentResponse(SpentBase):
    id: int


class NumberRequest(NumberBase):
    ...

class NumberResponse(NumberBase):
    id: int
