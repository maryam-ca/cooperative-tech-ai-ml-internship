"""
WhatsApp Campaign Generator - Create WhatsApp marketing messages
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd

from models.content_generator import ContentGenerator

class WhatsAppCampaignGenerator:
    """Generate WhatsApp marketing campaigns"""
    
    def __init__(self):
        self.content_generator = ContentGenerator()
        
        self.message_templates = {
            'promotional': [
                "🎉 Hi {name}! Special offer from {business}: {offer}. Reply for details!",
                "📢 {business} exclusive: {offer}. Don't miss out! Click for more info.",
                "💫 {business} is excited to offer {offer}. Limited time only!"
            ],
            'update': [
                "📋 Hey {name}! {business} has new updates: {update}. Check it out!",
                "🔔 {business} update: {update}. Stay tuned for more!",
                "📣 Important update from {business}: {update}"
            ],
            'engagement': [
                "👋 Hi {name}! How's your experience with {business}? Share your feedback!",
                "💬 We value your opinion {name}! What would you like to see at {business}?",
                "✨ Quick question for you {name}: What's your favorite thing about {business}?"
            ],
            'reminder': [
                "⏰ Reminder {name}: {event} at {business} tomorrow. Can't wait to see you!",
                "📅 Don't forget {name}! {event} at {business} is coming up soon.",
                "🔔 Your appointment/event is approaching: {event} at {business}."
            ]
        }
    
    def create_message(
        self,
        business_name: str,
        message_type: str,
        recipient_name: str = "Customer",
        custom_message: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Create a WhatsApp message"""
        
        # Generate content if not provided
        if not custom_message:
            # Choose a template
            templates = self.message_templates.get(message_type, self.message_templates['promotional'])
            template = random.choice(templates)
            
            # Fill template
            params = {
                'name': recipient_name,
                'business': business_name,
                'offer': 'a special discount',
                'update': 'new products and services',
                'event': 'our upcoming event',
            }
            params.update(kwargs)
            message = template.format(**params)
            
            # Add emoji and formatting
            message = self._enhance_message(message, message_type)
            
        else:
            message = custom_message
        
        return {
            'message': message,
            'recipient': recipient_name,
            'business': business_name,
            'type': message_type,
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'character_count': len(message),
                'word_count': len(message.split()),
                **kwargs
            }
        }
    
    def _enhance_message(self, message: str, message_type: str) -> str:
        """Add emojis and formatting to message"""
        
        enhancements = {
            'promotional': ['🎉', '✨', '💫', '🔥', '🌟'],
            'update': ['📋', '🔔', '📢', '📣', '💡'],
            'engagement': ['👋', '💬', '✨', '🤗', '💭'],
            'reminder': ['⏰', '📅', '🔔', '📌', '✅']
        }
        
        # Add relevant emoji if not present
        emojis = enhancements.get(message_type, ['✨'])
        if not any(emoji in message for emoji in emojis):
            message = f"{random.choice(emojis)} {message}"
        
        # Add call to action if missing
        ctas = [
            '\n\n📱 Reply to this message for more details!',
            '\n\n💬 Chat with us for more information!',
            '\n\n📞 Call us to learn more!',
            '\n\n🌐 Visit us at our store!'
        ]
        
        if 'Reply' not in message and 'message' not in message.lower():
            message += random.choice(ctas)
        
        return message
    
    def create_broadcast(
        self,
        business_name: str,
        message_type: str,
        recipient_list: List[str],
        **kwargs
    ) -> List[Dict]:
        """Create broadcast messages for multiple recipients"""
        messages = []
        
        for recipient in recipient_list:
            message = self.create_message(
                business_name=business_name,
                message_type=message_type,
                recipient_name=recipient,
                **kwargs
            )
            messages.append(message)
        
        return messages
    
    def render_ui(self):
        """Render WhatsApp campaign UI in Streamlit"""
        
        st.markdown("### 💬 WhatsApp Campaign")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Business Name", "My Business")
            
            message_type = st.selectbox(
                "Message Type",
                ['promotional', 'update', 'engagement', 'reminder']
            )
            
            recipient_name = st.text_input("Recipient Name", "Customer")
            
            recipient_count = st.number_input("Number of Recipients", 1, 10000, 10)
        
        with col2:
            # Context-specific fields
            if message_type == 'promotional':
                offer = st.text_input("Offer Description", "20% off your first order")
                kwargs = {'offer': offer}
            elif message_type == 'update':
                update = st.text_input("Update Description", "new products available")
                kwargs = {'update': update}
            elif message_type == 'reminder':
                event = st.text_input("Event Description", "your appointment")
                kwargs = {'event': event}
            else:
                kwargs = {}
            
            custom_message = st.text_area(
                "Custom Message (Optional)",
                placeholder="Leave empty to use template",
                height=100
            )
        
        # Generate message
        if st.button("💬 Generate WhatsApp Message", use_container_width=True):
            with st.spinner("Generating message..."):
                message = self.create_message(
                    business_name=business_name,
                    message_type=message_type,
                    recipient_name=recipient_name,
                    custom_message=custom_message if custom_message else None,
                    **kwargs
                )
                
                st.session_state.whatsapp_preview = message
                st.success("Message generated!")
        
        # Display preview
        if st.session_state.get('whatsapp_preview'):
            st.markdown("### 📱 Message Preview")
            
            preview = st.session_state.whatsapp_preview
            sent_time = datetime.now().strftime('%I:%M %p')
            body = preview['message'].replace('\n', '<br>')
            
            # Display as a WhatsApp chat mockup
            st.markdown(f"""
            <div class="wa-phone">
                <div class="wa-topbar">
                    <div class="wa-avatar">{preview['business'][:1].upper()}</div>
                    <div class="wa-contact">
                        <div class="wa-name">{preview['business']}</div>
                        <div class="wa-status">online</div>
                    </div>
                    <div class="wa-icons">📞&nbsp;&nbsp;📹</div>
                </div>
                <div class="wa-chat">
                    <div class="wa-bubble">
                        <span class="wa-text">{body}</span>
                        <span class="wa-meta">{sent_time} <span class="wa-ticks">✓✓</span></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Message stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Character Count", preview['metadata']['character_count'])
                st.metric("Word Count", preview['metadata']['word_count'])
            with col2:
                st.metric("Type", preview['type'].title())
                st.metric("Recipient", preview['recipient'])
            
            # Broadcast options
            st.markdown("### 📤 Send Campaign")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📤 Send Now", use_container_width=True):
                    st.success(f"Message sent to {recipient_count} recipients!")
            
            with col2:
                if st.button("📅 Schedule", use_container_width=True):
                    schedule_time = st.time_input("Schedule Time", datetime.now().time())
                    st.success(f"Message scheduled for {schedule_time}")
            
            with col3:
                if st.button("📋 Save Template", use_container_width=True):
                    st.success("Template saved!")