#!/usr/bin/env python3
"""
Quick Demo Test Script for ATLAS
Tests core functionality before the demo
"""

import os
import sys
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔧 Testing imports...")
    
    try:
        from config.llm_config import configure_api_keys, get_llm_instance
        print("✅ Config imports working")
        
        from models.state import AcademicState
        print("✅ State model working")
        
        from agents.planner_agent import PlannerAgent
        from agents.notewriter_agent import NoteWriterAgent
        print("✅ Agent imports working")
        
        from utils.data_manager import DataManager
        print("✅ Data manager working")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\n📁 Testing data files...")
    
    required_files = ['profile.json', 'calendar.json', 'task.json']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_env_setup():
    """Test environment setup"""
    print("\n🔑 Testing environment...")
    
    # Check for API key (don't print the actual key)
    api_key = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY")
    if api_key:
        print("✅ API key found")
        return True
    else:
        print("❌ API key missing - set NEMOTRON_4_340B_INSTRUCT_KEY")
        return False

async def test_basic_functionality():
    """Test basic ATLAS functionality"""
    print("\n⚙️ Testing basic functionality...")
    
    try:
        from config.llm_config import configure_api_keys, get_llm_instance
        from utils.data_manager import DataManager
        
        # Configure API
        if not configure_api_keys():
            print("❌ API configuration failed")
            return False
        
        # Initialize components
        llm = get_llm_instance()
        data_manager = DataManager()
        
        # Load data
        with open('profile.json', 'r') as f:
            profile_data = f.read()
        with open('calendar.json', 'r') as f:
            calendar_data = f.read()
        with open('task.json', 'r') as f:
            task_data = f.read()
        
        data_manager.load_data(profile_data, calendar_data, task_data)
        
        # Test data loading
        profile = data_manager.get_student_profile("student_123")
        if profile:
            print("✅ Student profile loaded")
        else:
            print("❌ Failed to load student profile")
            return False
        
        events = data_manager.get_upcoming_events()
        print(f"✅ Found {len(events)} upcoming events")
        
        tasks = data_manager.get_active_tasks()
        print(f"✅ Found {len(tasks)} active tasks")
        
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_web_interface():
    """Test if web interface can start"""
    print("\n🌐 Testing web interface...")
    
    try:
        import flask
        from flask_cors import CORS
        print("✅ Flask dependencies available")
        
        # Test if web_app can be imported
        import web_app
        print("✅ Web app module importable")
        
        return True
    except Exception as e:
        print(f"❌ Web interface test failed: {e}")
        return False

def print_demo_readiness():
    """Print final demo readiness assessment"""
    print("\n" + "="*50)
    print("🎯 DEMO READINESS ASSESSMENT")
    print("="*50)
    
    print("\n📋 PRE-DEMO CHECKLIST:")
    print("  □ Start web server: python web_app.py")
    print("  □ Open browser to http://localhost:5000")
    print("  □ Test both agents (Planner & NoteWriter)")
    print("  □ Prepare demo queries:")
    print("    - 'Help me plan my calculus study schedule'")
    print("    - 'Create study notes for derivatives'")
    print("    - 'I'm overwhelmed with assignments, help!'")
    
    print("\n🎤 DEMO TALKING POINTS:")
    print("  • Multi-agent AI system for academic assistance")
    print("  • Personalized to learning styles (including ADHD)")
    print("  • Real-time calendar and task integration")
    print("  • Intelligent content generation")
    print("  • Scalable architecture for universities")
    
    print("\n🚀 START DEMO WITH:")
    print("  python web_app.py")
    print("  Then navigate to: http://localhost:5000")
    
    print("\n💡 DEMO TIP:")
    print("  Focus on the problem: Students waste 2-3 hours daily")
    print("  Show the solution: AI that adapts to how they learn")

async def main():
    """Run all tests"""
    print("🎓 ATLAS Demo Preparation Test")
    print("="*40)
    
    tests_passed = 0
    total_tests = 5
    
    # Run tests
    if test_imports():
        tests_passed += 1
    
    if test_data_files():
        tests_passed += 1
    
    if test_env_setup():
        tests_passed += 1
    
    if await test_basic_functionality():
        tests_passed += 1
    
    if test_web_interface():
        tests_passed += 1
    
    # Results
    print(f"\n📊 TEST RESULTS: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - READY FOR DEMO!")
        print_demo_readiness()
    elif tests_passed >= 3:
        print("⚠️ MOSTLY READY - Some issues to address")
        print_demo_readiness()
    else:
        print("❌ DEMO NOT READY - Fix critical issues first")
        
        print("\n🔧 QUICK FIXES:")
        if not os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY"):
            print("  • Set API key: export NEMOTRON_4_340B_INSTRUCT_KEY='your_key'")
        print("  • Install missing dependencies: pip install flask flask-cors")
        print("  • Check data files are present")

if __name__ == "__main__":
    asyncio.run(main())
