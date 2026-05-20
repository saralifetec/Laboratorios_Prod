from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='assets')
    app.config.from_object(Config)
    app.secret_key = '123Afl741Pfr856qLp254Thp'  # Replace with a secure secret key

    db.init_app(app)
    
    with app.app_context():
        from .routes import init_routes
        init_routes(app)
        db.create_all()
        
    return app

