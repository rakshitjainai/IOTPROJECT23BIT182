@echo off
title AeroSense IoT - Stop Servers
color 0c

echo =====================================================================
echo           AeroSense IoT: Stopping All Running Servers
echo =====================================================================
echo.

echo [*] Terminating Python/Uvicorn Backend on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [*] Terminating Vite/Node Frontend on port 5173...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [OK] All IoT server instances have been stopped.
echo =====================================================================
echo.
timeout /t 3
