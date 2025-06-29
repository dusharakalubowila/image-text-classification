#!/usr/bin/env python3
"""
Test script for the Image Classification Flask App
"""

import requests
import os
import json

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_predict_endpoint():
    """Test the prediction endpoint with a sample image"""
    try:
        # You can replace this with a path to your test image
        test_image_path = "test_image.jpg"
        
        if not os.path.exists(test_image_path):
            print(f"⚠️  Test image not found: {test_image_path}")
            print("Please add a test image or update the path")
            return
        
        with open(test_image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/predict', files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction test passed")
            print(f"Predicted class: {result.get('prediction')}")
            print(f"Confidence: {result.get('confidence', 0):.2%}")
            print(f"Extracted text: {result.get('extracted_text', 'N/A')[:50]}...")
        else:
            print(f"❌ Prediction test failed: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Prediction test error: {e}")

def main():
    print("🧪 Testing Image Classification Flask App")
    print("=" * 50)
    
    print("\n1. Testing Health Endpoint...")
    test_health_endpoint()
    
    print("\n2. Testing Prediction Endpoint...")
    test_predict_endpoint()
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()
