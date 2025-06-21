import streamlit as st
from ai_utils import get_ai_reply

st.title("🤖 AI Response Test")

# Simple test interface
confession = st.text_area("Write something:", placeholder="Test the AI...")

ai_mode = st.selectbox("AI Style:", ["funny", "helpful", "poetic", "sarcastic", "wise", "chaotic"])

if st.button("Get AI Response"):
    if confession.strip():
        with st.spinner("AI is thinking..."):
            response = get_ai_reply(confession, ai_mode)
        
        st.success("AI Response:")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <strong>{ai_mode.title()} AI:</strong> {response}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please write something first!")
