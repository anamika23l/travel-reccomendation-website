@echo off
REM 🌍 TravelAI Website - Windows Quick Start

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  TravelAI Website Setup                        ║
echo ║             Professional Travel Booking Platform              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📦 Installing dependencies...
python -m pip install -r requirements.txt --quiet
echo ✅ Dependencies installed!
echo.

echo 💾 Initializing database...
python init_db.py
echo.

echo 🚀 Starting TravelAI Server...
echo.
echo 🌐 Website is now RUNNING at:
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
