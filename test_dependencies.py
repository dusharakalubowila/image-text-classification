#!/usr/bin/env python3
"""
Quick test to verify models and dependencies
"""

print("🧪 Testing dependencies and models...")

try:
    import cv2
    print("✅ OpenCV imported successfully")
except Exception as e:
    print(f"❌ OpenCV error: {e}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__} imported successfully")
except Exception as e:
    print(f"❌ NumPy error: {e}")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__} imported successfully")
except Exception as e:
    print(f"❌ TensorFlow error: {e}")

try:
    import joblib
    print("✅ Joblib imported successfully")
except Exception as e:
    print(f"❌ Joblib error: {e}")

try:
    import pytesseract
    print("✅ Pytesseract imported successfully")
except Exception as e:
    print(f"❌ Pytesseract error: {e}")

try:
    from flask import Flask
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask error: {e}")

# Test model loading
print("\n🤖 Testing model loading...")

try:
    import os
    if os.path.exists('ocr_text_model.pkl'):
        model = joblib.load('ocr_text_model.pkl')
        print("✅ OCR text model loaded successfully")
    else:
        print("⚠️  OCR text model file not found")
except Exception as e:
    print(f"❌ OCR model error: {e}")

try:
    if os.path.exists('image_model.h5'):
        from tensorflow.keras.models import load_model
        model = load_model('image_model.h5')
        print("✅ CNN image model loaded successfully")
    else:
        print("⚠️  CNN image model file not found")
except Exception as e:
    print(f"❌ CNN model error: {e}")

print("\n🎯 Test complete!")
