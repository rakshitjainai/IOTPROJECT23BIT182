@echo off
title AeroSense IoT - Project Launcher
color 0b

echo =====================================================================
echo           AeroSense IoT: ESP32 Climate & Air Quality Station
echo =====================================================================
echo.

:: Ensure we are running in the script's directory
cd /d "%~dp0"

echo [*] Checking Backend environment...
if not exist "backend\.venv\Scripts\python.exe" (
    echo [!] Virtual environment not found. Setting up backend environment...
    cd backend
    python -m venv .venv
    call .venv\Scripts\pip install -r requirements.txt
    cd ..
)

echo [*] Checking Frontend dependencies...
if not exist "frontend\node_modules" (
    echo [!] Node modules not found. Running npm install...
    cd frontend
    call npm install
    cd ..
)

echo [*] Launching FastAPI Backend Server on port 8000...
start "AeroSense - FastAPI Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"

echo [*] Launching React Vite Frontend Dashboard on port 5173...
start "AeroSense - React Dashboard" cmd /k "cd /d %~dp0frontend && npm run dev"

echo [*] Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak >nul

echo [*] Opening Dashboard in your default browser...
start http://localhost:5173

echo.
echo =====================================================================
echo [OK] Both servers are now running in separate terminal windows!
echo.
echo  - Dashboard: http://localhost:5173
echo  - Backend API: http://localhost:8000
echo  - API Docs:   http://localhost:8000/docs
echo.
echo To stop the servers, simply close the opened terminal windows 
echo or run stop_servers.bat.
echo =====================================================================
echo.
pause
