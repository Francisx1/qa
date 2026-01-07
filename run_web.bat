@echo off
echo Starting QuickHelp Web UI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\Lib\site-packages\flask\" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the web server
echo.
echo ========================================
echo QuickHelp Web UI
echo ========================================
echo.
echo Server starting at http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
