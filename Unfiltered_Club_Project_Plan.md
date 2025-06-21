# 🧠 Unfiltered Club – Anonymous Confession Feed with AI Replies

An anonymous, AI-powered social feed for rants, confessions, breakdowns, weird thoughts—anything you want to express without judgment. Think Reddit meets AI Therapist meets Twitter, built with **Streamlit + Supabase + OpenRouter**.

---

## ⚙️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Supabase (Auth, Realtime DB, Storage)
- **AI**: OpenRouter (GPT-4, Claude, or Mixtral with free API)
- **Deployment**: Streamlit Cloud / Netlify (via frontend wrapper)

---

## 🛠️ Features

- Anonymous or email login (Supabase)
- Confession post (text, emoji, optional image)
- Live feed of user confessions
- AI replies (funny, helpful, poetic, sarcastic modes)
- React with emojis
- Comment anonymously
- Private rooms (future)
- Mood tag (sad, angry, meh, lol, etc.)
- “Boost” your post (via credits)

---

## 📁 Folder Structure

```
unfiltered-club/
├── app.py                  # Main Streamlit app
├── supabase_config.py      # Supabase setup and functions
├── ai_utils.py             # Handles OpenRouter API
├── pages/
│   ├── Feed.py
│   ├── Post.py
│   ├── Profile.py
├── assets/
│   ├── styles.css
│   └── icons/
└── README.md
```

---

## 🔐 Supabase Setup

1. Create project at [supabase.com](https://supabase.com)
2. Enable:
   - Auth (email + anon)
   - Database (Post table, Comment table, Reaction table)
3. Tables:
   ```sql
   CREATE TABLE posts (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     content text,
     user_id uuid,
     mood text,
     created_at timestamp DEFAULT now()
   );

   CREATE TABLE comments (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     post_id uuid,
     content text,
     user_id uuid,
     created_at timestamp DEFAULT now()
   );
   ```

---

## 🔑 OpenRouter API

1. Get free API key: [https://openrouter.ai](https://openrouter.ai)
2. Store it in `.env`
3. Use model like `mistralai/mixtral-8x7b` or `openai/gpt-3.5-turbo`

```python
# ai_utils.py
import requests

def ai_reply_to_post(post_text, mode="funny"):
    prompt = f"Reply to this confession in a {mode} tone:\n'{post_text}'"
    headers = {
        "Authorization": f"Bearer {YOUR_API_KEY}"
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json={
        "model": "mistralai/mixtral-8x7b",
        "messages": [{"role": "user", "content": prompt}]
    }, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
```

---

## 🖥️ Run Locally

```bash
git clone https://github.com/rahul/unfiltered-club.git
cd unfiltered-club
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

- Push to GitHub
- Go to [streamlit.io/cloud](https://streamlit.io/cloud)
- Connect your repo
- Add `OPENROUTER_API_KEY` and `SUPABASE_URL` + `SUPABASE_KEY` to secrets

---

## 💰 Monetization Ideas

- Freemium daily usage limit
- Tip a post (like Reddit Gold)
- Private rooms (paid)
- Creator profiles (earn tips)
- Journaling + AI therapy assistant (premium)

---

## 📬 Contact

Made with chaos and heart by Rahul.  
Drop confessions or love letters: [rahullaptopp@gmail.com](mailto:rahullaptopp@gmail.com)