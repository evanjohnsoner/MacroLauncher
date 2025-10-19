@echo off
REM ==================================================
REM install_requirements.bat
REM Smart installer: verifies and installs dependencies.
REM No logs or text files are created.
REM ==================================================

SETLOCAL ENABLEDELAYEDEXPANSION
SET "SCRIPT_DIR=%~dp0"
SET "LAUNCHER_DIR=%SCRIPT_DIR%.."
cd /d "%LAUNCHER_DIR%"

echo ------------------------------------------
echo  Checking environment and dependencies...
echo ------------------------------------------

REM --- Python setup variables ---
SET "PYTHON_VERSION=3.12.0"
SET "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
SET "DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%"

REM --- Check Python Installation ---
python -V >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Downloading and installing...
    powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%PYTHON_INSTALLER%'"
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del "%PYTHON_INSTALLER%" >nul 2>&1
    echo Python installed successfully.
) ELSE (
    echo Python already installed.
)

REM --- Ensure pip works ---
python -m ensurepip >nul 2>&1
python -m pip install --upgrade pip --quiet

REM --- Core dependency list ---
SET DEPENDENCIES=customtkinter psutil requests python-dotenv pywinstyles

echo Checking for required dependencies...
FOR %%P IN (%DEPENDENCIES%) DO (
    python -c "import %%P" >nul 2>&1
    IF ERRORLEVEL 1 (
        echo Installing missing package: %%P
        python -m pip install %%P --quiet
    ) ELSE (
        echo Package %%P already installed.
    )
)

REM --- Search for macro install scripts recursively ---
IF EXIST "%LAUNCHER_DIR%\macros" (
    echo Scanning macros for local install scripts...
    for /R "%LAUNCHER_DIR%\macros" %%F in (install_requirements.bat) do (
        echo Running %%~nxF inside %%~dpF...
        call "%%F"
    )
)

echo ------------------------------------------
echo All dependencies verified and ready!
echo ------------------------------------------

ENDLOCAL
exit /b 0
