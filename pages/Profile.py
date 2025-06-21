import streamlit as st
from supabase_config import init_supabase, get_posts

st.set_page_config(page_title="Profile - Unfiltered Club", page_icon="👤")

def main():
    st.title("👤 Your Anonymous Profile")
    
    # Initialize Supabase
    supabase = init_supabase()
    if not supabase:
        st.error("Failed to connect to database.")
        return

    # Display anonymous ID
    if 'anon_id' not in st.session_state:
        import uuid
        st.session_state.anon_id = str(uuid.uuid4())[:8]

    st.markdown(f"**Your Anonymous ID:** `{st.session_state.anon_id}`")
    st.caption("This ID resets each session to keep you completely anonymous")

    # Get user stats
    from supabase_config import get_user_stats
    stats = get_user_stats(supabase)

    # Display stats in columns
    st.subheader("📊 Your Impact Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Confessions", stats['posts'])
    with col2:
        st.metric("Comments", stats['comments'])
    with col3:
        st.metric("Reactions", stats['reactions'])

    # Mood Journey
    st.subheader("🌈 Your Mood Journey")
    if stats['posts'] > 0:
        # Display mood stats
        st.metric("Unique Moods Expressed", stats['unique_moods'])
    else:
        st.info("Start posting confessions to track your mood journey!")

    # Achievements section
    st.subheader("🏆 Anonymous Achievements")
    
    achievements = [
        {
            "name": "First Steps",
            "desc": "Made your first confession",
            "unlocked": stats['posts'] > 0,
            "icon": "🎯"
        },
        {
            "name": "Community Player",
            "desc": "Commented on someone's confession",
            "unlocked": stats['comments'] > 0,
            "icon": "💬"
        },
        {
            "name": "Mood Ring",
            "desc": f"Expressed {stats['unique_moods']}/3 different moods",
            "unlocked": stats['unique_moods'] >= 3,
            "icon": "🎭"
        },
        {
            "name": "Reactor",
            "desc": "Reacted to 5+ confessions",
            "unlocked": stats['reactions'] >= 5,
            "icon": "⭐"
        },
        {
            "name": "Open Book",
            "desc": "Posted 5+ confessions",
            "unlocked": stats['posts'] >= 5,
            "icon": "📖"
        },
        {
            "name": "Support Squad",
            "desc": "Commented 10+ times",
            "unlocked": stats['comments'] >= 10,
            "icon": "🤝"
        }
    ]

    # Display achievements
    for achievement in achievements:
        if achievement["unlocked"]:
            st.success(f"{achievement['icon']} {achievement['name']}: {achievement['desc']}")
        else:
            st.info(f"🔒 {achievement['name']}: {achievement['desc']}")

    # Personal Reflection
    st.subheader("💭 Personal Reflection")
    reflection = st.text_area(
        "How are you feeling about your anonymous journey here?",
        placeholder="This is just for you. Write about your experience, what you've learned, how you've grown..."
    )
    if st.button("💾 Save Reflection (Local Only)"):
        if reflection:
            st.session_state.reflection = reflection
            st.success("Reflection saved locally!")

    # Privacy reminder
    st.subheader("🔒 Privacy Reminder")
    st.markdown("""
    * Your data is session-based and resets when you close the browser
    * No real identifying information is stored
    * All confessions are truly anonymous
    * Your reflections are stored only locally in your browser
    * We can't connect your confessions to you personally
    
    Stay authentic, stay anonymous, stay unfiltered. 😊
    """)

    # Danger Zone
    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    if st.button("🗑️ Delete All Posts", type="primary", use_container_width=True):
        with st.spinner("Deleting all data..."):
            from supabase_config import delete_all_data
            success, message = delete_all_data(supabase)
            if success:
                st.success("✅ All data has been deleted successfully!")
                st.rerun()
            else:
                st.error(f"❌ {message}")

if __name__ == "__main__":
    main()
