#!/usr/bin/env python3
"""
Create sample images and test real OCR extraction
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_images():
    """Create sample images with different document types"""
    
    print("🎨 Creating test images with different document types...")
    
    # Test images to create
    test_cases = [
        {
            'filename': 'invoice_test.png',
            'text': 'INVOICE\n\nInvoice #: 12345\nDate: June 29, 2025\nBill To: John Smith\n\nItem: Software License\nAmount: $299.99\nTax: $30.00\nTotal: $329.99\n\nThank you for your business!',
            'expected': 'invoice'
        },
        {
            'filename': 'form_test.png', 
            'text': 'APPLICATION FORM\n\nName: _________________\nAddress: _________________\nPhone: _________________\nEmail: _________________\n\nSignature: _________________\nDate: _________________',
            'expected': 'form'
        },
        {
            'filename': 'letter_test.png',
            'text': 'Dear Mr. Smith,\n\nI hope this letter finds you well.\nI am writing to inquire about the\nposition advertised in your company.\n\nI have 5 years of experience in\nsoftware development and would\nbe happy to discuss my qualifications.\n\nSincerely,\nJane Doe',
            'expected': 'letter'
        },
        {
            'filename': 'memo_test.png',
            'text': 'MEMORANDUM\n\nTO: All Staff\nFROM: Management\nDATE: June 29, 2025\nRE: Office Policy Update\n\nPlease note that starting Monday,\nthe office will implement new\nsecurity procedures.\n\nThank you for your cooperation.',
            'expected': 'memo'
        }
    ]
    
    for test_case in test_cases:
        # Create image
        img = Image.new('RGB', (500, 400), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        draw.text((20, 20), test_case['text'], fill='black', font=font)
        
        # Save image
        img.save(test_case['filename'])
        print(f"✅ Created: {test_case['filename']} (expected: {test_case['expected']})")
    
    return test_cases

def test_real_ocr_on_samples():
    """Test real OCR on sample images"""
    
    import pytesseract
    import cv2
    import joblib
    import platform
    
    # Configure Tesseract
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Load OCR model
    try:
        text_model = joblib.load('ocr_text_model.pkl')
        print("✅ OCR model loaded")
    except Exception as e:
        print(f"❌ Error loading OCR model: {e}")
        return
    
    print("\n🔍 Testing real OCR extraction and prediction:")
    print("=" * 60)
    
    # Create test images
    test_cases = create_test_images()
    
    # Test each image
    for test_case in test_cases:
        filename = test_case['filename']
        expected = test_case['expected']
        
        print(f"\n📁 Testing: {filename}")
        
        try:
            # Extract text using OCR
            image = cv2.imread(filename)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray).strip()
            
            print(f"📝 Extracted text: '{extracted_text[:100]}{'...' if len(extracted_text) > 100 else ''}'")
            print(f"📏 Text length: {len(extracted_text)}")
            
            if len(extracted_text) > 0:
                # Make prediction
                prediction = text_model.predict([extracted_text])[0]
                probabilities = text_model.predict_proba([extracted_text])[0]
                confidence = max(probabilities)
                
                print(f"🎯 Prediction: {prediction} (confidence: {confidence:.3f})")
                print(f"🎪 Expected: {expected}")
                print(f"✅ Correct: {'YES' if prediction == expected else 'NO'}")
                
                # Show top 3 predictions
                classes = text_model.classes_
                sorted_indices = probabilities.argsort()[::-1][:3]
                print("📊 Top 3 predictions:")
                for i, idx in enumerate(sorted_indices):
                    print(f"   {i+1}. {classes[idx]}: {probabilities[idx]:.3f}")
            else:
                print("❌ No text extracted")
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_real_ocr_on_samples()
    print("\n🎉 Real OCR testing complete!")
