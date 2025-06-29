#!/bin/bash

# DigitalOcean App Platform startup script
echo "🚀 Starting Image Classification App..."

# Update system packages
apt-get update

# Install system dependencies for OpenCV and Tesseract
apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgthread-2.0-0

echo "✅ System dependencies installed"

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

echo "✅ Python dependencies installed"

# Create uploads directory
mkdir -p uploads

echo "✅ Setup complete, starting application..."

# Start the application
exec gunicorn --config gunicorn_config.py app:app
