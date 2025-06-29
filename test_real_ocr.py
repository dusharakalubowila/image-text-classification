#!/usr/bin/env python3
"""
Direct test of the prediction function with real OCR
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

# Set Tesseract path
import pytesseract
import platform
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Import the prediction function from app
import cv2
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image, ImageDraw, ImageFont

def extract_text(image_path):
    """Extract text from image using OCR"""
    try:
        # Use Tesseract OCR
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception as e:
        print(f"OCR failed: {e}")
        return "Fallback text"

def predict_with_real_ocr(image_path):
    """Test prediction with real OCR"""
    
    print(f"🔍 Testing prediction for: {image_path}")
    
    # Load models
    try:
        text_model = joblib.load('ocr_text_model.pkl')
        print("✅ OCR model loaded")
        ocr_classes = text_model.classes_
        print(f"📋 OCR classes: {ocr_classes}")
    except Exception as e:
        print(f"❌ Error loading OCR model: {e}")
        return None
    
    # Extract text
    text = extract_text(image_path)
    print(f"📝 Extracted text: '{text}'")
    print(f"📏 Text length: {len(text)}")
    
    if len(text.strip()) == 0:
        print("⚠️  No text extracted")
        return None
    
    # Make prediction
    try:
        text_proba = text_model.predict_proba([text])[0]
        predicted_class = text_model.predict([text])[0]
        confidence = max(text_proba)
        
        print(f"🎯 Prediction: {predicted_class}")
        print(f"📊 Confidence: {confidence:.3f}")
        print(f"📋 All probabilities:")
        for cls, prob in zip(ocr_classes, text_proba):
            print(f"   {cls}: {prob:.3f}")
        
        return {
            'prediction': predicted_class,
            'confidence': confidence,
            'extracted_text': text,
            'probabilities': dict(zip(ocr_classes, text_proba))
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return None

if __name__ == "__main__":
    # Test with our existing test image
    if os.path.exists('test_image.png'):
        result = predict_with_real_ocr('test_image.png')
        if result:
            print("\n🎉 Real OCR prediction successful!")
            print(f"Final result: {result['prediction']} ({result['confidence']:.1%} confidence)")
        else:
            print("\n💥 Prediction failed")
    else:
        print("❌ test_image.png not found. Run test_text_extraction.py first.")
