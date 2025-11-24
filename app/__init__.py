# This is where we will construct our "application factory" or funct. that produces flask apps
from flask import Flask

def create_app(config_name: str):
    app = Flask(__name__)
    
    # We will import the appropriate config here
    
    return app