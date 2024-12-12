from sqlalchemy.sql import func
from sqlalchemy.types import String
from models.transaction import Transaction
from models.balance_history import BalanceHistory
from datetime import date, datetime
from schemas.transaction import TransactionType
from decimal import Decimal

def calculate_balance(session):
    # Get all transactions ordered by date
    transactions = session.query(Transaction).order_by(Transaction.date).all()
    
    running_balance = Decimal('0')
    balance_records = {}
    
    # First, clear existing balance history
    session.query(BalanceHistory).delete()
    
    for transaction in transactions:
        amount = Decimal(str(transaction.amount))
        date_key = transaction.date
        
        if date_key not in balance_records:
            balance_records[date_key] = {
                'date': date_key,
                'income': Decimal('0'),
                'expense': Decimal('0'),
                'balance': Decimal('0')
            }
            
        if transaction.type == TransactionType.INCOME:
            running_balance += amount
            balance_records[date_key]['income'] += amount
        else:
            running_balance -= amount
            balance_records[date_key]['expense'] += amount
            
        balance_records[date_key]['balance'] = running_balance
    
    try:
        # Update balance history
        for date, record in balance_records.items():
            balance_history = BalanceHistory(
                date=date,
                income=str(record['income']),
                expense=str(record['expense']),
                balance=str(record['balance'])
            )
            session.add(balance_history)
            
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
