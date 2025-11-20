#!/usr/bin/env python3
"""
Setup script for Intelligent Hospital Management System
AI for Software Engineering Final Project
"""

import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n🔧 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🏥 Intelligent Hospital Management System Setup")
    print("=" * 50)
    
    # Create necessary directories
    directories = ['backend', 'frontend', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    print("\n🎯 Setup complete! Now run these commands in order:")
    print("""
1. Start Backend:
   cd backend && uvicorn app:app --reload

2. Generate Sample Data (in new terminal):
   cd data && python synthetic_data.py

3. Start Frontend (in new terminal):
   cd frontend && streamlit run app.py

4. Access the system:
   - API: http://localhost:8000
   - Dashboard: http://localhost:8501
    """)

if __name__ == "__main__":
    main()