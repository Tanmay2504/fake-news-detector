@echo off
echo ============================================================
echo Starting Fake News Detection Frontend
echo ============================================================
echo.

cd /d "%~dp0\frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo ERROR: Dependencies not installed!
    echo Installing dependencies...
    call npm install
)

echo Starting development server...
echo.
echo Frontend will be available at: http://localhost:5173
echo.

call npm run dev

pause
