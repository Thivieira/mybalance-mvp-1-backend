from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from models import Session, BalanceHistory
from schemas import BalanceSchema, BalanceViewSchema
from datetime import datetime

balance_tag = Tag(name='Balance', description="Balance history operations")
balance_routes = APIBlueprint('balance', __name__, url_prefix='/balance', abp_tags=[balance_tag])

@balance_routes.get('/')
def get_balance_history():
    """Get balance history"""
    session = Session()
    try:
        history = session.query(BalanceHistory).all()
        
        result = []
        for record in history:
            result.append({
                "date": record.date.strftime('%Y-%m-%d'),
                "income": record.income,
                "expense": record.expense,
                "balance": record.balance
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return {"message": "Error fetching balance history"}, 400
    
    finally:
        session.close()

@balance_routes.get('/current')
def get_current_balance():
    """Get current day's balance"""
    session = Session()
    try:
        today = datetime.now().date()
        record = session.query(BalanceHistory).filter(
            BalanceHistory.date == today
        ).first()
        
        if not record:
            return {"message": "No balance record for today"}, 404
            
        result = {
            "date": record.date.strftime('%Y-%m-%d'),
            "income": record.income,
            "expense": record.expense,
            "balance": record.balance
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return {"message": "Error fetching current balance"}, 400
    
    finally:
        session.close()
        
@balance_routes.post('/')
def add_balance_history():
    """Add a new balance history record"""
    session = Session()
    try:
        data = request.get_json()
        
        # Create new balance history record
        balance_record = BalanceHistory(
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            income=data['income'],
            expense=data['expense'],
            balance=data['balance']
        )
        
        # Use merge instead of add to handle existing records
        balance_record = session.merge(balance_record)
        session.commit()
        
        result = {
            "date": balance_record.date.strftime('%Y-%m-%d'),
            "income": balance_record.income,
            "expense": balance_record.expense,
            "balance": balance_record.balance
        }
        
        return jsonify(result), 201
        
    except Exception as e:
        session.rollback()
        return {"message": f"Error adding balance history record: {str(e)}"}, 400
    
    finally:
        session.close()