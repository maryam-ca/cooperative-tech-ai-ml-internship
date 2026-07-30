"""
Analytics Engine - Track and analyze campaign performance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from utils.database import DatabaseManager

class AnalyticsEngine:
    """Track and analyze marketing campaign performance"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
    
    def track_campaign_metrics(
        self,
        campaign_id: int,
        metrics: Dict
    ) -> None:
        """Track metrics for a campaign"""
        self.db.save_analytics(campaign_id, metrics)
    
    def get_campaign_analytics(self, campaign_id: int) -> Dict:
        """Get detailed analytics for a campaign"""
        df = self.db.get_analytics(campaign_id)
        
        if df.empty:
            return {
                'total_metrics': 0,
                'average_metrics': {},
                'trend': 'insufficient_data'
            }
        
        # Calculate summary
        summary = {
            'total_metrics': len(df),
            'average_metrics': df.groupby('metric_name')['metric_value'].mean().to_dict(),
            'min_metrics': df.groupby('metric_name')['metric_value'].min().to_dict(),
            'max_metrics': df.groupby('metric_name')['metric_value'].max().to_dict(),
            'trend': self._calculate_trend(df)
        }
        
        return summary
    
    def _calculate_trend(self, df: pd.DataFrame) -> str:
        """Calculate trend direction"""
        if len(df) < 2:
            return 'insufficient_data'
        
        # Group by date and average
        daily_avg = df.groupby('date')['metric_value'].mean()
        
        if len(daily_avg) < 2:
            return 'stable'
        
        # Calculate trend using simple linear regression
        x = np.arange(len(daily_avg))
        y = daily_avg.values
        
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.05:
            return 'increasing'
        elif slope < -0.05:
            return 'decreasing'
        else:
            return 'stable'
    
    def get_performance_summary(self, days: int = 30) -> Dict:
        """Get overall performance summary"""
        performance = self.db.get_campaign_performance(days)
        
        if not performance:
            return {
                'total_campaigns': 0,
                'avg_engagement': 0,
                'top_platforms': {},
                'top_types': {}
            }
        
        df = pd.DataFrame(performance)
        
        summary = {
            'total_campaigns': df['total_campaigns'].sum(),
            'avg_engagement': df['avg_engagement'].mean(),
            'top_platforms': df.groupby('platform')['total_campaigns'].sum().to_dict(),
            'top_types': df.groupby('type')['total_campaigns'].sum().to_dict()
        }
        
        return summary
    
    def generate_insights(self, campaign_data: Dict) -> List[str]:
        """Generate insights from campaign data"""
        insights = []
        
        # Check engagement
        engagement = campaign_data.get('engagement', {})
        if engagement.get('reach', 0) > 500:
            insights.append("📈 High reach achieved! Consider increasing budget.")
        
        if engagement.get('likes', 0) > 50:
            insights.append("💡 Strong engagement. Your content resonates with the audience.")
        
        if engagement.get('shares', 0) > 10:
            insights.append("🔄 High shareability. Users find this content valuable.")
        
        # Check timing
        created_at = campaign_data.get('created_at')
        if created_at:
            try:
                created = datetime.fromisoformat(created_at)
                if created.hour > 18:
                    insights.append("⏰ Evening posting shows good results. Consider more evening campaigns.")
            except:
                pass
        
        # Add general suggestions
        if not insights:
            insights.append("📊 Consider testing different content formats.")
            insights.append("🎯 Review your audience targeting.")
            insights.append("📱 Try posting on multiple platforms.")
        
        return insights
    
    def get_recommendations(self, campaign_history: List[Dict]) -> List[str]:
        """Generate recommendations based on campaign history"""
        if not campaign_history:
            return [
                "📝 Start with creating your first campaign!",
                "📊 Track performance to get personalized recommendations."
            ]
        
        recommendations = []
        
        # Analyze successful campaigns
        successful = [c for c in campaign_history if c.get('engagement', {}).get('likes', 0) > 50]
        
        if successful:
            platforms = set(c.get('platform') for c in successful)
            recommendations.append(f"✅ Focus on platforms: {', '.join(platforms)}")
        
        # Analyze timing
        times = []
        for c in campaign_history:
            try:
                created = datetime.fromisoformat(c.get('created_at', ''))
                times.append(created.hour)
            except:
                pass
        
        if times:
            avg_hour = sum(times) / len(times)
            if avg_hour < 12:
                recommendations.append("🌅 Morning campaigns perform well. Keep posting in the morning!")
            else:
                recommendations.append("🌆 Evening campaigns show good results.")
        
        # Content suggestions
        recommendations.append("📝 Try mixing promotional and educational content.")
        recommendations.append("🎯 Add more visuals to your posts.")
        recommendations.append("💬 Encourage user engagement with questions.")
        
        return recommendations[:5]