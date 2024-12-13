from flask import jsonify, request, make_response
from flask_openapi3 import APIBlueprint, Tag
from typing import List
from schemas import (
    CategoryDeletePathSchema, CategoryBodySchema, CategoryViewSchema, ErrorSchema, CategoryListResponse,
    CategorySearchByIdPathSchema, CategoryUpdatePathSchema, CategoryUpdateBodySchema, CategoryUpdateResponse
)
from models import Session, Category

category_tag = Tag(name='Category', description="Adição, visualização e remoção de categorias para o banco de dados")
category_routes = APIBlueprint('category', __name__, url_prefix='/category', abp_tags=[category_tag])

@category_routes.get('/', responses={"200": CategoryListResponse})
def get_categories():
    """Lista todas as categorias
    
    Neste endpoint, o usuário pode listar todas as categorias existentes.
     
    """
    session = Session()
    categories = session.query(Category).all()
    
    result = []
    for category in categories:
        result.append(category.to_dict())
    
    return jsonify({"categories": result}), 200

@category_routes.get('/<int:id>', responses={"200": CategoryViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def get_category(path: CategorySearchByIdPathSchema):
    """Lista uma categoria
    
    Neste endpoint, o usuário pode listar uma categoria existente.
     
    """
    session = Session()
    category = session.query(Category).get(path.id)
    return jsonify(category.to_dict()), 200

@category_routes.post('/', responses={"201": CategoryViewSchema, "400": ErrorSchema})
def add_category(body: CategoryBodySchema):
    """Adiciona uma nova categoria
    
    Neste endpoint, o usuário pode adicionar uma nova categoria.
     
    """
    try:
        session = Session()
        category = Category(name=body.name)
        
        session.add(category)
        session.commit()
        
        return jsonify(category.to_dict()), 201
        
    except Exception as e:
        session.rollback()
        return {"message": "Não foi possível salvar a nova categoria"}, 400
    
    finally:
        session.close()

@category_routes.put('/<int:id>', responses={"200": CategoryUpdateResponse, "404": ErrorSchema, "400": ErrorSchema})
def update_category(path: CategoryUpdatePathSchema, body: CategoryUpdateBodySchema):
    """Atualiza uma categoria
    
    Neste endpoint, o usuário pode atualizar uma categoria existente.
     
    """
    try:
        session = Session()
        category = session.query(Category).get(path.id)
        category.name = body.name
        session.commit()
        return jsonify(category.to_dict()), 200
    
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao atualizar a categoria"}, 400
    
    finally:
        session.close()

@category_routes.delete('/<int:id>', responses={"204": None, "404": ErrorSchema, "400": ErrorSchema})
def delete_category(path: CategoryDeletePathSchema):
    """Deleta uma categoria
    
    Neste endpoint, o usuário pode deletar uma categoria existente.
    Retorna erro 400 se existirem transações associadas a esta categoria.
    """
    try:
        session = Session()
        category = session.query(Category).get(path.id)
        
        if category is None:
            return {"message": f"Categoria com id {path.id} não encontrada"}, 404
        
        # Check if there are any transactions using this category
        if hasattr(category, 'transactions') and len(category.transactions) > 0:
            return {
                "message": "Não é possível deletar uma categoria que possui transações. Remova ou reatribua as transações primeiro."
            }, 400
            
        session.delete(category)
        session.commit()
        return '', 204
        
    except Exception as e:
        session.rollback()
        print(e)
        return {"message": "Erro ao deletar a categoria"}, 400
        
    finally:
        session.close()
