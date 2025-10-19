@echo off
title MacroLauncher v4.4 - Dependency Installer
color 09
echo.
echo ==================================================
echo        MacroLauncher v4.4 - Dependency Setup
echo ==================================================
echo.

REM --- Move to this script’s directory ---
cd /d "%~dp0"

REM --- Define installer path ---
set "INSTALLER=.\sys\install_requirements.bat"

REM --- Check if installer exists ---
if not exist "%INSTALLER%" (
    echo [ERROR] Could not find "%INSTALLER%"
    echo Please make sure you extracted all launcher files correctly.
    pause
    exit /b 1
)

echo [INFO] Running dependency installer...
echo --------------------------------------------------
call "%INSTALLER%"
echo --------------------------------------------------
echo [OK] All dependencies verified and ready!
echo.

echo Press SPACE to delete this installer, or close the window to keep it.
echo.

REM --- Wait for Spacebar press using PowerShell ---
powershell -NoProfile -Command ^
"$key = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown'); if ($key.VirtualKeyCode -eq 32) { exit 0 } else { exit 1 }"

if %errorlevel%==0 (
    echo.
    echo Deleting this file...
    timeout /t 2 >nul
    del "%~f0"
) else (
    echo.
    echo Installer will remain on your system.
    pause
)
exit /b 0
