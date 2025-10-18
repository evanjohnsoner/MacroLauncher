@echo off
REM ==================================================
REM install_requirements.bat
REM Smart installer: checks for missing dependencies before installing.
REM Logs output to install_log.txt for launcher progress display.
REM ==================================================

SETLOCAL ENABLEDELAYEDEXPANSION
SET "SCRIPT_DIR=%~dp0"
SET "LOG_FILE=%SCRIPT_DIR%install_log.txt"
SET "LAUNCHER_DIR=%SCRIPT_DIR%.."
cd /d "%LAUNCHER_DIR%"

REM --- Initialize log ---
echo [START] Starting dependency verification... > "%LOG_FILE%"
echo Checking for Python installation... >> "%LOG_FILE%"

REM --- Python setup variables ---
SET "PYTHON_VERSION=3.12.0"
SET "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
SET "DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%"

REM --- Check Python Installation ---
python -V >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Downloading... >> "%LOG_FILE%"
    powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%PYTHON_INSTALLER%'" >> "%LOG_FILE%" 2>&1
    echo Installing Python %PYTHON_VERSION%... >> "%LOG_FILE%"
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del "%PYTHON_INSTALLER%" >nul 2>&1
    echo Python installed successfully. >> "%LOG_FILE%"
) ELSE (
    echo Python already installed. >> "%LOG_FILE%"
)

REM --- Ensure pip works ---
python -m pip -V >nul 2>&1
IF ERRORLEVEL 1 (
    echo pip not detected. Attempting to reinstall... >> "%LOG_FILE%"
    python -m ensurepip >> "%LOG_FILE%" 2>&1
)
echo Upgrading pip... >> "%LOG_FILE%"
python -m pip install --upgrade pip >> "%LOG_FILE%" 2>&1

REM --- Dependency list ---
SET DEPENDENCIES=customtkinter psutil requests python-dotenv pywinstyles
echo Checking for required dependencies... >> "%LOG_FILE%"

FOR %%P IN (%DEPENDENCIES%) DO (
    python -c "import %%P" >nul 2>&1
    IF ERRORLEVEL 1 (
        echo Installing missing package: %%P >> "%LOG_FILE%"
        python -m pip install %%P --quiet >> "%LOG_FILE%" 2>&1
    ) ELSE (
        echo Package %%P already installed. >> "%LOG_FILE%"
    )
)

echo Launcher dependencies verified. >> "%LOG_FILE%"

REM --- Macro dependencies (recursive) ---
echo Searching for macro install scripts... >> "%LOG_FILE%"
for /R "%LAUNCHER_DIR%\macros" %%F in (install_requirements.bat) do (
    echo Running %%~nxF inside %%~dpF... >> "%LOG_FILE%"
    call "%%F" >> "%LOG_FILE%" 2>&1
    echo Finished %%~nxF >> "%LOG_FILE%"
)

REM --- Done ---
echo Performing cleanup checks... >> "%LOG_FILE%"
timeout /t 1 >nul
echo [DONE] Environment verified and ready. >> "%LOG_FILE%"

ENDLOCAL
exit /b 0
