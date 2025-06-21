#!/usr/bin/env pwsh

Write-Host "🧠 Starting Unfiltered Club..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected. Activating..." -ForegroundColor Yellow
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "❌ Virtual environment not found. Please run: python -m venv venv" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if packages are installed
try {
    python -c "import streamlit" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Streamlit not found"
    }
} catch {
    Write-Host "📦 Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install packages" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host "📋 Copying .env.example to .env..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "❗ Please edit .env file with your actual credentials before running again" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🚀 Starting Streamlit app..." -ForegroundColor Green
Write-Host "📱 The app will open in your browser at http://localhost:8501" -ForegroundColor Blue
Write-Host "🔄 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
