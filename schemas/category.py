from pydantic import BaseModel
from typing import List

class CategoryViewSchema(BaseModel):
    """ Defines the structure of the category to be returned.
    """
    id: int
    name: str

class CategoryBodySchema(BaseModel):
    """ Defines the structure of the category to be added.
    """
    name: str

class CategoryDeletePathSchema(BaseModel):
    """ Defines the structure of the category to be deleted.
    """
    id: int

class CategoryListResponse(BaseModel):
    categories: List[CategoryViewSchema]

class CategoryUpdatePathSchema(BaseModel):
    id: int

class CategoryUpdateBodySchema(BaseModel):
    name: str
    
class CategoryUpdateResponse(BaseModel):
    category: CategoryViewSchema

class CategorySearchByIdPathSchema(BaseModel):
    id: int
