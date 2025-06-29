# Image-Based Text Classification

A machine learning application that classifies images containing text into predefined categories using an ensemble of OCR and CNN models.

## 🎯 Project Overview

This project implements an image classification system that can categorize images containing text into five classes:
- **Invoice** - Financial documents and billing statements
- **Note** - Handwritten or typed notes
- **Sign** - Street signs, shop signs, and similar
- **List** - Shopping lists, to-do lists, and similar
- **Form** - Application forms, questionnaires, etc.

## 🏗️ Architecture

The system uses an ensemble approach combining:
1. **OCR Model** - Extracts text using Tesseract OCR and classifies using TF-IDF + Logistic Regression
2. **CNN Model** - Uses MobileNetV2 for visual feature extraction and classification
3. **Smart Ensemble** - Dynamically weights predictions based on text quality

## 🚀 Features

- **Web Interface** - Beautiful, responsive Flask web application
- **Drag & Drop Upload** - Easy file upload with preview
- **Real-time Predictions** - Fast classification with confidence scores
- **OCR Integration** - Extracts and displays detected text
- **Model Ensemble** - Combines visual and textual features
- **Docker Support** - Ready for containerized deployment

## 📦 Installation

### Local Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd image-text-classification
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR**
- **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

### Docker Setup

1. **Build the image**
```bash
docker build -t image-classifier .
```

2. **Run the container**
```bash
docker run -p 5000:5000 image-classifier
```

## 🔧 API Usage

### Prediction Endpoint

**POST** `/predict`

Upload an image file to get classification results.

**Example using curl:**
```bash
curl -X POST -F "file=@your_image.jpg" http://localhost:5000/predict
```

**Response:**
```json
{
    "prediction": "invoice",
    "confidence": 0.87,
    "extracted_text": "Invoice #12345 Date: 2025-01-01...",
    "text_length": 45,
    "ensemble_weights": {
        "text": 0.7,
        "cnn": 0.3
    }
}
```

### Health Check

**GET** `/health`

Check if the application and models are loaded properly.

## 📊 Model Performance

The ensemble model achieves:
- **Overall Accuracy**: ~85-90% on test data
- **OCR Model**: Excellent for text-heavy images
- **CNN Model**: Strong visual pattern recognition
- **Smart Weighting**: Adapts based on text quality

## 🗂️ Project Structure

```
image-text-classification/
├── app.py                 # Flask web application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── image_model.h5        # Trained CNN model
├── ocr_text_model.pkl    # Trained OCR text model
├── Merge.ipynb          # Training notebook
├── templates/
│   └── index.html       # Web interface
├── uploads/             # Temporary upload directory
└── README.md           # This file
```

## 🔬 Model Details

### OCR Text Model
- **Pipeline**: TF-IDF Vectorizer + Logistic Regression
- **Input**: Extracted text from images
- **Preprocessing**: Tesseract OCR with grayscale conversion

### CNN Image Model
- **Base Model**: MobileNetV2 (ImageNet pretrained)
- **Input Size**: 224x224x3
- **Training**: Transfer learning with frozen base layers
- **Preprocessing**: MobileNetV2 preprocessing function

### Ensemble Strategy
- **Dynamic Weighting**: Text weight = 0.7 if text_length > 10, else 0.3
- **Combination**: Weighted average of probability distributions
- **Prediction**: Argmax of final probabilities

## 🚀 Deployment Options

### 1. Local Development
```bash
python app.py
```

### 2. Docker Container
```bash
docker build -t image-classifier .
docker run -p 5000:5000 image-classifier
```

### 3. Cloud Deployment (Heroku)
```bash
heroku create your-app-name
heroku container:push web
heroku container:release web
```

### 4. Cloud Deployment (Railway/Render)
- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn app:app`

## 🛠️ Development

### Adding New Classes
1. Update the `classes` dictionary in `app.py`
2. Retrain models with new data
3. Replace model files (`image_model.h5`, `ocr_text_model.pkl`)

### Model Retraining
Use the `Merge.ipynb` notebook to:
1. Prepare your dataset
2. Train OCR and CNN models
3. Evaluate performance
4. Export models

## 📈 Future Improvements

- [ ] Add more document types
- [ ] Implement data augmentation
- [ ] Add confidence threshold tuning
- [ ] Support for multi-language OCR
- [ ] Real-time video classification
- [ ] Model versioning and A/B testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created for Pre-Interview Assessment - ML/AI Developer Position

**Contact**: 
- Email: Contact@fonixss.com
- CC: nilaksha@fonixss.com

---

*Built with ❤️ using Flask, TensorFlow, and OpenCV*
