from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    description = Column(String(140))
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Category", back_populates="transactions")
    date = Column(DateTime, default=datetime.now())
    type = Column(String(10), nullable=False, default="income")  # income or expense

    # Creating a uniqueness requirement involving a pair of information
    __table_args__ = (UniqueConstraint("description", "category_id", name="transaction_unique_id"),)


    def __init__(self, description, amount, category, date, type):
        """
        Creates a transaction

        Arguments:
            description: transaction description.
            amount: transaction value
            category: Category object
            date: transaction date
            type: transaction type (income or expense)
        """
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date
        self.type = type

    def to_dict(self):
        """
        Returns the dictionary representation of the Transaction object.
        """
        return{
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category.to_dict(),
            "date": self.date,
            "type": self.type
        }

    def __repr__(self):
        """
        Returns a text representation of the Transaction object.
        """
        return f"Transaction(id={self.id}, description='{self.description}', amount={self.amount}, category='{self.category}', date='{self.date}', type='{self.type}')"