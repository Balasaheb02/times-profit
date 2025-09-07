@echo off
echo 🔄 Flask Backend Restart Instructions
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo The database admin routes need the backend to be restarted.
echo.
echo 📋 COPY AND RUN THESE COMMANDS ON YOUR VPS:
echo.
echo 1. SSH into your server:
echo    ssh newsapp@your-vps-ip
echo.
echo 2. Restart Flask backend:
echo    sudo systemctl restart newsapp
echo.
echo 3. Check status:
echo    sudo systemctl status newsapp
echo.
echo 4. Test database admin:
echo    curl http://api.timesprofit.com/api/admin/stats-json
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🌐 After restart, access your database admin at:
echo 📊 Dashboard: http://api.timesprofit.com/api/admin/db
echo 📋 Tables: http://api.timesprofit.com/api/admin/db/tables  
echo 📰 Articles: http://api.timesprofit.com/api/admin/db/table/articles
echo 🏷️ Categories: http://api.timesprofit.com/api/admin/db/table/categories
echo 👤 Authors: http://api.timesprofit.com/api/admin/db/table/authors
echo 📈 Statistics: http://api.timesprofit.com/api/admin/db/stats
echo.
echo 🔧 JSON APIs will also work:
echo http://api.timesprofit.com/api/admin/stats-json
echo http://api.timesprofit.com/api/admin/tables-json
echo http://api.timesprofit.com/api/admin/table-json/articles
echo.
pause
