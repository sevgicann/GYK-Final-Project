@echo off
echo ========================================
echo    TerraMind Full Stack Starter
echo    Backend (Docker) + Frontend (Flutter)
echo ========================================
echo.

echo [1/3] Starting Backend with Docker...
cd backend
start "TerraMind Backend" cmd /k "docker-compose up"
timeout /t 10 /nobreak >nul
echo.

echo [2/3] Waiting for backend to be ready...
timeout /t 5 /nobreak >nul
echo.

echo [3/3] Starting Frontend (Flutter Web)...
cd ..\frontend
start "TerraMind Frontend" cmd /k "flutter run -d chrome --web-port=8080"
echo.

cd ..
echo ========================================
echo    Full Stack Started!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Press any key to return...
pause >nul

