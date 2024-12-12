from pydantic import BaseModel

class BalanceSchema(BaseModel):
    date: str
    income: float
    expense: float
    balance: float


class BalanceViewSchema(BaseModel):
    date: str
    income: float
    expense: float
    balance: float
