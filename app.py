from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey, Column, Table, select
from datetime import date
from typing import List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hetaT-601@localhost:3306/library'

# Create a base class for our models
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base) # Instantiate SQLAlchemy database
ma = Marshmallow() # Instantiate Marshmallow instance

db.init_app(app) # Adding our db extension to our app
ma.init_app(app) # Adding marshmallow extension to our app

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


#======== SCHEMAS ========#
# Marshmellow Schema Declarations
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)





#======== ROUTES ========#

# /members

# Create Member
@app.route("/members", methods=['POST'])
def create_member():
    
    # We explicityly check if the json body is present since Flask's
    # stubs type request.json as Any | None which is incompatible 
    # with member_schema.load(). We will follow this design pattern for
    # all routes.
    
    # Validation
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    try:
        member_data = member_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email == member_data['email']) # Checking our db for a member with this email
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({"error": "Email already associated with an account"}), 400
    
    # Creation of Member row
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

# Get all Members
@app.route("/members", methods=['GET'])
def get_members():
    query = select(Member)
    # Returns a tuple, where:
    # - 1st item is a Member object based on Member's class definition
    # - All other items represent the values of respective columns for that row
    # Scalars() returns the first item in the tuple which would be the Member object
    members = db.session.execute(query).scalars().all()
    
    return members_schema.jsonify(members)

# Get a specific member based on his / her id
@app.route("/members/<int:member_id>", methods=['GET'])
def get_member(member_id):
    query = select(Member).where(Member.id == member_id)
    member = db.session.execute(query)
    if not member:
        return jsonify({"error": f"Member w/ id: {member_id} not found"}), 404
    else:
        return member_schema.jsonify(member), 200


    
# Create the table
with app.app_context():
    db.create_all()
    
app.run(debug=True)