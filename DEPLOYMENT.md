# Deployment Guide

This guide covers various deployment options for the Image Classification Flask App.

## 🚀 Quick Start (Local Development)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Install Tesseract OCR**
- **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

3. **Run the Application**
```bash
python app.py
```

4. **Access the Application**
Open your browser and go to: `http://localhost:5000`

## 🐳 Docker Deployment

### Local Docker

1. **Build the Image**
```bash
docker build -t image-classifier .
```

2. **Run the Container**
```bash
docker run -p 5000:5000 image-classifier
```

3. **Access the Application**
Open your browser and go to: `http://localhost:5000`

### Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./uploads:/app/uploads
```

Run with: `docker-compose up`

## ☁️ Cloud Deployment

### 1. Heroku Deployment

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create your-app-name
```

4. **Set Stack to Container**
```bash
heroku stack:set container -a your-app-name
```

5. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

6. **Open App**
```bash
heroku open -a your-app-name
```

### 2. Railway Deployment

1. **Connect GitHub Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub account
   - Import your repository

2. **Configure Environment**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Deploy**
   - Railway will automatically deploy on git push

### 3. Render Deployment

1. **Connect GitHub Repository**
   - Go to [Render](https://render.com)
   - Connect your GitHub account
   - Create new Web Service

2. **Configure Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.9

3. **Deploy**
   - Render will automatically deploy

### 4. Google Cloud Run

1. **Enable Cloud Run API**
```bash
gcloud services enable run.googleapis.com
```

2. **Build and Push to Container Registry**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/image-classifier
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy --image gcr.io/PROJECT_ID/image-classifier --platform managed
```

### 5. AWS ECS (Fargate)

1. **Build and Push to ECR**
```bash
aws ecr create-repository --repository-name image-classifier
docker tag image-classifier:latest AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/image-classifier:latest
docker push AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/image-classifier:latest
```

2. **Create ECS Task Definition**
3. **Create ECS Service**
4. **Configure Load Balancer**

## 🔧 Environment Variables

For production deployment, consider setting these environment variables:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
```

## 📊 Monitoring and Logging

### Health Checks

The application provides a health check endpoint:
```
GET /health
```

Response:
```json
{
    "status": "healthy",
    "models_loaded": true,
    "supported_classes": ["form", "invoice", "list", "note", "sign"]
}
```

### Logging

Add logging configuration in production:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
```

## 🔒 Security Considerations

### Production Security

1. **File Upload Security**
   - File type validation
   - File size limits
   - Virus scanning (optional)

2. **Rate Limiting**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/predict')
@limiter.limit("10 per minute")
def predict():
    # ...
```

3. **HTTPS Configuration**
   - Use SSL certificates
   - Redirect HTTP to HTTPS
   - Set secure headers

## 🚨 Troubleshooting

### Common Issues

1. **Tesseract Not Found**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows - Add to PATH or specify location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

2. **Memory Issues**
   - Increase container memory limits
   - Optimize image processing
   - Use model quantization

3. **Slow Predictions**
   - Use GPU acceleration
   - Implement caching
   - Optimize image preprocessing

### Debug Mode

For debugging, set environment variables:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

## 📈 Performance Optimization

### Tips for Production

1. **Use Gunicorn with Multiple Workers**
```bash
gunicorn --workers 4 --timeout 120 --bind 0.0.0.0:5000 app:app
```

2. **Enable Caching**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

3. **Optimize Model Loading**
```python
# Load models once at startup
@app.before_first_request
def load_models():
    global text_model, cnn_model
    text_model = joblib.load('ocr_text_model.pkl')
    cnn_model = load_model('image_model.h5')
```

## 📞 Support

For deployment issues or questions:
- Email: Contact@fonixss.com
- CC: nilaksha@fonixss.com

---

Happy Deploying! 🚀
