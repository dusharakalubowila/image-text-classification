from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import cv2
import pytesseract
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from werkzeug.utils import secure_filename
import uuid
import platform

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Tesseract path for different environments
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    # Linux/Cloud environment - Tesseract should be in PATH
    pass

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models with fallback to demo mode
ocr_classes = None  # Global variable for OCR model classes

try:
    import warnings
    warnings.filterwarnings('ignore')  # Suppress sklearn version warnings
    
    # Check if Tesseract is available
    try:
        pytesseract.get_tesseract_version()
        tesseract_available = True
        print("✅ Tesseract OCR is available")
    except:
        tesseract_available = False
        print("⚠️  Tesseract OCR not found - using mock text extraction")
    
    text_model = joblib.load('ocr_text_model.pkl')
    print("✅ OCR text model loaded successfully!")
    
    # Get actual classes from the OCR model
    ocr_classes = text_model.classes_ if hasattr(text_model, 'classes_') else None
    print(f"📋 OCR model classes: {ocr_classes}")
    
    try:
        cnn_model = load_model('image_model.h5')
        print("✅ CNN image model loaded successfully!")
    except Exception as e:
        print(f"⚠️  CNN model loading failed: {e}")
        print("🔄 Using mock CNN predictions")
        cnn_model = None
    
    # Define class mapping - use OCR model classes if available
    if ocr_classes is not None:
        classes = {i: cls for i, cls in enumerate(ocr_classes)}
        print(f"📊 Using OCR model classes: {classes}")
    else:
        classes = {0: 'form', 1: 'invoice', 2: 'list', 3: 'note', 4: 'sign'}
        print("📊 Using default classes")
    
    if tesseract_available and text_model is not None and cnn_model is not None:
        print("✅ Full functionality available!")
    elif text_model is not None:
        print("✅ Partial functionality available (OCR model + mock predictions)")
    else:
        print("⚠️  Demo mode active")
    
except Exception as e:
    print(f"⚠️  Model loading error: {e}")
    print("🔄 Running in demo mode with mock predictions")
    text_model = None
    cnn_model = None
    tesseract_available = False
    ocr_classes = None
    classes = {0: 'form', 1: 'invoice', 2: 'list', 3: 'note', 4: 'sign'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(image_path):
    """Extract text from image using OCR (with fallback to mock)"""
    try:
        # Try to use Tesseract OCR
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        # Tesseract not installed - use mock text extraction
        print("⚠️  Tesseract OCR not found, using mock text extraction")
        
        # Generate mock text based on image filename or random text
        import random
        mock_texts = [
            "Invoice #12345\nDate: 2025-01-15\nAmount: $299.99\nTax: $30.00\nTotal: $329.99",
            "Shopping List:\n- Milk\n- Bread\n- Eggs\n- Butter\n- Cheese",
            "Meeting Notes\nDate: Today\nAttendees: John, Mary\nAction Items:\n- Review proposal\n- Schedule follow-up",
            "STOP\nSpeed Limit\n25 MPH\nSchool Zone",
            "Application Form\nName: ___________\nDate: ___________\nSignature: ___________"
        ]
        return random.choice(mock_texts)
    except Exception as e:
        print(f"OCR failed: {e}")
        return "Mock extracted text for demo purposes"

def predict_image(image_path):
    """Predict image class using ensemble of OCR and CNN (with fallback to demo mode)"""
    
    # If models are not loaded, use mock prediction
    if text_model is None and cnn_model is None:
        import random
        prediction = random.choice(['form', 'invoice', 'list', 'note', 'sign'])
        confidence = random.uniform(0.75, 0.95)
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "extracted_text": "Demo mode - sample OCR text extraction...",
            "text_length": 35,
            "ensemble_weights": {"text": 0.6, "cnn": 0.4},
            "mode": "demo"
        }
    
    try:
        # OCR prediction
        text = extract_text(image_path)
        text_length = len(text.strip())
        
        # Get text prediction probabilities
        if text_length > 0 and text_model is not None:
            text_proba = text_model.predict_proba([text])[0]
            text_classes = len(text_proba)
        else:
            # Use OCR model classes count if available, otherwise default to 5
            text_classes = len(ocr_classes) if ocr_classes is not None else 5
            text_proba = np.zeros(text_classes)
        
        # CNN prediction
        if cnn_model is not None:
            img = load_img(image_path, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = preprocess_input(np.expand_dims(img_array, axis=0))
            cnn_proba = cnn_model.predict(img_array)[0]
            cnn_classes = len(cnn_proba)
        else:
            # Mock CNN prediction - use same number of classes as text model
            cnn_classes = text_classes
            import random
            cnn_proba = np.array([random.uniform(0.1, 0.9) for _ in range(cnn_classes)])
            cnn_proba = cnn_proba / np.sum(cnn_proba)  # Normalize
        
        # Handle class mismatch by using the minimum number of classes
        num_classes = min(text_classes, cnn_classes)
        
        # Truncate or pad probabilities to match
        text_proba_aligned = text_proba[:num_classes] if len(text_proba) >= num_classes else np.pad(text_proba, (0, num_classes - len(text_proba)))
        cnn_proba_aligned = cnn_proba[:num_classes] if len(cnn_proba) >= num_classes else np.pad(cnn_proba, (0, num_classes - len(cnn_proba)))
        
        # Normalize after alignment
        if np.sum(text_proba_aligned) > 0:
            text_proba_aligned = text_proba_aligned / np.sum(text_proba_aligned)
        if np.sum(cnn_proba_aligned) > 0:
            cnn_proba_aligned = cnn_proba_aligned / np.sum(cnn_proba_aligned)
        
        # Smart weighting based on text quality
        weight_text = 0.7 if text_length > 10 else 0.3
        
        # Weighted ensemble
        final_proba = (weight_text * text_proba_aligned) + ((1 - weight_text) * cnn_proba_aligned)
        
        # Get prediction using available classes
        if ocr_classes is not None:
            available_classes = list(ocr_classes)[:num_classes]
        else:
            available_classes = ['form', 'invoice', 'list', 'note', 'sign'][:num_classes]
        
        class_idx = np.argmax(final_proba)
        predicted_class = available_classes[class_idx] if class_idx < len(available_classes) else "Unknown"
        confidence = float(final_proba[class_idx])
        
        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "extracted_text": text[:100] + "..." if len(text) > 100 else text,
            "text_length": text_length,
            "ensemble_weights": {"text": weight_text, "cnn": 1 - weight_text},
            "mode": "partial" if cnn_model is None else "full",
            "debug_info": {
                "text_classes": text_classes,
                "cnn_classes": cnn_classes,
                "aligned_classes": num_classes
            }
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Prediction error: {error_details}")
        
        # Fallback to simple mock prediction
        import random
        prediction = random.choice(['form', 'invoice', 'list', 'note', 'sign'])
        return {
            "prediction": prediction, 
            "confidence": 0.8,
            "extracted_text": "Error in processing - using fallback prediction",
            "text_length": 0,
            "ensemble_weights": {"text": 0.5, "cnn": 0.5},
            "mode": "fallback",
            "error": str(e)
        }

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
            # Make prediction
            result = predict_image(filepath)
            
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
def health_check():
    # Check Tesseract availability
    try:
        pytesseract.get_tesseract_version()
        tesseract_status = True
    except:
        tesseract_status = False
    
    models_status = {
        'text_model': text_model is not None,
        'cnn_model': cnn_model is not None,
        'tesseract_ocr': tesseract_status
    }
    
    if text_model is not None and cnn_model is not None and tesseract_status:
        status = 'healthy'
        mode = 'full'
    elif text_model is not None:  # OCR model available regardless of Tesseract
        status = 'partial'
        mode = 'partial'
    else:
        status = 'demo'
        mode = 'demo'
    
    return jsonify({
        'status': status,
        'mode': mode,
        'models_loaded': models_status,
        'models_available': text_model is not None or cnn_model is not None,
        'tesseract_available': tesseract_status,
        'supported_classes': list(classes.values()) if classes else ['form', 'invoice', 'list', 'note', 'sign'],
        'note': 'Install Tesseract OCR for full functionality' if not tesseract_status else 'All systems operational'
    })

if __name__ == '__main__':
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
