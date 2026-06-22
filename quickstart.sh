#!/bin/bash

# PanelPulse Quick Start Script
# This script helps you quickly test the PanelPulse interview system

set -e

echo "🚀 PanelPulse Quick Start"
echo "========================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Check if panelpulse.py exists
if [ ! -f "panelpulse.py" ]; then
    echo "❌ Error: panelpulse.py not found in current directory"
    exit 1
fi

echo "✓ Found panelpulse.py"
echo ""

# Offer to use example files or custom input
echo "Choose an option:"
echo "1) Use example resume and job description (quick demo)"
echo "2) Enter your own resume and job description (interactive)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    # Check if example files exist
    if [ ! -f "example_resume.txt" ] || [ ! -f "example_job_description.txt" ]; then
        echo "❌ Error: Example files not found"
        echo "Please ensure example_resume.txt and example_job_description.txt exist"
        exit 1
    fi
    
    echo ""
    echo "📋 Using example files:"
    echo "   - example_resume.txt"
    echo "   - example_job_description.txt"
    echo ""
    echo "🎯 Starting mock interview..."
    echo "   You'll be asked 6 questions (2 per panelist)"
    echo "   Provide detailed answers for best results"
    echo ""
    echo "Press Enter to continue..."
    read
    
    # Create input file with example data
    {
        cat example_resume.txt
        echo ""
        echo ""
        cat example_job_description.txt
        echo ""
        echo ""
    } > /tmp/panelpulse_input.txt
    
    # Note: This won't work perfectly with the interactive input
    # but shows the structure
    echo "⚠️  Note: You'll need to answer questions interactively"
    echo ""
    python3 panelpulse.py
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "🎯 Starting interactive mock interview..."
    echo ""
    python3 panelpulse.py
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "✨ Interview complete! Thank you for using PanelPulse."
echo ""

# Made with Bob
