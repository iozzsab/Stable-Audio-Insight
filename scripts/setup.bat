@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."
chcp 65001 >nul

echo ============================================================
echo   Stable Audio Insight - dependencies refresh
echo ============================================================
echo.
echo This script reinstalls Python deps into the existing project Python.
echo For the full first-time setup (Python + models + token) use install.bat.
echo.

set "ROOT=%CD%"
set "PORTABLE_DIR=%ROOT%\python-portable"
set "PY_BIN="
if exist "!PORTABLE_DIR!\python.exe" set "PY_BIN=!PORTABLE_DIR!\python.exe"
if not defined PY_BIN if exist "%ROOT%\.venv\Scripts\python.exe" set "PY_BIN=%ROOT%\.venv\Scripts\python.exe"

if not defined PY_BIN (
    echo No project Python found at python-portable\ or .venv\.
    echo Run install.bat first.
    pause
    exit /b 1
)

echo Using: !PY_BIN!
echo.
echo [1/2] Upgrading pip + installing PyTorch...
"!PY_BIN!" -m pip install --upgrade pip wheel
nvidia-smi >nul 2>&1
if not errorlevel 1 (
    echo NVIDIA GPU detected - torch with CUDA 12.8...
    "!PY_BIN!" -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
) else (
    echo No NVIDIA GPU detected - CPU torch...
    "!PY_BIN!" -m pip install torch torchaudio
)
if errorlevel 1 (
    echo ERROR: torch install failed.
    pause
    exit /b 1
)

echo.
echo [2/2] Installing remaining dependencies from requirements.txt...
"!PY_BIN!" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: deps install failed.
    pause
    exit /b 1
)

echo.
echo Done. Use run.bat to start the app.
pause
