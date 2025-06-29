@echo off
REM Quick setup script for Windows
echo.
echo ========================================
echo  Image Classification Project Setup
echo ========================================
echo.

echo [1/5] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

echo.
echo [2/5] Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Some packages may have failed to install
)

echo.
echo [3/5] Creating uploads directory...
if not exist "uploads" mkdir uploads
echo Created uploads directory

echo.
echo [4/5] Checking model files...
if exist "image_model.h5" (
    echo ✓ image_model.h5 found
) else (
    echo ✗ image_model.h5 missing
)

if exist "ocr_text_model.pkl" (
    echo ✓ ocr_text_model.pkl found
) else (
    echo ✗ ocr_text_model.pkl missing
)

echo.
echo [5/5] Setup complete!
echo.
echo To start the application:
echo   python app.py
echo.
echo To test the application:
echo   python test_app.py
echo.
echo To initialize git repository:
echo   git init
echo   git add .
echo   git commit -m "Initial commit"
echo.
echo ========================================
echo  Ready for deployment!
echo ========================================
pause
