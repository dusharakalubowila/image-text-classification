#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to start the Flask app with proper encoding
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    print("🚀 Starting Flask app with real OCR support...")
    
    # Set environment variables for proper encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # Start the Flask app
    try:
        subprocess.run([sys.executable, 'app.py'], env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Flask app stopped by user")
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
