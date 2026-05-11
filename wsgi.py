<<<<<<< HEAD
"""
Simple WSGI entry point for production deployment
"""
import os
from app import app

if __name__ == "__main__":
    app.run()
=======
import os
os.environ.setdefault('FLASK_ENV', 'production')

from app import app, create_tables_and_seed

with app.app_context():
    create_tables_and_seed()
>>>>>>> f0cf3aaebcdfadd57343fa47bc5a5c138a69e28b
