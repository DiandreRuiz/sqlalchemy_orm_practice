from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey, String, Date
from typing import List
from datetime import date

# Create a base class for our models
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base) # Instantiate SQLAlchemy database

# Junction Table for Many-to-Many between loans & books tables
loan_book = Table(
    'loan_book',
    Base.metadata,
    Column('loan_id', ForeignKey("loans.id"), primary_key=True),
    Column('book_id', ForeignKey("books.id"), primary_key=True)
)

class Member(Base):
    __tablename__ = "members"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    DOB: Mapped[date]
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    # We are linking 2 attributes, not classes: We list 'member' as the back_population target
    loans: Mapped[List["Loan"]] = relationship(back_populates="member")
    
class Loan(Base):
    __tablename__ = "loans"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(Date)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    # We are linking 2 attributes again...
    member: Mapped["Member"] = relationship(back_populates="loans")
    books: Mapped[List["Book"]] = relationship(secondary=loan_book, back_populates="loans")
    
class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    desc: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    loans: Mapped[List["Loan"]] = relationship(secondary=loan_book, back_populates="books")

