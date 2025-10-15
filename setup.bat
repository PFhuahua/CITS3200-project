@echo off
REM ===========================================================
REM 🚀 Cascading Search Feature - Backend Setup
REM ===========================================================

setlocal enabledelayedexpansion

echo ===============================================
echo 🚀 Starting Backend Setup...
echo ===============================================

REM --- Step 1: Ensure .env file exists ---
if not exist ".env" (
    echo [INFO] .env file not found. Creating default .env...
    (
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo SEARCH_ID=your_google_search_engine_id_here
        echo DATABASE_URL=mysql+pymysql://root:3200@localhost:3306/project
    ) > .env
    echo [SUCCESS] Default .env file created.
    echo ⚠️  Please edit .env and add your real API keys if needed.
) else (
    echo [INFO] .env already exists. Skipping creation.
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

echo.
echo [SUCCESS] Backend setup complete. Keep this window open to monitor logs.
pause