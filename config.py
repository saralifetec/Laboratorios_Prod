import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://labtextil:Textil#2024@vi2wpc26462c/laboratorios_prod'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_ECHO = True  # Adicione esta linha para registrar todas as consultas SQL no console