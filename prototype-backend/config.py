"""
Configuration settings for different environments.
"""

import os
from datetime import timedelta

class Config:
    """Base configuration."""
    
    # Flask
    TESTING = False
    DEBUG = False
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    
    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5000"]
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    
    # File upload
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')
    ALLOWED_EXTENSIONS = {'sif', 'json', 'csv', 'tsv', 'txt'}


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///networkinsight_dev.db'
    )
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Cache settings (shorter for development)
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Logging
    LOGGING_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration."""
    
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError('DATABASE_URL environment variable not set')
    
    REDIS_URL = os.getenv('REDIS_URL')
    if not REDIS_URL:
        raise ValueError('REDIS_URL environment variable not set')
    
    # Cache settings (longer for production)
    CACHE_DEFAULT_TIMEOUT = 86400  # 24 hours
    
    # CORS - restrict origins in production
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://networkinsight.example.com').split(',')
    
    # Logging
    LOGGING_LEVEL = 'INFO'


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    REDIS_URL = 'redis://localhost:6379/15'  # Different DB for testing
    RATELIMIT_ENABLED = False
