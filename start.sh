#!/bin/bash

echo "🏦 Starting Personal Finance Agent..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from example..."
    cp .env.example .env
    echo "🔧 Please edit .env file with your Plaid API credentials before connecting real bank accounts."
    echo "💡 You can still use demo mode without API credentials!"
fi

# Start the application
echo "🚀 Starting the application..."
echo "🌐 Open http://localhost:5000 in your browser"
echo "🎮 Click 'Try Demo' to test with sample data"
echo "🔗 Click 'Connect Bank' to link real accounts (requires Plaid API setup)"
echo ""

python app.py