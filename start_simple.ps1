# Terramind Simple Docker Setup
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Terramind Simple Docker Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
Set-Location backend

Write-Host "[1/3] Starting database and backend..." -ForegroundColor Yellow
docker-compose up -d db redis backend

Write-Host ""
Write-Host "[2/3] Waiting for backend to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "[3/3] Starting Flutter web development server..." -ForegroundColor Yellow
docker-compose up -d frontend

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    Services Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "Backend API: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Gray
Write-Host "  docker-compose logs -f frontend" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop all services:" -ForegroundColor Gray
Write-Host "  docker-compose down" -ForegroundColor Gray
Write-Host ""

# Check if services are running
Write-Host "Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
