@echo off
:: ═══════════════════════════════════════════════════════════════════════════
:: Alasmia Windows Installer
:: ═══════════════════════════════════════════════════════════════════════════
:: Usage: Run this script to install Alasmia on Windows
:: Download from: https://github.com/alasmia/Alasmia/releases/latest
:: ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

set "BOLD=[1m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "RESET=[0m"

echo.
echo  [36m╔═══════════════════════════════════════════════════════════════════════╗[0m
echo  [36m║[0m                                                                       [36m║[0m
echo  [36m║[0m   [35m██████╗  █████╗ ██╗     ██╗████████╗ ██████╗ ██████╗ ██╗   ██╗[0m   [36m║[0m
echo  [36m║[0m  [35m██╔════╝ ██╔══██╗██║     ██║╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝[0m   [36m║[0m
echo  [36m║[0m  [35m██║  ███╗███████║██║     ██║   ██║   ██║   ██║██████╔╝ ╚████╔╝[0m    [36m║[0m
echo  [36m║[0m  [35m██║   ██║██╔══██║██║     ██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝[0m     [36m║[0m
echo  [36m║[0m   [35m╚██████╔╝██║  ██║███████╗██║   ██║   ╚██████╔╝██║  ██║   ██║[0m      [36m║[0m
echo  [36m║[0m   [35m╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝[0m      [36m║[0m
echo  [36m║[0m                                                                       [36m║[0m
echo  [36m║[0m                      [35m💜 Your AI Life Partner 💜[0m                       [36m║[0m
echo  [36m║[0m                                                                       [36m║[0m
echo  [36m╚═══════════════════════════════════════════════════════════════════════╝[0m
echo.

echo  [32m✓[0m Alasmia Windows Installer
echo.
echo  This script will:
echo    1. Check Python 3.10+ installation
echo    2. Create virtual environment
echo    3. Install dependencies
echo    4. Run setup wizard
echo.

:: ── Check Python ───────────────────────────────────────────────────────────
echo  [36m→[0m Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo  [31m✗[0m Python not found!
    echo.
    echo  Please install Python 3.10+ from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

for /f "delims=" %%i in ('python -c "import sys; print(f'%%sys.version_info.major%%.%%sys.version_info.minor%%')"') do set PYTHON_VERSION=%%i

echo  [32m✓[0m Python !PYTHON_VERSION! found

:: ── Create venv ─────────────────────────────────────────────────────────────
echo.
echo  [36m→[0m Creating virtual environment...

if exist "venv" (
    echo  [33m⚠[0m Virtual environment already exists
) else (
    python -m venv venv
    echo  [32m✓[0m Virtual environment created
)

:: ── Install dependencies ────────────────────────────────────────────────────
echo.
echo  [36m→[0m Installing dependencies...

call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo  [31m✗[0m Failed to install dependencies
    pause
    exit /b 1
)

echo  [32m✓[0m Dependencies installed

:: ── Create .env ─────────────────────────────────────────────────────────────
if not exist ".env" (
    copy .env.example .env >nul
    echo  [32m✓[0m .env file created
) else (
    echo  [33m⚠[0m .env already exists
)

:: ── Run setup wizard ─────────────────────────────────────────────────────────
echo.
echo  [32m✓[0m Installation complete!
echo.
echo  [36m→[0m Starting setup wizard...

python main.py setup

if errorlevel 1 (
    echo.
    echo  [31m✗[0m Setup failed
    pause
    exit /b 1
)

:: ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo  [32m
echo  ╔═══════════════════════════════════════════════════════════════════════╗
echo  ║                    ✅ Setup Complete! 💜                               ║
echo  ╠═══════════════════════════════════════════════════════════════════════╣
echo  ║                                                                       ║
echo  ║   To start Alasmia:                                                    ║
echo  ║     call venv\Scripts\activate.bat                                     ║
echo  ║     python main.py --platform cli                                      ║
echo  ║                                                                       ║
echo  ╚═══════════════════════════════════════════════════════════════════════╝
echo  [0m
pause