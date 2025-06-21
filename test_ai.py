#!/usr/bin/env python3
"""
Quick test for AI functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append('.')

def test_ai_connection():
    """Test AI API directly"""
    load_dotenv()
    
    print("🤖 Testing AI Connection...")
    print(f"API Key exists: {'Yes' if os.getenv('OPENROUTER_API_KEY') else 'No'}")
    
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ No API key found!")
        return False
    
    try:
        from ai_utils import get_ai_reply
        
        print("🧪 Testing AI response...")
        test_confession = "I eat cereal for dinner and I'm not sorry about it"
        
        response = get_ai_reply(test_confession, "funny")
        print(f"✅ AI Response: {response}")
        
        if "API key not configured" in response:
            print("❌ API key issue")
            return False
        elif "technical difficulties" in response:
            print("❌ API connection issue")
            return False
        elif "temporarily offline" in response:
            print("❌ Network or API error")
            return False
        else:
            print("✅ AI is working correctly!")
            return True
            
    except Exception as e:
        print(f"❌ Error testing AI: {e}")
        return False

if __name__ == "__main__":
    test_ai_connection()
