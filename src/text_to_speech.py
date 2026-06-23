"""
JARVIS AI Assistant - Text to Speech Module

This module handles text-to-speech functionality with multiple engine support,
voice customization, and advanced speech synthesis features.

Author: JARVIS AI Team
Version: 2.0.0
License: MIT
"""

import pyttsx3
import threading
import time
import json
import logging
import os
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum
from queue import Queue
import pygame

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSEngine(Enum):
    """Supported text-to-speech engines"""
    PYTTSX3 = "pyttsx3"
    GTTS = "gtts"
    AZURE = "azure"
    AMAZON = "amazon"


class VoiceGender(Enum):
    """Voice gender options"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


@dataclass
class VoiceConfig:
    """Configuration for text-to-speech"""
    engine: TTSEngine = TTSEngine.PYTTSX3
    voice_id: Optional[str] = None
    gender: VoiceGender = VoiceGender.MALE
    rate: int = 200  # Words per minute
    volume: float = 0.8  # Volume level (0.0 to 1.0)
    language: str = "en"
    pitch: int = 50  # Pitch level (0-100)


class TextToSpeech:
    """
    Advanced Text-to-Speech processor with multiple engine support
    and voice customization capabilities.
    """
    
    def __init__(self, config: Optional[VoiceConfig] = None):
        """
        Initialize the Text-to-Speech processor.
        
        Args:
            config: Voice configuration
        """
        self.config = config or VoiceConfig()
        self.engine = None
        self.is_speaking = False
        self.speech_queue = Queue()
        self.speech_thread = None
        self.stop_speaking = False
        
        # Initialize TTS engine
        self._initialize_engine()
        
        # Start speech processing thread
        self._start_speech_thread()
        
        logger.info(f"TextToSpeech initialized with engine: {self.config.engine.value}")
    
    def _initialize_engine(self) -> None:
        """Initialize the TTS engine based on configuration"""
        try:
            if self.config.engine == TTSEngine.PYTTSX3:
                self.engine = pyttsx3.init()
                self._configure_pyttsx3()
            else:
                logger.warning(f"Engine {self.config.engine.value} not fully implemented")
                # Fallback to pyttsx3
                self.engine = pyttsx3.init()
                self._configure_pyttsx3()
                
            logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            raise
    
    def _configure_pyttsx3(self) -> None:
        """Configure pyttsx3 engine with current settings"""
        try:
            # Set speech rate
            self.engine.setProperty('rate', self.config.rate)
            
            # Set volume
            self.engine.setProperty('volume', self.config.volume)
            
            # Set voice based on gender preference
            voices = self.engine.getProperty('voices')
            if voices:
                selected_voice = self._select_voice_by_gender(voices)
                if selected_voice:
                    self.engine.setProperty('voice', selected_voice.id)
                    logger.info(f"Voice set to: {selected_voice.name}")
            
        except Exception as e:
            logger.error(f"Failed to configure pyttsx3: {e}")
    
    def _select_voice_by_gender(self, voices) -> Optional[Any]:
        """
        Select voice based on gender preference.
        
        Args:
            voices: Available voices from TTS engine
            
        Returns:
            Selected voice object or None
        """
        try:
            # If specific voice ID is set, use it
            if self.config.voice_id:
                for voice in voices:
                    if voice.id == self.config.voice_id:
                        return voice
            
            # Filter by gender
            gender_keywords = {
                VoiceGender.MALE: ['male', 'man', 'david', 'mark', 'richard'],
                VoiceGender.FEMALE: ['female', 'woman', 'zira', 'hazel', 'susan'],
                VoiceGender.NEUTRAL: []
            }
            
            keywords = gender_keywords.get(self.config.gender, [])
            
            for voice in voices:
                voice_name = voice.name.lower()
                if any(keyword in voice_name for keyword in keywords):
                    return voice
            
            # Fallback to first available voice
            return voices[0] if voices else None
            
        except Exception as e:
            logger.error(f"Voice selection error: {e}")
            return voices[0] if voices else None
    
    def _start_speech_thread(self) -> None:
        """Start the speech processing thread"""
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        logger.info("Speech processing thread started")
    
    def _speech_worker(self) -> None:
        """Worker thread for processing speech queue"""
        while True:
            try:
                if not self.speech_queue.empty():
                    text, priority, callback = self.speech_queue.get()
                    
                    if text is None:  # Shutdown signal
                        break
                    
                    self._speak_text(text, callback)
                    self.speech_queue.task_done()
                else:
                    time.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"Speech worker error: {e}")
    
    def _speak_text(self, text: str, callback: Optional[Callable] = None) -> None:
        """
        Internal method to speak text using the configured engine.
        
        Args:
            text: Text to speak
            callback: Optional callback function to call when done
        """
        try:
            self.is_speaking = True
            self.stop_speaking = False
            
            if self.config.engine == TTSEngine.PYTTSX3:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Implement other engines here
                logger.warning(f"Engine {self.config.engine.value} not implemented")
            
            self.is_speaking = False
            
            if callback:
                callback(True)
                
            logger.info(f"Spoke: {text[:50]}...")
            
        except Exception as e:
            self.is_speaking = False
            logger.error(f"Speech synthesis error: {e}")
            if callback:
                callback(False)
    
    def speak(self, text: str, priority: int = 1, callback: Optional[Callable] = None) -> bool:
        """
        Add text to speech queue.
        
        Args:
            text: Text to speak
            priority: Speech priority (lower = higher priority)
            callback: Optional callback when speech completes
            
        Returns:
            True if added to queue successfully, False otherwise
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for speech")
                return False
            
            # Clean and prepare text
            clean_text = self._clean_text(text.strip())
            
            # Add to queue
            self.speech_queue.put((clean_text, priority, callback))
            logger.info(f"Added to speech queue: {clean_text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add text to speech queue: {e}")
            return False
    
    def speak_immediately(self, text: str, callback: Optional[Callable] = None) -> bool:
        """
        Speak text immediately, interrupting current speech.
        
        Args:
            text: Text to speak
            callback: Optional callback when speech completes
            
        Returns:
            True if spoken successfully, False otherwise
        """
        try:
            # Stop current speech
            self.stop_current_speech()
            
            # Clear queue
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except:
                    break
            
            # Speak immediately
            clean_text = self._clean_text(text.strip())
            self._speak_text(clean_text, callback)
            return True
            
        except Exception as e:
            logger.error(f"Immediate speech error: {e}")
            return False
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and prepare text for speech synthesis.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text ready for speech
        """
        # Remove or replace problematic characters
        replacements = {
            '&': 'and',
            '@': 'at',
            '#': 'hash',
            '$': 'dollar',
            '%': 'percent',
            '*': 'star',
            '+': 'plus',
            '=': 'equals',
            '<': 'less than',
            '>': 'greater than',
            '|': 'pipe',
            '\\': 'backslash',
            '/': 'slash',
            '~': 'tilde',
            '`': 'backtick',
            '^': 'caret'
        }
        
        cleaned = text
        for char, replacement in replacements.items():
            cleaned = cleaned.replace(char, f' {replacement} ')
        
        # Remove multiple spaces
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def stop_current_speech(self) -> bool:
        """
        Stop current speech synthesis.
        
        Returns:
            True if stopped successfully, False otherwise
        """
        try:
            if self.is_speaking:
                self.stop_speaking = True
                if self.engine:
                    self.engine.stop()
                logger.info("Speech stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop speech: {e}")
            return False
    
    def clear_speech_queue(self) -> bool:
        """
        Clear all pending speech from queue.
        
        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except:
                    break
            logger.info("Speech queue cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear speech queue: {e}")
            return False
    
    def set_rate(self, rate: int) -> bool:
        """
        Set speech rate (words per minute).
        
        Args:
            rate: Speech rate (50-400 WPM)
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            rate = max(50, min(400, rate))  # Clamp to reasonable range
            self.config.rate = rate
            
            if self.engine:
                self.engine.setProperty('rate', rate)
            
            logger.info(f"Speech rate set to: {rate} WPM")
            return True
        except Exception as e:
            logger.error(f"Failed to set speech rate: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """
        Set speech volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            volume = max(0.0, min(1.0, volume))  # Clamp to valid range
            self.config.volume = volume
            
            if self.engine:
                self.engine.setProperty('volume', volume)
            
            logger.info(f"Speech volume set to: {volume}")
            return True
        except Exception as e:
            logger.error(f"Failed to set speech volume: {e}")
            return False
    
    def set_voice_gender(self, gender: VoiceGender) -> bool:
        """
        Set voice gender preference.
        
        Args:
            gender: Preferred voice gender
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            self.config.gender = gender
            
            # Reconfigure voice
            if self.engine:
                voices = self.engine.getProperty('voices')
                if voices:
                    selected_voice = self._select_voice_by_gender(voices)
                    if selected_voice:
                        self.engine.setProperty('voice', selected_voice.id)
            
            logger.info(f"Voice gender set to: {gender.value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set voice gender: {e}")
            return False
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of available voices.
        
        Returns:
            List of voice information dictionaries
        """
        voices_info = []
        try:
            if self.engine:
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    voice_info = {
                        'id': voice.id,
                        'name': voice.name,
                        'languages': getattr(voice, 'languages', []),
                        'gender': self._detect_voice_gender(voice.name)
                    }
                    voices_info.append(voice_info)
            
            logger.info(f"Found {len(voices_info)} available voices")
        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
        
        return voices_info
    
    def _detect_voice_gender(self, voice_name: str) -> str:
        """
        Detect voice gender from name.
        
        Args:
            voice_name: Name of the voice
            
        Returns:
            Detected gender ('male', 'female', or 'unknown')
        """
        name_lower = voice_name.lower()
        
        male_indicators = ['male', 'man', 'david', 'mark', 'richard', 'james', 'george']
        female_indicators = ['female', 'woman', 'zira', 'hazel', 'susan', 'helen', 'linda']
        
        if any(indicator in name_lower for indicator in male_indicators):
            return 'male'
        elif any(indicator in name_lower for indicator in female_indicators):
            return 'female'
        else:
            return 'unknown'
    
    def set_voice_by_id(self, voice_id: str) -> bool:
        """
        Set voice by specific ID.
        
        Args:
            voice_id: Voice ID to use
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            if self.engine:
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if voice.id == voice_id:
                        self.engine.setProperty('voice', voice_id)
                        self.config.voice_id = voice_id
                        logger.info(f"Voice set to: {voice.name}")
                        return True
                
                logger.warning(f"Voice ID not found: {voice_id}")
                return False
            
        except Exception as e:
            logger.error(f"Failed to set voice by ID: {e}")
            return False
    
    def test_speech(self, test_text: str = "Hello, this is a test of the speech synthesis system.") -> bool:
        """
        Test speech synthesis with sample text.
        
        Args:
            test_text: Text to use for testing
            
        Returns:
            True if test successful, False otherwise
        """
        try:
            logger.info("Testing speech synthesis...")
            self.speak_immediately(test_text)
            return True
        except Exception as e:
            logger.error(f"Speech test failed: {e}")
            return False
    
    def save_config(self, filepath: str) -> bool:
        """
        Save current configuration to file.
        
        Args:
            filepath: Path to save configuration
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            config_dict = {
                "engine": self.config.engine.value,
                "voice_id": self.config.voice_id,
                "gender": self.config.gender.value,
                "rate": self.config.rate,
                "volume": self.config.volume,
                "language": self.config.language,
                "pitch": self.config.pitch
            }
            
            with open(filepath, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            logger.info(f"Configuration saved to: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def load_config(self, filepath: str) -> bool:
        """
        Load configuration from file.
        
        Args:
            filepath: Path to load configuration from
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(filepath, 'r') as f:
                config_dict = json.load(f)
            
            self.config = VoiceConfig(
                engine=TTSEngine(config_dict.get("engine", "pyttsx3")),
                voice_id=config_dict.get("voice_id"),
                gender=VoiceGender(config_dict.get("gender", "male")),
                rate=config_dict.get("rate", 200),
                volume=config_dict.get("volume", 0.8),
                language=config_dict.get("language", "en"),
                pitch=config_dict.get("pitch", 50)
            )
            
            # Reconfigure engine
            self._configure_pyttsx3()
            
            logger.info(f"Configuration loaded from: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            # Signal speech thread to stop
            self.speech_queue.put((None, 0, None))
            
            # Stop current speech
            self.stop_current_speech()
            
            # Wait for thread to finish
            if self.speech_thread and self.speech_thread.is_alive():
                self.speech_thread.join(timeout=2)
                
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize text-to-speech processor
    tts = TextToSpeech()
    
    # Test basic speech
    print("Testing basic speech...")
    tts.speak("Hello, this is JARVIS AI Assistant. Testing text to speech functionality.")
    
    # Wait for speech to complete
    time.sleep(3)
    
    # Test voice configuration
    print("Testing voice configuration...")
    voices = tts.get_available_voices()
    print(f"Available voices: {len(voices)}")
    for voice in voices[:3]:  # Show first 3 voices
        print(f"  - {voice['name']} ({voice['gender']})")
    
    # Test different settings
    print("Testing different speech rates...")
    tts.set_rate(150)
    tts.speak("This is slower speech.")
    time.sleep(2)
    
    tts.set_rate(250)
    tts.speak("This is faster speech.")
    time.sleep(2)
    
    # Test volume control
    print("Testing volume control...")
    tts.set_volume(0.5)
    tts.speak("This is quieter speech.")
    time.sleep(2)
    
    tts.set_volume(1.0)
    tts.speak("This is louder speech.")
    time.sleep(2)
    
    # Test gender switching
    print("Testing gender switching...")
    tts.set_voice_gender(VoiceGender.FEMALE)
    tts.speak("This should be a female voice.")
    time.sleep(3)
    
    tts.set_voice_gender(VoiceGender.MALE)
    tts.speak("This should be a male voice.")
    time.sleep(3)
    
    print("Text-to-speech test completed")