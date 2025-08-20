# PowerShell script to start both backend and frontend
Write-Host "Starting Flask Backend and Next.js Frontend..." -ForegroundColor Green

# Setup Backend
Write-Host "`nSetting up Flask backend..." -ForegroundColor Yellow
Set-Location backend

if (!(Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Starting Flask backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python run.py"

# Setup Frontend
Write-Host "`nWaiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Set-Location ..
Write-Host "Starting Next.js frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; yarn dev"

Write-Host "`nBoth services are starting!" -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "`nCheck the opened terminal windows for logs and status updates." -ForegroundColor Yellow
