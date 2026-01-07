@echo off
REM QuickHelp - Quick Start Script for Windows
REM This script sets up and runs a demo of QuickHelp

echo ========================================
echo QuickHelp - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/5] Checking virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
echo This may take a few minutes on first run...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Running example demonstration...
echo.
python example.py
if errorlevel 1 (
    echo ERROR: Demo failed
    pause
    exit /b 1
)

echo.
echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Add your own documents to: data\documents\
echo.
echo 2. Try CLI commands:
echo    python -m src.cli index --path .\data\documents
echo    python -m src.cli search "your query"
echo    python -m src.cli cluster
echo    python -m src.cli ask "your question"
echo.
echo 3. For OpenAI integration:
echo    set OPENAI_API_KEY=your-key-here
echo.
echo 4. Read documentation:
echo    - README.md - Project overview
echo    - USAGE.md - Detailed usage guide
echo    - TECHNICAL.md - Technical details
echo.
echo ========================================
echo.

pause
