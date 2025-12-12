@echo off
echo ============================================================
echo Starting Fake News Detection Backend
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then run: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Using virtual environment Python...
echo.

REM Start the backend server
".venv\Scripts\python.exe" main.py

pause
