@echo off
title Fake News Detection Backend - Health Monitor
color 0A

echo ================================================================
echo   FAKE NEWS DETECTION BACKEND - STARTING...
echo ================================================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.13 or higher
    pause
    exit /b 1
)

echo Starting backend server with health monitoring...
echo.
echo Health Check will run on startup
echo Access points:
echo   - API Docs:      http://localhost:8000/docs
echo   - Health Check:  http://localhost:8000/health
echo   - Frontend:      http://localhost:5173
echo.
echo ================================================================
echo.

REM Start the backend server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Backend stopped.
pause
