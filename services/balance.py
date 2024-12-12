from sqlalchemy.sql import func
from sqlalchemy.types import String
from models.transaction import Transaction
from models.balance_history import BalanceHistory
from datetime import date, datetime
from schemas.transaction import TransactionType
from decimal import Decimal

def calculate_balance(session):
    today = date.today()

    # Get all transactions grouped by date
    daily_totals = session.query(
        Transaction.date,
        func.sum(func.cast(Transaction.amount, String)).filter(Transaction.type == TransactionType.INCOME).label("total_income"),
        func.sum(func.cast(Transaction.amount, String)).filter(Transaction.type == TransactionType.EXPENSE).label("total_expense")
    ).group_by(Transaction.date).all()

    # Delete all existing balance history records
    session.query(BalanceHistory).delete()
    
    running_balance = Decimal('0')
    for day_total in daily_totals:
        day_date = day_total[0]
        day_income = Decimal(str(day_total[1] or '0'))
        day_expense = Decimal(str(day_total[2] or '0'))
        
        # Calculate running balance
        running_balance += (day_income - day_expense)
        
        # Create balance history record
        balance_history = BalanceHistory(
            date=day_date,
            income=day_income,
            expense=day_expense,
            balance=running_balance
        )
        session.add(balance_history)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
