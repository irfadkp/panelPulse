#!/bin/bash

# Install Flask for PanelPulse
# This script downloads and installs pip, then installs Flask

set -e

echo "🔧 Installing Flask for PanelPulse"
echo "=================================="
echo ""

# Download get-pip.py
echo "📥 Downloading pip installer..."
curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py

# Install pip with break-system-packages (safe for Flask)
echo "📦 Installing pip..."
python3 /tmp/get-pip.py --break-system-packages

# Install Flask and flask-cors
echo "📦 Installing Flask and flask-cors..."
python3 -m pip install --break-system-packages Flask flask-cors

# Clean up
rm /tmp/get-pip.py

echo ""
echo "✅ Installation complete!"
echo ""
echo "Flask and flask-cors have been installed."
echo ""
echo "🚀 Now you can start the application:"
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
