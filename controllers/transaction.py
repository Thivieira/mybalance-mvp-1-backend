from flask import jsonify, request
from flask_openapi3 import APIBlueprint, Tag
from models import Session, Transaction, Category
from datetime import datetime
from schemas import (
    TransactionSchema, TransactionSearchQuery, TransactionViewSchema,
    TransactionListResponse, ErrorSchema, TransactionUpdatePathSchema,
    TransactionUpdateBodySchema, TransactionUpdateResponse, TransactionDeletePathSchema,
    TransactionSearchByIdPathSchema
)

transaction_tag = Tag(name='Transaction', description="Operações de transação para gerenciar registros financeiros")
transaction_routes = APIBlueprint('transaction', __name__, url_prefix='/transaction', abp_tags=[transaction_tag])

@transaction_routes.get('/', responses={"200": TransactionListResponse})
def get_transactions():
    """Listar todas as transações
    
    Este endpoint permite aos usuários recuperar todas as transações existentes.
    """
    session = Session()
    transactions = session.query(Transaction).all()
    
    result = []
    for transaction in transactions:
        result.append(transaction.to_dict())
    
    return jsonify({"transactions": result}), 200

@transaction_routes.get('/<int:id>', responses={"200": TransactionViewSchema, "404": ErrorSchema})
def get_transaction(path: TransactionSearchByIdPathSchema):
    """Obter uma transação específica
    
    Este endpoint permite aos usuários recuperar uma transação específica por ID.
    """
    try:
        session = Session()
        transaction = session.query(Transaction).get(path.id)
        
        if transaction is None:
            return {"message": f"Transaction with id {path.id} not found"}, 404
            
        return jsonify(transaction.to_dict()), 200
        
    except Exception as e:
        return {"message": "Error retrieving transaction"}, 400
    
    finally:
        session.close()

@transaction_routes.post('/', responses={"201": TransactionViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def add_transaction(body: TransactionSchema):
    """Adicionar uma nova transação
    
    Este endpoint permite aos usuários criar um novo registro de transação.
    """
    try:
        session = Session()
        
        category = None
        if body.category_id:
            category = session.query(Category).filter(Category.id == body.category_id).first()
            if not category:
                return {"message": "Category not found"}, 404
            
        transaction_date = datetime.strptime(body.date, '%Y-%m-%d').date()
        
        transaction = Transaction(
            description=body.description,
            amount=body.amount,
            category=category,
            date=transaction_date,
            type=body.type
        )
        
        session.add(transaction)
        session.commit()
        
        return jsonify(transaction.to_dict()), 201
        
    except Exception as e:
        session.rollback()
        return {"message": f"Could not save the new transaction: {str(e)}"}, 400
    
    finally:
        session.close()

@transaction_routes.put('/<int:id>', responses={"200": TransactionUpdateResponse, "404": ErrorSchema, "400": ErrorSchema})
def update_transaction(path: TransactionUpdatePathSchema, body: TransactionSchema):
    """Atualizar uma transação
    
    Este endpoint permite aos usuários atualizar uma transação existente.
    """
    try:
        session = Session()
        transaction = session.query(Transaction).get(path.id)
        
        if transaction is None:
            return {"message": f"Transaction with id {path.id} not found"}, 404
            
        category = session.query(Category).filter(Category.id == body.category_id).first()
        if not category:
            return {"message": "Category not found"}, 404
            
        date = datetime.strptime(body.date, '%Y-%m-%d')
        
        transaction.description = body.description
        transaction.amount = body.amount
        transaction.category = category
        transaction.date = date
        transaction.type = body.type
        
        session.commit()
        return jsonify(transaction.to_dict()), 200
        
    except Exception as e:
        session.rollback()
        return {"message": "Error updating transaction"}, 400
    
    finally:
        session.close()

@transaction_routes.get('/search', responses={"200": TransactionListResponse, "400": ErrorSchema})
def search_transactions(query: TransactionSearchQuery):
    """Pesquisar transações por descrição
    
    Este endpoint permite aos usuários pesquisar transações pela descrição.
    """
    try:
        session = Session()
        transactions = session.query(Transaction).filter(
            Transaction.description.ilike(f'%{query.term}%')
        ).all()
        
        result = []
        for transaction in transactions:
            result.append(transaction.to_dict())
            
        return jsonify({"transactions": result}), 200
        
    except Exception as e:
        return {"message": "Error searching transactions"}, 400
        
    finally:
        session.close()

@transaction_routes.delete('/<int:id>', responses={"204": None, "404": ErrorSchema, "400": ErrorSchema})
def delete_transaction(path: TransactionDeletePathSchema):
    """Excluir uma transação
    
    Este endpoint permite aos usuários excluir uma transação existente.
    """
    try:
        session = Session()
        transaction = session.query(Transaction).get(path.id)
        
        if transaction is None:
            return {"message": f"Transaction with id {path.id} not found"}, 404
            
        session.delete(transaction)
        session.commit()
        return '', 204
        
    except Exception as e:
        session.rollback()
        return {"message": "Error deleting transaction"}, 400
    
    finally:
        session.close()
