"""
Main entry point for backend server.
Run with: python wsgi.py
Or with gunicorn: gunicorn wsgi:app
"""

import os
from app import create_app

# Create Flask app for Gunicorn
app = create_app(config_name=os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', False))
