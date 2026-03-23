@echo off
echo Starting Farm Fresh Vegetables App...

REM Install dependencies
pip install -r requirements.txt

REM Create necessary directories
if not exist "static\uploads" mkdir "static\uploads"
if not exist "instance" mkdir "instance"

REM Initialize database
python -c "from app import create_tables_and_seed; create_tables_and_seed()"

REM Start the application
echo App starting on http://localhost:5000
python run.py
pause
