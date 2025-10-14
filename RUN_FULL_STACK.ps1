# TerraMind Full Stack Starter
# Backend (Docker) + Frontend (Flutter)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TerraMind Full Stack Starter" -ForegroundColor Green
Write-Host "   Backend (Docker) + Frontend (Flutter)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Backend'i Docker ile başlat
Write-Host "[1/3] Starting Backend with Docker..." -ForegroundColor Yellow
Set-Location backend

# Yeni PowerShell penceresinde backend başlat
Start-Process powershell -ArgumentList "-NoExit", "-Command", "docker-compose up"

Write-Host "   Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 15

Set-Location ..

# 2. Frontend'i Flutter ile başlat
Write-Host "[2/3] Starting Frontend (Flutter Web)..." -ForegroundColor Yellow
Set-Location frontend

# Yeni PowerShell penceresinde frontend başlat
Start-Process powershell -ArgumentList "-NoExit", "-Command", "flutter run -d chrome --web-port=8080"

Set-Location ..

# 3. Tamamlandı
Write-Host "[3/3] Full Stack Started!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Services Running:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend API:  http://localhost:5000" -ForegroundColor White
Write-Host "Frontend UI:  http://localhost:8080" -ForegroundColor White
Write-Host "ML Endpoints: http://localhost:5000/api/ml" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Log Monitoring:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "To monitor backend logs, run in new terminal:" -ForegroundColor Gray
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  docker-compose logs -f backend" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this script..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

