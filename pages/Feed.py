import streamlit as st
from supabase_config import init_supabase, get_posts, get_comments, add_reaction
from ai_utils import get_ai_reply

st.set_page_config(page_title="Feed - Unfiltered Club", page_icon="🌊")

def main():
    st.title("🌊 The Feed of Feels")
    
    # Initialize Supabase
    supabase = init_supabase()
    if not supabase:
        st.error("Failed to connect to database.")
        return

    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mood_filter = st.selectbox(
            "Filter by mood:",
            ["All", "sad", "angry", "meh", "lol", "happy", "confused"]
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Latest", "Most Commented", "Most Reacted"]
        )
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()

    # Get posts
    posts = get_posts(supabase, limit=100)
    
    # Apply filters
    if mood_filter != "All":
        posts = [p for p in posts if p['mood'] == mood_filter]
    
    if not posts:
        st.info("No confessions match your filters. Try adjusting them!")
        return

    # Display posts
    for post in posts:
        with st.container():
            # Mood badge
            mood_colors = {
                "sad": "🔴", "angry": "🟠", "meh": "🟡", 
                "lol": "🔵", "happy": "🟢", "confused": "🟣"
            }
            
            st.markdown(f"**{mood_colors.get(post['mood'], '⚪')} {post['mood'].upper()}**")
            st.markdown(post['content'])
            st.caption(f"Posted {post['created_at'][:10]} • Anonymous")
            
            # Comments
            comments = get_comments(supabase, post['id'])
            if comments:
                with st.expander(f"💬 {len(comments)} comments"):
                    for comment in comments:
                        if comment['user_id'] == 'ai_bot':
                            st.markdown(f"🤖 {comment['content']}")
                        else:
                            st.markdown(f"👤 {comment['content']}")
            
            # Quick reactions
            col1, col2, col3, col4 = st.columns(4)
            reactions = ["❤️", "😭", "😂", "🔥"]
            
            for i, (col, emoji) in enumerate(zip([col1, col2, col3, col4], reactions)):
                with col:
                    if st.button(emoji, key=f"feed_react_{post['id']}_{i}"):
                        add_reaction(supabase, post['id'], emoji)
                        st.success(f"Reacted with {emoji}")
            
            st.divider()

if __name__ == "__main__":
    main()
