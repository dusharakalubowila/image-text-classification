#!/usr/bin/env python3
"""
Test script to verify OCR model functionality
"""

import joblib
import numpy as np

def test_ocr_model():
    print("🔍 Testing OCR Model...")
    
    try:
        # Load the model
        model = joblib.load('ocr_text_model.pkl')
        print("✅ Model loaded successfully")
        print(f"📋 Model type: {type(model)}")
        
        # Check model classes
        if hasattr(model, 'classes_'):
            classes = model.classes_
            print(f"📊 Model classes ({len(classes)}): {classes}")
        else:
            print("⚠️  Model has no classes_ attribute")
            return False
        
        # Test with sample texts
        test_texts = [
            "Invoice #12345\nDate: 2025-01-15\nAmount: $299.99\nTax: $30.00\nTotal: $329.99",
            "Shopping List:\n- Milk\n- Bread\n- Eggs\n- Butter\n- Cheese",
            "Meeting Notes\nDate: Today\nAttendees: John, Mary\nAction Items:\n- Review proposal",
            "Application Form\nName: ___________\nDate: ___________\nSignature: ___________",
            "Dear Sir/Madam,\nI am writing to inquire about...",
            "John Smith\nSoftware Engineer\nExperience: 5 years\nSkills: Python, JavaScript"
        ]
        
        print("\n🧪 Testing predictions:")
        for i, text in enumerate(test_texts):
            try:
                # Get prediction
                prediction = model.predict([text])[0]
                probabilities = model.predict_proba([text])[0]
                confidence = max(probabilities)
                
                print(f"Test {i+1}: '{text[:30]}...' -> {prediction} (confidence: {confidence:.3f})")
                print(f"  Probabilities: {dict(zip(classes, probabilities))}")
                
            except Exception as e:
                print(f"❌ Error in prediction {i+1}: {e}")
                return False
        
        print("\n✅ OCR model is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

if __name__ == "__main__":
    success = test_ocr_model()
    if success:
        print("\n🎉 OCR model test passed!")
    else:
        print("\n💥 OCR model test failed!")
