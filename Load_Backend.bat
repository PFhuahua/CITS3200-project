@echo off
REM ===========================================================
REM 🚀 Cascading Search Feature - Backend Setup
REM ===========================================================

setlocal enabledelayedexpansion

echo ===============================================
echo 🚀 Starting Backend Setup...
echo ===============================================

REM --- Step 1: Ensure .env file exists in Backend ---
if not exist "Backend\.env" (
    echo [INFO] .env file not found in Backend. Creating default .env...
    (
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo SEARCH_ID=your_google_search_engine_id_here
        echo DATABASE_URL=mysql+pymysql://root:3200@localhost:3306/project
    ) > Backend\.env
    echo [SUCCESS] Default .env file created in Backend.
    echo ⚠️  Please edit Backend\.env and add your real API keys if needed.
) else (
    echo [INFO] Backend\.env already exists. Skipping creation.
)

REM --- Step 2: Start Docker containers in foreground ---
echo.
echo [INFO] Starting Docker containers (backend + database)...
echo [NOTE] This window will show backend logs. Press CTRL+C to stop.
echo =============================================================
docker-compose up --build

REM --- Step 3: Import Initial Data ---
echo.
echo [INFO] Importing libraries and bureaus...
docker-compose exec backend python -c "import requests; requests.post('http://localhost:8000/api/import-libraries'); requests.post('http://localhost:8000/api/import-bureaus')"

REM --- Step 4: Check Node.js installation and install if missing ---
echo.
node --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Node.js not found. Installing via winget...
    winget install --id=OpenJS.NodeJS -e --silent
    if errorlevel 1 (
        echo [ERROR] Node.js installation failed. Please install manually from https://nodejs.org/
        pause
        exit /b 1
    )
) else (
    echo [INFO] Node.js version:
    node --version
)

REM --- Step 5: Check npm installation ---
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm not found. Node.js installation may have failed.
    pause
    exit /b 1
) else (
    echo [INFO] npm version:
    npm --version
)

echo.
echo [SUCCESS] Backend setup complete. Keep this window open to monitor logs.
pause