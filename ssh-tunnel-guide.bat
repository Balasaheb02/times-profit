@echo off
echo 🔒 Secure SSH Tunnel for Database Connection
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo.
echo This method is more secure than opening PostgreSQL to the internet
echo.

echo 📋 STEP 1: Create SSH Tunnel
echo.
echo Open PowerShell or Command Prompt and run:
echo.
echo ssh -L 5432:localhost:5432 newsapp@YOUR_VPS_IP
echo.
echo This creates a tunnel:
echo   Local Port 5432 → VPS localhost:5432
echo.

echo 📊 STEP 2: Configure DBeaver with SSH Tunnel
echo.
echo In DBeaver connection settings:
echo   Host: localhost
echo   Port: 5432
echo   Database: newsdb
echo   Username: newsuser
echo   Password: [from .env file]
echo.

echo 🔧 STEP 3: Alternative - DBeaver Built-in SSH
echo.
echo In DBeaver, use SSH tab:
echo   ☑ Use SSH Tunnel
echo   SSH Host: YOUR_VPS_IP
echo   SSH Port: 22
echo   SSH User: newsapp
echo   SSH Auth: Public Key or Password
echo.
echo   Then in Main tab:
echo   Host: localhost
echo   Port: 5432
echo.

echo ⚡ STEP 4: Keep Tunnel Active
echo.
echo The SSH tunnel must stay open while using DBeaver.
echo Leave the PowerShell/Terminal window open.
echo.

echo 🔒 SECURITY BENEFITS:
echo   ✅ No need to open PostgreSQL port 5432 to internet
echo   ✅ Encrypted connection through SSH
echo   ✅ Uses existing SSH access
echo   ✅ More secure for production environments
echo.

pause
