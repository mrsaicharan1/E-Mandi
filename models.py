from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///user.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    user_type = db.Column(db.String(1))
	

    def __init__(self, name, email, password, user_type):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type

class Transaction(Base):
    __tablename__ = 'Transaction'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(10))
    seller_id = db.Column(db.String(10))
    vegetable_id = db.Column(db.String(60))
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)

    def __init__(self,user_id,seller_id,vegetable_id,amount):
        self.user_id = user_id
        self.seller_id = seller_id
        self.vegetable_id = vegetable_id
        self.amount = amount

class Wholeseller(Base):
    __tablename__ = 'Wholeseller'

    id = db.Column(db.Integer,primary_key=True)
    wholeseller_name = db.Column(db.String(10))
    vegetable_name = db.Column(db.String(60))
    price = db.Column(db.Float)

    def __init__(self,wholeseller_name,vegetable_name,price):
        self.wholeseller_name = wholeseller_name
        self.vegetable_name = vegetable_name
        self.price = price

class Retailer(Base):
    __tablename__ = 'Retailer'

    id = db.Column(db.Integer,primary_key=True)
    retailer_name = db.Column(db.String(10))
    vegetable_name = db.Column(db.String(60))
    price = db.Column(db.Integer)

    def __init__(self,retailer_name,vegetable_name,price):
        self.retailer_name = retailer_name
        self.vegetable_name = vegetable_name
        self.price = price

class Complaint(Base):
    __tablename__ = 'Complaint'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.String(),db.ForeignKey('Users.id'))
    title = db.Column(db.String)
    category =  db.Column(db.String)
    date = db.Column(db.Date)
    status = db.Column(db.String)

    def __init__(self, user_id, title, category, date, status):
            self.user_id = user_id
            self.title = title
            self.category = category
            self.date = date
            self.status = status

# Create tables.
Base.metadata.create_all(bind=engine)
