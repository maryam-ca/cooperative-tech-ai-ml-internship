"""
Google Business Manager - Create and manage Google Business updates
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd

from models.content_generator import ContentGenerator

class GoogleBusinessManager:
    """Manage Google Business profile updates and posts"""
    
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.posts = []
        
        self.post_templates = {
            'announcement': [
                "📢 We're excited to announce our new {offering} at {business}! Come visit us today!",
                "🎉 Big news! {business} now offers {offering}. Stop by and check it out!",
                "✨ Exciting update from {business}: We've added {offering} to our services!"
            ],
            'offer': [
                "🎯 Special offer: {offer} at {business}. Valid until {date}. Don't miss out!",
                "💰 Limited time deal at {business}: {offer}. Come in today!",
                "⭐ Exclusive offer: {offer} at {business}. Shop now!"
            ],
            'event': [
                "📅 Join us at {business} for {event} on {date}. We can't wait to see you!",
                "🎪 {event} at {business}! Mark your calendars for {date}.",
                "🗓️ Save the date! {event} at {business} on {date}."
            ],
            'update': [
                "🆕 {business} update: {update}. Check out our latest improvements!",
                "📋 New from {business}: {update}. We're always improving!",
                "💡 Did you know? {business} now {update}."
            ]
        }
    
    def create_post(
        self,
        business_name: str,
        post_type: str,
        custom_content: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a Google Business post"""
        
        # Generate content if not provided
        if not custom_content:
            templates = self.post_templates.get(post_type, self.post_templates['update'])
            template = random.choice(templates)
            
            params = {
                'business': business_name,
                'offering': 'new products and services',
                'offer': 'a special discount',
                'date': datetime.now().strftime('%B %d, %Y'),
                'event': 'our upcoming event',
                'update': 'offers new services',
            }
            params.update(kwargs)
            params['business'] = business_name
            content = template.format(**params)
        else:
            content = custom_content
        
        post = {
            'id': f"gbp_{len(self.posts) + 1}",
            'business_name': business_name,
            'post_type': post_type,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'status': 'draft',
            'engagement': {
                'views': 0,
                'clicks': 0,
                'calls': 0,
                'direction_requests': 0
            },
            'metadata': kwargs
        }
        
        self.posts.append(post)
        return post
    
    def publish_post(self, post_id: str) -> Dict:
        """Publish a Google Business post"""
        for post in self.posts:
            if post['id'] == post_id:
                post['status'] = 'published'
                post['published_at'] = datetime.now().isoformat()
                
                # Simulate engagement
                post['engagement']['views'] = random.randint(50, 500)
                post['engagement']['clicks'] = random.randint(10, 100)
                post['engagement']['calls'] = random.randint(1, 20)
                post['engagement']['direction_requests'] = random.randint(5, 50)
                
                return post
        
        return None
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary for Google Business posts"""
        published_posts = [p for p in self.posts if p['status'] == 'published']
        
        if not published_posts:
            return {
                'total_posts': 0,
                'total_views': 0,
                'total_clicks': 0,
                'total_calls': 0,
                'total_directions': 0
            }
        
        return {
            'total_posts': len(published_posts),
            'total_views': sum(p['engagement']['views'] for p in published_posts),
            'total_clicks': sum(p['engagement']['clicks'] for p in published_posts),
            'total_calls': sum(p['engagement']['calls'] for p in published_posts),
            'total_directions': sum(p['engagement']['direction_requests'] for p in published_posts)
        }
    
    def render_ui(self):
        """Render Google Business UI in Streamlit"""
        
        st.markdown("### 📍 Google Business Updates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Business Name", "My Business")
            
            post_type = st.selectbox(
                "Post Type",
                ['announcement', 'offer', 'event', 'update']
            )
            
            # Context fields based on post type
            context_fields = {}
            
            if post_type == 'announcement':
                context_fields['offering'] = st.text_input("Offering", "new services")
            elif post_type == 'offer':
                context_fields['offer'] = st.text_input("Offer Description", "20% off")
                context_fields['date'] = st.date_input("Valid Until")
            elif post_type == 'event':
                context_fields['event'] = st.text_input("Event Name", "Open House")
                context_fields['date'] = st.date_input("Event Date")
            elif post_type == 'update':
                context_fields['update'] = st.text_input("Update Description", "extended hours")
        
        with col2:
            custom_content = st.text_area(
                "Custom Content (Optional)",
                placeholder="Leave empty to use template",
                height=150
            )
            
            # Image upload
            image = st.file_uploader(
                "Add Image",
                type=['jpg', 'png', 'jpeg']
            )
        
        # Generate post
        if st.button("📍 Generate Google Business Post", use_container_width=True):
            with st.spinner("Generating post..."):
                post = self.create_post(
                    business_name=business_name,
                    post_type=post_type,
                    custom_content=custom_content if custom_content else None,
                    **context_fields
                )
                
                st.session_state.google_post = post
                st.success("Post generated!")
        
        # Display post
        if st.session_state.get('google_post'):
            st.markdown("### 📝 Post Preview")
            
            preview = st.session_state.google_post
            body = preview['content'].replace('\n', '<br>')
            post_date = datetime.now().strftime('%b %d, %Y')
            type_label = preview['post_type'].title()
            
            st.markdown(f"""
            <div class="gbp-card">
                <div class="gbp-head">
                    <div class="gbp-avatar">{preview['business_name'][:1].upper()}</div>
                    <div>
                        <div class="gbp-name">{preview['business_name']}</div>
                        <div class="gbp-sub">Google Business Profile · {post_date}</div>
                    </div>
                    <div class="gbp-tag">{type_label}</div>
                </div>
                <div class="gbp-body">{body}</div>
                <div class="gbp-actions">
                    <span>👍 Like</span><span>💬 Comment</span><span>↗ Share</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📤 Publish Now", use_container_width=True):
                    post = self.publish_post(preview['id'])
                    st.success("Post published to Google Business!")
                    st.json(post['engagement'])
            
            with col2:
                if st.button("📅 Schedule", use_container_width=True):
                    st.success("Post scheduled!")
            
            with col3:
                if st.button("📋 Save Draft", use_container_width=True):
                    st.success("Draft saved!")
            
            # Performance analytics
            st.markdown("### 📊 Performance")
            
            performance = self.get_performance_summary()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Posts", performance['total_posts'])
            with col2:
                st.metric("Views", performance['total_views'])
            with col3:
                st.metric("Clicks", performance['total_clicks'])
            with col4:
                st.metric("Directions", performance['total_directions'])