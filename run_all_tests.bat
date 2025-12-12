@echo off
echo ================================================================
echo   FAKE NEWS DETECTION - COMPLETE TEST SUITE
echo ================================================================
echo.

echo Running Quick Validation Tests...
echo ----------------------------------------------------------------
python quick_test.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo CRITICAL TESTS FAILED - Fix issues before proceeding
    pause
    exit /b 1
)

echo.
echo.
echo Running Model Accuracy Tests...
echo ----------------------------------------------------------------
python test_models_accuracy.py

echo.
echo.
echo ================================================================
echo   ALL TESTS COMPLETE
echo ================================================================
echo.
pause
