#!/usr/bin/env python3
"""
Production-ready runner for Farm Fresh Vegetables App
"""
import os
from app import create_app, create_tables_and_seed

# Create app instance
app = create_app('production')

# Initialize database if needed
if __name__ == '__main__':
    create_tables_and_seed()
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run in production mode
    app.run(host='0.0.0.0', port=port, debug=False)
