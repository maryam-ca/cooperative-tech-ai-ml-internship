"""
Formatters - Output formatting utilities
"""

from datetime import datetime
from typing import Dict, Any

class Formatters:
    """Collection of formatting functions"""
    
    @staticmethod
    def format_date(date_str: str, format: str = '%B %d, %Y') -> str:
        """Format date string"""
        try:
            dt = datetime.fromisoformat(date_str)
            return dt.strftime(format)
        except (ValueError, TypeError):
            return date_str
    
    @staticmethod
    def format_datetime(dt_str: str, format: str = '%B %d, %Y %I:%M %p') -> str:
        """Format datetime string"""
        try:
            dt = datetime.fromisoformat(dt_str)
            return dt.strftime(format)
        except (ValueError, TypeError):
            return dt_str
    
    @staticmethod
    def format_currency(amount: float, currency: str = '$') -> str:
        """Format currency"""
        return f"{currency}{amount:,.2f}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """Format percentage"""
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_number(num: int) -> str:
        """Format number with commas"""
        return f"{num:,}"
    
    @staticmethod
    def format_engagement(metrics: Dict[str, int]) -> str:
        """Format engagement metrics"""
        likes = metrics.get('likes', 0)
        comments = metrics.get('comments', 0)
        shares = metrics.get('shares', 0)
        
        parts = []
        if likes:
            parts.append(f"❤️ {likes:,}")
        if comments:
            parts.append(f"💬 {comments:,}")
        if shares:
            parts.append(f"🔄 {shares:,}")
        
        return " • ".join(parts) if parts else "No engagement"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length].strip() + suffix
    
    @staticmethod
    def format_business_type(type_name: str) -> str:
        """Format business type for display"""
        mapping = {
            'restaurant': 'Restaurant',
            'gym': 'Gym/Fitness',
            'shop': 'Retail/Shop',
            'clinic': 'Clinic/Healthcare'
        }
        return mapping.get(type_name, type_name.title())
    
    @staticmethod
    def format_platform_name(platform: str) -> str:
        """Format platform name for display"""
        mapping = {
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'google_business': 'Google Business',
            'whatsapp': 'WhatsApp',
            'email': 'Email'
        }
        return mapping.get(platform, platform.title())
    
    @staticmethod
    def format_time_ago(dt_str: str) -> str:
        """Format time ago"""
        try:
            dt = datetime.fromisoformat(dt_str)
            now = datetime.now()
            diff = now - dt
            
            if diff.days > 365:
                years = diff.days // 365
                return f"{years} year{'s' if years > 1 else ''} ago"
            elif diff.days > 30:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
            elif diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                return "Just now"
        except (ValueError, TypeError):
            return dt_str