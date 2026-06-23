"""
JARVIS AI Assistant - Speech to Text Module

This module handles speech recognition functionality with multiple engine support,
noise filtering, and adaptive recognition settings.

Author: JARVIS AI Team
Version: 2.0.0
License: MIT
"""

import speech_recognition as sr
import pyaudio
import threading
import time
import json
import logging
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecognitionEngine(Enum):
    """Supported speech recognition engines"""
    GOOGLE = "google"
    SPHINX = "sphinx"
    WHISPER = "whisper"
    AZURE = "azure"


@dataclass
class SpeechConfig:
    """Configuration for speech recognition"""
    engine: RecognitionEngine = RecognitionEngine.GOOGLE
    language: str = "en-US"
    timeout: float = 5.0
    phrase_timeout: float = 1.0
    energy_threshold: int = 4000
    dynamic_energy_threshold: bool = True
    pause_threshold: float = 0.8
    non_speaking_duration: float = 0.5


class SpeechToText:
    """
    Advanced Speech-to-Text processor with multiple engine support
    and adaptive recognition capabilities.
    """
    
    def __init__(self, config: Optional[SpeechConfig] = None):
        """
        Initialize the Speech-to-Text processor.
        
        Args:
            config: Speech recognition configuration
        """
        self.config = config or SpeechConfig()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.background_listener = None
        self.callbacks: Dict[str, Callable] = {}
        
        # Configure recognizer settings
        self._configure_recognizer()
        
        # Calibrate microphone
        self._calibrate_microphone()
        
        logger.info(f"SpeechToText initialized with engine: {self.config.engine.value}")
    
    def _configure_recognizer(self) -> None:
        """Configure the speech recognizer with optimal settings"""
        self.recognizer.energy_threshold = self.config.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.config.dynamic_energy_threshold
        self.recognizer.pause_threshold = self.config.pause_threshold
        self.recognizer.non_speaking_duration = self.config.non_speaking_duration
        
        logger.info("Speech recognizer configured successfully")
    
    def _calibrate_microphone(self) -> None:
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info(f"Microphone calibrated. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            logger.error(f"Microphone calibration failed: {e}")
    
    def listen_once(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Listen for a single speech input and return the recognized text.
        
        Args:
            timeout: Maximum time to wait for speech input
            
        Returns:
            Recognized text or None if recognition failed
        """
        timeout = timeout or self.config.timeout
        
        try:
            with self.microphone as source:
                logger.info("Listening for speech...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=self.config.phrase_timeout
                )
                
            # Recognize speech using configured engine
            text = self._recognize_audio(audio)
            
            if text:
                logger.info(f"Recognized: {text}")
                return text.strip()
            else:
                logger.warning("No speech recognized")
                return None
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during speech recognition: {e}")
            return None
    
    def _recognize_audio(self, audio: sr.AudioData) -> Optional[str]:
        """
        Recognize audio using the configured engine.
        
        Args:
            audio: Audio data to recognize
            
        Returns:
            Recognized text or None
        """
        try:
            if self.config.engine == RecognitionEngine.GOOGLE:
                return self.recognizer.recognize_google(audio, language=self.config.language)
            elif self.config.engine == RecognitionEngine.SPHINX:
                return self.recognizer.recognize_sphinx(audio)
            elif self.config.engine == RecognitionEngine.WHISPER:
                return self.recognizer.recognize_whisper(audio, language=self.config.language)
            else:
                logger.error(f"Unsupported recognition engine: {self.config.engine}")
                return None
                
        except Exception as e:
            logger.error(f"Recognition error with {self.config.engine.value}: {e}")
            return None
    
    def start_continuous_listening(self, callback: Callable[[str], None]) -> bool:
        """
        Start continuous speech recognition in background.
        
        Args:
            callback: Function to call with recognized text
            
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_listening:
            logger.warning("Continuous listening already active")
            return False
        
        try:
            def recognition_callback(recognizer, audio):
                """Background recognition callback"""
                try:
                    text = self._recognize_audio(audio)
                    if text:
                        callback(text.strip())
                except Exception as e:
                    logger.error(f"Background recognition error: {e}")
            
            # Start background listening
            self.background_listener = self.recognizer.listen_in_background(
                self.microphone, 
                recognition_callback,
                phrase_time_limit=self.config.phrase_timeout
            )
            
            self.is_listening = True
            logger.info("Continuous listening started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start continuous listening: {e}")
            return False
    
    def stop_continuous_listening(self) -> bool:
        """
        Stop continuous speech recognition.
        
        Returns:
            True if stopped successfully, False otherwise
        """
        if not self.is_listening:
            logger.warning("Continuous listening not active")
            return False
        
        try:
            if self.background_listener:
                self.background_listener(wait_for_stop=False)
                self.background_listener = None
            
            self.is_listening = False
            logger.info("Continuous listening stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop continuous listening: {e}")
            return False
    
    def set_language(self, language: str) -> bool:
        """
        Set the recognition language.
        
        Args:
            language: Language code (e.g., 'en-US', 'es-ES')
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            self.config.language = language
            logger.info(f"Language set to: {language}")
            return True
        except Exception as e:
            logger.error(f"Failed to set language: {e}")
            return False
    
    def set_engine(self, engine: RecognitionEngine) -> bool:
        """
        Set the recognition engine.
        
        Args:
            engine: Recognition engine to use
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            self.config.engine = engine
            logger.info(f"Recognition engine set to: {engine.value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set engine: {e}")
            return False
    
    def get_available_microphones(self) -> Dict[int, str]:
        """
        Get list of available microphones.
        
        Returns:
            Dictionary mapping microphone index to name
        """
        microphones = {}
        try:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                microphones[index] = name
            logger.info(f"Found {len(microphones)} microphones")
        except Exception as e:
            logger.error(f"Failed to get microphones: {e}")
        
        return microphones
    
    def set_microphone(self, device_index: int) -> bool:
        """
        Set the microphone device.
        
        Args:
            device_index: Index of the microphone device
            
        Returns:
            True if set successfully, False otherwise
        """
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            self._calibrate_microphone()
            logger.info(f"Microphone set to device index: {device_index}")
            return True
        except Exception as e:
            logger.error(f"Failed to set microphone: {e}")
            return False
    
    def test_microphone(self) -> Dict[str, Any]:
        """
        Test microphone functionality and return diagnostics.
        
        Returns:
            Dictionary with test results and diagnostics
        """
        results = {
            "microphone_working": False,
            "energy_level": 0,
            "test_recognition": False,
            "error_message": None
        }
        
        try:
            with self.microphone as source:
                # Test microphone access
                results["microphone_working"] = True
                
                # Measure ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                results["energy_level"] = self.recognizer.energy_threshold
                
                # Test recognition
                logger.info("Say something to test recognition...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                text = self._recognize_audio(audio)
                
                if text:
                    results["test_recognition"] = True
                    results["recognized_text"] = text
                
        except Exception as e:
            results["error_message"] = str(e)
            logger.error(f"Microphone test failed: {e}")
        
        return results
    
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
                "language": self.config.language,
                "timeout": self.config.timeout,
                "phrase_timeout": self.config.phrase_timeout,
                "energy_threshold": self.config.energy_threshold,
                "dynamic_energy_threshold": self.config.dynamic_energy_threshold,
                "pause_threshold": self.config.pause_threshold,
                "non_speaking_duration": self.config.non_speaking_duration
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
            
            self.config = SpeechConfig(
                engine=RecognitionEngine(config_dict.get("engine", "google")),
                language=config_dict.get("language", "en-US"),
                timeout=config_dict.get("timeout", 5.0),
                phrase_timeout=config_dict.get("phrase_timeout", 1.0),
                energy_threshold=config_dict.get("energy_threshold", 4000),
                dynamic_energy_threshold=config_dict.get("dynamic_energy_threshold", True),
                pause_threshold=config_dict.get("pause_threshold", 0.8),
                non_speaking_duration=config_dict.get("non_speaking_duration", 0.5)
            )
            
            self._configure_recognizer()
            logger.info(f"Configuration loaded from: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if self.is_listening:
            self.stop_continuous_listening()


# Example usage and testing
if __name__ == "__main__":
    # Initialize speech-to-text processor
    stt = SpeechToText()
    
    # Test microphone
    print("Testing microphone...")
    test_results = stt.test_microphone()
    print(f"Test results: {test_results}")
    
    # Single recognition test
    print("\nSingle recognition test:")
    text = stt.listen_once(timeout=5)
    if text:
        print(f"You said: {text}")
    else:
        print("No speech recognized")
    
    # Continuous listening test
    print("\nStarting continuous listening (say 'stop' to end)...")
    
    def handle_speech(text):
        print(f"Heard: {text}")
        if "stop" in text.lower():
            stt.stop_continuous_listening()
    
    stt.start_continuous_listening(handle_speech)
    
    # Keep running until stopped
    while stt.is_listening:
        time.sleep(0.1)
    
    print("Speech recognition test completed")