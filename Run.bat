@echo off
setlocal

echo Checking for Python...

REM --- Check python ---
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PYTHON=python
    goto install_requirements
)

REM --- Check py ---
py --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PYTHON=py
    goto install_requirements
)

REM --- Check python3 ---
python3 --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PYTHON=python3
    goto install_requirements
)

REM --- Check default Windows install location ---
IF EXIST "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto install_requirements
)

echo Python niet gevonden. Installeren...

powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python_installer.exe"
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

set PYTHON=python

:install_requirements
echo Using Python: %PYTHON%
%PYTHON% -m pip install --upgrade pip
%PYTHON% -m pip install -r requirements.txt

echo Starting listener...
%PYTHON% Main.py
