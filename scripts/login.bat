@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."
chcp 65001 >nul

set "ROOT=%CD%"
set "HF_HOME=%ROOT%\hf-cache"

set "HF_BIN="
if exist "%ROOT%\python-portable\Scripts\hf.exe" set "HF_BIN=%ROOT%\python-portable\Scripts\hf.exe"
if not defined HF_BIN if exist "%ROOT%\.venv\Scripts\hf.exe" set "HF_BIN=%ROOT%\.venv\Scripts\hf.exe"

if not defined HF_BIN (
    echo ERROR: hf CLI not found. Run install.bat first.
    pause
    exit /b 1
)

echo Get a token: https://huggingface.co/settings/tokens
echo Accept license: https://huggingface.co/stabilityai/stable-audio-open-1.0
echo.
"!HF_BIN!" auth login
pause
