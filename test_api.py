#!/usr/bin/env python3
"""
Test script to verify the Flask app prediction functionality
"""

import requests
import json

def test_prediction_api():
    print("🔍 Testing Flask App Prediction API...")
    
    base_url = "http://127.0.0.1:5000"
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health endpoint working")
            print(f"📊 Status: {health_data.get('status', 'unknown')}")
            print(f"🔧 Mode: {health_data.get('mode', 'unknown')}")
            print(f"📋 Models: {health_data.get('models_loaded', {})}")
            print(f"🏷️  Classes: {health_data.get('supported_classes', [])}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False
    
    # Test prediction with a sample image (we'll create a simple test image)
    print("\n2. Testing prediction endpoint...")
    try:
        # Create a simple test image file
        from PIL import Image
        import io
        
        # Create a simple test image with text
        img = Image.new('RGB', (200, 100), color='white')
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Test the prediction endpoint
        files = {'file': ('test_image.png', img_byte_arr, 'image/png')}
        response = requests.post(f"{base_url}/predict", files=files)
        
        if response.status_code == 200:
            prediction_data = response.json()
            print("✅ Prediction endpoint working")
            print(f"🎯 Prediction: {prediction_data.get('prediction', 'unknown')}")
            print(f"📊 Confidence: {prediction_data.get('confidence', 0):.3f}")
            print(f"📝 Extracted text: {prediction_data.get('extracted_text', 'none')[:50]}...")
            print(f"🔧 Mode: {prediction_data.get('mode', 'unknown')}")
            if 'debug_info' in prediction_data:
                print(f"🐛 Debug: {prediction_data['debug_info']}")
        else:
            print(f"❌ Prediction endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing prediction endpoint: {e}")
        return False
    
    print("\n✅ All API tests passed!")
    return True

if __name__ == "__main__":
    success = test_prediction_api()
    if success:
        print("\n🎉 Flask app is working correctly!")
    else:
        print("\n💥 Flask app test failed!")
