#!/bin/bash

echo "🚀 Setting up Math Routing Agent Backend..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the backend:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
