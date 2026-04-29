@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
chcp 65001 >nul

set "FORCE_DEVICE=cpu"
set "HF_HOME=%~dp0hf-cache"
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"

set "PY_BIN="
if exist "%~dp0python-portable\python.exe" set "PY_BIN=%~dp0python-portable\python.exe"
if not defined PY_BIN if exist "%~dp0.venv\Scripts\python.exe" set "PY_BIN=%~dp0.venv\Scripts\python.exe"

if not defined PY_BIN (
    echo ERROR: project Python not found.
    echo Run install.bat first.
    pause
    exit /b 1
)

"!PY_BIN!" src\app.py
pause
