#!/usr/bin/env python3
"""
Startup script to test and run the Flask application
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'tensorflow', 'scikit-learn', 
        'opencv-python', 'pytesseract', 'numpy', 'joblib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def check_models():
    """Check if model files exist"""
    required_models = ['ocr_text_model.pkl', 'image_model.h5']
    missing_models = []
    
    for model in required_models:
        if not os.path.exists(model):
            missing_models.append(model)
    
    return missing_models

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Image Classification Flask App Startup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check dependencies
    print("\n📋 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        
        if os.path.exists('requirements.txt'):
            install_choice = input("Install missing packages? (y/n): ").lower().strip()
            if install_choice == 'y':
                if not install_dependencies():
                    sys.exit(1)
            else:
                print("❌ Cannot proceed without required packages")
                sys.exit(1)
        else:
            print("❌ requirements.txt not found")
            sys.exit(1)
    else:
        print("✅ All Python packages are installed")
    
    # Check Tesseract
    print("\n🔍 Checking Tesseract OCR...")
    if check_tesseract():
        print("✅ Tesseract OCR is installed")
    else:
        print("⚠️  Tesseract OCR not found")
        print("Please install Tesseract OCR:")
        print("  - Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  - Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("  - macOS: brew install tesseract")
    
    # Check models
    print("\n🤖 Checking model files...")
    missing_models = check_models()
    
    if missing_models:
        print(f"⚠️  Missing models: {', '.join(missing_models)}")
        print("Please ensure model files are in the current directory")
        print("You may need to run the training notebook first")
    else:
        print("✅ All model files found")
    
    # Create uploads directory
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("✅ Created uploads directory")
    
    print("\n" + "=" * 50)
    
    if missing_models:
        print("⚠️  Warning: Some model files are missing")
        print("The application may not work properly")
    
    # Start Flask app
    start_choice = input("Start the Flask application? (y/n): ").lower().strip()
    
    if start_choice == 'y':
        print("\n🌐 Starting Flask application...")
        print("Access the app at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 30)
        
        try:
            # Import and run the Flask app
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except ImportError as e:
            print(f"❌ Failed to import Flask app: {e}")
        except KeyboardInterrupt:
            print("\n👋 Application stopped")
        except Exception as e:
            print(f"❌ Error starting application: {e}")
    else:
        print("👋 Setup complete. Run 'python app.py' to start the server")

if __name__ == "__main__":
    main()
