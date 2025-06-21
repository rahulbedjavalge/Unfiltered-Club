import streamlit as st
import uuid
from datetime import datetime
from supabase_config import init_supabase, create_post, get_posts
from ai_utils import get_ai_reply, get_random_ai_encouragement

# Page config
st.set_page_config(
    page_title="Unfiltered Club 🧠",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .tagline {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .post-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .mood-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .mood-sad { background: #FFE5E5; color: #D63384; }
    .mood-angry { background: #FFE5E5; color: #DC3545; }
    .mood-meh { background: #FFF3CD; color: #F57C00; }
    .mood-lol { background: #D1ECF1; color: #0C63E4; }
    .mood-happy { background: #D4EDDA; color: #198754; }
    .mood-confused { background: #E2E3E5; color: #6C757D; }
    
    .ai-reply {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-style: italic;
    }
    
    .ai-reply strong {
        color: #fff;
        font-weight: bold;
    }
    
    .timestamp {
        color: #999;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize all session state variables
    if 'posts_count' not in st.session_state:
        st.session_state.posts_count = 0
    if 'comments_count' not in st.session_state:
        st.session_state.comments_count = 0
    if 'reactions_count' not in st.session_state:
        st.session_state.reactions_count = 0
    if 'ai_responses' not in st.session_state:
        st.session_state.ai_responses = {}
    if 'current_ai_response' not in st.session_state:
        st.session_state.current_ai_response = None
    
    # Initialize Supabase
    supabase = init_supabase()
    if not supabase:
        st.error("Failed to connect to database. Please check your configuration.")
        return

    # Header
    st.markdown('<h1 class="main-header">🧠 Unfiltered Club</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Anonymous confessions, AI wisdom, zero judgment</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🎭 Express Yourself")
        
        # Mood selector
        mood = st.selectbox(
            "How are you feeling?",
            ["😭 sad", "😡 angry", "😑 meh", "😂 lol", "😊 happy", "🤔 confused"],
            help="Pick your current vibe"
        )
        
        # Confession input
        confession = st.text_area(
            "What's on your mind?",
            placeholder="Spill everything here... no judgment, just authenticity ✨",
            height=150,
            max_chars=2000
        )
        # AI reply mode
        ai_mode = st.selectbox(
            "AI Reply Style",
            ["funny", "helpful", "poetic", "sarcastic", "wise", "chaotic"],
            help="How should AI respond to your confession?"
        )
        
        # Buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🤖 Get AI Response", use_container_width=True):
                if confession.strip():
                    with st.spinner("🤖 AI is thinking..."):
                        ai_response = get_ai_reply(confession, ai_mode)

                    if ai_response:
                        st.markdown("### 🤖 AI Response:")
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                                <strong>{ai_mode.title()} AI:</strong> {ai_response}
                            </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.warning("Write something first!")
        
        with col2:
            # Post button
            if st.button("🚀 Post & Get AI Reply", use_container_width=True):
                if confession.strip():
                    # Generate AI reply first
                    with st.spinner("🤖 AI is crafting a response..."):
                        ai_response = get_ai_reply(confession, ai_mode)
                        st.session_state.current_ai_response = ai_response
                
                    # Create post
                    mood_clean = mood.split(" ")[1]  # Extract just the word
                    post = create_post(supabase, confession, mood_clean)
                    
                    if post:
                        # Store AI response for this post
                        st.session_state.ai_responses[post['id']] = {
                            'response': ai_response,
                            'mode': ai_mode
                        }
                        
                        # Create AI comment
                        if ai_response:
                            create_comment(supabase, post["id"], f"🤖 AI ({ai_mode}): {ai_response}", "ai_bot")
                            st.success("🎉 Confession posted with AI response!")
                        
                        # Increment posts count
                        st.session_state.posts_count += 1

                        # Don't rerun immediately so user can see the AI response
                        st.info("👀 Check out the main feed below to see your confession live!")
                    else:
                        st.error("Failed to post confession. Try again!")
            else:
                st.warning("Write something first! Even 'blah' counts as authentic expression.")
        
        st.markdown("---")
        st.markdown("💡 **Tip**: Be real, be raw, be you. This is your safe space.")
        st.markdown(get_random_ai_encouragement())

    # Main feed
    st.header("🌊 The Feed of Feels")
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Refresh Feed", use_container_width=True):
            st.rerun()

    # Get and display posts
    posts = get_posts(supabase, limit=50)
    
    if not posts:
        st.info("🌱 Be the first to share something!")
        return
        
    for post in posts:
        with st.container():
            st.markdown(f"""
            <div class="post-card">
                <span class="mood-tag mood-{post['mood']}">{post['mood'].upper()}</span>
                <p>{post['content']}</p>
                <div class="timestamp">Posted {format_time_ago(post['created_at'])}</div>
            </div>
            """, unsafe_allow_html=True)

            # Get AI response for this post if not already in session state
            if post['id'] not in st.session_state.ai_responses:
                ai_response = get_ai_reply(post['content'], "wise")
                st.session_state.ai_responses[post['id']] = {
                    'response': ai_response,
                    'mode': 'wise'
                }
            
            # Display AI response if it exists
            if 'ai_responses' in st.session_state and post['id'] in st.session_state.ai_responses:
                ai_data = st.session_state.ai_responses[post['id']]
                st.markdown(f"""
                <div class="ai-reply">
                    AI ({ai_data['mode']}): {ai_data['response']}
                </div>
                """, unsafe_allow_html=True)
            
            # Reaction buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("❤️", key=f"love_{post['id']}")
            with col2:
                st.button("😂", key=f"laugh_{post['id']}")
            with col3:
                st.button("🤝", key=f"support_{post['id']}")
            with col4:
                st.button("🔥", key=f"fire_{post['id']}")
        
        # Comment section
        with st.expander("💬 Add Anonymous Comment"):
            comment_text = st.text_area(
                "Your anonymous comment:",
                key=f"comment_{post['id']}",
                placeholder="Share your thoughts, support, or just say 'felt that'..."
            )
            
            if st.button("Post Comment", key=f"post_comment_{post['id']}"):
                if comment_text.strip():
                    from supabase_config import create_comment
                    create_comment(supabase, post['id'], comment_text)
                    st.success("Comment posted anonymously!")
                    
                    # Increment session state for comments count
                    if 'comments_count' not in st.session_state:
                        st.session_state.comments_count = 0
                    st.session_state.comments_count += 1

                    st.rerun()
        
        st.markdown("---")

def format_time_ago(timestamp):
    """Format timestamp to 'X time ago' format"""
    try:
        from datetime import datetime, timezone
        import re
        
        # Parse the timestamp
        if isinstance(timestamp, str):
            # Remove timezone info if present and parse
            clean_timestamp = re.sub(r'\+\d{2}:\d{2}$', '', timestamp)
            dt = datetime.fromisoformat(clean_timestamp)
        else:
            dt = timestamp
        
        # Calculate time difference
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return "just now"
    except:
        return "some time"

if __name__ == "__main__":
    main()
