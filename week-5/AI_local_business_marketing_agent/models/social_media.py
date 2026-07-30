"""
Social Media Management - Create and schedule posts for different platforms
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd
import plotly.express as px

from config.settings import PLATFORMS, BUSINESS_TYPES
from models.content_generator import ContentGenerator

class SocialMediaManager:
    """Manage social media content creation and scheduling"""
    
    def __init__(self):
        self.platforms = PLATFORMS
        self.content_generator = ContentGenerator()
        self.post_schedule = []
        self.post_history = []
    
    def create_post(
        self,
        business_type: str,
        platform: str,
        content: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        schedule_time: Optional[datetime] = None,
        **kwargs
    ) -> Dict:
        """Create a social media post"""
        
        # Generate content if not provided
        if not content:
            generated = self.content_generator.generate_content(
                business_type=business_type,
                platform=platform,
                campaign_type=kwargs.get('campaign_type', 'promotional'),
                additional_context=kwargs.get('context', {})
            )
            content = generated['content']
        
        # Prepare post data
        post = {
            'id': f"post_{len(self.post_history) + 1}",
            'platform': platform,
            'content': content,
            'business_type': business_type,
            'media_urls': media_urls or [],
            'schedule_time': schedule_time.isoformat() if schedule_time else None,
            'status': 'scheduled' if schedule_time else 'draft',
            'created_at': datetime.now().isoformat(),
            'engagement': {
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'reach': 0
            },
            'metadata': kwargs
        }
        
        # Store post
        if schedule_time:
            self.post_schedule.append(post)
        self.post_history.append(post)
        
        return post
    
    def get_posts_for_platform(self, platform: str) -> List[Dict]:
        """Get all posts for a specific platform"""
        return [p for p in self.post_history if p['platform'] == platform]
    
    def get_scheduled_posts(self) -> List[Dict]:
        """Get all scheduled posts"""
        return sorted(
            [p for p in self.post_history if p['status'] == 'scheduled'],
            key=lambda x: x.get('schedule_time', '')
        )
    
    def publish_post(self, post_id: str) -> Dict:
        """Publish a scheduled post"""
        for post in self.post_history:
            if post['id'] == post_id:
                post['status'] = 'published'
                post['published_at'] = datetime.now().isoformat()
                
                # Simulate engagement
                post['engagement']['likes'] = random.randint(10, 100)
                post['engagement']['comments'] = random.randint(1, 20)
                post['engagement']['shares'] = random.randint(0, 10)
                post['engagement']['reach'] = random.randint(100, 1000)
                
                return post
        
        return None
    
    def analyze_performance(self, days: int = 30) -> Dict:
        """Analyze social media performance"""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()
        
        # Filter posts in timeframe
        recent_posts = [
            p for p in self.post_history
            if p.get('published_at', '') >= cutoff_str
        ]
        
        if not recent_posts:
            return {
                'total_posts': 0,
                'total_engagement': 0,
                'avg_engagement_rate': 0,
                'platform_breakdown': {}
            }
        
        # Calculate metrics
        total_likes = sum(p['engagement']['likes'] for p in recent_posts)
        total_comments = sum(p['engagement']['comments'] for p in recent_posts)
        total_shares = sum(p['engagement']['shares'] for p in recent_posts)
        total_reach = sum(p['engagement']['reach'] for p in recent_posts)
        
        # Platform breakdown
        platform_breakdown = {}
        for platform in PLATFORMS:
            platform_posts = [p for p in recent_posts if p['platform'] == platform]
            if platform_posts:
                platform_breakdown[platform] = {
                    'count': len(platform_posts),
                    'likes': sum(p['engagement']['likes'] for p in platform_posts),
                    'comments': sum(p['engagement']['comments'] for p in platform_posts),
                    'shares': sum(p['engagement']['shares'] for p in platform_posts),
                    'reach': sum(p['engagement']['reach'] for p in platform_posts)
                }
        
        return {
            'total_posts': len(recent_posts),
            'total_engagement': total_likes + total_comments + total_shares,
            'avg_engagement_rate': (total_engagement / total_reach * 100) if total_reach > 0 else 0,
            'total_reach': total_reach,
            'platform_breakdown': platform_breakdown
        }
    
    def render_ui(self):
        """Render the social media management UI in Streamlit"""
        
        st.markdown("### 📱 Create Social Media Post")
        
        # Business type selection
        business_type = st.selectbox(
            "Business Type",
            list(BUSINESS_TYPES.keys()),
            format_func=lambda x: BUSINESS_TYPES[x]['name']
        )
        
        # Platform selection
        platform = st.selectbox(
            "Platform",
            list(PLATFORMS.keys()),
            format_func=lambda x: f"{PLATFORMS[x]['icon']} {PLATFORMS[x]['name']}"
        )
        
        # Campaign type
        campaign_type = st.selectbox(
            "Campaign Type",
            ['promotional', 'educational', 'engagement', 'brand_story', 'testimonial']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Content generation
            if st.button("🤖 Generate AI Content", use_container_width=True):
                with st.spinner("Generating content..."):
                    generated = self.content_generator.generate_content(
                        business_type=business_type,
                        platform=platform,
                        campaign_type=campaign_type
                    )
                    st.session_state.generated_content = generated['content']
                    st.success("Content generated!")
            
            # Schedule
            schedule_date = st.date_input("Schedule Date", datetime.now())
            schedule_time = st.time_input("Schedule Time", datetime.now().time())
            schedule_datetime = datetime.combine(schedule_date, schedule_time)
        
        with col2:
            # Content editor
            content = st.text_area(
                "Post Content",
                value=st.session_state.get('generated_content', ''),
                height=200
            )
            
            # Media upload
            media_files = st.file_uploader(
                "Add Images/Videos",
                type=['jpg', 'png', 'jpeg', 'mp4'],
                accept_multiple_files=True
            )
            
            # Hashtags
            hashtags = st.text_input(
                "Hashtags (comma-separated)",
                placeholder="#marketing #business"
            )
        
        # Create post button
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Save as Draft", use_container_width=True):
                post = self.create_post(
                    business_type=business_type,
                    platform=platform,
                    content=content,
                    schedule_time=None,
                    campaign_type=campaign_type
                )
                st.success("Post saved as draft!")
                st.json(post)
        
        with col2:
            if st.button("📅 Schedule Post", use_container_width=True):
                post = self.create_post(
                    business_type=business_type,
                    platform=platform,
                    content=content,
                    schedule_time=schedule_datetime,
                    campaign_type=campaign_type
                )
                st.success(f"Post scheduled for {schedule_datetime}")
                st.json(post)
        
        with col3:
            if st.button("🚀 Publish Now", use_container_width=True):
                post = self.create_post(
                    business_type=business_type,
                    platform=platform,
                    content=content,
                    schedule_time=datetime.now(),
                    campaign_type=campaign_type
                )
                post = self.publish_post(post['id'])
                st.success("Post published!")
                st.json(post)
        
        # Show post history
        st.markdown("---")
        st.markdown("### 📊 Post History")
        
        if self.post_history:
            # Convert to DataFrame for visualization
            df_posts = pd.DataFrame(self.post_history)
            
            # Show recent posts
            st.dataframe(
                df_posts[[
                    'platform', 'content', 'status', 'created_at'
                ]].tail(10),
                use_container_width=True
            )
            
            # Performance metrics
            st.markdown("### 📈 Performance Analytics")
            
            performance = self.analyze_performance(30)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Posts", performance['total_posts'])
            with col2:
                st.metric("Total Engagement", performance['total_engagement'])
            with col3:
                st.metric("Total Reach", f"{performance['total_reach']:,}")
            with col4:
                st.metric("Engagement Rate", f"{performance['avg_engagement_rate']:.1f}%")
            
            # Platform breakdown chart
            if performance['platform_breakdown']:
                platform_data = []
                for platform, metrics in performance['platform_breakdown'].items():
                    platform_data.append({
                        'Platform': PLATFORMS[platform]['name'],
                        'Posts': metrics['count'],
                        'Engagement': metrics['likes'] + metrics['comments'] + metrics['shares'],
                        'Reach': metrics['reach']
                    })
                
                if platform_data:
                    df_platform = pd.DataFrame(platform_data)
                    fig = px.bar(
                        df_platform,
                        x='Platform',
                        y=['Posts', 'Engagement'],
                        title='Performance by Platform',
                        barmode='group'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No posts created yet. Start by creating your first social media post!")