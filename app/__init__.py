from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='assets')
    app.config.from_object(Config)
    app.secret_key = '123Afl741Pfr856qLp254Thp'

    db.init_app(app)

    from .routes import init_routes, gbs_bp, relatorios_bp

    with app.app_context():
        init_routes(app)
        app.register_blueprint(gbs_bp)
        app.register_blueprint(relatorios_bp)

        db.create_all()

    return app
