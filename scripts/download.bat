@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."
chcp 65001 >nul

set "ROOT=%CD%"
set "HF_HOME=%ROOT%\hf-cache"
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"

set "PY_BIN="
if exist "%ROOT%\python-portable\python.exe" set "PY_BIN=%ROOT%\python-portable\python.exe"
if not defined PY_BIN if exist "%ROOT%\.venv\Scripts\python.exe" set "PY_BIN=%ROOT%\.venv\Scripts\python.exe"

if not defined PY_BIN (
    echo ERROR: project Python not found. Run install.bat first.
    pause
    exit /b 1
)

"!PY_BIN!" src\download_model.py
pause
