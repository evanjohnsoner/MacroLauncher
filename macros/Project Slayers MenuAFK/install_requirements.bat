@echo off
REM ==============================
REM Python AFK Macro Setup Script
REM ==============================

echo Installing required Python packages...

REM Check if python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ and add it to your PATH.
    pause
    exit /b
)

REM Install pyautogui
pip install --upgrade pip
pip install pyautogui

echo.
echo Installation complete!

