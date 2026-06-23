# Universal Dynamic Multilingual Support for All DualAI Features
import pyttsx3
import datetime
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class MultilingualJarvis:
    def __init__(self):
        # Load saved language or default to English
        try:
            if os.path.exists('current_language.txt'):
                with open('current_language.txt', 'r') as f:
                    self.current_language = f.read().strip()
            else:
                self.current_language = 'english'
        except:
            self.current_language = 'english'
        
        # Language configurations
        self.supported_languages = {
            'english': {'code': 'en', 'tts_code': 'en', 'recognition': 'en-IN'},
            'hindi': {'code': 'hi', 'tts_code': 'hi', 'recognition': 'hi-IN'},
            'kannada': {'code': 'kn', 'tts_code': 'kn', 'recognition': 'kn-IN'},
            'bengali': {'code': 'bn', 'tts_code': 'bn', 'recognition': 'bn-IN'},
            'gujarati': {'code': 'gu', 'tts_code': 'gu', 'recognition': 'gu-IN'},
            'malayalam': {'code': 'ml', 'tts_code': 'ml', 'recognition': 'ml-IN'},
            'marathi': {'code': 'mr', 'tts_code': 'mr', 'recognition': 'mr-IN'},
            'tamil': {'code': 'ta', 'tts_code': 'ta', 'recognition': 'ta-IN'},
            'telugu': {'code': 'te', 'tts_code': 'te', 'recognition': 'te-IN'},
            'urdu': {'code': 'ur', 'tts_code': 'ur', 'recognition': 'ur-IN'},
            'punjabi': {'code': 'pa', 'tts_code': 'pa', 'recognition': 'pa-IN'},
            'assamese': {'code': 'as', 'tts_code': 'as', 'recognition': 'as-IN'},
            'odia': {'code': 'or', 'tts_code': 'or', 'recognition': 'or-IN'},
            'spanish': {'code': 'es', 'tts_code': 'es', 'recognition': 'es-ES'},
            'french': {'code': 'fr', 'tts_code': 'fr', 'recognition': 'fr-FR'},
            'german': {'code': 'de', 'tts_code': 'de', 'recognition': 'de-DE'},
            'italian': {'code': 'it', 'tts_code': 'it', 'recognition': 'it-IT'},
            'portuguese': {'code': 'pt', 'tts_code': 'pt', 'recognition': 'pt-PT'},
            'russian': {'code': 'ru', 'tts_code': 'ru', 'recognition': 'ru-RU'},
            'dutch': {'code': 'nl', 'tts_code': 'nl', 'recognition': 'nl-NL'},
            'swedish': {'code': 'sv', 'tts_code': 'sv', 'recognition': 'sv-SE'},
            'norwegian': {'code': 'no', 'tts_code': 'no', 'recognition': 'no-NO'},
            'danish': {'code': 'da', 'tts_code': 'da', 'recognition': 'da-DK'},
            'polish': {'code': 'pl', 'tts_code': 'pl', 'recognition': 'pl-PL'},
            'czech': {'code': 'cs', 'tts_code': 'cs', 'recognition': 'cs-CZ'},
            'hungarian': {'code': 'hu', 'tts_code': 'hu', 'recognition': 'hu-HU'},
            'romanian': {'code': 'ro', 'tts_code': 'ro', 'recognition': 'ro-RO'},
            'greek': {'code': 'el', 'tts_code': 'el', 'recognition': 'el-GR'},
            'norwegian': {'code': 'no', 'tts_code': 'no', 'recognition': 'no-NO'},
            'danish': {'code': 'da', 'tts_code': 'da', 'recognition': 'da-DK'}
        }
        
        # Dynamic translation cache
        self.translation_cache = {}
        
        # Common responses
        self.responses = {
            'english': {
                'not_understood': "I didn't understand that",
                'processing': "I'm processing your request",
                'error': 'Something went wrong'
            },
            'kannada': {
                'not_understood': 'ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ',
                'processing': 'ನಾನು ನಿಮ್ಮ ಅನುರೋಧವನ್ನು ಪ್ರಕ್ರಿಯೆ ಮಾಡುತ್ತಿದ್ದೇನೆ',
                'error': 'ಏನೋ ತಪ್ಪಾಗಿದೆ'
            },
            'hindi': {
                'not_understood': 'मैं समझ नहीं पाया',
                'processing': 'मैं आपके अनुरोध पर काम कर रहा हूँ',
                'error': 'कुछ गलत हो गया'
            }
        }
    
    def get_response(self, key):
        """Get response in current language"""
        return self.responses.get(self.current_language, {}).get(key, self.responses['english'][key])
    
    def process_multilingual_command(self, query):
        """Process any command in any language"""
        # Auto-detect language and set it
        detected_lang = self.detect_language(query)
        if detected_lang != 'english':
            self.current_language = detected_lang
        
        return self.process_command_in_language(query, self.current_language)
    
    def process_command_in_language(self, command, language):
        """Process command in specified language"""
        try:
            # Import DualAI to access all functions
            from engine.dual_ai import DualAI
            dual_ai = DualAI()
            
            # Try to match with any function dynamically
            for function_name, function_action in dual_ai.functions.items():
                if self._matches_function(command.lower(), function_name):
                    # Safety check: Skip dangerous commands
                    if function_name in ['shutdown', 'restart', 'hibernate']:
                        print(f"Skipping dangerous command: {function_name}")
                        return f"Dangerous command {function_name} blocked for safety"
                    
                    try:
                        result = function_action()
                        
                        # Always return actual result if it exists and is meaningful
                        if result and str(result).strip() and str(result) != 'None':
                            return str(result)
                        
                        # For functions without meaningful return, give success message
                        response = f"{function_name.replace('_', ' ').title()} executed"
                        return self._get_native_response(response)
                    except Exception as e:
                        return self.get_response('error')
            
            return self.get_response('not_understood')
            
        except Exception as e:
            print(f"Command processing error: {e}")
            return self.get_response('error')
    
    def _matches_function(self, command, function_name):
        """Dynamic universal function matching for all languages"""
        # Get semantic meaning of command
        english_intent = self._get_semantic_intent(command.lower())
        
        # Dynamic semantic matching
        return self._semantic_match(english_intent, function_name)
    
    def _get_semantic_intent(self, command):
        """Extract semantic intent from any language command"""
        # Check cache first
        if command in self.translation_cache:
            return self.translation_cache[command]
        
        # Dynamic intent extraction using AI-like pattern matching
        intent = self._extract_intent_dynamically(command)
        
        # Cache the result
        self.translation_cache[command] = intent
        return intent
    
    def _extract_intent_dynamically(self, command):
        """Extract intent without predefined mappings"""
        try:
            # Use Google Translate for dynamic translation
            from googletrans import Translator
            translator = Translator()
            
            # Translate to English
            result = translator.translate(command, dest='en')
            return result.text.lower()
        except Exception as e:
            # Fallback: Use phonetic and character analysis
            return self._phonetic_intent_extraction(command)
    
    def _phonetic_intent_extraction(self, command):
        """Pure fallback - return original command for fuzzy matching"""
        return command
    
    def _semantic_match(self, intent, function_name):
        """Precise semantic matching to prevent incorrect matches"""
        # Direct exact matching
        if function_name == intent or function_name.replace('_', ' ') == intent:
            return True
        
        # Check if function name is in intent
        if function_name in intent:
            return True
        
        # Special handling for volume commands
        if 'volume' in intent or 'sound' in intent or 'audio' in intent:
            if ('up' in intent or 'increase' in intent or 'raise' in intent) and function_name == 'volume_up':
                return True
            elif ('down' in intent or 'decrease' in intent or 'lower' in intent) and function_name == 'volume_down':
                return True
            elif ('mute' in intent or 'silent' in intent) and function_name == 'mute':
                return True
        
        # Prevent dangerous command false matches
        dangerous_commands = ['shutdown', 'restart', 'hibernate']
        if function_name in dangerous_commands:
            # Only match if intent explicitly contains the dangerous word
            return function_name in intent.lower()
        
        # Safe fuzzy matching for non-dangerous commands
        intent_words = intent.split()
        function_words = function_name.replace('_', ' ').split()
        
        # Require exact word matches for safety
        for intent_word in intent_words:
            for func_word in function_words:
                if intent_word == func_word:
                    return True
        
        return False
    
    def _get_native_response(self, english_response):
        """Get response in native language using dynamic translation"""
        if self.current_language == 'english':
            return english_response
        
        try:
            from googletrans import Translator
            translator = Translator()
            
            # Get target language code
            target_lang = self.supported_languages.get(self.current_language, {}).get('code', 'en')
            
            # Translate response to native language
            result = translator.translate(english_response, dest=target_lang)
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return english_response
    
    def detect_language(self, text):
        """Auto-detect language from text"""
        if any(0x0C80 <= ord(char) <= 0x0CFF for char in text):
            return 'kannada'
        elif any(0x0900 <= ord(char) <= 0x097F for char in text):
            return 'hindi'
        elif any(0x0980 <= ord(char) <= 0x09FF for char in text):
            return 'bengali'
        elif any(0x0A80 <= ord(char) <= 0x0AFF for char in text):
            return 'gujarati'
        elif any(0x0D00 <= ord(char) <= 0x0D7F for char in text):
            return 'malayalam'
        elif any(0x0900 <= ord(char) <= 0x097F for char in text):
            return 'marathi'
        elif any(0x0B80 <= ord(char) <= 0x0BFF for char in text):
            return 'tamil'
        elif any(0x0C00 <= ord(char) <= 0x0C7F for char in text):
            return 'telugu'
        elif any(0x0600 <= ord(char) <= 0x06FF for char in text):
            return 'urdu'
        elif any(0x0370 <= ord(char) <= 0x03FF for char in text):
            return 'greek'
        elif any(0x0400 <= ord(char) <= 0x04FF for char in text):
            return 'russian'
        return 'english'
    
    def get_speech_recognition_language(self):
        """Get language code for speech recognition"""
        return self.supported_languages.get(self.current_language, {}).get('recognition', 'en-IN')
    
    def get_tts_language(self):
        """Get language code for text-to-speech"""
        return self.supported_languages.get(self.current_language, {}).get('tts_code', 'en')
    
    def set_language(self, language):
        """Set the current language"""
        if language in self.supported_languages:
            self.current_language = language
            # Save to file
            try:
                with open('current_language.txt', 'w') as f:
                    f.write(language)
                return True
            except:
                return False
        return False
    
    def speak_multilingual(self, text, language=None):
        """Return text for main system to handle TTS"""
        # Don't speak here - let main system handle TTS
        return text

# Create global instance for backward compatibility
multilingual = MultilingualJarvis()