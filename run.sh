#!/usr/bin/env bash

# Group 6: AI-Based Customer Support System - Startup Script
echo "==========================================================="
echo "  Starting ApexMart AI Customer Support System (Group 6)"
echo "  Stack: FastAPI REST Backend + Modern HTML/Tailwind UI"
echo "==========================================================="

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found. Creating and installing..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check for .env and API Keys
if [ -f ".env" ]; then
    if grep -q "NVIDIA_API_KEY=nvapi-" .env; then
        echo "✅ NVIDIA_API_KEY detected in .env"
        echo "   Active Model: nvidia/nemotron-3.5-super-vl-120b-a12b (Fastest & Verified)"
    elif grep -q "GEMINI_API_KEY=AIza" .env; then
        echo "✅ GEMINI_API_KEY detected in .env"
    else
        echo "ℹ️ Note: No active API key found in .env. Running in Demo Simulation Mode."
    fi
else
    echo "⚠️ .env file not found. Creating from template..."
    cp .env.example .env
fi

PORT=8000
echo ""
echo "🚀 Launching Web Application on: http://localhost:$PORT"
echo "   Press Ctrl+C to stop."
echo ""

# Run FastAPI server with uvicorn
python server.py
