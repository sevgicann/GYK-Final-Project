@echo off
chcp 65001 >nul
cls
echo ========================================
echo    TERRAMIND UYGULAMASI
echo ========================================
echo.
echo TEST KULLANICI BILGILERI:
echo -------------------------
echo Email: test@gmail.com
echo Sifre: 123456
echo -------------------------
echo.
echo.
echo [1] Backend baslatiliyor...
start "Terramind Backend" cmd /k "cd /d C:\Users\sevgi\GYK-Final-Project\backend && py run.py"

timeout /t 3 /nobreak >nul

echo [2] Frontend baslatiliyor...
start "Terramind Frontend" cmd /k "cd /d C:\Users\sevgi\GYK-Final-Project\frontend && flutter run -d chrome --web-port=8080"

echo.
echo ========================================
echo   SERVISLER BASLATILDI!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Login bilgileri:
echo   Email: test@gmail.com
echo   Sifre: 123456
echo.
echo ========================================
pause


