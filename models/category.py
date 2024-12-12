from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    transactions = relationship("Transaction", back_populates="category")

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        """
        Retorna uma representação do Category em forma de texto.
        """
        return f"Category(id={self.id}, name='{self.name}')"
