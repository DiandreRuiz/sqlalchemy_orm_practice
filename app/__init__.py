# This is where we will construct our "application factory" or funct. that produces flask apps
from flask import Flask
from app.extensions import ma

def create_app(config_name: str):
    app = Flask(__name__)
    
    # Import appropriate config
    app.config.from_object(f"config.{config_name}")
    
    # Initialize extensions
    ma.init_app(app)
    
    # Register blueprints
    
    return app