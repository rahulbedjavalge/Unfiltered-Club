import os
import uuid
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def init_supabase():
    """Initialize Supabase client"""
    url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
    
    if not url or not key:
        st.error("Supabase credentials not found! Please check your .env file or Streamlit secrets.")
        return None
    
    return create_client(url, key)

def create_post(supabase: Client, content: str, mood: str, user_id: str = None):
    """Create a new post"""
    try:
        data = {
            "content": content,
            "mood": mood,
            "user_id": user_id
        }
        result = supabase.table("posts").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error creating post: {str(e)}")
        return None

def get_posts(supabase: Client, limit: int = 50):
    """Get all posts ordered by creation time"""
    try:
        result = supabase.table("posts").select("*").order("created_at", desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching posts: {str(e)}")
        return []

def create_comment(supabase: Client, post_id: str, content: str, user_id: str = None):
    """Create a comment on a post"""
    try:
        # Generate a valid UUID for AI bot if user_id is 'ai_bot'
        if user_id == "ai_bot":
            user_id = str(uuid.uuid4())

        data = {
            "post_id": post_id,
            "content": content,
            "user_id": user_id
        }
        result = supabase.table("comments").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error creating comment: {str(e)}")
        return None

def get_comments(supabase: Client, post_id: str):
    """Get comments for a specific post"""
    try:
        result = supabase.table("comments").select("*").eq("post_id", post_id).order("created_at", desc=False).execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching comments: {str(e)}")
        return []

def add_reaction(supabase: Client, post_id: str, emoji: str, user_id: str = None):
    """Add a reaction to a post"""
    try:
        # Check if user already reacted
        existing = supabase.table("reactions").select("*").eq("post_id", post_id).eq("user_id", user_id or "anon").execute()
        
        if existing.data:
            # Update existing reaction
            result = supabase.table("reactions").update({"emoji": emoji}).eq("id", existing.data[0]["id"]).execute()
        else:
            # Create new reaction
            data = {
                "post_id": post_id,
                "emoji": emoji,
                "user_id": user_id or "anon"
            }
            result = supabase.table("reactions").insert(data).execute()
        
        return result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Error adding reaction: {str(e)}")
        return None

def get_reactions(supabase: Client, post_id: str):
    """Get reactions for a specific post"""
    try:
        result = supabase.table("reactions").select("*").eq("post_id", post_id).execute()
        return result.data
    except Exception as e:
        st.error(f"Error fetching reactions: {str(e)}")
        return []

def count_reactions(supabase: Client, post_id: str):
    """Count reactions for a specific post"""
    try:
        result = supabase.table("reactions").select("emoji").eq("post_id", post_id).execute()
        if result.data:
            counts = {}
            for reaction in result.data:
                emoji = reaction['emoji']
                counts[emoji] = counts.get(emoji, 0) + 1
            return [{"emoji": emoji, "count": count} for emoji, count in counts.items()]
        return []
    except Exception as e:
        st.error(f"Error counting reactions: {str(e)}")
        return None

def delete_all_data(supabase: Client):
    """Delete all posts, comments, and reactions from the database"""
    try:
        # Delete all records with proper WHERE clauses
        supabase.table("reactions").delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        supabase.table("comments").delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        supabase.table("posts").delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        return True, "All data deleted successfully"
    except Exception as e:
        return False, f"Error deleting data: {str(e)}"

def get_user_stats(supabase: Client, user_id: str = None):
    """Get user statistics"""
    try:
        # Get post count
        posts = supabase.table("posts").select("id").execute()
        post_count = len(posts.data) if posts.data else 0

        # Get comment count
        comments = supabase.table("comments").select("id").execute()
        comment_count = len(comments.data) if comments.data else 0

        # Get reaction count
        reactions = supabase.table("reactions").select("id").execute()
        reaction_count = len(reactions.data) if reactions.data else 0

        # Get unique moods
        if posts.data:
            unique_moods = len(set(post['mood'] for post in posts.data if 'mood' in post))
        else:
            unique_moods = 0

        return {
            "posts": post_count,
            "comments": comment_count,
            "reactions": reaction_count,
            "unique_moods": unique_moods
        }
    except Exception as e:
        st.error(f"Error fetching stats: {str(e)}")
        return {
            "posts": 0,
            "comments": 0,
            "reactions": 0,
            "unique_moods": 0
        }
