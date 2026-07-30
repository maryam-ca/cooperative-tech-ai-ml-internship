"""
Content Generator - Light version without heavy ML dependencies
Uses template-based generation for marketing content
"""

import random
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd

from config.settings import CONTENT_TEMPLATES, BUSINESS_TYPES

class ContentGenerator:
    """Content generation using templates - No AI/ML dependencies required"""
    
    def __init__(self):
        self.templates = CONTENT_TEMPLATES
        self.business_types = BUSINESS_TYPES
        
        # Marketing content templates by business type
        self.fallback_templates = {
            'restaurant_promotional': [
                "Indulge in our {cuisine} cuisine! Special offer: {offer} 🍽️",
                "Experience fine dining at {restaurant}. Book your table now! 🌟",
                "New dish alert! Try our {dish} - available this week only. 🆕",
                "Craving something delicious? Visit {restaurant} today! 😋",
                "Family dinner night? {restaurant} has the perfect menu! 👨‍👩‍👧‍👦"
            ],
            'restaurant_educational': [
                "Did you know? Our chefs use only the freshest ingredients! 🌿",
                "Learn the art of {cuisine} cooking at our special workshops! 👨‍🍳",
                "Wine pairing 101: Discover the perfect match for your meal 🍷"
            ],
            'restaurant_engagement': [
                "What's your favorite dish at {restaurant}? Tell us below! 💬",
                "Tag someone you'd love to dine with at {restaurant}! 📸",
                "Poll: What cuisine should we feature next week? 🗳️"
            ],
            'restaurant_brand_story': [
                "Since 2010, {restaurant} has been serving authentic {cuisine} cuisine...",
                "Our story began with a simple dream: to bring {cuisine} flavors to our community",
                "Family recipes passed down through generations - that's what makes {restaurant} special"
            ],
            'restaurant_testimonial': [
                "⭐ 'The best {cuisine} I've ever had!' - Happy Customer",
                "'Amazing service and incredible food!' - Google Review 5⭐",
                "'Will definitely come back again!' - Regular Customer"
            ],
            
            'gym_promotional': [
                "Get fit this season! Join {gym} and get {offer} 💪",
                "Transform your body with our {program} program! 🏋️",
                "New year, new you! Start your fitness journey at {gym} 🌟",
                "Join {gym} today and get your first month free! 🎉",
                "Shape your future at {gym} - where fitness meets community"
            ],
            'gym_educational': [
                "Did you know? Just 30 minutes of exercise daily boosts health! 🏃",
                "Nutrition tips: Pre-workout meals for maximum energy 🥗",
                "Recovery is key! Learn the best post-workout stretches 🧘",
                "5 exercises for a full body workout 💪",
                "The science of muscle growth explained 🧬"
            ],
            'gym_engagement': [
                "What's your fitness goal this month? Share below! 💪",
                "Tag your workout buddy who motivates you! 👊",
                "Vote: What class should we add next? 💪",
                "Share your progress photos! We want to celebrate with you 📸",
                "What's your favorite workout song? 🎵"
            ],
            'gym_brand_story': [
                "Founded by fitness enthusiasts, {gym} is more than a gym - it's a community",
                "Our mission: Make fitness accessible to everyone in our community",
                "From humble beginnings to the premier fitness center in town"
            ],
            'gym_testimonial': [
                "💪 'Lost 20 lbs in 3 months thanks to {gym}!' - Member Success Story",
                "'The trainers at {gym} are the best in town!' - Happy Member",
                "'I've never felt stronger!' - 5⭐ Review from a dedicated member"
            ],
            
            'shop_promotional': [
                "Summer sale is here! Up to {discount}% off on all items. 🛍️",
                "New collection just arrived at {shop}! Be the first to shop. 👗",
                "Exclusive offer: Buy one get one free at {shop} this week! 🎉",
                "Flash sale: {discount}% off everything for 24 hours only! ⚡",
                "New arrivals - the season's hottest trends at {shop} 🔥"
            ],
            'shop_educational': [
                "Style tips: How to wear this season's hottest trends! 👔",
                "Sustainable fashion: Why quality matters more than quantity 🌱",
                "Fabric guide: Learn about our premium materials 🧵",
                "How to style basics for any occasion 🎯",
                "The ultimate guide to building a versatile wardrobe 📚"
            ],
            'shop_engagement': [
                "What's your must-have item for the season? 🛍️",
                "Show us your style! Tag us in your outfit photos 📸",
                "Vote: What should we restock next? 🗳️",
                "How would you style this? Share your ideas! 💡",
                "Tag a friend who needs a wardrobe refresh! 👯"
            ],
            'shop_brand_story': [
                "From a small boutique to the community's favorite {shop}",
                "Quality, style, and affordability - our promise since 2015",
                "We believe fashion should be accessible to everyone"
            ],
            'shop_testimonial': [
                "⭐ 'Found the perfect outfit! Great quality and service!'",
                "'My go-to store for all my fashion needs' - Loyal Customer",
                "'Excellent customer service and amazing products!'"
            ],
            
            'clinic_promotional': [
                "Your health matters. Book a consultation at {clinic} today! 🏥",
                "Special health checkup package available at {clinic} 💉",
                "Feel better today! Visit {clinic} for expert care 🌟",
                "Comprehensive health packages starting at just ${price} 🏥",
                "Your wellness journey starts at {clinic}"
            ],
            'clinic_educational': [
                "Health tips: {tip} 🌿",
                "Did you know? Regular checkups can prevent major issues! 🔍",
                "Mental health matters: Tips for better wellbeing 🧠",
                "The importance of annual health screenings 📋",
                "5 signs you should see a doctor 🚨"
            ],
            'clinic_engagement': [
                "Share your wellness tips with our community! 💚",
                "What health topic should we cover next? 🗳️",
                "Tag someone who inspires you to stay healthy! 💪",
                "How do you stay healthy? Share your routine! 🌿",
                "What's your favorite way to de-stress? 🧘"
            ],
            'clinic_brand_story': [
                "Compassionate care since 2008 - that's the {clinic} promise",
                "Our team of experts is dedicated to your wellbeing",
                "We treat every patient like family at {clinic}"
            ],
            'clinic_testimonial': [
                "🏥 'Best medical care I've ever received!' - Patient Review",
                "'The doctors at {clinic} truly care about their patients'",
                "'Life-saving treatment and compassionate care'"
            ]
        }
        
        # Platform-specific formatting
        self.platform_formats = {
            'instagram': {
                'max_length': 2200,
                'format': lambda x: x.replace('. ', '.\n\n')[:2200]
            },
            'facebook': {
                'max_length': 63206,
                'format': lambda x: x[:63206]
            },
            'google_business': {
                'max_length': 1500,
                'format': lambda x: x.replace('!', '! ')[:1500]
            },
            'whatsapp': {
                'max_length': 4096,
                'format': lambda x: f"Hello! 👋\n\n{x[:4096]}\n\nChat with us for more details!"
            },
            'email': {
                'max_length': 50000,
                'format': lambda x: f"Subject: {x[:50]}...\n\nDear Valued Customer,\n\n{x[:50000]}\n\nBest regards,\nThe Team"
            }
        }
    
    def generate_content(
        self,
        business_type: str,
        platform: str,
        campaign_type: str,
        custom_prompt: Optional[str] = None,
        additional_context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate marketing content using templates
        
        Args:
            business_type: Type of business (restaurant, gym, shop, clinic)
            platform: Target platform (facebook, instagram, etc.)
            campaign_type: Type of campaign (promotional, educational, etc.)
            custom_prompt: Custom prompt (used as additional context)
            additional_context: Additional context for generation
            
        Returns:
            Dictionary containing generated content and metadata
        """
        
        # Get business info
        business_info = self.business_types.get(business_type, {})
        
        # Build context
        context = {
            'business_type': business_type,
            'business_name': business_info.get('name', 'Business'),
            'platform': platform,
            'campaign_type': campaign_type,
            'themes': business_info.get('content_themes', []),
            'hashtags': business_info.get('hashtags', []),
            'additional_context': additional_context or {}
        }
        
        # Generate content using templates
        content = self._generate_with_templates(context, custom_prompt)
        
        # Format for platform
        formatted_content = self._format_for_platform(content, platform)
        
        # Optimize for engagement
        if campaign_type in ['engagement', 'promotional']:
            formatted_content = self._optimize_for_engagement(formatted_content)
        
        # Add metadata
        result = {
            'content': formatted_content,
            'metadata': {
                'business_type': business_type,
                'platform': platform,
                'campaign_type': campaign_type,
                'generated_at': pd.Timestamp.now().isoformat(),
                'word_count': len(formatted_content.split()),
                'character_count': len(formatted_content),
                'template_used': 'marketing_template'
            }
        }
        
        return result
    
    def _generate_with_templates(self, context: Dict, custom_prompt: Optional[str] = None) -> str:
        """Generate content using template-based approach"""
        
        business_type = context.get('business_type', 'shop')
        campaign_type = context.get('campaign_type', 'promotional')
        business_name = context.get('business_name', 'our business')
        
        # Get templates for business type and campaign type
        template_key = f"{business_type}_{campaign_type}"
        templates = self.fallback_templates.get(
            template_key,
            self.fallback_templates.get(
                f"{business_type}_promotional",
                [
                    f"Check out {business_name} for amazing {campaign_type} offers! 🎉",
                    f"Experience the best at {business_name} - {campaign_type} deals! 🌟",
                    f"Don't miss out on {campaign_type} offers at {business_name}! 🔥"
                ]
            )
        )
        
        # Choose random template
        template = random.choice(templates)
        
        # Prepare fillers
        fillers = self._get_fillers(business_type, context)
        
        # Apply fillers to template
        try:
            content = template.format(**fillers)
        except KeyError:
            # If template has missing keys, use default
            content = f"Check out {business_name} for amazing offers! 🎉"
        
        # Add custom prompt context if provided
        if custom_prompt:
            content = f"{content}\n\n📝 {custom_prompt[:100]}..."
        
        # Add relevant hashtags
        hashtags = context.get('hashtags', [])
        if hashtags and random.random() > 0.3:
            selected_hashtags = random.sample(hashtags, min(3, len(hashtags)))
            content += "\n\n" + " ".join(selected_hashtags)
        
        return content
    
    def _get_fillers(self, business_type: str, context: Dict) -> Dict:
        """Get filler values for templates"""
        
        cuisine_options = ['Italian', 'Mexican', 'Japanese', 'Chinese', 'Indian', 'French', 'Thai', 'Spanish']
        dish_options = ['pizza', 'pasta', 'sushi', 'burger', 'salad', 'steak', 'tacos', 'ramen', 'pasta', 'pizza']
        
        fillers = {
            'cuisine': random.choice(cuisine_options),
            'restaurant': context.get('business_name', 'our restaurant'),
            'offer': random.choice(['20% off', 'free dessert', 'buy one get one free', 'complimentary drink', 'special discount', 'free delivery']),
            'dish': random.choice(dish_options),
            'gym': context.get('business_name', 'our gym'),
            'program': random.choice(['HIIT', 'Yoga', 'CrossFit', 'Strength Training', 'Pilates', 'Zumba', 'Boxing']),
            'discount': str(random.randint(10, 60)),
            'shop': context.get('business_name', 'our shop'),
            'clinic': context.get('business_name', 'our clinic'),
            'price': str(random.randint(50, 500)),
            'tip': random.choice([
                'Stay hydrated throughout the day 💧',
                'Get 7-8 hours of quality sleep 😴',
                'Exercise regularly for better health 🏃',
                'Eat a balanced diet with plenty of vegetables 🥗',
                'Take breaks during work to reduce stress 🧘',
                'Practice mindfulness and meditation 🌿',
                'Stay connected with loved ones ❤️',
                'Drink at least 8 glasses of water daily 💧',
                'Take a 10-minute walk after meals 🚶'
            ]),
            'business': context.get('business_name', 'our business')
        }
        
        # Add marketing elements
        hooks = [
            "Your search for quality ends here!",
            "We've got something special for you!",
            "Don't miss out on this opportunity!",
            "What if we told you...",
            "Ready for an amazing experience?",
            "Imagine waking up to...",
            "The secret to..."
        ]
        
        values = [
            "Premium quality at affordable prices",
            "Expert service you can trust",
            "Proven results that speak for themselves",
            "A team dedicated to your satisfaction",
            "Innovative solutions for your needs",
            "Unmatched quality and service"
        ]
        
        ctas = [
            "Visit us today! 🚀",
            "Book your appointment now! 📅",
            "Contact us for more details! 📞",
            "Don't wait - act now! ⚡",
            "Experience the difference today! 🌟",
            "Join us now! 🤝"
        ]
        
        questions = [
            "Are you looking for something special?",
            "Have you been searching for quality?",
            "Ready for a change?",
            "What's important to you?",
            "Did you know we can help?",
            "Want to experience something amazing?"
        ]
        
        answers = [
            "We have exactly what you need!",
            "We're here to make it happen!",
            "We specialize in that!",
            "We have the expertise you need!",
            "We're the solution you've been looking for!",
            "We'll make it happen!"
        ]
        
        learnings = [
            "Quality is our priority",
            "We focus on results",
            "We're dedicated to excellence",
            "We understand your needs",
            "We're experts in our field",
            "We deliver results"
        ]
        
        stories = [
            "We started with a simple vision...",
            "Our journey began 10 years ago...",
            "We believe in making a difference...",
            "Every customer has a story...",
            "We've been serving our community..."
        ]
        
        engagements = [
            "Tell us what you think! 💬",
            "Share your experience! 📝",
            "Join our community! 🤝",
            "We'd love to hear from you! 💌",
            "Your opinion matters to us! ⭐"
        ]
        
        fillers.update({
            'hook': random.choice(hooks),
            'value': random.choice(values),
            'cta': random.choice(ctas),
            'question': random.choice(questions),
            'answer': random.choice(answers),
            'learning': random.choice(learnings),
            'story': random.choice(stories),
            'engagement': random.choice(engagements)
        })
        
        return fillers
    
    def _format_for_platform(self, content: str, platform: str) -> str:
        """Format content for specific platform"""
        
        platform_config = self.platform_formats.get(platform, self.platform_formats['facebook'])
        return platform_config['format'](content)
    
    def _optimize_for_engagement(self, content: str) -> str:
        """Optimize content for better engagement"""
        
        # Add emojis if not present
        emojis = ['🎉', '🔥', '✨', '💯', '🌟', '🚀', '💪', '🎯', '⭐', '💎', '🌈', '⚡']
        if not any(emoji in content for emoji in emojis[:5]):
            content = f"{random.choice(emojis)} {content}"
        
        # Add a question for engagement if none exists
        question_markers = ['?', 'what', 'how', 'why', 'when', 'which', 'who']
        if not any(marker in content.lower() for marker in question_markers):
            engagement_questions = [
                " What do you think? 💭",
                " Share your thoughts below! 💬",
                " Have you tried this? 🤔",
                " Tell us your experience! ⭐",
                " What would you add? ✨",
                " Do you agree? 💡"
            ]
            content += random.choice(engagement_questions)
        
        # Add call to action if missing
        action_words = ['visit', 'contact', 'click', 'call', 'book', 'join', 'sign up', 'register', 'download']
        if not any(word in content.lower() for word in action_words):
            ctas = [
                " Visit us today! 🚀",
                " Book your spot now! 📅",
                " Contact us for more! 📞",
                " Join the experience! 🌟",
                " Don't wait - act now! ⚡",
                " Secure your spot today! 🎯"
            ]
            content += random.choice(ctas)
        
        return content
    
    def generate_multiple_variations(
        self,
        business_type: str,
        platform: str,
        num_variations: int = 3,
        **kwargs
    ) -> List[Dict]:
        """Generate multiple content variations"""
        variations = []
        
        for i in range(num_variations):
            variation_context = kwargs.copy()
            variation_context['variation'] = i + 1
            
            content = self.generate_content(
                business_type=business_type,
                platform=platform,
                campaign_type=kwargs.get('campaign_type', 'promotional'),
                additional_context=variation_context
            )
            variations.append(content)
        
        return variations

# Standalone function for easier import
def generate_marketing_content(
    business_type: str,
    platform: str,
    campaign_type: str = 'promotional',
    **kwargs
) -> Dict:
    """Convenience function for generating content"""
    generator = ContentGenerator()
    return generator.generate_content(
        business_type=business_type,
        platform=platform,
        campaign_type=campaign_type,
        **kwargs
    )