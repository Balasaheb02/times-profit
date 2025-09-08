@echo off
echo 📥 Installing DBeaver - Universal Database Tool
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo.
echo 🖥️  WINDOWS INSTALLATION OPTIONS:
echo.
echo Option 1: Download from Official Website
echo   1. Go to: https://dbeaver.io/download/
echo   2. Click "Download" for Windows
echo   3. Choose "DBeaver Community Edition" (Free)
echo   4. Run the installer and follow the setup wizard
echo.

echo Option 2: Using Chocolatey (if you have it)
echo   choco install dbeaver
echo.

echo Option 3: Using Winget (Windows Package Manager)
echo   winget install dbeaver.dbeaver
echo.

echo Option 4: Portable Version
echo   1. Download portable ZIP from https://dbeaver.io/download/
echo   2. Extract to a folder
echo   3. Run dbeaver.exe
echo.

echo 🍎 macOS Installation:
echo   brew install --cask dbeaver-community
echo.

echo 🐧 Linux Installation:
echo   # Ubuntu/Debian:
echo   sudo snap install dbeaver-ce
echo   # Or download .deb from https://dbeaver.io/download/
echo.

echo ✅ RECOMMENDED: Download from official website for latest version
echo    https://dbeaver.io/download/
echo.

echo 📋 System Requirements:
echo   • Java 11+ (usually included with DBeaver)
echo   • 2GB RAM minimum
echo   • Windows 7+ / macOS 10.12+ / Linux
echo.

pause
