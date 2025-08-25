@echo off
setlocal
cd /d %~dp0

REM 1) Use Python inside venv
set "PY=%~dp0venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [ERROR] Missing venv Python: "%PY%"
  echo Create venv:  python -m venv venv
  echo Install deps: venv\Scripts\pip install pydantic
  exit /b 1
)

REM 2) Input/Output
set "INPUT=%~dp0queries.csv"
set "OUT=%~dp0exports\results.csv"
set "ERR=%~dp0exports\errors.json"

REM 3) Run offline batch (no keys, no network)
"%PY%" "%~dp0structured_batch_validated.py" --input "%INPUT%" --out "%OUT%" --errors "%ERR%" --top_k 3
if errorlevel 1 (
  echo [FAIL] Batch failed. See "%ERR%"
  exit /b %errorlevel%
)

echo [OK] Done.
echo Outputs:
echo   %OUT%
echo   %~dp0exports\results.json
echo   %~dp0exports\errors.json
endlocal
