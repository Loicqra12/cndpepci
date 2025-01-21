import os

class Config:
    # Configuration de base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('mysql://', 'mysql+pymysql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de sécurité
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ma_cle_secrete_tres_longue')
    
    # Configuration de l'upload
    UPLOAD_FOLDER = os.path.join('static', 'images', 'members')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configuration Flask
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', '1')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    
    # Configuration email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
