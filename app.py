from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date

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
    DOB: Mapped[Date]
    password: Mapped[str] = mapped_column(String(255), nullable=False)