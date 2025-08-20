@echo off
echo Starting Flask Backend and Next.js Frontend...

echo.
echo Setting up Python virtual environment...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask backend...
start "Flask Backend" cmd /k "python run.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

cd ..
echo Starting Next.js frontend...
start "Next.js Frontend" cmd /k "yarn dev"

echo.
echo Both services are starting!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
