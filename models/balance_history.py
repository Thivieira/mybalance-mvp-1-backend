from sqlalchemy import Column, String, Integer, Date
from decimal import Decimal
from models import Base

# Balance History Table
class BalanceHistory(Base):
    __tablename__ = "balance_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    income = Column(String(20), default='0', nullable=False)
    expense = Column(String(20), default='0', nullable=False)
    balance = Column(String(20), default='0', nullable=False)

    def __init__(self, date, balance, income='0', expense='0'):
        self.date = date
        self.balance = str(Decimal(str(balance)))
        self.income = str(Decimal(str(income)))
        self.expense = str(Decimal(str(expense)))

    def get_balance(self):
        return Decimal(self.balance)
