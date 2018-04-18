from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///user.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=False,
                                         bind=engine))
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
    region = db.Column(db.String(20))


    def __init__(self, name, email, password, user_type,region):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.region = region

class Transaction(Base):
    __tablename__ = 'Transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('Users.id'))
    create_user_id = db.relationship("User", foreign_keys=user_id)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    region = db.Column(db.String(20))

    def __init__(self,user_id,date,amount,region):
        self.user_id = user_id
        self.date = date
        self.amount = amount
        self.region = region

class Retailer(Base):
    __tablename__ = 'Retailer'

    id = db.Column(db.Integer,primary_key=True)
    retailer_name = db.Column(db.String(10))
    vegetable_name = db.Column(db.String(60))
    price = db.Column(db.Float)

    def __init__(self,retailer_name,vegetable_name,price):
        self.retailer_name = retailer_name
        self.vegetable_name = vegetable_name
        self.price = price

class Wholeseller(Base):
    __tablename__ = 'Wholeseller'

    id = db.Column(db.Integer,primary_key=True)
    wholeseller_name = db.Column(db.String(10))
    vegetable_name = db.Column(db.String(60))
    price = db.Column(db.Integer)

    def __init__(self,wholeseller_name,vegetable_name,price):
        self.wholeseller_name = wholeseller_name
        self.vegetable_name = vegetable_name
        self.price = price

class Government(Base):
     __tablename__='Government'

     id = db.Column(db.Integer,primary_key=True)
     vegetable_name = db.Column(db.String(60))
     price = db.Column(db.Integer)

     def __init__(self,vegetable_name,price):
         self.vegetable_name = vegetable_name
         self.price = price

class Feedback(Base):
    __tablename__='Feedback'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    create_user_id = db.relationship("User", foreign_keys=user_id)
    title = db.Column(db.String(60))
    status = db.Column(db.String(60))
    date = date = db.Column(db.Date)

    def __init__(self,user_id,date,title,status):
        self.user_id = user_id
        self.date = date
        self.title = title
        self.status = status




# Create tables.
Base.metadata.create_all(bind=engine)
