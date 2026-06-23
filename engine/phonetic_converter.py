# Simple Phonetic Conversion for Natural TTS
class PhoneticConverter:
    def __init__(self):
        # Direct word translations for common phrases
        self.translations = {
            'kannada': {
                'ಕ್ಯಾಲ್ಕುಲೇಟರ್': 'calculator',
                'ತೆರೆ': 'open',
                'ತೆರೆಯಲಾಗಿದೆ': 'opened',
                'ಧ್ವನಿ': 'volume',
                'ಹೆಚ್ಚಿಸು': 'increase',
                'ಹೆಚ್ಚಿಸಲಾಗಿದೆ': 'increased',
                'ಕಡಿಮೆ': 'decrease',
                'ಸ್ಕ್ರೀನ್ಶಾಟ್': 'screenshot',
                'ತೆಗೆ': 'take',
                'ಉಳಿಸಲಾಗಿದೆ': 'saved',
                'ನೋಟ್ಪ್ಯಾಡ್': 'notepad',
                'ಕ್ರೋಮ್': 'chrome'
            },
            'hindi': {
                'कैलकुलेटर': 'calculator',
                'खोलो': 'open',
                'खुला': 'opened',
                'आवाज़': 'volume',
                'बढ़ाओ': 'increase',
                'बढ़ाई': 'increased',
                'कम': 'decrease',
                'स्क्रीनशॉट': 'screenshot',
                'लो': 'take',
                'सेव': 'saved',
                'नोटपैड': 'notepad',
                'क्रोम': 'chrome'
            }
        }
    
    def convert_to_phonetic(self, text, language):
        if language not in self.translations:
            return text
        
        result = text
        for native_word, english_word in self.translations[language].items():
            result = result.replace(native_word, english_word)
        
        # Clean up extra spaces
        result = ' '.join(result.split())
        return result

# Global instance
phonetic_converter = PhoneticConverter()