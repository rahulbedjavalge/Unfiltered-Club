# 🧠 Unfiltered Club

**Anonymous Confession Feed with AI Replies**

An anonymous, AI-powered social feed for rants, confessions, breakdowns, weird thoughts—anything you want to express without judgment. Think Reddit meets AI Therapist meets Twitter.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28.0-red.svg)
![Supabase](https://img.shields.io/badge/supabase-backend-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **🎭 Anonymous Confessions**: Share anything without revealing your identity
- **🤖 AI Responses**: Get replies in different modes (funny, helpful, poetic, sarcastic, wise, chaotic)
- **😭 Mood Tracking**: Tag your confessions with emotions
- **💬 Anonymous Comments**: Support others without revealing yourself
- **❤️ Reactions**: React with emojis to show support
- **📊 Session Stats**: Track your anonymous journey
- **🌙 Dark Mode**: Comfortable viewing in any lighting
- **📱 Mobile Responsive**: Works great on all devices

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Supabase (PostgreSQL, Auth, Realtime)
- **AI**: OpenRouter API (GPT-4, Claude, Mixtral)
- **Deployment**: Streamlit Cloud
- **Styling**: Custom CSS with modern UI/UX

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Supabase account
- OpenRouter API key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/unfiltered-club.git
cd unfiltered-club
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Copy the database setup SQL from `database_setup.sql`
3. Run it in your Supabase SQL editor
4. Get your project URL and anon key from Settings > API

### 5. Set Up OpenRouter

1. Go to [openrouter.ai](https://openrouter.ai) and create an account
2. Get your API key from the dashboard
3. You get free credits to start!

### 6. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 7. Run the App

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` and start confessing! 🎉

## 📁 Project Structure

```
unfiltered-club/
├── app.py                      # Main Streamlit app
├── supabase_config.py          # Database functions
├── ai_utils.py                 # AI response generation
├── requirements.txt            # Python dependencies
├── database_setup.sql          # Database schema
├── .env.example               # Environment template
├── pages/
│   ├── Feed.py                # Browse confessions
│   ├── Post.py                # Create confessions
│   └── Profile.py             # Anonymous profile
├── assets/
│   ├── styles.css             # Custom styling
│   └── icons/                 # App icons
└── README.md                  # You are here!
```

## 🗄️ Database Schema

### Core Tables

- **posts**: User confessions with mood and content
- **comments**: Anonymous comments and AI replies
- **reactions**: Emoji reactions to posts
- **user_profiles**: Anonymous session-based profiles
- **rooms**: Private confession rooms (future feature)

### Key Features

- Row Level Security (RLS) enabled
- Anonymous access policies
- Automatic timestamps
- Performance indexes
- Stats aggregation

## 🤖 AI Modes

The AI can respond in different personality modes:

- **🤣 Funny**: Humorous and witty responses
- **🤝 Helpful**: Practical advice and support
- **🎭 Poetic**: Artistic and metaphorical replies
- **😏 Sarcastic**: Playful sarcasm (but kind)
- **🧠 Wise**: Deep insights and wisdom
- **🌪️ Chaotic**: Unhinged but supportive chaos

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add your environment variables in "Advanced settings":
   - `SUPABASE_URL`
   - `SUPABASE_KEY` 
   - `OPENROUTER_API_KEY`
5. Deploy!

### Other Options

- **Heroku**: Use the included `Procfile`
- **Railway**: Direct GitHub deployment
- **DigitalOcean App Platform**: Container deployment
- **Self-hosted**: Use Docker or traditional VPS

## 💰 Monetization Ideas

- **Freemium Model**: Daily usage limits
- **Tip System**: Support favorite confessions
- **Private Rooms**: Paid exclusive spaces
- **Creator Profiles**: Earn from authentic content
- **AI Therapy**: Premium therapeutic AI assistant
- **Custom AI Modes**: Personalized response styles

## 🛡️ Privacy & Security

- **True Anonymity**: No real user tracking
- **Session-based**: Data resets with browser
- **Content Moderation**: Basic filtering for safety
- **No Personal Data**: Zero PII collection
- **Open Source**: Transparent code

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add docstrings to functions
- Test your changes thoroughly
- Update documentation as needed

## 📝 Roadmap

### Phase 1 (Current)
- [x] Basic confession posting
- [x] AI responses
- [x] Anonymous comments
- [x] Emoji reactions
- [x] Mobile responsive design

### Phase 2 (Next)
- [ ] Image uploads
- [ ] Private rooms
- [ ] Advanced content moderation
- [ ] Real-time notifications
- [ ] Enhanced AI personalities

### Phase 3 (Future)
- [ ] Voice confessions
- [ ] AI therapy sessions
- [ ] Community challenges
- [ ] Mood analytics
- [ ] Integration APIs

## 🐛 Known Issues

- AI responses may occasionally be slow due to API limits
- Large posts might not display perfectly on very small screens
- Session data is lost when browser is closed (by design)

## 📧 Support

- **Email**: rahullaptopp@gmail.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/unfiltered-club/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/unfiltered-club/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing framework
- **Supabase** for the backend infrastructure  
- **OpenRouter** for AI API access
- **The Community** for being authentically unfiltered

---

**Made with chaos and heart by [Rahul](mailto:rahullaptopp@gmail.com)** 💙

*"In a world of filters, be unfiltered."* ✨
