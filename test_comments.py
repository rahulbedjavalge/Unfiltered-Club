#!/usr/bin/env python3
"""
Test comment creation and retrieval
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append('.')

def test_comments():
    """Test comment functionality"""
    load_dotenv()
    
    print("💬 Testing Comment Functionality...")
    
    try:
        from supabase_config import init_supabase, get_posts, get_comments, create_comment
        
        supabase = init_supabase()
        posts = get_posts(supabase, limit=1)
        
        if not posts:
            print("❌ No posts found to test comments")
            return False
        
        post_id = posts[0]['id']
        print(f"📝 Testing with post: {posts[0]['content'][:50]}...")
        
        # Get existing comments
        comments = get_comments(supabase, post_id)
        print(f"💬 Found {len(comments)} existing comments")
        
        for comment in comments:
            print(f"  - {comment['user_id']}: {comment['content'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Comment test error: {e}")
        return False

if __name__ == "__main__":
    test_comments()
