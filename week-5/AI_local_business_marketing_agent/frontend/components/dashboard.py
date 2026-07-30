"""
Dashboard Component - Main dashboard view
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any

from utils.analytics import AnalyticsEngine

class DashboardComponent:
    """Render the main dashboard"""
    
    def __init__(self, components: Dict[str, Any]):
        self.components = components
        self.analytics = components.get('analytics', AnalyticsEngine())
    
    def render(self):
        """Render the dashboard"""
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        # Get performance summary
        summary = self.analytics.get_performance_summary(30)
        
        with col1:
            st.markdown("""
            <div class="metric-card fade-up">
                <div class="metric-value">{:,}</div>
                <div class="metric-label">Total Campaigns</div>
            </div>
            """.format(summary.get('total_campaigns', 0)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card fade-up stagger-1">
                <div class="metric-value">{:.0f}</div>
                <div class="metric-label">Avg Engagement</div>
            </div>
            """.format(summary.get('avg_engagement', 0)), unsafe_allow_html=True)
        
        with col3:
            # Active campaigns
            active = len([c for c in st.session_state.campaign_history if c.get('status') == 'published'])
            st.markdown("""
            <div class="metric-card fade-up stagger-2">
                <div class="metric-value">{}</div>
                <div class="metric-label">Active Campaigns</div>
            </div>
            """.format(active), unsafe_allow_html=True)
        
        with col4:
            # Total reach
            total_reach = sum(c.get('engagement', {}).get('reach', 0) for c in st.session_state.campaign_history)
            st.markdown("""
            <div class="metric-card fade-up stagger-3">
                <div class="metric-value">{:,}</div>
                <div class="metric-label">Total Reach</div>
            </div>
            """.format(total_reach), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Campaign Performance")
            
            if st.session_state.campaign_history:
                # Create performance data
                data = []
                for c in st.session_state.campaign_history:
                    if c.get('engagement'):
                        data.append({
                            'Campaign': c.get('name', f"Campaign {c.get('id', '')}"),
                            'Reach': c['engagement'].get('reach', 0),
                            'Engagement': c['engagement'].get('likes', 0) + 
                                          c['engagement'].get('comments', 0) + 
                                          c['engagement'].get('shares', 0),
                            'Platform': c.get('platform', 'Unknown')
                        })
                
                if data:
                    df = pd.DataFrame(data)
                    fig = px.bar(
                        df,
                        x='Campaign',
                        y=['Reach', 'Engagement'],
                        title='Campaign Performance',
                        barmode='group',
                        color_discrete_sequence=['#6C63FF', '#FF6584']
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No campaigns yet. Start creating your first campaign!")
        
        with col2:
            st.markdown("### Platform Distribution")
            
            if st.session_state.campaign_history:
                # Platform distribution
                platform_data = {}
                for c in st.session_state.campaign_history:
                    platform = c.get('platform', 'Unknown')
                    platform_data[platform] = platform_data.get(platform, 0) + 1
                
                if platform_data:
                    df = pd.DataFrame({
                        'Platform': list(platform_data.keys()),
                        'Count': list(platform_data.values())
                    })
                    
                    fig = px.pie(
                        df,
                        values='Count',
                        names='Platform',
                        title='Campaigns by Platform',
                        color_discrete_sequence=['#6C63FF', '#00D2FF', '#FF6584', '#FFC857']
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("### Recent Activity")
        
        if st.session_state.campaign_history:
            recent = st.session_state.campaign_history[-5:]
            for c in reversed(recent):
                status_emoji = "✅" if c.get('status') == 'published' else "📝"
                st.markdown(f"""
                <div style="padding: 0.8rem; background: rgba(255,255,255,0.03); border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #6C63FF;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 600;">{c.get('name', 'Unnamed')}</span>
                        <span style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">{c.get('platform', 'Unknown')} {status_emoji}</span>
                    </div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 0.3rem;">
                        {c.get('created_at', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity")
        
        # Quick actions
        st.markdown("---")
        st.markdown("### Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 New Post", use_container_width=True):
                st.session_state.nav = "create"
                st.session_state["nav_radio"] = "create"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analytics", use_container_width=True):
                st.session_state.nav = "analytics"
                st.session_state["nav_radio"] = "analytics"
                st.rerun()
        
        with col3:
            if st.button("📋 Templates", use_container_width=True):
                st.session_state.nav = "settings"
                st.session_state["nav_radio"] = "settings"
                st.rerun()
        
        with col4:
            if st.button("📱 Social Media", use_container_width=True):
                st.session_state.nav = "social"
                st.session_state["nav_radio"] = "social"
                st.rerun()