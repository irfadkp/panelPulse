#!/bin/bash

# PanelPulse Web Application Startup Script
# This script starts both the Flask backend and React frontend

set -e

echo "🚀 Starting PanelPulse Web Application"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo "✓ Node.js found: $(node --version)"
echo "✓ npm found: $(npm --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -q -r requirements.txt 2>/dev/null || {
    echo "⚠️  Installing with --user flag..."
    pip3 install --user -q -r requirements.txt
}

# Install Node dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing Node dependencies (this may take a few minutes)..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "✅ All dependencies installed!"
echo ""
echo "🎯 Starting services..."
echo "   Backend (Flask): http://localhost:5000"
echo "   Frontend (React): http://localhost:3000"
echo ""
echo "📱 Open http://localhost:3000 in your browser"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Flask backend in background
echo "🔧 Starting Flask backend..."
python3 app.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start React frontend in background
echo "⚛️  Starting React frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

# Made with Bob
