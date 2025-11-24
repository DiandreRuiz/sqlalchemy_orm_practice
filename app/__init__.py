# This is where we will construct our "application factory" or funct. that produces flask apps
from flask import Flask
from app.extensions import ma
from app.models import db
from app.blueprints.members import members_bp

def create_app(config_name: str):
    app = Flask(__name__)
    
    # Import appropriate config
    app.config.from_object(f"config.{config_name}")
    
    # Initialize extensions
    ma.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(members_bp, url_prefix="/members")
    
    return app