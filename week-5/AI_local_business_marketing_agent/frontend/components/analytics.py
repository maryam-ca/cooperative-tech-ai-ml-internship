"""
Analytics Component - Campaign performance analytics and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List

class AnalyticsComponent:
    """Render analytics and insights dashboard"""
    
    def __init__(self, components: Dict[str, Any]):
        self.components = components
        self.analytics = components.get('analytics')
        self.db = components.get('db')
    
    def render(self):
        """Render the analytics page"""
        # Date filter
        col1, col2, col3 = st.columns(3)
        with col1:
            date_range = st.selectbox(
                "Time Period",
                ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"]
            )
        with col2:
            platform_filter = st.selectbox(
                "Platform",
                ["All"] + list(self._get_platforms())
            )
        with col3:
            status_filter = st.selectbox(
                "Status",
                ["All", "Published", "Scheduled", "Draft", "Archived"]
            )
        
        # Get campaigns
        campaigns = self._get_filtered_campaigns(platform_filter, status_filter)
        
        if not campaigns:
            st.info("No campaigns found. Start creating campaigns to see analytics!")
            return
        
        # Key metrics
        st.markdown("### Key Metrics")
        self._render_metrics(campaigns)
        
        # Charts
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_performance_chart(campaigns)
        
        with col2:
            self._render_platform_distribution(campaigns)
        
        # Engagement trends
        st.markdown("---")
        self._render_engagement_trends(campaigns)
        
        # Insights & Recommendations
        st.markdown("---")
        st.markdown("### Insights & Recommendations")
        
        insights = self._generate_insights(campaigns)
        for insight in insights:
            st.markdown(f"- {insight}")
        
        # Campaign table
        st.markdown("---")
        st.markdown("### Campaign Details")
        self._render_campaign_table(campaigns)
    
    def _get_platforms(self) -> List[str]:
        """Get list of unique platforms from campaigns"""
        platforms = set()
        for c in st.session_state.get('campaign_history', []):
            if c.get('platform'):
                platforms.add(c['platform'])
        return list(platforms)
    
    def _get_filtered_campaigns(self, platform: str, status: str) -> List[Dict]:
        """Get filtered campaigns"""
        campaigns = st.session_state.get('campaign_history', [])
        
        # Filter by platform
        if platform != "All":
            campaigns = [c for c in campaigns if c.get('platform') == platform]
        
        # Filter by status
        if status != "All":
            campaigns = [c for c in campaigns if c.get('status', '').lower() == status.lower()]
        
        return campaigns
    
    def _render_metrics(self, campaigns: List[Dict]):
        """Render key metrics cards"""
        total_campaigns = len(campaigns)
        published = len([c for c in campaigns if c.get('status') == 'published'])
        
        total_reach = sum(c.get('engagement', {}).get('reach', 0) for c in campaigns)
        total_engagement = sum(
            c.get('engagement', {}).get('likes', 0) +
            c.get('engagement', {}).get('comments', 0) +
            c.get('engagement', {}).get('shares', 0)
            for c in campaigns
        )
        
        engagement_rate = (total_engagement / total_reach * 100) if total_reach > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_campaigns}</div>
                <div class="metric-label">Total Campaigns</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{published}</div>
                <div class="metric-label">Published</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_reach:,}</div>
                <div class="metric-label">Total Reach</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{engagement_rate:.1f}%</div>
                <div class="metric-label">Engagement Rate</div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_performance_chart(self, campaigns: List[Dict]):
        """Render performance chart"""
        st.markdown("#### Performance by Campaign")
        
        if not campaigns:
            st.info("No data to display")
            return
        
        # Prepare data
        data = []
        for c in campaigns:
            data.append({
                'Campaign': c.get('name', f"Campaign {c.get('id', '')}")[:20],
                'Reach': c.get('engagement', {}).get('reach', 0),
                'Engagement': (
                    c.get('engagement', {}).get('likes', 0) +
                    c.get('engagement', {}).get('comments', 0) +
                    c.get('engagement', {}).get('shares', 0)
                ),
                'Platform': c.get('platform', 'Unknown')
            })
        
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
            font_color='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_platform_distribution(self, campaigns: List[Dict]):
        """Render platform distribution chart"""
        st.markdown("#### Platform Distribution")
        
        if not campaigns:
            st.info("No data to display")
            return
        
        platform_data = {}
        for c in campaigns:
            platform = c.get('platform', 'Unknown')
            platform_data[platform] = platform_data.get(platform, 0) + 1
        
        df = pd.DataFrame({
            'Platform': list(platform_data.keys()),
            'Count': list(platform_data.values())
        })
        
        fig = px.pie(
            df,
            values='Count',
            names='Platform',
            title='Campaigns by Platform',
            color_discrete_sequence=['#6C63FF', '#00D2FF', '#FF6584', '#FFC857', '#4ECDC4']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_engagement_trends(self, campaigns: List[Dict]):
        """Render engagement trends"""
        st.markdown("#### Engagement Trends")
        
        # Simulate trend data
        dates = []
        engagement_data = []
        reach_data = []
        
        if campaigns:
            # Use last 10 campaigns
            recent = campaigns[-10:]
            for c in recent:
                dates.append(c.get('created_at', datetime.now().isoformat())[:10])
                engagement_data.append(
                    c.get('engagement', {}).get('likes', 0) +
                    c.get('engagement', {}).get('comments', 0) +
                    c.get('engagement', {}).get('shares', 0)
                )
                reach_data.append(c.get('engagement', {}).get('reach', 0))
        
        if not dates:
            st.info("Not enough data for trend analysis")
            return
        
        df = pd.DataFrame({
            'Date': dates,
            'Engagement': engagement_data,
            'Reach': reach_data
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Engagement'],
            name='Engagement',
            line=dict(color='#6C63FF', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Reach'],
            name='Reach',
            line=dict(color='#00D2FF', width=3),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='Engagement & Reach Trends',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _generate_insights(self, campaigns: List[Dict]) -> List[str]:
        """Generate insights from campaign data"""
        insights = []
        
        if not campaigns:
            return ["Start creating campaigns to get personalized insights!"]
        
        # Find top performing campaign
        best_campaign = max(
            campaigns,
            key=lambda x: x.get('engagement', {}).get('reach', 0),
            default=None
        )
        
        if best_campaign:
            insights.append(
                f"🏆 Best performing campaign: **{best_campaign.get('name', 'Unnamed')}** "
                f"with {best_campaign.get('engagement', {}).get('reach', 0):,} reach"
            )
        
        # Platform insights
        platform_performance = {}
        for c in campaigns:
            platform = c.get('platform', 'Unknown')
            reach = c.get('engagement', {}).get('reach', 0)
            if platform in platform_performance:
                platform_performance[platform] += reach
            else:
                platform_performance[platform] = reach
        
        if platform_performance:
            best_platform = max(platform_performance, key=platform_performance.get)
            insights.append(
                f"📱 Best performing platform: **{best_platform}** "
                f"with {platform_performance[best_platform]:,} total reach"
            )
        
        # Engagement rate insights
        total_reach = sum(c.get('engagement', {}).get('reach', 0) for c in campaigns)
        total_engagement = sum(
            c.get('engagement', {}).get('likes', 0) +
            c.get('engagement', {}).get('comments', 0) +
            c.get('engagement', {}).get('shares', 0)
            for c in campaigns
        )
        
        if total_reach > 0:
            engagement_rate = total_engagement / total_reach * 100
            if engagement_rate > 5:
                insights.append(f"🔥 High engagement rate: {engagement_rate:.1f}% - Your content resonates well!")
            elif engagement_rate < 1:
                insights.append("📊 Low engagement rate detected. Try adding more visuals and CTAs.")
        
        # Content length insights
        long_content = [c for c in campaigns if len(c.get('content', '')) > 500]
        if long_content and len(long_content) / len(campaigns) > 0.5:
            insights.append("📝 Your campaigns have long-form content. Short-form might perform better on social media.")
        
        # Scheduling insights
        if campaigns:
            # Check if any campaigns were scheduled
            scheduled = [c for c in campaigns if c.get('status') == 'scheduled']
            if scheduled:
                insights.append("📅 You have scheduled campaigns. Great for consistent posting!")
            else:
                insights.append("💡 Consider scheduling campaigns for consistent social media presence.")
        
        # Add general suggestions
        insights.append("🎯 Use A/B testing to optimize your content.")
        insights.append("📱 Post consistently to build audience engagement.")
        
        return insights[:7]  # Limit to 7 insights
    
    def _render_campaign_table(self, campaigns: List[Dict]):
        """Render campaign details table"""
        if not campaigns:
            st.info("No campaigns to display")
            return
        
        # Prepare data
        data = []
        for c in campaigns:
            engagement = c.get('engagement', {})
            data.append({
                'Name': c.get('name', 'Unnamed')[:30],
                'Platform': c.get('platform', 'N/A'),
                'Status': c.get('status', 'Draft'),
                'Reach': engagement.get('reach', 0),
                'Likes': engagement.get('likes', 0),
                'Comments': engagement.get('comments', 0),
                'Shares': engagement.get('shares', 0),
                'Created': c.get('created_at', 'N/A')[:10] if c.get('created_at') else 'N/A'
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Export option
        if st.button("📥 Export Data as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"campaign_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )