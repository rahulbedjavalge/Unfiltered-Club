#!/usr/bin/env python3
"""
Test database connection
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append('.')

def test_database():
    """Test Supabase connection"""
    load_dotenv()
    
    print("🗄️ Testing Database Connection...")
    print(f"Supabase URL exists: {'Yes' if os.getenv('SUPABASE_URL') else 'No'}")
    print(f"Supabase Key exists: {'Yes' if os.getenv('SUPABASE_KEY') else 'No'}")
    
    try:
        from supabase_config import init_supabase, get_posts
        
        supabase = init_supabase()
        if not supabase:
            print("❌ Failed to initialize Supabase client")
            return False
        
        print("✅ Supabase client initialized")
        
        # Test getting posts
        posts = get_posts(supabase, limit=5)
        print(f"✅ Retrieved {len(posts)} posts from database")
        
        if posts:
            print("📝 Sample posts:")
            for i, post in enumerate(posts[:2]):
                print(f"  {i+1}. {post['content'][:50]}... (mood: {post['mood']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    test_database()
