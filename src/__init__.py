from flask import Flask
from flask_cors import CORS
from .config import Config
from .db import mongo
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)
    CORS(app)
    register_routes(app)
    return app
