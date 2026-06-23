import pyttsx3
import json
import os
import re
import threading

class VoiceGenderControl:
    def __init__(self):
        self.config_file = "config/voice_config.json"
        self.current_gender = "male"
        self._engine = None
        self._engine_lock = threading.Lock()
        self.load_config()
        
    def load_config(self):
        """Load voice configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_gender = config.get('gender', 'male')
        except:
            self.current_gender = "male"
    
    def save_config(self):
        """Save voice configuration to file"""
        try:
            config = {'gender': self.current_gender}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def get_available_voices(self):
        """Get available system voices"""
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.stop()
            return voices
        except:
            return []
    
    def get_voice_by_gender(self, gender="male"):
        """Get voice ID by gender preference"""
        voices = self.get_available_voices()
        if not voices:
            return None
            
        male_voices = []
        female_voices = []
        
        for voice in voices:
            voice_name = voice.name.lower()
            # Common patterns for identifying voice gender
            if any(keyword in voice_name for keyword in ['david', 'mark', 'richard', 'male', 'man']):
                male_voices.append(voice.id)
            elif any(keyword in voice_name for keyword in ['zira', 'hazel', 'susan', 'female', 'woman']):
                female_voices.append(voice.id)
            else:
                # Default classification by index (usually 0=male, 1=female)
                if voices.index(voice) % 2 == 0:
                    male_voices.append(voice.id)
                else:
                    female_voices.append(voice.id)
        
        if gender == "female" and female_voices:
            return female_voices[0]
        elif gender == "male" and male_voices:
            return male_voices[0]
        else:
            # Fallback to first available voice
            return voices[0].id if voices else None
    
    def switch_to_male(self):
        """Switch to male voice"""
        self.current_gender = "male"
        self.save_config()
        return "Voice switched to male"
    
    def switch_to_female(self):
        """Switch to female voice"""
        self.current_gender = "female"
        self.save_config()
        return "Voice switched to female"
    
    def get_current_gender(self):
        """Get current voice gender"""
        return self.current_gender
    
    def stop_speaking(self):
        """Best-effort stop for active pyttsx3 speech."""
        try:
            with self._engine_lock:
                if self._engine is not None:
                    self._engine.stop()
        except Exception:
            pass

    def _split_speech_chunks(self, text):
        parts = re.split(r'(?<=[.!?。！？])\s+', str(text or '').strip())
        chunks = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if len(part) <= 220:
                chunks.append(part)
                continue
            words = part.split()
            buf = []
            for word in words:
                if sum(len(x) + 1 for x in buf) + len(word) > 180:
                    chunks.append(' '.join(buf))
                    buf = [word]
                else:
                    buf.append(word)
            if buf:
                chunks.append(' '.join(buf))
        return chunks or [str(text or '')]

    def speak_with_gender(self, text, gender=None):
        """Speak text with specified gender voice.

        The text is spoken in short chunks so the UI Cancel/Interrupt button can
        stop long answers between chunks. pyttsx3 itself is synchronous, so this
        is the most reliable cooperative interrupt approach without rewriting the
        whole TTS stack.
        """
        if gender is None:
            gender = self.current_gender

        try:
            from core.utils.interrupt import is_interrupted
        except Exception:
            def is_interrupted():
                return False

        try:
            with self._engine_lock:
                engine = pyttsx3.init('sapi5')
                self._engine = engine

            voice_id = self.get_voice_by_gender(gender)
            if voice_id:
                engine.setProperty('voice', voice_id)

            # Get voice settings from UI config
            try:
                import json
                with open('config/ui_config.json', 'r') as f:
                    ui_config = json.load(f)

                speed_settings = {'slow': 120, 'normal': 174, 'fast': 220}
                voice_speed = ui_config.get('voice_speed', 'normal')
                rate = speed_settings.get(voice_speed, 174)
                engine.setProperty('rate', rate)

                volume_settings = {'low': 0.5, 'medium': 0.9, 'high': 1.0}
                voice_volume = ui_config.get('voice_volume', 'medium')
                volume = volume_settings.get(voice_volume, 0.9)
                engine.setProperty('volume', volume)
            except Exception:
                engine.setProperty('rate', 174)
                engine.setProperty('volume', 0.9)

            for chunk in self._split_speech_chunks(text):
                if is_interrupted():
                    engine.stop()
                    return False
                engine.say(chunk)
                engine.runAndWait()

            engine.stop()
            return not is_interrupted()
        except Exception as e:
            print(f"Voice error: {e}")
            return False
        finally:
            try:
                with self._engine_lock:
                    if self._engine is not None:
                        self._engine.stop()
                    self._engine = None
            except Exception:
                pass

# Global instance
voice_control = VoiceGenderControl()