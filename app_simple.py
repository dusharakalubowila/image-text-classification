from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import cv2
import pytesseract
import numpy as np
import joblib
from werkzeug.utils import secure_filename
import uuid
import platform

# Configure Tesseract path for Windows
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models
try:
    text_model = joblib.load('ocr_text_model.pkl')
    ocr_classes = text_model.classes_ if hasattr(text_model, 'classes_') else None
    print("✅ OCR text model loaded successfully!")
    print(f"📋 OCR model classes: {ocr_classes}")
except Exception as e:
    print(f"❌ Error loading OCR model: {e}")
    text_model = None
    ocr_classes = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(image_path):
    """Extract text from image using OCR"""
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception as e:
        print(f"OCR failed: {e}")
        return "Error extracting text"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text
            extracted_text = extract_text(filepath)
            print(f"📝 Extracted text: '{extracted_text}'")
            
            # Make prediction if model is available
            if text_model and len(extracted_text.strip()) > 0:
                prediction = text_model.predict([extracted_text])[0]
                probabilities = text_model.predict_proba([extracted_text])[0]
                confidence = float(max(probabilities))
                
                result = {
                    "prediction": prediction,
                    "confidence": confidence,
                    "extracted_text": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text,
                    "text_length": len(extracted_text),
                    "mode": "real_ocr",
                    "probabilities": {cls: float(prob) for cls, prob in zip(ocr_classes, probabilities)}
                }
            else:
                result = {
                    "prediction": "unknown",
                    "confidence": 0.0,
                    "extracted_text": extracted_text if extracted_text else "No text extracted",
                    "text_length": len(extracted_text) if extracted_text else 0,
                    "mode": "ocr_only",
                    "error": "No model available or no text extracted"
                }
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify(result)
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health')
def health():
    tesseract_available = False
    try:
        pytesseract.get_tesseract_version()
        tesseract_available = True
    except:
        pass
    
    return jsonify({
        'status': 'healthy' if text_model and tesseract_available else 'partial',
        'models': {
            'text_model': text_model is not None,
            'tesseract_ocr': tesseract_available
        },
        'classes': list(ocr_classes) if ocr_classes is not None else []
    })

if __name__ == '__main__':
    print("🚀 Starting Flask app with real OCR support...")
    app.run(debug=False, host='0.0.0.0', port=5000)
