@echo off
echo Preparing for Vercel deployment...
echo.

echo 1. Cleaning up files...
if exist netlify.toml del netlify.toml
if exist "public\_redirects" del "public\_redirects"

echo 2. Installing dependencies...
npm install

echo 3. Testing build...
npm run build

echo.
if %ERRORLEVEL% == 0 (
    echo ✅ Build successful! Ready for deployment.
    echo.
    echo Next steps:
    echo 1. git add .
    echo 2. git commit -m "Ready for Vercel deployment"
    echo 3. git push origin main
    echo 4. Go to vercel.com and import your repository
) else (
    echo ❌ Build failed. Check the errors above.
)

pause
