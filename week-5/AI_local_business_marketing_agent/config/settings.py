"""
Configuration Settings for AI Local Business Marketing Agent
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
ASSETS_DIR = BASE_DIR / 'assets'

# API Keys (loaded from environment variables)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')

# Business Types
BUSINESS_TYPES = {
    'restaurant': {
        'name': 'Restaurant',
        'icon': '🍽️',
        'content_themes': ['Food', 'Dining', 'Cuisine', 'Ambiance', 'Service'],
        'hashtags': ['#Foodie', '#Restaurant', '#Dining', '#Cuisine', '#FoodLovers']
    },
    'gym': {
        'name': 'Gym/Fitness',
        'icon': '💪',
        'content_themes': ['Fitness', 'Workout', 'Health', 'Transformation', 'Motivation'],
        'hashtags': ['#Fitness', '#Gym', '#Workout', '#Health', '#FitLife']
    },
    'shop': {
        'name': 'Shop/Retail',
        'icon': '🛍️',
        'content_themes': ['Products', 'Sale', 'Fashion', 'Deals', 'Style'],
        'hashtags': ['#Shop', '#Retail', '#Fashion', '#Deals', '#Shopping']
    },
    'clinic': {
        'name': 'Clinic/Healthcare',
        'icon': '🏥',
        'content_themes': ['Health', 'Wellness', 'Care', 'Medical', 'Wellbeing'],
        'hashtags': ['#Health', '#Wellness', '#Healthcare', '#Medical', '#Care']
    }
}

# Social Media Platforms
PLATFORMS = {
    'facebook': {
        'name': 'Facebook',
        'icon': '📘',
        'max_length': 63206,
        'supports_media': True,
        'supports_links': True
    },
    'instagram': {
        'name': 'Instagram',
        'icon': '📸',
        'max_length': 2200,
        'supports_media': True,
        'supports_links': False
    },
    'google_business': {
        'name': 'Google Business',
        'icon': '📍',
        'max_length': 1500,
        'supports_media': True,
        'supports_links': True
    },
    'whatsapp': {
        'name': 'WhatsApp',
        'icon': '💬',
        'max_length': 4096,
        'supports_media': True,
        'supports_links': True
    },
    'email': {
        'name': 'Email',
        'icon': '📧',
        'max_length': 50000,
        'supports_media': True,
        'supports_links': True
    }
}

# Content Templates
CONTENT_TEMPLATES = {
    'promotional': {
        'name': 'Promotional',
        'description': 'Promote products, services, or special offers',
        'structure': 'Hook → Value Proposition → Call to Action'
    },
    'educational': {
        'name': 'Educational',
        'description': 'Share knowledge, tips, or how-to content',
        'structure': 'Question → Answer → Learning → Call to Action'
    },
    'engagement': {
        'name': 'Engagement',
        'description': 'Encourage audience interaction and participation',
        'structure': 'Question → Story → Engagement → Call to Action'
    },
    'brand_story': {
        'name': 'Brand Story',
        'description': 'Share your brand\'s story, values, or mission',
        'structure': 'Hook → Story → Connection → Call to Action'
    },
    'testimonial': {
        'name': 'Testimonial',
        'description': 'Share customer success stories and reviews',
        'structure': 'Problem → Solution → Result → Call to Action'
    }
}

# Content Generation Settings
CONTENT_SETTINGS = {
    'max_tokens': 500,
    'temperature': 0.7,
    'model': 'gpt-3.5-turbo',
    'languages': ['en', 'es', 'fr', 'de', 'zh', 'hi']
}

# Analytics Settings
ANALYTICS_SETTINGS = {
    'track_engagement': True,
    'track_conversions': True,
    'track_reach': True,
    'retention_days': 90
}

# Database Settings
DATABASE_CONFIG = {
    'path': str(DATA_DIR / 'campaigns.db'),
    'backup_interval': 24,  # hours
    'max_backups': 7
}

# UI Settings
UI_SETTINGS = {
    'theme': 'dark',
    'primary_color': '#6C63FF',
    'secondary_color': '#FF6584',
    'accent_color': '#00D2FF'
}

# Application Configuration
APP_CONFIG = {
    'name': 'AI Local Business Marketing Agent',
    'version': '1.0.0',
    'author': 'Cooperative Tech Private Limited',
    'description': 'AI-powered marketing automation for local businesses',
    'debug': os.getenv('DEBUG', 'False').lower() == 'true'
}