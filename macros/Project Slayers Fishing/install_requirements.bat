@echo off
REM ==================================================
REM Fishing Macro - Smart Dependency Installer
REM Checks and installs only missing Python packages.
REM ==================================================

SETLOCAL ENABLEDELAYEDEXPANSION
echo ------------------------------------------
echo  Checking Fishing Macro dependencies...
echo ------------------------------------------

REM --- Check for Python ---
python -V >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found!
    echo Please install Python 3.x and ensure "python" is on PATH.
    pause
    exit /b 1
)

REM --- Ensure pip works ---
python -m ensurepip >nul 2>&1
python -m pip install --upgrade pip setuptools wheel --quiet

REM --- Required packages for this macro ---
SET DEPENDENCIES=opencv-python numpy pyautogui pynput mss Pillow pygetwindow pymsgbox

echo Checking installed packages...
FOR %%P IN (%DEPENDENCIES%) DO (
    python -c "import %%P" >nul 2>&1
    IF ERRORLEVEL 1 (
        echo Installing missing package: %%P
        python -m pip install %%P --quiet
    ) ELSE (
        echo Package %%P already installed.
    )
)

echo ------------------------------------------
echo  Fishing Macro dependencies ready!
echo ------------------------------------------

ENDLOCAL
exit /b 0
