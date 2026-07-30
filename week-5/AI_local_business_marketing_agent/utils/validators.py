"""
Validators - Input validation utilities
"""

import re
from typing import Union, Optional

class Validators:
    """Collection of validation functions"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return bool(re.match(r'^\+?[0-9]{7,15}$', cleaned))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL"""
        pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_business_type(business_type: str) -> bool:
        """Validate business type"""
        valid_types = ['restaurant', 'gym', 'shop', 'clinic']
        return business_type in valid_types
    
    @staticmethod
    def validate_platform(platform: str) -> bool:
        """Validate platform"""
        valid_platforms = ['facebook', 'instagram', 'google_business', 'whatsapp', 'email']
        return platform in valid_platforms
    
    @staticmethod
    def validate_content_length(content: str, max_length: int = 50000) -> bool:
        """Validate content length"""
        return len(content) <= max_length
    
    @staticmethod
    def validate_hashtags(hashtags: str) -> bool:
        """Validate hashtags format"""
        if not hashtags:
            return True
        tags = [t.strip() for t in hashtags.split(',')]
        for tag in tags:
            if not tag.startswith('#'):
                return False
            if not re.match(r'^#[a-zA-Z0-9_]+$', tag):
                return False
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>\"\'=;]', '', text)
        return sanitized.strip()
    
    @staticmethod
    def validate_schedule_date(date_str: str) -> bool:
        """Validate schedule date format"""
        try:
            from datetime import datetime
            datetime.fromisoformat(date_str)
            return True
        except (ValueError, TypeError):
            return False