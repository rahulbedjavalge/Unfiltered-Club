#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For Unix/Linux
# .\venv\Scripts\activate  # For Windows (uncomment this line and comment the above line)

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please update .env with your credentials"
fi

# Create Streamlit secrets if not exists
if [ ! -f .streamlit/secrets.toml ]; then
    echo "Creating Streamlit secrets..."
    mkdir -p .streamlit
    cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    echo "Please update .streamlit/secrets.toml with your credentials"
fi

# Run database migrations if needed
# Add your database migration commands here

echo "Setup complete! You can now run the app with:"
echo "streamlit run app.py"
