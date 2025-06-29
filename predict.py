#!/usr/bin/env python3
"""
Standalone prediction script for testing the models without Flask
"""

import cv2
import pytesseract
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os
import sys

def extract_text(image_path):
    """Extract text from image using OCR"""
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception as e:
        print(f"OCR failed: {e}")
        return ""

def predict_image(image_path, text_model, cnn_model):
    """Predict image class using ensemble of OCR and CNN"""
    
    # Class mapping (adjust based on your actual classes)
    classes = {0: 'form', 1: 'invoice', 2: 'list', 3: 'note', 4: 'sign'}
    
    try:
        # OCR prediction
        text = extract_text(image_path)
        text_length = len(text.strip())
        
        print(f"📄 Extracted text ({text_length} chars): {text[:100]}...")
        
        # Get text prediction probabilities
        if text_length > 0:
            text_proba = text_model.predict_proba([text])[0]
        else:
            text_proba = np.zeros(len(classes))
        
        # CNN prediction
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = preprocess_input(np.expand_dims(img_array, axis=0))
        cnn_proba = cnn_model.predict(img_array, verbose=0)[0]
        
        # Smart weighting based on text quality
        weight_text = 0.7 if text_length > 10 else 0.3
        
        # Weighted ensemble
        final_proba = (weight_text * text_proba) + ((1 - weight_text) * cnn_proba)
        
        # Get prediction
        class_idx = np.argmax(final_proba)
        predicted_class = classes.get(class_idx, "Unknown")
        confidence = float(final_proba[class_idx])
        
        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "extracted_text": text,
            "text_length": text_length,
            "ensemble_weights": {"text": weight_text, "cnn": 1 - weight_text},
            "text_proba": text_proba.tolist(),
            "cnn_proba": cnn_proba.tolist(),
            "final_proba": final_proba.tolist()
        }
        
    except Exception as e:
        return {"error": str(e), "prediction": None, "confidence": 0}

def main():
    """Main function for testing predictions"""
    
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        print("Example: python predict.py test_image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        sys.exit(1)
    
    print("🧠 Loading models...")
    
    try:
        # Load models
        text_model = joblib.load('ocr_text_model.pkl')
        cnn_model = load_model('image_model.h5')
        print("✅ Models loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        print("Make sure ocr_text_model.pkl and image_model.h5 are in the current directory")
        sys.exit(1)
    
    print(f"🖼️  Analyzing image: {image_path}")
    print("=" * 60)
    
    # Make prediction
    result = predict_image(image_path, text_model, cnn_model)
    
    if result.get("error"):
        print(f"❌ Prediction error: {result['error']}")
        return
    
    # Display results
    print(f"🎯 Predicted Class: {result['prediction']}")
    print(f"📊 Confidence: {result['confidence']:.2%}")
    print(f"📝 Text Length: {result['text_length']} characters")
    print(f"⚖️  Ensemble Weights - Text: {result['ensemble_weights']['text']:.1%}, CNN: {result['ensemble_weights']['cnn']:.1%}")
    
    print("\n📈 Detailed Probabilities:")
    print("-" * 30)
    classes = ['form', 'invoice', 'list', 'note', 'sign']
    
    for i, class_name in enumerate(classes):
        text_prob = result['text_proba'][i]
        cnn_prob = result['cnn_proba'][i]
        final_prob = result['final_proba'][i]
        
        print(f"{class_name:<8}: Text={text_prob:.3f}, CNN={cnn_prob:.3f}, Final={final_prob:.3f}")
    
    if result['extracted_text']:
        print("\n📄 Extracted Text:")
        print("-" * 30)
        print(result['extracted_text'][:200] + ("..." if len(result['extracted_text']) > 200 else ""))

if __name__ == "__main__":
    main()
