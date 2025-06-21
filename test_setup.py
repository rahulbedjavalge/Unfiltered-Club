#!/usr/bin/env python3
"""
Test script for Unfiltered Club
Run this to verify your setup is working correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from supabase import create_client, Client
        print("✅ Supabase imported successfully")
    except ImportError as e:
        print(f"❌ Supabase import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    return True

def test_env_file():
    """Test if environment file exists"""
    print("\n🔧 Testing environment configuration...")
    
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'OPENROUTER_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
            print("   Copy .env.example to .env and fill in your credentials")
            return False
        else:
            print("✅ All required environment variables are set")
            return True
    else:
        print("⚠️  .env file not found")
        print("   Copy .env.example to .env and fill in your credentials")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🗄️  Testing Supabase connection...")
    
    try:
        from supabase_config import init_supabase
        supabase = init_supabase()
        
        if supabase:
            print("✅ Supabase connection established")
            return True
        else:
            print("❌ Failed to connect to Supabase")
            return False
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def test_ai_api():
    """Test OpenRouter AI API"""
    print("\n🤖 Testing AI API connection...")
    
    try:
        from ai_utils import get_ai_reply
        response = get_ai_reply("Hello", "funny")
        
        if "API key not configured" in response or "technical difficulties" in response:
            print("⚠️  AI API not properly configured")
            return False
        else:
            print("✅ AI API connection successful")
            print(f"   Sample response: {response[:50]}...")
            return True
    except Exception as e:
        print(f"❌ AI API error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Unfiltered Club - Setup Verification\n")
    
    tests = [
        test_imports,
        test_env_file,
        test_supabase_connection,
        test_ai_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Unfiltered Club setup is ready to go!")
        print("   Run 'streamlit run app.py' to start the application")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("   Check the README.md for setup instructions")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
