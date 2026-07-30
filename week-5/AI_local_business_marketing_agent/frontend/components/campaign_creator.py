"""
Campaign Creator Component - UI for creating new marketing campaigns
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any

from config.settings import BUSINESS_TYPES, PLATFORMS, CONTENT_TEMPLATES

class CampaignCreator:
    """Render campaign creation interface"""

    def __init__(self, components: Dict[str, Any]):
        self.components = components
        self.content_generator = components.get('content')
        self.db = components.get('db')

    def _persist(self, campaign_data: Dict, campaign_id=None, editing_id=None):
        """Save to database and keep session state in sync so Dashboard/Analytics update."""
        if self.db:
            if editing_id is not None:
                self.db.update_campaign(editing_id, {
                    'name': campaign_data.get('name'),
                    'type': campaign_data.get('type'),
                    'platform': campaign_data.get('platform'),
                    'business_type': campaign_data.get('business_type'),
                    'content': campaign_data.get('content'),
                    'status': campaign_data.get('status'),
                    'metadata': campaign_data.get('metadata', {}),
                    'engagement': campaign_data.get('engagement', {}),
                })
                campaign_id = editing_id
            else:
                campaign_id = self.db.save_campaign(campaign_data)

        entry = dict(campaign_data)
        entry['id'] = campaign_id
        if 'engagement' not in entry:
            entry['engagement'] = {}
        if 'metadata' not in entry:
            entry['metadata'] = {}

        history = st.session_state.setdefault('campaign_history', [])
        if editing_id is not None:
            for i, c in enumerate(history):
                if c.get('id') == editing_id:
                    history[i] = entry
                    break
        else:
            history.append(entry)
        return campaign_id

    def render(self):
        """Render the campaign creation page"""
        edit_campaign = st.session_state.get('edit_campaign')
        editing_id = edit_campaign.get('id') if isinstance(edit_campaign, dict) else None

        if editing_id is not None:
            st.info("✏️ Editing campaign: **{}**".format(edit_campaign.get('name', '')))

        # Campaign setup
        col1, col2 = st.columns(2)

        business_types_keys = list(BUSINESS_TYPES.keys())
        platforms_keys = list(PLATFORMS.keys())
        templates_keys = list(CONTENT_TEMPLATES.keys())

        with col1:
            default_name = edit_campaign.get('name', '') if edit_campaign else ''
            campaign_name = st.text_input("Campaign Name", value=default_name, placeholder="e.g., Summer Sale 2024")

            default_bt = edit_campaign.get('business_type', 'shop') if edit_campaign else 'restaurant'
            if default_bt not in business_types_keys:
                default_bt = 'shop'
            bt_index = business_types_keys.index(default_bt)
            business_type = st.selectbox(
                "Business Type",
                business_types_keys,
                format_func=lambda x: f"{BUSINESS_TYPES[x]['icon']} {BUSINESS_TYPES[x]['name']}",
                index=bt_index
            )

            default_pf = edit_campaign.get('platform', 'facebook') if edit_campaign else 'facebook'
            if default_pf not in platforms_keys:
                default_pf = 'facebook'
            pf_index = platforms_keys.index(default_pf)
            platform = st.selectbox(
                "Platform",
                platforms_keys,
                format_func=lambda x: f"{PLATFORMS[x]['icon']} {PLATFORMS[x]['name']}",
                index=pf_index
            )

        with col2:
            default_ct = edit_campaign.get('type', 'promotional') if edit_campaign else 'promotional'
            if default_ct not in templates_keys:
                default_ct = 'promotional'
            ct_index = templates_keys.index(default_ct)
            campaign_type = st.selectbox(
                "Campaign Type",
                templates_keys,
                format_func=lambda x: CONTENT_TEMPLATES[x]['name'],
                index=ct_index
            )

            # Show template description
            st.info(f"**Description:** {CONTENT_TEMPLATES[campaign_type]['description']}")

            schedule_date = st.date_input("Schedule Date", datetime.now() + timedelta(days=1))
            schedule_time = st.time_input("Schedule Time", datetime.now().time())
            schedule_datetime = datetime.combine(schedule_date, schedule_time)

        st.markdown("---")

        # Content Generation
        st.markdown("### AI Content Generation")

        col1, col2 = st.columns([2, 1])

        with col1:
            custom_prompt = st.text_area(
                "Custom Instructions (Optional)",
                placeholder="e.g., Make it casual and friendly, target young professionals...",
                height=80
            )
            context_input = st.text_input("Additional Context", placeholder="e.g., New product launch, holiday season...")
        with col2:
            if st.button("✨ Generate Content", use_container_width=True, type="primary"):
                with st.spinner("Generating AI content..."):
                    if self.content_generator:
                        generated = self.content_generator.generate_content(
                            business_type=business_type,
                            platform=platform,
                            campaign_type=campaign_type,
                            custom_prompt=custom_prompt if custom_prompt else None,
                            additional_context={
                                'context': context_input,
                                'campaign_name': campaign_name
                            } if context_input else {}
                        )
                        st.session_state.generated_campaign = {
                            'content': generated['content'],
                            'metadata': generated['metadata'],
                            'business_type': business_type,
                            'platform': platform,
                            'campaign_type': campaign_type,
                            'name': campaign_name or 'Untitled Campaign',
                            'schedule': schedule_datetime.isoformat()
                        }
                        st.success("Content generated successfully!")

        # Content Editor
        st.markdown("### Content Editor")

        default_content = ""
        if st.session_state.get('generated_campaign'):
            default_content = st.session_state.generated_campaign.get('content', '')
        elif edit_campaign:
            default_content = edit_campaign.get('content', '')

        content = st.text_area(
            "Post Content",
            value=default_content,
            height=250,
            placeholder="Your marketing content will appear here. Edit as needed..."
        )

        if content:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Words", len(content.split()))
            with col2:
                st.metric("Characters", len(content))
            with col3:
                st.metric("Sentences", content.count('.') + content.count('!') + content.count('?'))
            with col4:
                reading_time = len(content.split()) / 200
                st.metric("Read Time", f"{reading_time:.1f} min")

        st.markdown("---")

        # Media & Hashtags
        st.markdown("### Media & Tags")

        col1, col2 = st.columns(2)

        with col1:
            media_files = st.file_uploader(
                "Add Images/Videos",
                type=['jpg', 'png', 'jpeg', 'gif', 'mp4', 'webp'],
                accept_multiple_files=True,
                help="Upload up to 10 files"
            )
            if media_files:
                st.success(f"📎 {len(media_files)} file(s) uploaded")
                for file in media_files:
                    st.caption(f"- {file.name} ({file.size // 1024} KB)")

        with col2:
            hashtags = st.text_input("Hashtags", placeholder="#marketing #business #local", help="Separate with commas")
            suggested = BUSINESS_TYPES.get(business_type, {}).get('hashtags', [])
            if suggested:
                st.caption(f"💡 Suggested: {', '.join(suggested[:3])}")

        # Sentiment analysis of the content
        if content and self.components.get('sentiment'):
            with st.expander("🧠 Sentiment Analysis"):
                result = self.components['sentiment'].analyze(content)
                col1, col2, col3 = st.columns(3)
                with col1:
                    emoji = self.components['sentiment'].get_sentiment_emoji(result['sentiment'])
                    st.metric("Sentiment", f"{result['sentiment'].title()} {emoji}")
                with col2:
                    st.metric("Score", f"{result['score']:.2f}")
                with col3:
                    st.metric("Confidence", f"{result['confidence']:.0%}")
                for s in result.get('suggestions', []):
                    st.caption(s)

        st.markdown("---")

        # Action Buttons
        st.markdown("### Publish Campaign")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("💾 Save Draft", use_container_width=True):
                campaign_data = {
                    'name': campaign_name or 'Untitled Campaign',
                    'type': campaign_type,
                    'platform': platform,
                    'business_type': business_type,
                    'content': content,
                    'status': 'draft',
                    'schedule': schedule_datetime.isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {'hashtags': hashtags, 'media_count': len(media_files) if media_files else 0,
                                 'custom_prompt': custom_prompt, 'context': context_input}
                }
                self._persist(campaign_data, editing_id=editing_id)
                st.success("✅ Campaign saved as draft!")
                if editing_id is not None:
                    st.session_state.edit_campaign = None
                st.rerun()

        with col2:
            if st.button("📅 Schedule", use_container_width=True):
                campaign_data = {
                    'name': campaign_name or 'Untitled Campaign',
                    'type': campaign_type,
                    'platform': platform,
                    'business_type': business_type,
                    'content': content,
                    'status': 'scheduled',
                    'schedule': schedule_datetime.isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {'hashtags': hashtags, 'media_count': len(media_files) if media_files else 0,
                                 'custom_prompt': custom_prompt, 'context': context_input}
                }
                self._persist(campaign_data, editing_id=editing_id)
                st.success(f"✅ Campaign scheduled for {schedule_datetime.strftime('%Y-%m-%d %H:%M')}!")
                if editing_id is not None:
                    st.session_state.edit_campaign = None
                st.rerun()

        with col3:
            if st.button("🚀 Publish Now", use_container_width=True, type="primary"):
                campaign_data = {
                    'name': campaign_name or 'Untitled Campaign',
                    'type': campaign_type,
                    'platform': platform,
                    'business_type': business_type,
                    'content': content,
                    'status': 'published',
                    'published_at': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {'hashtags': hashtags, 'media_count': len(media_files) if media_files else 0,
                                 'custom_prompt': custom_prompt, 'context': context_input},
                    'engagement': {'likes': 0, 'comments': 0, 'shares': 0, 'reach': 0}
                }
                self._persist(campaign_data, editing_id=editing_id)
                st.success("✅ Campaign published successfully!")
                st.balloons()
                if editing_id is not None:
                    st.session_state.edit_campaign = None
                st.rerun()

        with col4:
            if st.button("🔄 Preview", use_container_width=True):
                st.session_state.preview_content = content
                st.session_state.preview_platform = platform
                st.rerun()

        # Preview Section
        if st.session_state.get('preview_content'):
            st.markdown("---")
            st.markdown("### Preview")

            preview_content = st.session_state.preview_content
            preview_platform = st.session_state.preview_platform

            if preview_platform == 'facebook':
                st.markdown(f"""
                <div style="background: #1877F2; padding: 20px; border-radius: 12px; color: white;">
                    <div style="background: white; padding: 15px; border-radius: 8px; color: #333;">
                        <p style="font-size: 16px;">{preview_content}</p>
                        <div style="border-top: 1px solid #ddd; padding-top: 10px; margin-top: 10px;">
                            <span style="color: #666;">👍 Like · 💬 Comment · 🔄 Share</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif preview_platform == 'instagram':
                st.markdown(f"""
                <div style="background: #fafafa; padding: 20px; border-radius: 12px; max-width: 400px; margin: 0 auto;">
                    <div style="background: white; border-radius: 8px; overflow: hidden;">
                        <div style="padding: 15px; border-bottom: 1px solid #efefef;">
                            <span style="font-weight: 600;">📸 Your Business</span>
                        </div>
                        <div style="padding: 15px;"><p>{preview_content}</p></div>
                        <div style="padding: 10px 15px; border-top: 1px solid #efefef; color: #999;">❤️ 0 likes · 💬 0 comments</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif preview_platform == 'whatsapp':
                st.markdown(f"""
                <div style="background: #075E54; padding: 20px; border-radius: 12px;">
                    <div style="background: #DCF8C6; padding: 15px; border-radius: 10px; max-width: 80%; margin: 10px 0;">
                        <p style="margin: 0; font-size: 14px;">{preview_content}</p>
                        <div style="font-size: 11px; color: #666; margin-top: 5px;">{datetime.now().strftime('%I:%M %p')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif preview_platform == 'google_business':
                st.markdown(f"""
                <div style="background: #4285F4; padding: 20px; border-radius: 12px; color: white;">
                    <div style="background: white; padding: 20px; border-radius: 8px; color: #333;">
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="font-size: 24px; margin-right: 10px;">📍</span>
                            <span style="font-weight: 600;">Google Business</span>
                        </div>
                        <p>{preview_content}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif preview_platform == 'email':
                st.markdown(f"""
                <div style="background: #f4f4f4; padding: 20px; border-radius: 12px;">
                    <div style="background: white; padding: 20px; border-radius: 8px;">
                        <div style="border-bottom: 2px solid #6C63FF; padding-bottom: 10px; margin-bottom: 15px;">
                            <span style="font-weight: 600; color: #6C63FF;">📧 Email Preview</span>
                        </div>
                        <pre style="white-space: pre-wrap; font-family: inherit; background: #f8f8f8; padding: 15px; border-radius: 8px;">{preview_content}</pre>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.text(preview_content)

            if st.button("Close Preview"):
                st.session_state.preview_content = None
                st.rerun()
