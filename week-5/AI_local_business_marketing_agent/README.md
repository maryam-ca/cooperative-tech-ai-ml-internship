# AI Local Business Marketing Agent

**Automated Marketing Suite for Local Businesses**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.59+-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-Pytest-orange)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)

---

## 1. PROJECT OVERVIEW

**AI Local Business Marketing Agent** is a comprehensive marketing automation platform designed for local businesses. It leverages artificial intelligence to generate and manage marketing content across multiple platforms — including Facebook, Instagram, Google Business, WhatsApp, and Email — from a single, unified dashboard.

The system uses a **keyword + template based AI content engine** that maps business type, campaign objective, and platform to generate high-quality, platform-optimized marketing copy. Business owners can create, schedule, and publish campaigns without writing a single line of copy themselves.

### System Workflow

```
Business Owner selects: Business Type + Platform + Campaign Type + Custom Instructions
                              ↓
AI Content Generator maps context → Template + Dynamic Content
                              ↓
Content Editor (review, edit, sentiment analysis, hashtag suggestions)
                              ↓
Media Upload (images/videos) + Hashtag optimization
                              ↓
┌─────────────────────────────┴─────────────────────────────┐
↓                                                           ↓
Save as Draft                                        Schedule / Publish
                                                           ↓
                                                ┌──────────────┴──────────────┐
                                                ↓                             ↓
                                           Immediate                         Scheduled
                                                ↓                             ↓
                                       Platform API / Webhook           Background Scheduler
                                                ↓                             ↓
                                          Live Post                       Auto-Publish
```

---

## 2. KEY FEATURES

| Feature | Description |
|---------|-------------|
| **AI Content Generation** | Template-based engine generates platform-optimized copy for Facebook, Instagram, Google Business, WhatsApp, Email |
| **Multi-Platform Support** | Publish to Facebook, Instagram, Google Business Profile, WhatsApp, and Email from one dashboard |
| **Business Type Templates** | Pre-built templates for Restaurants, Gyms, Retail Shops, Clinics with industry-specific language |
| **Campaign Types** | Promotional, Educational, Engagement, Seasonal, Announcement, Loyalty, Event, UGC, Review Request |
| **Smart Scheduling** | Schedule posts for future dates/times with timezone awareness |
| **Content Editor** | Rich text editor with live character/word count, reading time, sentiment analysis |
| **Sentiment Analysis** | Real-time sentiment scoring (Positive/Neutral/Negative) with confidence and suggestions |
| **Hashtag Optimization** | Auto-suggested hashtags per business type + custom tag input |
| **Media Upload** | Drag-and-drop image/video upload with preview and file size validation |
| **Post Preview** | Platform-specific preview cards (Facebook, Instagram, WhatsApp, Google, Email) |
| **Campaign History** | Full CRUD with filtering by platform, date range, status (Draft/Scheduled/Published/Archived) |
| **Analytics Dashboard** | Campaign performance (reach, engagement), platform distribution, recent activity |
| **Google Business Integration** | Direct posting to Google Business Profile via API |
| **Email Campaign Builder** | HTML email template generation with preview |
| **WhatsApp Campaign Builder** | WhatsApp-formatted message generation with preview |
| **Settings & Customization** | Business profile, AI tone/style, API keys, data management, appearance themes |
| **Duplicate & Clone Campaigns** | One-click campaign duplication for rapid iteration |
| **Data Export/Import** | Backup and restore campaign data in JSON format |

---

## 3. TECH STACK

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.8+ |
| **Frontend Framework** | Streamlit 1.59+ |
| **AI/ML** | Custom template engine + TextBlob sentiment analysis |
| **Database** | SQLite (via custom DatabaseManager with connection pooling) |
| **Scheduling** | APScheduler (background jobs) |
| **Visualization** | Plotly (interactive charts) |
| **Data Processing** | Pandas, NumPy |
| **Image Processing** | Pillow (PIL) |
| **Environment Config** | python-dotenv |
| **Styling** | Custom CSS3 with CSS Variables, animations, glassmorphism |
| **Icons** | Inline SVG (no external dependencies) |
| **Fonts** | Space Grotesk + Manrope (Google Fonts) |
| **Testing** | Pytest |
| **Code Formatting** | Black, isort |
| **Linting** | Flake8, Pylint |

---

## 4. FOLDER STRUCTURE

```
ai-local-business-marketing-agent/
│
├── app.py                      # Main Streamlit application entry point
├── check_syntax.py             # Syntax validation script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .gitignore
├── README.md
│
├── assets/                     # Static assets (logos, icons, images)
│   └── __init__.py
│
├── config/
│   ├── __init__.py
│   └── settings.py             # App config, business types, platforms, templates
│
├── models/
│   ├── __init__.py
│   ├── content_generator.py    # AI template-based content generation
│   ├── social_media.py         # Facebook/Instagram posting logic
│   ├── email_campaign.py       # Email campaign builder
│   ├── whatsapp_campaign.py    # WhatsApp message builder
│   ├── google_business.py      # Google Business Profile API
│   └── sentiment_analyzer.py   # TextBlob-based sentiment scoring
│
├── frontend/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py          # Navigation sidebar component
│   │   ├── dashboard.py        # Analytics + quick actions
│   │   ├── campaign_creator.py # Content creation wizard
│   │   ├── analytics.py        # Charts + insights
│   │   └── settings.py         # Business profile, AI, API, data, appearance
│   └── styles/
│       ├── __init__.py
│       └── custom.css          # Complete design system (Aurora/Neon theme)
│
├── utils/
│   ├── __init__.py
│   ├── database.py             # SQLite CRUD + connection pooling
│   ├── analytics.py            # Aggregation + performance summaries
│   ├── validators.py           # Input validation utilities
│   └── formatters.py           # Data formatting utilities
│
├── data/
│   ├── __init__.py
│   └── campaigns.db            # SQLite database (auto-created)
│
├── tests/                      # Unit & integration tests
│   ├── __init__.py
│   ├── test_content_generator.py
│   └── test_campaigns.py
│
└── notebooks/                  # Jupyter notebooks for experimentation
```

---

## 5. INSTALLATION & SETUP

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1 — Clone the repository
```bash
git clone https://github.com/your-username/ai-local-business-marketing-agent.git
cd ai-local-business-marketing-agent
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Step 5 — Run the application
```bash
streamlit run app.py
```
The app will be available at **http://localhost:8501**

---

## 6. CONFIGURATION

### Environment Variables (`.env`)
```env
# Social Media APIs (optional - for actual posting)
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_long_lived_token
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
WHATSAPP_API_TOKEN=your_whatsapp_business_token
GOOGLE_BUSINESS_API_KEY=your_google_api_key
GOOGLE_BUSINESS_LOCATION_ID=your_location_id

# Email (for email campaigns)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password

# Scheduling
SCHEDULER_TIMEZONE=UTC
```

---

## 7. USAGE GUIDE

### Creating Your First Campaign
1. **Launch the app** → Navigate to **"Create Campaign"**
2. **Enter Campaign Name** → e.g., "Summer Sale 2024"
3. **Select Business Type** → Restaurant, Gym, Shop, or Clinic
4. **Choose Platform** → Facebook, Instagram, Google Business, WhatsApp, or Email
5. **Pick Campaign Type** → Promotional, Educational, Engagement, etc.
6. **Add Custom Instructions** (optional) → Tone, target audience, special offers
7. **Click "Generate Content"** → AI creates platform-optimized copy
8. **Review & Edit** → Use the content editor, check sentiment, add hashtags
9. **Upload Media** → Drag & drop images/videos
10. **Save / Schedule / Publish** → Choose your workflow

### Dashboard Overview
- **Quick Stats** — Total campaigns, avg engagement, active campaigns, total reach
- **Charts** — Campaign performance bar chart, platform distribution pie chart
- **Recent Activity** — Last 5 campaigns with status indicators
- **Quick Actions** — One-click navigation to Create, Analytics, Templates, Social

### Analytics
- **Campaign Performance** — Reach & engagement per campaign
- **Platform Distribution** — Campaign count by platform
- **Engagement Trends** — Time-series analysis
- **Campaign Details** — Drill-down with filters

### Settings
- **Business Profile** — Name, type, contact info, address, description
- **Appearance** — Theme, font, sidebar behavior
- **AI Settings** — Tone, creativity, length preferences
- **API Keys** — Social media, email, Google Business
- **Data Management** — Export/Import, backup, clear history

---

## 8. DATABASE SCHEMA (SQLite)

### campaigns
```sql
id INTEGER PRIMARY KEY,
name TEXT,
type TEXT,                    -- promotional, educational, etc.
platform TEXT,                -- facebook, instagram, google_business, whatsapp, email
business_type TEXT,           -- restaurant, gym, shop, clinic
content TEXT,                 -- generated marketing copy
status TEXT,                  -- draft, scheduled, published, archived
schedule TEXT,                -- ISO datetime string
created_at TEXT,              -- ISO datetime
published_at TEXT,            -- ISO datetime (nullable)
metadata TEXT,                -- JSON: hashtags, media_count, custom_prompt, context
engagement_data TEXT          -- JSON: likes, comments, shares, reach
```

---

## 9. DEVELOPMENT

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=.

# Run specific test file
pytest tests/test_content_generator.py -v
```

### Code Quality
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type checking (if using mypy)
mypy .
```

### Syntax Check
```bash
python check_syntax.py
```

---

## 10. FUTURE ROADMAP

- [ ] **Real LLM Integration** — Replace template engine with OpenAI/Anthropic for true generative AI
- [ ] **Direct API Publishing** — Full Facebook/Instagram Graph API, Google Business API, WhatsApp Business API
- [ ] **Video Generation** — AI-generated video clips for Reels/TikTok
- [ ] **A/B Testing** — Auto-generate variants and track performance
- [ ] **Competitor Monitoring** — Track competitor posts and trends
- [ ] **Multi-language Support** — Generate content in Hindi, Spanish, Arabic, etc.
- [ ] **Team Collaboration** — Role-based access, approval workflows
- [ ] **Advanced Analytics** — ROI tracking, customer acquisition cost, LTV
- [ ] **Mobile App** — React Native companion app
- [ ] **White-label SaaS** — Multi-tenant architecture for agencies

---

## 11. CONTRIBUTING

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation for API changes
- Use conventional commit messages

---

## 12. LICENSE

Distributed under the MIT License. See `LICENSE` for more information.

---

## 13. AUTHOR

**Samra Fatima**  
Email: sminhas1405@gmail.com  
GitHub: [https://github.com/Samra-ca/ctpl-aiml-internship/tree/main/week-5/AI_local_business_marketing_agent](https://github.com/Samra-ca/ctpl-aiml-internship/tree/main/week-5/AI_local_business_marketing_agent)

---

## 14. ACKNOWLEDGMENTS

- [Streamlit](https://streamlit.io/) — Rapid data app framework
- [Plotly](https://plotly.com/python/) — Interactive visualizations
- [TextBlob](https://textblob.readthedocs.io/) — Sentiment analysis
- [APScheduler](https://apscheduler.readthedocs.io/) — Background scheduling
- [Pandas](https://pandas.pydata.org/) — Data manipulation
- [NumPy](https://numpy.org/) — Numerical computing
- [Pillow](https://pillow.readthedocs.io/) — Image processing
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Environment management
- [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) & [Manrope](https://fonts.google.com/specimen/Manrope) — Typography
- [SVG Repo](https://www.svgrepo.com/) — Navigation icons

---

## 15. TOOLS & UTILITIES

### Built-in Tools
| Tool | Purpose | Location |
|------|---------|----------|
| **Content Generator** | Template-based AI content creation | `models/content_generator.py` |
| **Sentiment Analyzer** | Real-time sentiment scoring | `models/sentiment_analyzer.py` |
| **Social Media Manager** | Facebook/Instagram posting | `models/social_media.py` |
| **Email Campaign Builder** | HTML email templates | `models/email_campaign.py` |
| **WhatsApp Campaign Builder** | WhatsApp message formatting | `models/whatsapp_campaign.py` |
| **Google Business Manager** | Google Business Profile API | `models/google_business.py` |
| **Database Manager** | SQLite CRUD operations | `utils/database.py` |
| **Analytics Engine** | Performance aggregation | `utils/analytics.py` |
| **Validators** | Input validation utilities | `utils/validators.py` |
| **Formatters** | Data formatting utilities | `utils/formatters.py` |

### External Tools Integrated
| Tool | Purpose | Integration |
|------|---------|-------------|
| **Facebook Graph API** | Social media posting | `models/social_media.py` |
| **Instagram Basic Display API** | Instagram posting | `models/social_media.py` |
| **WhatsApp Business API** | WhatsApp messaging | `models/whatsapp_campaign.py` |
| **Google My Business API** | Google Business posts | `models/google_business.py` |
| **SMTP** | Email delivery | `models/email_campaign.py` |
| **APScheduler** | Background job scheduling | `app.py` |

---

> **Built with ❤️ for local businesses everywhere**  
> *Empowering small businesses to compete with enterprise marketing — powered by AI*