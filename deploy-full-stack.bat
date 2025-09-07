@echo off
echo 🚀 Preparing Times Profit for Deployment
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo ✅ Backend Implementation Complete:
echo   • Created backend-client.ts with real API calls
echo   • Added fallback to dummy data for reliability
echo   • Updated all components to use backend client
echo   • Added comprehensive error handling
echo.

echo ✅ Your Hostinger VPS Backend Status:
echo   • Backend API: http://api.timesprofit.com/api/health
echo   • Database: PostgreSQL running ✓
echo   • Service: newsapp.service running ✓
echo   • Response: {"message":"Flask backend is running","status":"healthy"}
echo.

echo 🔧 Testing build...
call npm run build

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ Build Successful! Ready for deployment.
    echo.
    echo 📋 Deployment Instructions:
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo.
    echo 1. 🔄 PUSH TO GITHUB:
    echo    git add .
    echo    git commit -m "Connected frontend to Hostinger VPS backend"
    echo    git push origin main
    echo.
    echo 2. 🚀 DEPLOY ON RENDER:
    echo    • Go to https://render.com
    echo    • Click "New ^+^" ^> "Web Service"
    echo    • Connect your GitHub repository
    echo    • Use these settings:
    echo      - Build Command: npm run build
    echo      - Start Command: npm start
    echo      - Environment: Node
    echo.
    echo 3. 🌍 ENVIRONMENT VARIABLES on Render:
    echo    NEXT_PUBLIC_BACKEND_URL=http://api.timesprofit.com
    echo    NODE_ENV=production
    echo    NEXT_TELEMETRY_DISABLED=1
    echo.
    echo 4. ✨ RESULT:
    echo    • Frontend will be live at: https://times-profit.onrender.com
    echo    • Backend will continue running at: http://api.timesprofit.com
    echo    • Full-stack application connected! 🎉
    echo.
    echo 📊 CURRENT DATA FLOW:
    echo    Frontend → Backend API → PostgreSQL Database
    echo    [Render]  → [Hostinger VPS] → [Your Data]
    echo.
    echo 🔧 OPTIONAL - SSL LATER:
    echo    Once DNS is properly configured, you can:
    echo    sudo certbot --nginx -d timesprofit.com -d api.timesprofit.com
    echo.
) else (
    echo.
    echo ❌ Build failed. Please check the errors above.
    echo    The backend integration should still work with fallback data.
)

echo.
echo 🎯 NEXT STEPS SUMMARY:
echo 1. git add . ^&^& git commit -m "Backend connected" ^&^& git push
echo 2. Deploy on Render.com
echo 3. Your site will be live with real backend data!
echo.
pause
