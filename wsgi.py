"""
WSGI entry point for production deployment
"""
import os
os.environ.setdefault('FLASK_ENV', 'production')

from app import app, create_tables_and_seed

with app.app_context():
    create_tables_and_seed()

if __name__ == "__main__":
    app.run()
