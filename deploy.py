#!/usr/bin/env python3
"""
Simple deployment script for Farm Fresh Vegetables App
Creates a standalone deployment package
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_deployment_package():
    """Create a deployment package with all dependencies"""
    
    print("🚀 Creating Farm App deployment package...")
    
    # Create deployment directory
    deploy_dir = Path("farm_app_deployment")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy application files
    app_files = [
        'app.py', 'models.py', 'config.py', 'requirements.txt',
        'run.py', 'wsgi.py', 'Procfile', 'gunicorn.conf.py'
    ]
    
    for file in app_files:
        if Path(file).exists():
            shutil.copy2(file, deploy_dir / file)
            print(f"✓ Copied {file}")
    
    # Copy directories
    for dir_name in ['templates', 'static']:
        if Path(dir_name).exists():
            shutil.copytree(dir_name, deploy_dir / dir_name)
            print(f"✓ Copied {dir_name}/ directory")
    
    # Create startup script
    startup_script = deploy_dir / "start.sh"
    with open(startup_script, 'w') as f:
        f.write("""#!/bin/bash
# Farm App Startup Script
echo "Starting Farm Fresh Vegetables App..."

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static/uploads
mkdir -p instance

# Initialize database
python -c "from app import create_tables_and_seed; create_tables_and_seed()"

# Start the application
echo "App starting on http://localhost:5000"
python run.py
""")
    
    # Create Windows startup script
    startup_bat = deploy_dir / "start.bat"
    with open(startup_bat, 'w') as f:
        f.write("""@echo off
echo Starting Farm Fresh Vegetables App...

REM Install dependencies
pip install -r requirements.txt

REM Create necessary directories
if not exist "static\\uploads" mkdir "static\\uploads"
if not exist "instance" mkdir "instance"

REM Initialize database
python -c "from app import create_tables_and_seed; create_tables_and_seed()"

REM Start the application
echo App starting on http://localhost:5000
python run.py
pause
""")
    
    # Create README for deployment
    readme_content = """# Farm Fresh Vegetables App - Deployment Package

## Quick Start

### Windows:
```bash
start.bat
```

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### Manual Start:
```bash
pip install -r requirements.txt
python run.py
```

## Access
After starting, open your browser and go to:
- http://localhost:5000

## Admin Access
- URL: http://localhost:5000/admin/login
- Username: admin
- Password: admin123

## Features
- Browse fresh vegetables
- Shopping cart functionality  
- Checkout system
- Admin panel for product management
- Customer feedback system

## Deployment Options
1. **Local**: Use the startup scripts above
2. **Cloud**: Upload this folder to any Python hosting service
3. **Docker**: Use the included Dockerfile
4. **VPS**: Follow DEPLOYMENT.md for server setup

## Support
Check DEPLOYMENT.md for detailed deployment instructions.
"""
    
    with open(deploy_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print(f"\nDeployment package created in: {deploy_dir.absolute()}")
    print("\nNext steps:")
    print("1. Copy the 'farm_app_deployment' folder")
    print("2. Run start.sh (Linux/Mac) or start.bat (Windows)")
    print("3. Open http://localhost:5000 in your browser")
    
    return deploy_dir

if __name__ == "__main__":
    create_deployment_package()
