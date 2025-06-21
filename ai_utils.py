import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

load_dotenv()

def get_ai_reply(post_text: str, mode: str = "funny"):
    """Generate AI reply to a post using OpenRouter API"""
    api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
    
    if not api_key:
        return "🤖 AI is taking a coffee break... (API key not configured)"
    
    # Define different response modes with optimized prompts for Mistral Small
    mode_prompts = {
        "funny": "You are a witty and humorous AI friend. Reply to this confession with light humor and supportive wit. Keep it friendly and funny:",
        "helpful": "You are a supportive counselor. Reply to this confession with genuine, practical advice and empathy. Be constructive and encouraging:",
        "poetic": "You are a creative poet. Reply to this confession using beautiful, metaphorical language and artistic expression:",
        "sarcastic": "You are a playfully sarcastic friend. Reply with gentle, good-natured sarcasm while still being supportive. Don't be mean:",
        "wise": "You are a wise mentor. Reply to this confession with deep insight, wisdom, and thoughtful perspective:",
        "chaotic": "You are an unhinged but caring friend. Reply in the most chaotic, random way possible while still being supportive and positive:"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct:free",
        "messages": [
            {"role": "user", "content": f"{mode_prompts.get(mode, mode_prompts['funny'])}\n\nConfession: '{post_text}'\n\nReply in 1 sentence:"}
        ],
        "max_tokens": 100,  # Limit response length for conciseness
        "temperature": 0.75,  # Adjusted for consistent creativity
        "top_p": 1.0,  # Ensure diverse responses
        "frequency_penalty": 0.0  # Avoid repetition
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            json=data, 
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # Return single response without alternatives
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"🤖 AI is having technical difficulties... (Error {response.status_code})"
            
    except Exception as e:
        return f"🤖 AI is temporarily offline... ({str(e)[:50]})"

def get_random_ai_encouragement():
    """Get a random encouraging message"""
    encouragements = [
        "🌟 You're braver than you think for sharing this!",
        "💫 Sometimes the best confessions come from the heart.",
        "🔥 Your authenticity is refreshing in this fake world.",
        "✨ Thank you for being real with us.",
        "🌈 Every confession is a step toward freedom.",
        "💎 Your vulnerability is your superpower.",
        "🚀 You're not alone in feeling this way.",
        "🌸 Healing happens when we speak our truth."
    ]
    
    import random
    return random.choice(encouragements)

def moderate_content(text: str):
    """Basic content moderation (can be enhanced)"""
    # Simple keyword filtering - can be made more sophisticated
    banned_words = ["hate", "kill", "die", "suicide"]  # Add more as needed
    
    text_lower = text.lower()
    for word in banned_words:
        if word in text_lower:
            return False, f"Content contains inappropriate language: '{word}'"
    
    if len(text) > 2000:
        return False, "Content is too long (max 2000 characters)"
    
    if len(text.strip()) < 3:
        return False, "Content is too short"
    
    return True, "Content approved"
