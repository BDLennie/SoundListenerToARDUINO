@echo off
setlocal
echo Checking for Python...

REM --- Zoek een bruikbare Python ---
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PYTHON=python
    goto setup_venv
)
py --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PYTHON=py
    goto setup_venv
)
python3 --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PYTHON=python3
    goto setup_venv
)
IF EXIST "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto setup_venv
)

echo Python niet gevonden. Installeren...
powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python_installer.exe"
IF %ERRORLEVEL% NEQ 0 (
    echo Download van Python mislukt. Check je internetverbinding.
    pause
    exit /b 1
)
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
set PYTHON=python

:setup_venv
echo Using Python: %PYTHON%

REM --- Venv aanmaken als die er nog niet is (belangrijk op een nieuwe machine) ---
IF NOT EXIST ".venv\Scripts\python.exe" (
    echo Virtual environment aanmaken...
    %PYTHON% -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        echo Aanmaken van venv mislukt.
        pause
        exit /b 1
    )
)
set PYTHON=.venv\Scripts\python.exe

echo Installing requirements...
%PYTHON% -m pip install --upgrade pip
%PYTHON% -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Installeren van requirements mislukt.
    pause
    exit /b 1
)

echo Starting listener...
%PYTHON% Main.py

echo.
echo Listener gestopt.
pause