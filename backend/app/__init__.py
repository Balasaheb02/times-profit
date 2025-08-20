from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes.articles import articles_bp
    from app.routes.categories import categories_bp
    from app.routes.authors import authors_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(articles_bp, url_prefix='/api/articles')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(authors_bp, url_prefix='/api/authors')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Flask backend is running'}
    
    return app
