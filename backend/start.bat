@echo off
REM RadioX Backend Start Script (Windows)

echo 🚀 Starting RadioX Backend API...

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo 📝 Copy env.template to .env and add your API keys
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Start server
echo ✅ Starting server on http://localhost:8000
python main.py

