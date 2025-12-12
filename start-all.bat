@echo off
echo ============================================================
echo Starting Fake News Detection System
echo ============================================================
echo.
echo This will start both Backend and Frontend servers
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press Ctrl+C in each window to stop the servers
echo.
pause

cd /d "%~dp0"

REM Start backend in new window
echo Starting Backend...
start "Fake News Backend" cmd /k "start-backend.bat"

REM Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting Frontend...
start "Fake News Frontend" cmd /k "start-frontend.bat"

echo.
echo ============================================================
echo Both servers are starting in separate windows
echo ============================================================
echo.
echo Backend:  http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Close this window or press any key to exit...
pause >nul
