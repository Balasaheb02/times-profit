@echo off
echo 🚀 Deploying Missing API Routes to Backend
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo ✅ Added Missing Routes:
echo   📰 /api/articles/recent-with-main - For recent articles component
echo   📊 /api/homepage - Homepage data endpoint  
echo   📝 /api/homepage/metadata - Homepage SEO metadata
echo   🔍 /api/articles/by-category-slug - Articles by category
echo   📊 /api/articles/count - Article count
echo   📋 /api/articles/by-slugs - Multiple articles by slug
echo.

echo 📋 TO DEPLOY THESE CHANGES:
echo.
echo 1. 📤 Upload new files to your VPS:
echo    - backend/app/routes/articles.py (updated)
echo    - backend/app/routes/homepage.py (new)
echo    - backend/app/__init__.py (updated)
echo.
echo 2. 🔄 SSH into your VPS and restart backend:
echo.
echo    ssh newsapp@your-vps-ip
echo    cd /home/newsapp/times-profit/backend
echo    
echo    # If using Git:
echo    git pull origin main
echo    
echo    # Or manually copy the files, then restart:
echo    sudo systemctl restart newsapp
echo    sudo systemctl status newsapp
echo.
echo 3. ✅ Test the new endpoints:
echo    curl http://api.timesprofit.com/api/homepage
echo    curl "http://api.timesprofit.com/api/articles/recent-with-main?locale=en&skip=1&first=3"
echo    curl "http://api.timesprofit.com/api/homepage/metadata?locale=en"
echo.

echo 🌟 AFTER DEPLOYMENT:
echo   ✅ Your frontend will connect to real backend APIs
echo   ✅ No more 404 errors for homepage and articles
echo   ✅ Real data instead of dummy data fallbacks
echo   ✅ Full-stack application working perfectly!
echo.

echo 🔧 ALTERNATIVE - Quick Git Deployment:
echo   1. git add .
echo   2. git commit -m "Add missing API endpoints for frontend"
echo   3. git push origin main
echo   4. SSH to VPS: git pull origin main && sudo systemctl restart newsapp
echo.
pause
