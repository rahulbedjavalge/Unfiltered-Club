import streamlit as st
from supabase_config import init_supabase, create_post, create_comment
from ai_utils import get_ai_reply, moderate_content

st.set_page_config(page_title="Post - Unfiltered Club", page_icon="✍️")

def main():
    # Initialize session state for AI response
    if 'ai_response' not in st.session_state:
        st.session_state.ai_response = None
        st.session_state.ai_mode = None

    st.title("✍️ Share Your Truth")
    
    # Initialize Supabase
    supabase = init_supabase()
    if not supabase:
        st.error("Failed to connect to database.")
        return

    # Display previous AI response if it exists
    if st.session_state.ai_response:
        st.markdown("### 🤖 AI's Response:")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <strong>{st.session_state.ai_mode.title()} AI:</strong> {st.session_state.ai_response}
        </div>
        """, unsafe_allow_html=True)

    # Confession form
    with st.form("confession_form", clear_on_submit=True):
        st.subheader("📝 Your Confession")
        
        # Mood selection
        mood = st.selectbox(
            "What's your current vibe?",
            ["Select your mood...", "😭 sad", "😡 angry", "😑 meh", "😂 lol", "😊 happy", "🤔 confused"]
        )
        
        # Main confession text
        confession = st.text_area(
            "Spill everything here...",
            height=200,
            max_chars=2000,
            help="Share at least 10 characters"
        )
        
        # AI response mode selection
        ai_mode = st.selectbox(
            "How should AI respond to your confession?",
            ["wise", "funny", "poetic", "sarcastic", "helpful", "chaotic"]
        )

        # Submit button
        submitted = st.form_submit_button("✏️ Share Anonymously")

        if submitted:
            if mood == "Select your mood...":
                st.error("Please select a mood first! 🎭")
            elif len(confession.strip()) < 10:
                st.error("Please share at least 10 characters! 📝")
            else:
                is_appropriate, message = moderate_content(confession)
                if not is_appropriate:
                    st.error(f"Oops! {message}")
                else:
                    try:
                        # Get AI response first
                        ai_response = get_ai_reply(confession, ai_mode)
                        
                        # Create post
                        mood_clean = mood.split(" ")[1]  # Extract 'sad' from '😭 sad'
                        post = create_post(supabase, confession, mood_clean)
                        
                        if post and ai_response:
                            # Create AI comment with proper format
                            ai_comment = f"AI ({ai_mode}): {ai_response}"
                            comment = create_comment(supabase, post["id"], ai_comment, "ai_bot")
                            
                            if comment:
                                st.success("✨ Your truth has been shared!")
                                st.markdown(f"""
                                <div class="ai-reply">
                                    <strong>AI ({ai_mode}):</strong> {ai_response}
                                </div>
                                """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Something went wrong: {str(e)}")

    # Tips section
    st.markdown("---")
    st.markdown("""
    ### 💡 Pro Tips for Maximum Authenticity
    
    - **Be specific**: "I hate my job" vs "I spend 8 hours pretending to care about spreadsheets while dying inside"
    - **Embrace the weird**: Your strangest thoughts are often the most relatable
    - **No humble bragging**: This isn't LinkedIn, keep it real
    - **Vulnerability is strength**: The more honest you are, the more people will connect
    - **Use humor**: Even dark stuff can be funny when you own it
    
    Remember: Everyone here is just as weird and struggling as you are. You're among friends. 🤝
    """)

if __name__ == "__main__":
    main()
