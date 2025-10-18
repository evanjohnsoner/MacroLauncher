@echo off
REM ----------------------------------------
REM install_requirements.bat
REM Installs Python packages required by fishing.pyw
REM Save and run this file (double-click). Run as Admin if permissions errors occur.
REM ----------------------------------------

REM Check for Python
python -V >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python was not found on the PATH.
    echo Please install Python 3.x and ensure "python" is available from the command line.
    pause
    exit /b 1
)

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install required packages
echo Installing required Python packages...
python -m pip install --upgrade ^
    opencv-python ^
    numpy ^
    pyautogui ^
    pynput ^
    mss ^
    Pillow ^
    pygetwindow ^
    pymsgbox

IF ERRORLEVEL 1 (
    echo.
    echo One or more packages failed to install.
    echo Try running this script as Administrator, or inspect the error messages above.
    pause
    exit /b 1
)

echo.
echo All packages installed successfully.
echo Note: Tkinter typically ships with Python on Windows. If your system lacks it, install the OS package or a Python distribution that includes it.

