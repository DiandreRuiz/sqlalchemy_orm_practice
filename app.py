from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey, Column
from datetime import date
from typing import List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<YOUR MYSQL PASSWORD>@localhost/<YOUR DATABASE>'

# Create a base class for our models
class Base(DeclarativeBase):
    pass

# Instantiate SQLAlchemy database
db = SQLAlchemy(model_class=Base)

# Adding our db extension to our app
db.init_app(app)

class Member(Base):
    __tablename__ = "members"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    DOB: Mapped[date]
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    # We are linking 2 attributes, not classes: We list 'member' as the back_population target
    loans: Mapped["Loan"] = relationship(back_populates="member")
    
class Loan(Base):
    __tablename__ = "loans"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(Date)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    
    member: Mapped["Member"] = relationship(back_populates="loans")
    
class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    desc: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
loan_book = db.Table(
    'loan_book',
    Base.metadata,
    Column('loan_id', ForeignKey(Loan.id), primary_key=True),
    Column('book_id', ForeignKey(Book.id), primary_key=True)
)
    
    
    
    
# Create the table
with app.app_context():
    db.create_all()
    
app.run(debug=True)