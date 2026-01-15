#!/bin/bash

# Setup script for Local Podcast Agent

echo "Local Podcast Agent Setup Script"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm and try again."
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed. Installing FFmpeg..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo "Please install FFmpeg manually for your operating system."
        exit 1
    fi
fi

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting up frontend..."
cd web
npm install

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Open a terminal and run the API server:"
echo "   cd /path/to/local-podcast-agent"
echo "   source .venv/bin/activate"
echo "   python api.py"
echo ""
echo "2. Open another terminal and run the web interface:"
echo "   cd /path/to/local-podcast-agent/web"
echo "   npm run dev"
echo ""
echo "3. Access the application at http://localhost:3000"
echo ""
echo "Note: Make sure Ollama is running with a model pulled (e.g., 'ollama pull qwen2.5:0.5b')"