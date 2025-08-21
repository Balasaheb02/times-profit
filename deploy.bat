@echo off
REM Production deployment script for Windows
echo 🚀 Starting production deployment...

REM Check if required tools are installed
echo 🔍 Checking dependencies...

where heroku >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Heroku CLI is not installed. Please install it first.
    exit /b 1
)

where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Vercel CLI is not installed. Installing...
    npm install -g vercel
)

where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git is not installed. Please install it first.
    exit /b 1
)

echo ✅ All dependencies are installed

REM Get app name from user
set /p HEROKU_APP_NAME=Enter your Heroku app name: 

if "%HEROKU_APP_NAME%"=="" (
    echo ❌ App name is required
    exit /b 1
)

REM Deploy backend
echo 🔧 Deploying backend to Heroku...
cd backend

REM Create Heroku app
heroku create %HEROKU_APP_NAME% 2>nul

REM Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini --app %HEROKU_APP_NAME% 2>nul

REM Set environment variables
echo ✅ Setting environment variables...
heroku config:set FLASK_ENV=production --app %HEROKU_APP_NAME%
heroku config:set SECRET_KEY=your-secret-key-here --app %HEROKU_APP_NAME%
heroku config:set JWT_SECRET_KEY=your-jwt-secret-here --app %HEROKU_APP_NAME%

REM Deploy to Heroku
echo ✅ Deploying to Heroku...
git add .
git commit -m "Deploy backend to production"
git push heroku main

REM Run database setup
echo ✅ Setting up database...
heroku run python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()" --app %HEROKU_APP_NAME%
heroku run python add_comprehensive_dummy_data.py --app %HEROKU_APP_NAME%

cd ..

REM Deploy frontend
echo 🎨 Deploying frontend to Vercel...

REM Update environment variables
echo NEXT_PUBLIC_API_URL=https://%HEROKU_APP_NAME%.herokuapp.com/api > .env.production
echo NEXT_PUBLIC_SITE_URL=https://your-domain.vercel.app >> .env.production

REM Deploy to Vercel
vercel --prod

echo 🎉 Deployment completed successfully!
echo 📱 Backend URL: https://%HEROKU_APP_NAME%.herokuapp.com
echo 🌐 Frontend URL: Check Vercel output above

pause
