"""
AI Personality Manager - Controls response style and personality across all Jarvis features
"""

import json
import os

class PersonalityManager:
    def __init__(self):
        self.config_file = 'personality_config.json'
        self.load_config()
        
        # Response style templates
        self.response_styles = {
            'professional': {
                'prefix': 'I shall ',
                'suffix': ', sir.',
                'tone': 'formal',
                'examples': {
                    'success': 'I have successfully completed the requested operation',
                    'error': 'I regret to inform you that the operation could not be completed',
                    'executing': 'I am proceeding with the requested task'
                }
            },
            'casual': {
                'prefix': '',
                'suffix': '!',
                'tone': 'relaxed',
                'examples': {
                    'success': 'Got it done for you',
                    'error': 'Oops, that didn\'t work out',
                    'executing': 'Working on it'
                }
            },
            'friendly': {
                'prefix': 'I\'d be happy to ',
                'suffix': '!',
                'tone': 'warm',
                'examples': {
                    'success': 'I\'m glad I could help you with that',
                    'error': 'Sorry, I couldn\'t get that to work',
                    'executing': 'I\'m working on that for you right now'
                }
            },
            'technical': {
                'prefix': 'Executing ',
                'suffix': '...',
                'tone': 'precise',
                'examples': {
                    'success': 'Operation completed successfully',
                    'error': 'Error: Operation failed with status code',
                    'executing': 'Processing request with system parameters'
                }
            }
        }
        
        # AI personality traits
        self.personalities = {
            'normal': {
                'greeting': 'Hello! How can I help you?',
                'acknowledgment': 'Okay.',
                'completion': 'Task completed.',
                'style': 'default and natural'
            },
            'formal': {
                'greeting': 'Good day, sir. How may I assist you?',
                'acknowledgment': 'Very well, sir.',
                'completion': 'The task has been completed to your specifications.',
                'style': 'respectful and structured'
            },
            'humorous': {
                'greeting': 'Hey there! Ready for some digital magic?',
                'acknowledgment': 'You got it, boss!',
                'completion': 'Mission accomplished! *virtual high-five*',
                'style': 'witty and playful'
            },
            'serious': {
                'greeting': 'Ready for commands.',
                'acknowledgment': 'Understood.',
                'completion': 'Task completed.',
                'style': 'direct and focused'
            },
            'creative': {
                'greeting': 'Hello! Let\'s create something amazing together!',
                'acknowledgment': 'Interesting choice! Let me work my magic.',
                'completion': 'Voilà! Another masterpiece delivered!',
                'style': 'imaginative and inspiring'
            }
        }
    
    def load_config(self):
        """Load personality configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_style = config.get('response_style', 'professional')
                    self.current_personality = config.get('ai_personality', 'formal')
            else:
                self.current_style = 'professional'
                self.current_personality = 'formal'
                self.save_config()
        except:
            self.current_style = 'professional'
            self.current_personality = 'formal'
    
    def save_config(self):
        """Save personality configuration"""
        try:
            config = {
                'response_style': self.current_style,
                'ai_personality': self.current_personality
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def set_response_style(self, style):
        """Set response style"""
        if style.lower() in self.response_styles:
            self.current_style = style.lower()
            self.save_config()
            return f"Response style set to {style}"
        return "Invalid response style"
    
    def set_personality(self, personality):
        """Set AI personality"""
        if personality.lower() in self.personalities:
            self.current_personality = personality.lower()
            self.save_config()
            return f"AI personality set to {personality}"
        return "Invalid personality type"
    
    def transform_response(self, base_response, context='general'):
        """Transform response using Groq AI for personality"""
        if not base_response:
            return "Task completed."
        
        # If normal personality, return original response without transformation
        if self.current_personality == 'normal':
            return base_response
        
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            # Get both style and personality from config
            style_tone = self.response_styles.get(self.current_style, {}).get('tone', 'normal')
            personality_trait = self.personalities.get(self.current_personality, {}).get('style', 'normal')
            
            prompt = f'Transform "{base_response}" using {style_tone} tone with {personality_trait} personality. Max 8 words:'
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=30
            )
            
            transformed = response.choices[0].message.content.strip().strip('"').strip("'")
            
            return transformed if transformed else base_response
            
        except:
            return base_response
    
    def _apply_personality_transform(self, response, personality):
        """Apply personality transformations"""
        if self.current_personality == 'humorous':
            response += ' (with style!)'
        elif self.current_personality == 'creative':
            response = response.replace('increased', 'amplified').replace('opened', 'summoned').replace('completed', 'crafted')
        elif self.current_personality == 'serious':
            response = response.replace('!', '.').replace('...', '.')
        
        return response
    
    def _apply_style_transform(self, response, style, context):
        """Apply style transformations"""
        if self.current_style == 'professional':
            if not response.endswith('.'):
                response += '.'
            response = response.replace('opened', 'has been opened')
        elif self.current_style == 'casual':
            if not response.endswith('!'):
                response = response.rstrip('.') + '!'
        elif self.current_style == 'friendly':
            response = f"Great! {response}"
        elif self.current_style == 'technical':
            response = f"[SUCCESS] {response}"
        
        return response
    
    def get_greeting(self):
        """Get personality-appropriate greeting"""
        personality = self.personalities.get(self.current_personality, self.personalities['formal'])
        return self.transform_response(personality['greeting'])
    
    def get_acknowledgment(self):
        """Get personality-appropriate acknowledgment"""
        personality = self.personalities.get(self.current_personality, self.personalities['formal'])
        return self.transform_response(personality['acknowledgment'])
    
    def get_current_settings(self):
        """Get current personality settings"""
        return {
            'response_style': self.current_style.capitalize(),
            'ai_personality': self.current_personality.capitalize()
        }

# Global instance
personality_manager = PersonalityManager()