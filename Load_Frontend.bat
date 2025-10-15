@echo off
REM ===========================================================
REM 🚀 Cascading Search Feature - Frontend Launch
REM ===========================================================

echo ===============================================
echo 🚀 Starting Frontend...
echo ===============================================

REM --- Navigate to Frontend directory ---
cd Frontend

REM --- Install dependencies if needed ---
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies...
    npm install
)

REM --- Start frontend dev server ---
echo [INFO] Launching frontend dev server...
echo [NOTE] This window will stay open for frontend logs.
echo =============================================================
npm run dev

pause
