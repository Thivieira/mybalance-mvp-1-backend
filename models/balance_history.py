from sqlalchemy import Column, String, Integer, Date, Float
from models import Base

# Balance History Table
class BalanceHistory(Base):
    __tablename__ = "balance_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)
    income = Column(Float, default=0.0, nullable=False)
    expense = Column(Float, default=0.0, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)

    def __init__(self, date, income, expense, balance):
        self.date = date
        self.income = income
        self.expense = expense
        self.balance = balance
