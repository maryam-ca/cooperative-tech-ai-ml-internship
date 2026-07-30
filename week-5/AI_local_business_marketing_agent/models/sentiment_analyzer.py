"""
Sentiment Analyzer - Analyze sentiment of marketing content
"""

import re
from typing import Dict, List, Tuple
import random

class SentimentAnalyzer:
    """Analyze sentiment of text content"""
    
    def __init__(self):
        self.positive_words = self._get_positive_words()
        self.negative_words = self._get_negative_words()
        self.neutral_words = self._get_neutral_words()
    
    def _get_positive_words(self) -> List[str]:
        """Get list of positive sentiment words"""
        return [
            'great', 'good', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'incredible', 'outstanding', 'superb', 'brilliant',
            'perfect', 'love', 'best', 'top', 'quality', 'satisfied',
            'happy', 'delighted', 'pleased', 'enjoy', 'recommend',
            'value', 'worth', 'success', 'achieve', 'improve',
            'positive', 'beautiful', 'creative', 'innovative',
            'exceptional', 'flawless', 'genius', 'impressive'
        ]
    
    def _get_negative_words(self) -> List[str]:
        """Get list of negative sentiment words"""
        return [
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'disappointing',
            'disappointed', 'worst', 'useless', 'waste', 'unhappy',
            'frustrated', 'annoying', 'problem', 'issue', 'error',
            'fail', 'failure', 'damage', 'destroy', 'broken',
            'incompetent', 'unacceptable', 'regret', 'avoid'
        ]
    
    def _get_neutral_words(self) -> List[str]:
        """Get list of neutral sentiment words"""
        return [
            'average', 'okay', 'fine', 'normal', 'standard', 'regular',
            'typical', 'common', 'basic', 'simple', 'enough',
            'acceptable', 'decent', 'moderate', 'fair'
        ]
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment analysis results
        """
        text_lower = text.lower()
        words = re.findall(r'\w+', text_lower)
        
        # Count sentiment words
        positive_count = sum(1 for w in words if w in self.positive_words)
        negative_count = sum(1 for w in words if w in self.negative_words)
        neutral_count = sum(1 for w in words if w in self.neutral_words)
        
        total_sentiment_words = positive_count + negative_count + neutral_count
        
        if total_sentiment_words == 0:
            sentiment = 'neutral'
            score = 0.0
            confidence = 0.0
        else:
            # Calculate score (-1 to 1)
            score = (positive_count - negative_count) / total_sentiment_words
            
            # Determine sentiment
            if score > 0.1:
                sentiment = 'positive'
            elif score < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Calculate confidence (0 to 1)
            confidence = min(1.0, total_sentiment_words / 10)
        
        # Get key phrases
        positive_phrases = [w for w in words if w in self.positive_words][:5]
        negative_phrases = [w for w in words if w in self.negative_words][:5]
        
        return {
            'sentiment': sentiment,
            'score': round(score, 3),
            'confidence': round(confidence, 3),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_phrases': positive_phrases,
            'negative_phrases': negative_phrases,
            'suggestions': self._get_suggestions(sentiment, score)
        }
    
    def _get_suggestions(self, sentiment: str, score: float) -> List[str]:
        """Get suggestions based on sentiment analysis"""
        suggestions = []
        
        if sentiment == 'positive':
            suggestions.append("✅ Content has positive sentiment - great for marketing!")
            if score > 0.5:
                suggestions.append("🌟 Strong positive sentiment - this content will resonate well")
            suggestions.append("📊 Consider using this as a testimonial or success story")
        
        elif sentiment == 'negative':
            suggestions.append("⚠️ Negative sentiment detected - consider revising the content")
            suggestions.append("💡 Try rephrasing to be more positive and constructive")
            suggestions.append("🎯 Focus on benefits rather than problems")
        
        else:
            suggestions.append("📝 Content is neutral - consider adding emotional appeal")
            suggestions.append("💡 Add more positive language to increase engagement")
            suggestions.append("🎯 Use power words to make the content more compelling")
        
        return suggestions
    
    def get_sentiment_emoji(self, sentiment: str) -> str:
        """Get emoji for sentiment"""
        emojis = {
            'positive': '😊',
            'negative': '😞',
            'neutral': '😐'
        }
        return emojis.get(sentiment, '😐')
    
    def get_sentiment_color(self, sentiment: str) -> str:
        """Get color for sentiment"""
        colors = {
            'positive': '#4CAF50',
            'negative': '#f44336',
            'neutral': '#FFC107'
        }
        return colors.get(sentiment, '#FFC107')
    
    def get_sentiment_icon(self, sentiment: str) -> str:
        """Get icon for sentiment"""
        icons = {
            'positive': '✅',
            'negative': '❌',
            'neutral': '⚖️'
        }
        return icons.get(sentiment, '⚖️')