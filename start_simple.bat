@echo off
echo ========================================
echo    Terramind Simple Docker Setup
echo ========================================
echo.

echo [1/3] Starting database and backend...
cd backend
docker-compose up -d db redis backend

echo.
echo [2/3] Waiting for backend to be ready...
timeout /t 10 /nobreak > nul

echo.
echo [3/3] Starting Flutter web development server...
docker-compose up -d frontend

echo.
echo ========================================
echo    Services Started Successfully!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo.
echo To view logs:
echo   docker-compose logs -f frontend
echo.
echo To stop all services:
echo   docker-compose down
echo.
pause
