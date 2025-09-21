#!/usr/bin/env python3
"""
ATLAS Demo Startup Script
Quick setup and launch for demo presentations
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def print_banner():
    """Print demo banner"""
    print("🎓" + "="*60 + "🎓")
    print("    ATLAS Demo Setup - Academic Task Learning Agent System")
    print("="*64)

def check_requirements():
    """Check if demo requirements are met"""
    print("\n🔧 Checking demo requirements...")
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False
    
    # Check required files
    required_files = ['profile.json', 'calendar.json', 'task.json', 'web_app.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Missing {file}")
            return False
    
    # Check API key
    api_key = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY")
    if api_key:
        print("✅ API key configured")
    else:
        print("❌ API key missing")
        print("   Options to fix:")
        print("   1. Set in terminal: export NEMOTRON_4_340B_INSTRUCT_KEY='your_key'")
        print("   2. Add to .env file: NEMOTRON_4_340B_INSTRUCT_KEY=your_key")
        if os.path.exists('.env'):
            print("   (.env file found - check if key is set correctly)")
        else:
            print("   (no .env file found)")
        return False
    
    # Check dependencies
    try:
        import flask
        import flask_cors
        import langchain
        import openai
        import rich
        print("✅ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    return True

def print_demo_guide():
    """Print demo guide"""
    print("\n🎯 DEMO GUIDE")
    print("-" * 50)
    print("1. Web interface will open automatically")
    print("2. Try these demo queries:")
    print("   • 'Help me create a study plan for calculus'")
    print("   • 'I'm overwhelmed with multiple deadlines'") 
    print("   • 'Generate study notes for derivatives'")
    print("3. Switch between agents to show specialization")
    print("4. Highlight personalization for ADHD/learning styles")
    
    print("\n🗣️ KEY TALKING POINTS:")
    print("   • Multi-agent AI architecture")
    print("   • Personalized to individual learning patterns")
    print("   • Real-time calendar and task integration")
    print("   • Addresses the time management crisis in education")
    
    print("\n⏱️ TIMING:")
    print("   • Demo: 5-7 minutes")
    print("   • Questions: 3-5 minutes")
    print("   • Total: 10-12 minutes")

def start_demo():
    """Start the demo application"""
    print("\n🚀 Starting ATLAS Demo...")
    
    try:
        # Start the web application
        print("Starting web server...")
        process = subprocess.Popen([
            sys.executable, 'web_app.py'
        ])
        
        # Give it a moment to start
        import time
        time.sleep(3)
        
        # Open browser
        print("Opening browser...")
        webbrowser.open('http://localhost:5000')
        
        print("\n✨ Demo ready!")
        print("🌐 Web interface: http://localhost:5000")
        print("\n📋 Quick reference: Check DEMO_SCRIPT.md")
        print("\n⏹️  Press Ctrl+C to stop demo")
        
        # Wait for user to stop
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping demo...")
            process.terminate()
            print("✅ Demo stopped successfully")
        
    except Exception as e:
        print(f"❌ Failed to start demo: {e}")
        return False
    
    return True

def main():
    """Main demo setup function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Demo setup failed. Please fix the issues above.")
        return 1
    
    print("\n✅ All requirements met!")
    
    # Print demo guide
    print_demo_guide()
    
    # Ask for confirmation
    print("\n" + "="*64)
    response = input("Ready to start demo? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        if start_demo():
            return 0
        else:
            return 1
    else:
        print("Demo cancelled. Run again when ready!")
        return 0

if __name__ == "__main__":
    exit(main())
