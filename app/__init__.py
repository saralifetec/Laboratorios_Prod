from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

from .routes import (
    init_routes,
    gbs_bp,
    relatorios_bp,
    ensaios_bp,
    calendario_bp,
    horasauto_bp,
    horas_horasauto_bp,
    index_bp,
    testes_bp,
    horas_bp,
    dashboard_bp,
    login_bp
)

def create_app():

    app = Flask(__name__, static_folder='assets')
    app.config.from_object(Config)
    app.secret_key = '123Afl741Pfr856qLp254Thp'

    db.init_app(app)

    with app.app_context():

        init_routes(app)

        app.register_blueprint(gbs_bp)
        app.register_blueprint(relatorios_bp)
        app.register_blueprint(calendario_bp, url_prefix='/calendario')
        app.register_blueprint(ensaios_bp)
        app.register_blueprint(horasauto_bp, url_prefix='/horasauto')
        app.register_blueprint(horas_horasauto_bp, url_prefix='/horas_horasauto')
        app.register_blueprint(index_bp, url_prefix='/index')
        app.register_blueprint(testes_bp, url_prefix='/testes')
        app.register_blueprint(horas_bp, url_prefix='/horas')
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(login_bp)

        db.create_all()

    return app
