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
    cnn_model = load_model('image_model.h5')
    
    # Define class mapping - adjust these based on your actual trained model classes
    # You may need to check your training notebook to get the exact class order
    classes = {0: 'form', 1: 'invoice', 2: 'list', 3: 'note', 4: 'sign'}
    
    # Alternative: Try to load class mapping from model if available
    # Uncomment and modify if you have access to the original training generator
    # try:
    #     with open('class_mapping.json', 'r') as f:
    #         classes = json.load(f)
    # except FileNotFoundError:
    #     pass  # Use default mapping above
    
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    text_model = None
    cnn_model = None
    classes = {}

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
        print("OCR failed:", e)
        return ""

def predict_image(image_path):
    """Predict image class using ensemble of OCR and CNN"""
    if text_model is None or cnn_model is None:
        return {"error": "Models not loaded", "prediction": None, "confidence": 0}
    
    try:
        # OCR prediction
        text = extract_text(image_path)
        text_length = len(text.strip())
        
        # Get text prediction probabilities
        if text_length > 0:
            text_proba = text_model.predict_proba([text])[0]
        else:
            text_proba = np.zeros(len(classes))
        
        # CNN prediction
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = preprocess_input(np.expand_dims(img_array, axis=0))
        cnn_proba = cnn_model.predict(img_array)[0]
        
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
            "extracted_text": text[:100] + "..." if len(text) > 100 else text,
            "text_length": text_length,
            "ensemble_weights": {"text": weight_text, "cnn": 1 - weight_text}
        }
        
    except Exception as e:
        return {"error": str(e), "prediction": None, "confidence": 0}

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
    return jsonify({
        'status': 'healthy',
        'models_loaded': text_model is not None and cnn_model is not None,
        'supported_classes': list(classes.values())
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
