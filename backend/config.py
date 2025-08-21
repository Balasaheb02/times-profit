import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///news_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Performance settings
    COMPRESS_MIMETYPES = [
        'text/html', 'text/css', 'text/xml', 'application/json',
        'application/javascript', 'text/javascript', 'application/xml'
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://newsuser:password@localhost/newsdb'
    CORS_ORIGINS = [os.environ.get('FRONTEND_URL', 'https://yourdomain.com')]

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
