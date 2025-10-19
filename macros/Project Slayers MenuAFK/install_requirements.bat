@echo off
REM ==================================================
REM AFK Macro - Smart Dependency Installer
REM Checks for missing dependencies and installs only what’s needed.
REM ==================================================

SETLOCAL ENABLEDELAYEDEXPANSION
echo ------------------------------------------
echo  Checking AFK Macro dependencies...
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

REM --- Required dependencies for this macro ---
SET DEPENDENCIES=pyautogui

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
echo  AFK Macro dependencies ready!
echo ------------------------------------------

ENDLOCAL
exit /b 0
