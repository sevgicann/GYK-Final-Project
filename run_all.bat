@echo off
cls
echo ========================================
echo    TERRAMIND - FULL STACK STARTER
echo ========================================
echo.
echo [1/2] Backend baslatiliyor...
start "Terramind Backend" cmd /k "cd backend && py run.py"

echo.
echo Backend baslatildi! 3 saniye bekleniyor...
timeout /t 3 /nobreak > nul

echo.
echo [2/2] Frontend baslatiliyor...
echo.

REM Flutter kurulu mu kontrol et
where flutter >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Flutter bulundu! Frontend baslatiliyor...
    start "Terramind Frontend" cmd /k "cd frontend && flutter run -d chrome --web-port=8080"
    echo.
    echo ========================================
    echo   BASARILI!
    echo ========================================
    echo.
    echo Backend:  http://localhost:5000
    echo Frontend: http://localhost:8080
    echo.
    echo Her iki servis ayri pencerelerde calisiyor.
    echo Durdurmak icin her iki pencerede Ctrl+C basin.
) else (
    echo.
    echo [UYARI] Flutter kurulu degil!
    echo.
    echo Sadece Backend baslatildi: http://localhost:5000
    echo.
    echo Frontend icin Flutter kurmaniz gerekiyor:
    echo   https://flutter.dev/docs/get-started/install/windows
    echo.
    echo Veya backend API'yi Postman/Thunder Client ile test edebilirsiniz.
)

echo.
echo ========================================
pause


