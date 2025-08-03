#!/bin/bash

# VulnShop Startup Script
# This script sets up and runs the vulnerable e-commerce lab

echo "=================================================="
echo "🔥 VulnShop - Vulnerable E-Commerce Lab Setup 🔥"
echo "=================================================="
echo "⚠️  WARNING: This contains intentional vulnerabilities!"
echo "⚠️  DO NOT use in production environments!"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p templates

echo "✅ Directories created"

# Start the application
echo "🚀 Starting VulnShop..."
echo ""
echo "📌 Access the application at: http://localhost:5000"
echo "📌 Use Ctrl+C to stop the application"
echo ""
echo "🎯 Default Credentials:"
echo "   Admin: admin / admin123"
echo "   User:  john_doe / password123"
echo ""
echo "🐛 Vulnerability Endpoints:"
echo "   • SQL Injection: /login"
echo "   • XSS: Product comments"
echo "   • IDOR: /receipt/<id>"
echo "   • CSRF: /change_password"
echo "   • Directory Traversal: /view_file?file="
echo "   • SSRF: /check_url"
echo "   • SSTI: /render_template"
echo "   • Command Injection: /ping"
echo "   • Admin Panel: /admin"
echo ""
echo "=================================================="

# Run the application
python3 app.py
