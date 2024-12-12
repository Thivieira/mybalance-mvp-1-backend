from pydantic import BaseModel, condecimal
from decimal import Decimal
from typing import List

class BalanceSchema(BaseModel):
    date: str
    income: condecimal(max_digits=10, decimal_places=2)
    expense: condecimal(max_digits=10, decimal_places=2)
    balance: condecimal(max_digits=10, decimal_places=2)

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v)
        }

class BalanceViewSchema(BalanceSchema):
    pass

class BalanceListResponse(BaseModel):
    balances: List[BalanceViewSchema]

class BalanceCurrentResponse(BaseModel):
    date: str
    income: float
    expense: float
    balance: float
