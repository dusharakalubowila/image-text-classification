#!/bin/bash
# Build script for DigitalOcean deployment

echo "🚀 Starting build process..."

# Update package lists
echo "📦 Installing system dependencies..."
apt-get update

# Install Tesseract OCR
echo "🔍 Installing Tesseract OCR..."
apt-get install -y tesseract-ocr tesseract-ocr-eng

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed successfully!"
