"""
Simple WSGI entry point for production deployment
"""
import os
from app import create_app
from models import db

# Create app instance
app = create_app('production')

# Initialize database on startup
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization: {e}")

if __name__ == "__main__":
    app.run()
