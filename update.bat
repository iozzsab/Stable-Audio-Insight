@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
chcp 65001 >nul

echo ============================================================
echo   Stable Audio Insight - update
echo ============================================================
echo.
echo This script refreshes Python dependencies and re-syncs models
echo with the HuggingFace cache. It does NOT pull new code from
echo GitHub - run "git pull" yourself first (or replace files from
echo a fresh ZIP) before running this.
echo.

set "PORTABLE_DIR=%~dp0python-portable"
set "PY_BIN="
if exist "!PORTABLE_DIR!\python.exe" set "PY_BIN=!PORTABLE_DIR!\python.exe"
if not defined PY_BIN if exist "%~dp0.venv\Scripts\python.exe" set "PY_BIN=%~dp0.venv\Scripts\python.exe"

if not defined PY_BIN (
    echo No project Python found at python-portable\ or .venv\.
    echo Run install.bat first.
    pause
    exit /b 1
)

echo Using: !PY_BIN!
echo.
echo [1/3] Upgrading pip / wheel...
"!PY_BIN!" -m pip install --upgrade pip wheel

echo.
echo [2/3] Refreshing dependencies from requirements.txt...
"!PY_BIN!" -m pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo ERROR: dependency update failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Syncing models with HuggingFace cache (downloads only diffs)...
set "HF_HOME=%~dp0hf-cache"
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"
"!PY_BIN!" src\download_model.py
if errorlevel 1 (
    echo WARNING: model sync had issues. Dependencies were updated though.
    echo You can re-run this script later or run download.bat manually.
)

echo.
echo ============================================================
echo   Update complete. Use run.bat to start.
echo ============================================================
pause
