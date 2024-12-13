from sqlalchemy import Column, String, Integer, Date, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date, datetime
from typing import Union
from decimal import Decimal

from models import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    description = Column(String(140))
    amount = Column(String(20), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship("Category", back_populates="transactions")
    date = Column(Date, default=date.today)
    type = Column(String(10), nullable=False, default="income")  # income or expense

    # Creating a uniqueness requirement involving a pair of information
    __table_args__ = (UniqueConstraint("description", "category_id", name="transaction_unique_id"),)


    def __init__(self, description, amount, date, type, category=None):
        """
        Creates a transaction

        Arguments:
            description: transaction description.
            amount: transaction value
            date: transaction date (date object or YYYY-MM-DD string)
            type: transaction type (income or expense)
            category: Category object (optional)
        """
        self.description = description
        self.amount = str(Decimal(str(amount)))
        self.category = category
        self.category_id = category.id if category else None
        if isinstance(date, str):
            self.date = datetime.strptime(date, '%Y-%m-%d').date()
        elif isinstance(date, date):
            self.date = date
        else:
            raise ValueError("Date must be a string in YYYY-MM-DD format or a date object")
        self.type = type

    def get_amount(self):
        """Returns the amount as a Decimal object"""
        return Decimal(self.amount)

    def to_dict(self):
        """
        Returns the dictionary representation of the Transaction object.
        """
        return{
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category.to_dict() if self.category else None,
            "date": self.date.strftime('%Y-%m-%d'),
            "type": self.type
        }

    def __repr__(self):
        """
        Returns a text representation of the Transaction object.
        """
        return f"Transaction(id={self.id}, description='{self.description}', amount={self.amount}, category='{self.category}', date='{self.date}', type='{self.type}')"