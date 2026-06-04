@echo off
REM Feedback Intelligence - Complete Startup Script for Windows

setlocal enabledelayedexpansion

echo.
echo 🚀 Feedback Intelligence - Startup Script
echo ==========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please copy .env.example to .env and configure it:
    echo   copy .env.example .env
    pause
    exit /b 1
)

echo 1. Starting Backend...
cd backend

REM Install dependencies
echo Installing backend dependencies...
pip install -q -r requirements.txt

echo ✓ Backend ready
echo Starting uvicorn server on http://localhost:8000...
start cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak

echo.
echo 2. Starting Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

echo ✓ Frontend ready
echo Starting Next.js dev server on http://localhost:3000...
start cmd /k "npm run dev"

cd ..

echo.
echo ✅ Both services are starting!
echo.
echo 📍 Frontend:  http://localhost:3000
echo 📍 Backend:   http://localhost:8000
echo 📍 API Docs:  http://localhost:8000/docs
echo.
echo Close the command windows to stop the services
echo.
pause