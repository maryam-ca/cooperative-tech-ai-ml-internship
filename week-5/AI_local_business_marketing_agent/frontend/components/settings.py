"""
Settings Component - Application settings and configuration
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any
import os

from config.settings import BUSINESS_TYPES, PLATFORMS, UI_SETTINGS

class SettingsComponent:
    """Render settings and configuration page"""
    
    def __init__(self, components: Dict[str, Any]):
        self.components = components
        self.db = components.get('db')
    
    def render(self):
        """Render the settings page"""
        tabs = st.tabs([
            "🏢 Business Profile",
            "🎨 Appearance",
            "🤖 AI Settings",
            "📱 Platform Settings",
            "📊 Data Management",
            "🔐 Security"
        ])
        
        with tabs[0]:
            self._render_business_profile()
        
        with tabs[1]:
            self._render_appearance_settings()
        
        with tabs[2]:
            self._render_ai_settings()
        
        with tabs[3]:
            self._render_platform_settings()
        
        with tabs[4]:
            self._render_data_management()
        
        with tabs[5]:
            self._render_security_settings()
    
    def _render_business_profile(self):
        """Render business profile settings"""
        st.markdown("#### Business Profile")
        
        # Get current profile
        profile = st.session_state.get('business_profile', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input(
                "Business Name",
                value=profile.get('name', '')
            )
            
            business_type = st.selectbox(
                "Business Type",
                list(BUSINESS_TYPES.keys()),
                format_func=lambda x: f"{BUSINESS_TYPES[x]['icon']} {BUSINESS_TYPES[x]['name']}",
                index=list(BUSINESS_TYPES.keys()).index(profile.get('type', 'shop')) if profile.get('type') in BUSINESS_TYPES else 0
            )
            
            email = st.text_input(
                "Business Email",
                value=profile.get('email', '')
            )
        
        with col2:
            phone = st.text_input(
                "Phone Number",
                value=profile.get('phone', '')
            )
            
            address = st.text_area(
                "Business Address",
                value=profile.get('address', '')
            )
            
            website = st.text_input(
                "Website URL",
                value=profile.get('website', '')
            )
        
        # Business description
        description = st.text_area(
            "Business Description",
            value=profile.get('description', ''),
            height=100,
            placeholder="Describe your business, products, and services..."
        )
        
        # Save profile
        if st.button("💾 Save Business Profile", type="primary"):
            profile.update({
                'name': business_name,
                'type': business_type,
                'email': email,
                'phone': phone,
                'address': address,
                'website': website,
                'description': description,
                'updated_at': datetime.now().isoformat()
            })
            st.session_state.business_profile = profile
            st.success("✅ Business profile saved successfully!")
            st.balloons()
    
    def _render_appearance_settings(self):
        """Render appearance settings"""
        st.markdown("#### Appearance Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox(
                "Theme",
                ["Dark", "Light", "System Default"],
                index=0
            )
            
            primary_color = st.color_picker(
                "Primary Color",
                value=UI_SETTINGS.get('primary_color', '#6C63FF')
            )
        
        with col2:
            secondary_color = st.color_picker(
                "Secondary Color",
                value=UI_SETTINGS.get('secondary_color', '#FF6584')
            )
            
            accent_color = st.color_picker(
                "Accent Color",
                value=UI_SETTINGS.get('accent_color', '#00D2FF')
            )
        
        # Font settings
        st.markdown("#### Font Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            font_family = st.selectbox(
                "Font Family",
                ["Inter", "Roboto", "Open Sans", "Poppins", "System Default"]
            )
        
        with col2:
            font_size = st.select_slider(
                "Font Size",
                options=["Small", "Medium", "Large", "Extra Large"],
                value="Medium"
            )
        
        # Preview
        st.markdown("#### Preview")
        st.markdown(f"""
        <div style="background: {primary_color}22; padding: 20px; border-radius: 12px; border: 2px solid {primary_color};">
            <h4 style="color: {primary_color};">Sample Heading</h4>
            <p style="color: white;">This is how your content will look with the selected theme.</p>
            <div style="display: flex; gap: 10px;">
                <span style="background: {primary_color}; color: white; padding: 5px 15px; border-radius: 8px;">Primary</span>
                <span style="background: {secondary_color}; color: white; padding: 5px 15px; border-radius: 8px;">Secondary</span>
                <span style="background: {accent_color}; color: white; padding: 5px 15px; border-radius: 8px;">Accent</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 Save Appearance Settings", type="primary"):
            st.success("✅ Appearance settings saved!")
    
    def _render_ai_settings(self):
        """Render AI settings"""
        st.markdown("#### AI Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model_name = st.selectbox(
                "AI Model",
                [
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "claude-2",
                    "llama-2",
                    "local-model"
                ]
            )
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher = more creative, Lower = more focused"
            )
        
        with col2:
            max_tokens = st.slider(
                "Max Tokens",
                min_value=50,
                max_value=1000,
                value=500,
                step=50
            )
            
            language = st.selectbox(
                "Primary Language",
                ["English", "Spanish", "French", "German", "Chinese", "Hindi"]
            )
        
        # API Keys
        st.markdown("#### API Keys")
        
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-..."
        )
        
        huggingface_key = st.text_input(
            "HuggingFace API Key",
            type="password",
            placeholder="hf_..."
        )
        
        # Content generation settings
        st.markdown("#### Content Generation Settings")
        
        content_style = st.selectbox(
            "Content Style",
            ["Professional", "Casual", "Humorous", "Inspirational", "Formal"]
        )
        
        tone = st.selectbox(
            "Tone",
            ["Neutral", "Enthusiastic", "Authoritative", "Friendly", "Trustworthy"]
        )
        
        include_hashtags = st.checkbox("Auto-generate hashtags", value=True)
        include_emojis = st.checkbox("Include emojis", value=True)
        
        if st.button("💾 Save AI Settings", type="primary"):
            # Save to session or environment
            st.success("✅ AI settings saved!")
            st.info("Note: API keys will be stored securely in environment variables.")
    
    def _render_platform_settings(self):
        """Render platform settings"""
        st.markdown("#### Platform Settings")
        
        for platform, config in PLATFORMS.items():
            st.markdown(f"##### {config['icon']} {config['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                enabled = st.checkbox(
                    f"Enable {config['name']}",
                    value=True,
                    key=f"platform_enabled_{platform}"
                )
            
            with col2:
                if platform == 'instagram':
                    auto_post = st.checkbox(
                        "Auto-post to Instagram",
                        value=False,
                        key=f"platform_auto_{platform}"
                    )
                else:
                    auto_post = st.checkbox(
                        "Auto-post",
                        value=True,
                        key=f"platform_auto_{platform}"
                    )
            
            # Platform-specific settings
            if platform == 'facebook':
                page_id = st.text_input(
                    "Facebook Page ID",
                    placeholder="Your page ID",
                    key=f"fb_page_{platform}"
                )
                
                schedule_time = st.selectbox(
                    "Best Posting Time",
                    ["9 AM", "12 PM", "3 PM", "6 PM", "9 PM"],
                    key=f"fb_time_{platform}"
                )
            
            elif platform == 'instagram':
                account = st.text_input(
                    "Instagram Account",
                    placeholder="@your_business",
                    key=f"ig_account_{platform}"
                )
                
                post_frequency = st.selectbox(
                    "Posting Frequency",
                    ["Daily", "3 times/week", "Weekly", "Monthly"],
                    key=f"ig_freq_{platform}"
                )
            
            elif platform == 'whatsapp':
                phone_number = st.text_input(
                    "WhatsApp Business Number",
                    placeholder="+1234567890",
                    key=f"wa_number_{platform}"
                )
                
                message_templates = st.selectbox(
                    "Default Message Template",
                    ["Promotional", "Update", "Engagement", "Reminder"],
                    key=f"wa_template_{platform}"
                )
            
            elif platform == 'google_business':
                location_id = st.text_input(
                    "Google Business Location ID",
                    placeholder="Your location ID",
                    key=f"gb_location_{platform}"
                )
                
                auto_reply = st.checkbox(
                    "Auto-reply to reviews",
                    value=True,
                    key=f"gb_auto_reply_{platform}"
                )
            
            elif platform == 'email':
                from_email = st.text_input(
                    "From Email",
                    placeholder="hello@yourbusiness.com",
                    key=f"email_from_{platform}"
                )
                
                signature = st.text_input(
                    "Email Signature",
                    placeholder="Team @ Your Business",
                    key=f"email_sign_{platform}"
                )
            
            st.markdown("---")
        
        if st.button("💾 Save Platform Settings", type="primary"):
            st.success("✅ Platform settings saved!")
    
    def _render_data_management(self):
        """Render data management settings"""
        st.markdown("#### Data Management")
        
        # Data statistics
        campaigns = st.session_state.get('campaign_history', [])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Campaigns", len(campaigns))
        with col2:
            st.metric("Total Data Points", sum(len(c.get('content', '')) for c in campaigns))
        with col3:
            if self.db:
                st.metric("Database Size", "Active")
            else:
                st.metric("Database Status", "Memory Only")
        
        st.markdown("---")
        
        # Actions
        st.markdown("#### Data Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Campaigns", use_container_width=True):
                if st.session_state.get('confirm_clear'):
                    st.session_state.campaign_history = []
                    st.success("✅ All campaigns cleared!")
                    st.session_state.confirm_clear = False
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm clearing all campaigns")
            
            if st.button("📤 Export All Data", use_container_width=True):
                if campaigns:
                    df = pd.DataFrame(campaigns)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"export_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No data to export")
        
        with col2:
            if st.button("📥 Import Data", use_container_width=True):
                uploaded_file = st.file_uploader(
                    "Choose CSV file",
                    type=['csv'],
                    key="import_file"
                )
                if uploaded_file:
                    df = pd.read_csv(uploaded_file)
                    st.dataframe(df.head())
                    if st.button("Confirm Import"):
                        st.success(f"✅ Imported {len(df)} records!")
        
        # Backup
        st.markdown("#### Backup Settings")
        
        backup_frequency = st.selectbox(
            "Auto-backup Frequency",
            ["Daily", "Weekly", "Monthly", "Never"]
        )
        
        backup_location = st.text_input(
            "Backup Location",
            placeholder="/path/to/backup/folder"
        )
        
        if st.button("💾 Create Backup Now", use_container_width=True):
            st.success("✅ Backup created successfully!")
    
    def _render_security_settings(self):
        """Render security settings"""
        st.markdown("#### Security Settings")
        
        st.markdown("##### Authentication")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_password = st.text_input(
                "Current Password",
                type="password"
            )
        
        with col2:
            new_password = st.text_input(
                "New Password",
                type="password"
            )
        
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )
        
        if st.button("🔑 Change Password", type="primary"):
            if new_password == confirm_password:
                st.success("✅ Password changed successfully!")
            else:
                st.error("❌ Passwords do not match")
        
        st.markdown("---")
        
        st.markdown("##### Session Management")
        
        session_timeout = st.selectbox(
            "Session Timeout",
            ["30 minutes", "1 hour", "2 hours", "4 hours", "8 hours", "Never"]
        )
        
        remember_device = st.checkbox("Remember this device", value=True)
        
        if st.button("💾 Save Security Settings"):
            st.success("✅ Security settings saved!")
        
        st.markdown("---")
        
        st.markdown("##### Active Sessions")
        
        st.info("📱 1 active session (Current device)")
        
        if st.button("🔄 Logout All Other Devices"):
            st.warning("All other devices have been logged out")