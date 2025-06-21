@echo off
echo 🧠 Starting Unfiltered Club...
echo.

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo ⚠️  Virtual environment not detected. Activating...
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        echo ✅ Virtual environment activated
    ) else (
        echo ❌ Virtual environment not found. Please run: python -m venv venv
        pause
        exit /b 1
    )
)

REM Check if packages are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo 📋 Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo ❗ Please edit .env file with your actual credentials before running again
    echo.
    pause
    exit /b 1
)

echo 🚀 Starting Streamlit app...
echo 📱 The app will open in your browser at http://localhost:8501
echo 🔄 Press Ctrl+C to stop the server
echo.

streamlit run app.py
