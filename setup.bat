@echo off
REM Windows setup script for Unfiltered Club

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is required but not installed. Please install Python and try again.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from example...
    copy .env.example .env
    echo Please update .env with your credentials
)

REM Create Streamlit secrets if not exists
if not exist .streamlit\secrets.toml (
    echo Creating Streamlit secrets...
    if not exist .streamlit mkdir .streamlit
    copy .streamlit\secrets.toml.example .streamlit\secrets.toml
    echo Please update .streamlit/secrets.toml with your credentials
)

echo Setup complete! You can now run the app with:
echo streamlit run app.py
pause
