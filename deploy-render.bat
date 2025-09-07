@echo off
echo Preparing for Render deployment...
echo.

echo ✅ Removed problematic routes:
echo - API routes (stockdaily, webhooks, og)
echo - Sitemap generation routes  
echo - Catch-all routes
echo - package-lock.json conflicts
echo.

echo 📦 Testing build...
call npm run build

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ Build successful! Ready for Render deployment.
    echo.
    echo 🚀 Next steps:
    echo 1. git add .
    echo 2. git commit -m "Simplified for Render deployment"
    echo 3. git push origin main
    echo 4. Go to render.com and create a new Web Service
    echo.
    echo 📋 Render Settings:
    echo Build Command: npm run build
    echo Start Command: npm start
    echo Environment: Node
    echo.
    echo Your site will be: https://times-profit.onrender.com
) else (
    echo.
    echo ❌ Build failed. Check the errors above.
)

echo.
pause
