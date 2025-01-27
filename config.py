import os

class Config:
    # Configuration de base de données
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://')
    
    # Ajouter sslmode=require à l'URL de la base de données
    if database_url and '?' not in database_url:
        database_url = database_url + '?sslmode=require'
    
    SQLALCHEMY_DATABASE_URI = database_url or 'postgresql://cndpepci_db_user:zdsNMumG2njiK6kc7xrXsBTyU3ejydh5@dpg-cu7v7g5ds78s73bqeoi0-a.oregon-postgres.render.com/cndpepci_db?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de sécurité
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ma_cle_secrete_tres_longue')
    
    # Configuration de l'upload
    UPLOAD_FOLDER = os.path.join('static', 'images', 'members')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configuration Flask
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', '0')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    
    # Configuration email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
