#!/bin/bash

# PanelPulse AI Startup Script
# Starts the AI-powered interview system with IBM watsonx.ai

set -e

echo "🚀 PanelPulse AI - Starting..."
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your IBM watsonx.ai credentials:"
    echo "   - WATSONX_API_KEY (from https://cloud.ibm.com/iam/apikeys)"
    echo "   - WATSONX_PROJECT_ID (from https://dataplatform.cloud.ibm.com/wx/home)"
    echo ""
    echo "   Then run this script again."
    exit 1
fi

# Check if credentials are set
source .env
if [ "$WATSONX_API_KEY" = "your_ibm_cloud_api_key_here" ] || [ -z "$WATSONX_API_KEY" ]; then
    echo "❌ Error: WATSONX_API_KEY not configured in .env"
    echo "   Please edit .env and add your IBM Cloud API key"
    exit 1
fi

if [ "$WATSONX_PROJECT_ID" = "your_watsonx_project_id_here" ] || [ -z "$WATSONX_PROJECT_ID" ]; then
    echo "❌ Error: WATSONX_PROJECT_ID not configured in .env"
    echo "   Please edit .env and add your watsonx.ai project ID"
    exit 1
fi

echo "✓ Credentials configured"
echo ""

# Check Python dependencies
echo "📦 Checking dependencies..."
python3 -c "import flask, flask_cors, requests" 2>/dev/null || {
    echo "⚠️  Installing missing dependencies..."
    pip3 install --break-system-packages Flask flask-cors requests
}

echo "✓ Dependencies ready"
echo ""

# Kill any existing processes
pkill -9 -f "python3 app_ai.py" 2>/dev/null || true
pkill -9 -f "vite" 2>/dev/null || true
sleep 1

# Start backend
echo "🤖 Starting AI-powered backend..."
python3 app_ai.py > /tmp/panelpulse_ai_backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start. Check logs:"
    tail -20 /tmp/panelpulse_ai_backend.log
    exit 1
fi

echo "✓ Backend running (PID: $BACKEND_PID)"

# Start frontend
echo "⚛️  Starting frontend..."
cd frontend
npm run dev > /tmp/panelpulse_ai_frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 2

echo ""
echo "================================"
echo "✅ PanelPulse AI is running!"
echo "================================"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:5000"
echo "🤖 AI:       IBM watsonx.ai"
echo ""
echo "📋 Backend PID:  $BACKEND_PID"
echo "📋 Frontend PID: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f /tmp/panelpulse_ai_backend.log"
echo "   Frontend: tail -f /tmp/panelpulse_ai_frontend.log"
echo ""
echo "🛑 To stop: pkill -f 'python3 app_ai.py' && pkill -f vite"
echo ""

# Made with Bob
