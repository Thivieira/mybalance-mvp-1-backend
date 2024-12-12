from pydantic import BaseModel
from typing import Optional, List, Literal
from models.transaction import Transaction

# TransactionType with Pydantic
class TransactionType:
    INCOME = "income"
    EXPENSE = "expense"
    
class TransactionSchema(BaseModel):
    """ Defines the structure of the new transaction to be inserted.
    """
    description: str
    amount: float
    category_id: int
    date: str
    type: Literal[TransactionType.INCOME, TransactionType.EXPENSE]

class TransactionSearchByDescriptionSchema(BaseModel):
    """ Defines the structure of the search. Which will be
        made only based on the transaction description.
    """
    term: str
    
class TransactionSearchQuery(BaseModel):
    term: str

class TransactionSearchByIdSchema(BaseModel):
    """ Defines the structure of the search. Which will be
        made only based on the transaction id.
    """
    id: int

class TransactionViewSchema(BaseModel):
    """ Defines how a transaction will be returned: transaction + comments.
    """
    id: int
    description: str
    amount: float
    category_id: int
    date: str
    type: str

class TransactionDeleteSchema(BaseModel):
    """ Defines the structure of the data returned after a removal request.
    """
    message: str
    id: int

class TransactionListResponse(BaseModel):
    """ Defines the structure of the response when listing transactions.
    """
    transactions: List[TransactionViewSchema]

class TransactionUpdatePathSchema(BaseModel):
    """ Defines the path parameters for updating a transaction.
    """
    id: int

class TransactionUpdateBodySchema(BaseModel):
    """ Defines the body parameters for updating a transaction.
    """
    description: str
    amount: float
    category_id: int
    date: str
    type: Literal[TransactionType.INCOME, TransactionType.EXPENSE]

class TransactionUpdateResponse(BaseModel):
    """ Defines the response structure for transaction updates.
    """
    id: int
    description: str
    amount: float
    category_id: int
    date: str
    type: str

class TransactionSearchByIdPathSchema(BaseModel):
    """ Defines the path parameters for searching a transaction by ID.
    """
    id: int

class TransactionDeletePathSchema(BaseModel):
    """ Defines the path parameters for deleting a transaction.
    """
    id: int