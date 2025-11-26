@echo off
echo ========================================
echo Starting FastAPI Server Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/2] Installing dependencies...
echo ----------------------------------------
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/2] Starting FastAPI server...
echo ----------------------------------------
echo Server will be accessible at your local IP address
echo Scan the QR code to connect from your phone
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

fastapi run main.py

pause
