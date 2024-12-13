from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os

# importing base first
from models.base import Base

db_path = "database/"
# Check if directory doesn't exist
if not os.path.exists(db_path):
   # then create directory
   os.makedirs(db_path)

# database access url (this is a url for local sqlite access)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# create the connection engine with the database
engine = create_engine(
    db_url,
    echo=False,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

# Instance a session creator with the database
Session = sessionmaker(bind=engine)

# create the database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url) 

# Now import the models
from models.transaction import Transaction
from models.category import Category
from models.balance_history import BalanceHistory
# create the database tables, if they don't exist
Base.metadata.create_all(engine)

