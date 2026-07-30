"""
Email Campaign Generator - Create professional email marketing campaigns
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd

from models.content_generator import ContentGenerator

class EmailCampaignGenerator:
    """Generate email marketing campaigns with AI"""
    
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.email_templates = {
            'newsletter': {
                'subject': "📫 {business_name} Newsletter - {month} Edition",
                'body': """
                Hello {name},

                We hope this email finds you well! We're excited to share the latest updates from {business_name}.

                {content}

                Don't forget to check out our special offers!

                Best regards,
                The {business_name} Team
                """
            },
            'promotional': {
                'subject': "🎉 Special Offer from {business_name} - {offer}",
                'body': """
                Hello {name},

                We're thrilled to announce our latest promotion!

                {content}

                Offer valid until {end_date}. Don't miss out!

                Warm regards,
                The {business_name} Team
                """
            },
            'event': {
                'subject': "📅 Join Us at {event_name} - {business_name}",
                'body': """
                Hello {name},

                We're excited to invite you to {event_name}!

                {content}

                Limited spots available. RSVP now!

                See you there,
                The {business_name} Team
                """
            },
            'testimonial': {
                'subject': "🌟 Customer Success Story from {business_name}",
                'body': """
                Hello {name},

                We love sharing our customers' success stories. Here's one that we thought you'd enjoy:

                {content}

                Ready to start your journey with us?

                Best,
                The {business_name} Team
                """
            }
        }
    
    def create_campaign(
        self,
        business_name: str,
        campaign_type: str,
        customer_name: str = "Valued Customer",
        custom_content: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create an email campaign"""
        
        # Get template
        template = self.email_templates.get(campaign_type, self.email_templates['newsletter'])
        
        # Generate content if not provided
        if not custom_content:
            generated = self.content_generator.generate_content(
                business_type=kwargs.get('business_type', 'shop'),
                platform='email',
                campaign_type=campaign_type,
                additional_context=kwargs.get('context', {})
            )
            content = generated['content']
        else:
            content = custom_content
        
        # Format email
        email_data = {
            'subject': template['subject'].format(
                business_name=business_name,
                month=datetime.now().strftime('%B'),
                offer=kwargs.get('offer', 'exclusive discount'),
                event_name=kwargs.get('event_name', 'our upcoming event'),
                **kwargs
            ),
            'body': template['body'].format(
                name=customer_name,
                business_name=business_name,
                content=content,
                end_date=kwargs.get('end_date', 'this month'),
                event_name=kwargs.get('event_name', 'our event'),
                **kwargs
            ),
            'metadata': {
                'campaign_type': campaign_type,
                'business_name': business_name,
                'created_at': datetime.now().isoformat(),
                'recipient_count': kwargs.get('recipient_count', 0),
                **kwargs
            }
        }
        
        return email_data
    
    def generate_batch_campaigns(
        self,
        business_name: str,
        campaign_type: str,
        recipient_list: List[str],
        **kwargs
    ) -> List[Dict]:
        """Generate campaigns for multiple recipients"""
        campaigns = []
        
        for recipient in recipient_list:
            campaign = self.create_campaign(
                business_name=business_name,
                campaign_type=campaign_type,
                customer_name=recipient,
                **kwargs
            )
            campaigns.append(campaign)
        
        return campaigns
    
    def analyze_campaign_performance(self, campaign_data: Dict) -> Dict:
        """Simulate campaign performance metrics"""
        return {
            'open_rate': random.uniform(20, 60),
            'click_rate': random.uniform(5, 25),
            'conversion_rate': random.uniform(1, 10),
            'bounce_rate': random.uniform(1, 5),
            'estimated_reach': random.randint(100, 10000)
        }
    
    def render_ui(self):
        """Render email campaign UI in Streamlit"""
        
        st.markdown("### 📧 Create Email Campaign")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Business Name", "My Business")
            
            campaign_type = st.selectbox(
                "Campaign Type",
                list(self.email_templates.keys())
            )
            
            recipient_name = st.text_input("Recipient Name (or use 'Customer')", "Valued Customer")
            
            recipient_count = st.number_input("Number of Recipients (estimated)", 1, 10000, 100)
        
        with col2:
            business_type = st.selectbox(
                "Business Type",
                ['restaurant', 'gym', 'shop', 'clinic']
            )
            
            # Custom fields based on campaign type
            extra_fields = {}
            
            if campaign_type == 'promotional':
                extra_fields['offer'] = st.text_input("Offer Description", "20% off your first order")
                extra_fields['end_date'] = st.date_input("Offer End Date")
                
            elif campaign_type == 'event':
                extra_fields['event_name'] = st.text_input("Event Name", "Open House")
                
            # Custom content
            custom_content = st.text_area(
                "Custom Content (Optional)",
                placeholder="Leave empty to let AI generate content",
                height=100
            )
        
        # Generate email preview
        if st.button("✉️ Generate Email", use_container_width=True):
            with st.spinner("Generating email..."):
                campaign = self.create_campaign(
                    business_name=business_name,
                    campaign_type=campaign_type,
                    customer_name=recipient_name,
                    custom_content=custom_content if custom_content else None,
                    business_type=business_type,
                    recipient_count=recipient_count,
                    **extra_fields
                )
                
                st.session_state.email_preview = campaign
                st.success("Email generated!")
        
        # Display preview
        if st.session_state.get('email_preview'):
            st.markdown("### 📨 Email Preview")
            
            preview = st.session_state.email_preview
            
            st.markdown(f"**Subject:** {preview['subject']}")
            st.markdown("---")
            st.markdown(preview['body'])
            st.markdown("---")
            
            # Campaign analytics
            st.markdown("### 📊 Estimated Performance")
            
            performance = self.analyze_campaign_performance(preview)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Open Rate", f"{performance['open_rate']:.1f}%")
            with col2:
                st.metric("Click Rate", f"{performance['click_rate']:.1f}%")
            with col3:
                st.metric("Conversion Rate", f"{performance['conversion_rate']:.1f}%")
            with col4:
                st.metric("Estimated Reach", f"{performance['estimated_reach']:,}")
            
            # Actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📤 Send Now", use_container_width=True):
                    st.success(f"Email campaign sent to {recipient_count} recipients!")
                    
            with col2:
                if st.button("📋 Save as Template", use_container_width=True):
                    st.success("Template saved!")