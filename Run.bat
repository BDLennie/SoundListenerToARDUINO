@echo off

REM 1. Check of Python bestaat
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python niet gevonden. Installeren...
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python_installer.exe"
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
)

REM 2. Installeer requirements
pip install -r requirements.txt

REM 3. Run jouw script
python Main.py
