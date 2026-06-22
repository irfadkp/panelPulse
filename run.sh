#!/bin/bash

# Simple PanelPulse Startup Script (No Virtual Environment)
# Run backend and frontend in separate terminals

echo "🚀 PanelPulse Web Application"
echo "=============================="
echo ""

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js required"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm required"; exit 1; }

echo "✓ All dependencies found"
echo ""

# Install Python packages
echo "📦 Installing Python packages..."
pip3 install --user Flask flask-cors 2>/dev/null || pip3 install Flask flask-cors

# Install Node packages if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing Node packages (first time only)..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 To start the application, run these commands in separate terminals:"
echo ""
echo "   Terminal 1 (Backend):"
echo "   cd /root/panelpulse && python3 app.py"
echo ""
echo "   Terminal 2 (Frontend):"
echo "   cd /root/panelpulse/frontend && npm run dev"
echo ""
echo "   Then open: http://localhost:3000"
echo ""

# Made with Bob
