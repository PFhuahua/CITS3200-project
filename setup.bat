@echo off
REM CITS3200 Project Setup Script for Windows
REM This script initializes both frontend and backend environments

setlocal enabledelayedexpansion

echo 🚀 Starting CITS3200 Project Setup...
echo ======================================

REM Check if we're in the right directory
if not exist "Frontend\" (
    echo [ERROR] Frontend directory not found. Please run this script from the CITS3200-project root directory
    pause
    exit /b 1
)

if not exist "Backend\" (
    echo [ERROR] Backend directory not found. Please run this script from the CITS3200-project root directory
    pause
    exit /b 1
)

REM Backend Setup
echo.
echo [INFO] Setting up Backend (Python Virtual Environment)...
echo ==================================================

cd Backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo [INFO] Python version:
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
if exist "requirements.txt" (
    echo [INFO] Installing Python dependencies from requirements.txt...
    pip install -r requirements.txt
    echo [SUCCESS] Python dependencies installed
) else (
    echo [WARNING] requirements.txt not found in Backend directory
)

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo [SUCCESS] Backend setup completed!

REM Frontend Setup
echo.
echo [INFO] Setting up Frontend (Node.js Dependencies)...
echo ==============================================

cd ..\Frontend

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

echo [INFO] Node.js version:
node --version

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo [INFO] npm version:
npm --version

REM Install dependencies
if exist "package.json" (
    echo [INFO] Installing Node.js dependencies...
    npm install
    echo [SUCCESS] Node.js dependencies installed
) else (
    echo [WARNING] package.json not found in Frontend directory
)

echo [SUCCESS] Frontend setup completed!

REM Final instructions
echo.
echo 🎉 Setup Complete!
echo ==================
echo [SUCCESS] Both frontend and backend have been initialized successfully!

echo.
echo 📝 Next Steps:
echo -------------
echo To run the backend:
echo   cd Backend
echo   venv\Scripts\activate.bat  # Activate virtual environment
echo   python start_api.py        # Start the backend server

echo.
echo To run the frontend:
echo   cd Frontend
echo   npm run dev               # Start the development server

echo.
echo To run both simultaneously, open two command prompt windows and run the commands above in each.

echo [SUCCESS] Happy coding! 🚀

cd ..
pause
