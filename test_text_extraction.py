#!/usr/bin/env python3
"""
Test script to debug the OCR text extraction and prediction
"""

import cv2
import pytesseract
import numpy as np
import joblib
from PIL import Image, ImageDraw, ImageFont
import io

def test_text_extraction():
    print("🔍 Testing Text Extraction...")
    
    # Create a test image with text
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    text = "Invoice #12345\nDate: 2025-01-15\nAmount: $299.99"
    
    try:
        # Try to use a font (fallback to default if not available)
        font = ImageFont.load_default()
        draw.text((20, 20), text, fill='black', font=font)
    except:
        draw.text((20, 20), text, fill='black')
    
    # Save the image
    img.save('test_image.png')
    print("✅ Test image created: test_image.png")
    
    # Test text extraction function
    def extract_text_test(image_path):
        """Test version of extract_text function"""
        try:
            # Try to use Tesseract OCR
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray)
            print(f"✅ Tesseract extraction: '{extracted_text.strip()}'")
            return extracted_text.strip()
        except pytesseract.TesseractNotFoundError:
            # Tesseract not installed - use mock text extraction
            print("⚠️  Tesseract OCR not found, using mock text extraction")
            
            # Generate mock text based on image filename or random text
            import random
            mock_texts = [
                "Invoice #12345\nDate: 2025-01-15\nAmount: $299.99\nTax: $30.00\nTotal: $329.99",
                "Shopping List:\n- Milk\n- Bread\n- Eggs\n- Butter\n- Cheese",
                "Meeting Notes\nDate: Today\nAttendees: John, Mary\nAction Items:\n- Review proposal",
                "STOP\nSpeed Limit\n25 MPH\nSchool Zone",
                "Application Form\nName: ___________\nDate: ___________\nSignature: ___________"
            ]
            mock_text = random.choice(mock_texts)
            print(f"🎭 Mock extraction: '{mock_text}'")
            return mock_text
        except Exception as e:
            print(f"❌ OCR failed: {e}")
            return "Mock extracted text for demo purposes"
    
    # Test extraction
    extracted_text = extract_text_test('test_image.png')
    print(f"📝 Final extracted text: '{extracted_text}'")
    print(f"📏 Text length: {len(extracted_text)}")
    
    # Test OCR model prediction
    print("\n🧪 Testing OCR model prediction...")
    try:
        model = joblib.load('ocr_text_model.pkl')
        
        if len(extracted_text.strip()) > 0:
            prediction = model.predict([extracted_text])[0]
            probabilities = model.predict_proba([extracted_text])[0]
            confidence = max(probabilities)
            
            print(f"🎯 Prediction: {prediction}")
            print(f"📊 Confidence: {confidence:.3f}")
            print(f"📋 Probabilities: {dict(zip(model.classes_, probabilities))}")
        else:
            print("❌ No text extracted - cannot make prediction")
            
    except Exception as e:
        print(f"❌ Error in OCR model prediction: {e}")
    
    return extracted_text

if __name__ == "__main__":
    test_text_extraction()
