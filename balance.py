from sqlalchemy.sql import func
from models.transaction import Transaction
from models.balance_history import BalanceHistory
from datetime import date
from schemas.transaction import TransactionType

def calculate_balance(session):
    today = date.today()

    # Get today's income and expenses
    totals = session.query(
        func.sum(Transaction.amount).filter(Transaction.type == TransactionType.INCOME).label("total_income"),
        func.sum(Transaction.amount).filter(Transaction.type == TransactionType.EXPENSE).label("total_expense"),
    ).filter(Transaction.date == today).one()

    total_income = totals.total_income or 0.0
    total_expense = totals.total_expense or 0.0
    balance = total_income - total_expense

    # Check if there's an existing record for today
    existing_record = session.query(BalanceHistory).filter(BalanceHistory.date == today).first()

    if existing_record:
        # Update existing record
        existing_record.income = total_income
        existing_record.expense = total_expense
        existing_record.balance = balance
    else:
        # Create new record
        balance_history = BalanceHistory(
            date=today,
            income=total_income,
            expense=total_expense,
            balance=balance
        )
        session.add(balance_history)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
