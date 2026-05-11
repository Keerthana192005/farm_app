import os
from datetime import timedelta

def get_db_url():
    url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url

class Config:
<<<<<<< HEAD
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'farm_fresh_vegetables_secret_key_2024'
=======
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = get_db_url()
>>>>>>> f0cf3aaebcdfadd57343fa47bc5a5c138a69e28b
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def get_database_uri():
        database_url = os.environ.get('DATABASE_URL')
        if database_url and database_url.startswith('postgres://'):
            # Convert postgres:// to postgresql:// for SQLAlchemy
            database_url = database_url.replace('postgres://', 'postgresql://')
        return database_url or 'sqlite:///database.db'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()
    
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
=======
>>>>>>> f0cf3aaebcdfadd57343fa47bc5a5c138a69e28b

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
