from flask import Flask, request, jsonify, render_template
import os
import cv2
import numpy as np
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple mock prediction for testing (replace with actual models in production)
def mock_predict(image_path):
    """Mock prediction function for testing"""
    import random
    classes = ['form', 'invoice', 'list', 'note', 'sign']
    prediction = random.choice(classes)
    confidence = random.uniform(0.7, 0.95)
    
    return {
        "prediction": prediction,
        "confidence": confidence,
        "extracted_text": "Sample extracted text from OCR...",
        "text_length": 25,
        "ensemble_weights": {"text": 0.6, "cnn": 0.4}
    }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            # Use mock prediction for testing
            result = mock_predict(filepath)
            
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
        'models_loaded': True,  # Mock for testing
        'supported_classes': ['form', 'invoice', 'list', 'note', 'sign']
    })

if __name__ == '__main__':
    print("🚀 Starting Flask app in demo mode...")
    print("📝 Note: Using mock predictions for testing")
    print("🌐 Open: http://localhost:5000")
    
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
