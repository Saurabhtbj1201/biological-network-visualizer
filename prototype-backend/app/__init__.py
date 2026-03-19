"""
NetworkInsight - Backend Flask Application Factory
Main entry point for the backend server.
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler

# Initialize database
db = SQLAlchemy()

def create_app(config_name: str = None) -> Flask:
    """Application factory for Flask app."""
    
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    if config_name == 'production':
        from config import ProductionConfig as Config
    elif config_name == 'testing':
        from config import TestingConfig as Config
    else:
        from config import DevelopmentConfig as Config
    
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Setup logging
    _setup_logging(app)
    
    # Register blueprints
    from app.api import networks, analysis
    app.register_blueprint(networks.bp)
    app.register_blueprint(analysis.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'NetworkInsight backend running'}, 200
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'bad_request', 'message': str(error)}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'not_found', 'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return {'error': 'internal_error', 'message': 'Internal server error'}, 500
    
    return app


def _setup_logging(app: Flask) -> None:
    """Configure application logging."""
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/networkinsight.log',
                                          maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('NetworkInsight backend startup')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
