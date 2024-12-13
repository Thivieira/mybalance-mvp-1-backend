from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from models import Session, BalanceHistory
from schemas import (
    BalanceSchema, BalanceViewSchema, ErrorSchema, BalanceListResponse,
    BalanceCurrentResponse
)
from datetime import datetime
from services.balance import calculate_balance

balance_tag = Tag(name='Balance', description="Operações de histórico de saldo")
balance_routes = APIBlueprint('balance', __name__, url_prefix='/balance', abp_tags=[balance_tag])

@balance_routes.get('/', responses={"200": BalanceListResponse, "400": ErrorSchema})
def get_balance_history():
    """Listar todo histórico de saldo
    
    Este endpoint permite aos usuários recuperar todo o histórico de saldo existente.
    """
    session = Session()
    try:
        with session.begin():
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
        return {"message": f"Erro ao recuperar o histórico de saldo: {str(e)}"}, 400
    
    finally:
        session.close()

@balance_routes.get('/current', responses={"200": BalanceCurrentResponse, "404": ErrorSchema})
def get_current_balance():
    """Recuperar saldo atual
    
    Este endpoint permite aos usuários recuperar o saldo atual.
    """
    session = Session()
    try:
        # Get the latest balance record
        latest_balance = session.query(BalanceHistory)\
            .order_by(BalanceHistory.date.desc())\
            .first()
        
        if not latest_balance:
            return {"balance": "0.00", "income": "0.00", "expense": "0.00"}, 200
            
        return {
            "balance": str(latest_balance.get_balance()),
            "income": str(latest_balance.income),
            "expense": str(latest_balance.expense)
        }, 200
        
    except Exception as e:
        return {"message": "Erro ao recuperar o saldo atual"}, 400
    
    finally:
        session.close()
        
@balance_routes.post('/', responses={"201": BalanceViewSchema, "400": ErrorSchema})
def add_balance_history(body: BalanceSchema):
    """Adicionar um novo registro de saldo
    
    Este endpoint permite aos usuários criar um novo registro de saldo.
    """
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
        return {"message": f"Erro ao adicionar o registro de saldo: {str(e)}"}, 400
    
    finally:
        session.close()

@balance_routes.post('/recalculate', responses={"200": None, "400": ErrorSchema})
def recalculate_balance():
    """Recalcular histórico de saldo
    
    Este endpoint permite aos usuários recalcular todo o histórico de saldo.
    """
    session = Session()
    try:
        calculate_balance(session)
        return {"message": "Histórico de saldo recalculado com sucesso"}, 200
    except Exception as e:
        return {"message": f"Erro ao recalcular o saldo: {str(e)}"}, 400
    finally:
        session.close()