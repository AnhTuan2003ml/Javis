import pyttsx3
import speech_recognition as sr
import eel
import time
import threading
import json
import numpy as np
from datetime import datetime, timedelta
import random
import os
import subprocess
import schedule
from engine.command_history import command_history

# Emotion Detection System
class EmotionSystem:
    def __init__(self):
        self.current_emotion = 'neutral'
        self.enabled = False
        self.emotion_history = []
        self.monitoring = False
        self.monitor_thread = None
        self.emotion_file = 'emotion_config.json'
        self.load_emotion_data()
        
        # Emotion response templates
        self.responses = {
            'happy': {
                'greetings': ["Great to see you in such a good mood!", "You sound wonderful today!"],
                'acknowledgments': ["Absolutely! Let's keep this positive momentum!", "Perfect! I'm excited to help!"],
                'completions': ["Done! Hope that keeps your day bright!", "All set! Keep that smile going!"]
            },
            'sad': {
                'greetings': ["I'm here for you. How can I help?", "Let me help make things easier."],
                'acknowledgments': ["I understand. Let me take care of that.", "Of course. I'll handle this gently."],
                'completions': ["All done. I hope this helps a little.", "Completed. Take care of yourself."]
            },
            'stressed': {
                'greetings': ["I can sense you're under pressure. Let me help.", "Take a deep breath. I'll handle this."],
                'acknowledgments': ["Got it. I'll take care of this quickly.", "I'll make this as smooth as possible."],
                'completions': ["Done efficiently. One less thing on your plate!", "Completed quickly. Hope that helps."]
            },
            'angry': {
                'greetings': ["I understand you're frustrated. Let me help.", "I'm here to help make things right."],
                'acknowledgments': ["I understand your frustration. I'll handle this carefully.", "Got it. Let me fix this properly."],
                'completions': ["Completed. I hope this helps resolve the issue.", "Done correctly. Let me know if you need more help."]
            },
            'excited': {
                'greetings': ["I love your enthusiasm! What are we doing today?", "Your energy is incredible!"],
                'acknowledgments': ["Yes! I'm as excited as you are!", "Absolutely! This is going to be fantastic!"],
                'completions': ["Done! That was as exciting as I hoped!", "Completed with enthusiasm! What's next?"]
            },
            'neutral': {
                'greetings': ["Hello! How can I help you today?", "Hi there! I'm ready to help."],
                'acknowledgments': ["Understood. I'll take care of that.", "Got it. Working on it now."],
                'completions': ["Task completed successfully.", "All done! Anything else?"]
            }
        }
    
    def detect_emotion_from_text(self, text):
        """AI-powered emotion detection using Groq"""
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'Analyze emotion in: "{text}". Return only one word: happy, sad, stressed, angry, excited, or neutral.'
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=10
            )
            
            emotion = response.choices[0].message.content.strip().lower()
            
            # Validate emotion
            valid_emotions = ['happy', 'sad', 'stressed', 'angry', 'excited', 'neutral']
            return emotion if emotion in valid_emotions else 'neutral'
            
        except Exception as e:
            print(f"Groq emotion detection error: {e}")
            # Fallback to keyword detection
            text = text.lower()
            if any(word in text for word in ['great', 'awesome', 'fantastic', 'love', 'happy']):
                return 'happy'
            elif any(word in text for word in ['sad', 'down', 'upset', 'cry']):
                return 'sad'
            elif any(word in text for word in ['stress', 'busy', 'overwhelmed', 'pressure']):
                return 'stressed'
            elif any(word in text for word in ['angry', 'mad', 'frustrated']):
                return 'angry'
            elif any(word in text for word in ['amazing', 'incredible', 'wow', 'excited']):
                return 'excited'
            else:
                return 'neutral'
    
    def load_emotion_data(self):
        """Load emotion data from file"""
        try:
            if os.path.exists(self.emotion_file):
                with open(self.emotion_file, 'r') as f:
                    data = json.load(f)
                    self.current_emotion = data.get('last_emotion', 'neutral')
                    self.emotion_history = data.get('emotion_history', [])
                    self.enabled = data.get('enabled', False)
                pass  # Silent loading
        except Exception as e:
            print(f"Error loading emotion data: {e}")
    
    def save_emotion_data(self):
        """Save emotion data to file"""
        try:
            data = {
                'enabled': self.enabled,
                'sensitivity': 0.7,
                'last_emotion': self.current_emotion,
                'timestamp': datetime.now().isoformat(),
                'emotion_history': self.emotion_history
            }
            with open(self.emotion_file, 'w') as f:
                json.dump(data, f)
            pass  # Silent saving
        except Exception as e:
            print(f"Error saving emotion data: {e}")
    
    def update_emotion(self, emotion):
        """Update current emotion"""
        self.current_emotion = emotion
        self.emotion_history.append({
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.emotion_history) > 10:
            self.emotion_history = self.emotion_history[-10:]
        self.save_emotion_data()
    
    def get_adaptive_response(self, base_text, emotion="neutral"):
        """Fully rephrase sentence with same meaning and emotional tone"""
        if not self.enabled:
            return base_text
        
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'''Rephrase this message for someone feeling {self.current_emotion}: "{base_text}"

Rules:
- Keep EXACT same meaning and information
- Change wording to match {self.current_emotion} tone
- Return ONLY the rephrased sentence
- No explanations or alternatives
- Keep similar length

Examples:
Original: "File uploaded successfully"
Happy: "Your file has been successfully uploaded! 🎉"
Sad: "I've managed to upload your file for you"

Rephrase: "{base_text}"'''
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=100,
                temperature=0.8
            )
            
            adapted_text = response.choices[0].message.content.strip()
            
            # Extract only the first sentence, remove any explanations
            if adapted_text:
                # Split by common separators and take first part
                first_sentence = adapted_text.split('\n')[0].split('.')[0]
                if '"' in first_sentence:
                    # Extract text between quotes if present
                    import re
                    quoted = re.findall(r'"([^"]+)"', first_sentence)
                    if quoted:
                        return quoted[0]
                return first_sentence if first_sentence else base_text
            return base_text
            
        except Exception as e:
            print(f"Groq rephrasing error: {e}")
            return base_text
    
    def get_encouraging_response(self):
        """Get AI-powered encouraging message"""
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'''Generate a warm, encouraging message for someone feeling {self.current_emotion}.
            
Make it:
            - Personal and caring
            - Natural and conversational
            - Specifically tailored to {self.current_emotion} emotion
            - 10-20 words maximum
            - Avoid clichés, be genuine and supportive'''
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=60
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Groq encouragement error: {e}")
            return "I'm here for you."  # Simple fallback
    
    def get_humor_response(self):
        """Get AI-powered appropriate humor"""
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'''Tell a gentle, appropriate joke for someone feeling {self.current_emotion}.
            
Make it:
            - Light and uplifting
            - Appropriate for their {self.current_emotion} mood
            - Clean and family-friendly
            - Under 25 words
            - Genuinely funny but sensitive to their emotional state'''
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=80
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Groq humor error: {e}")
            return "Here's a smile for you! 😊"  # Simple fallback
    
    def start_real_time_monitoring(self):
        """Start continuous emotion monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Real-time emotion monitoring started")
    
    def stop_real_time_monitoring(self):
        """Stop continuous emotion monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        
        # Clean up temp file
        if hasattr(self, 'temp_audio_file'):
            try:
                import os
                os.unlink(self.temp_audio_file)
                delattr(self, 'temp_audio_file')
            except:
                pass
        
        print("Real-time emotion monitoring stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        try:
            import cv2
            import pyaudio
            import numpy as np
            
            # Initialize camera and audio
            cap = cv2.VideoCapture(0)
            p = pyaudio.PyAudio()
            
            stream = p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=22050,
                input=True,
                frames_per_buffer=1024
            )
            
            while self.monitoring:
                try:
                    # Analyze voice tone continuously with larger buffer for better accuracy
                    audio_data = stream.read(2048, exception_on_overflow=False)  # Larger buffer
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    # Accumulate audio for better analysis
                    if not hasattr(self, 'audio_buffer'):
                        self.audio_buffer = []
                    
                    self.audio_buffer.extend(audio_array)
                    
                    # Analyze when we have enough data (2 seconds for better accuracy)
                    if len(self.audio_buffer) >= 44100:  # 2 seconds at 22050 Hz
                        analysis_data = np.array(self.audio_buffer[-44100:])  # Last 2 seconds
                        
                        # Only analyze if significant audio and enough time passed
                        if not hasattr(self, 'last_analysis_time'):
                            self.last_analysis_time = 0
                        
                        current_time = time.time()
                        if (np.max(np.abs(analysis_data)) > 0.01 and 
                            current_time - self.last_analysis_time >= 5):  # Analyze every 5 seconds max
                            
                            voice_emotion = self._analyze_voice_tone(analysis_data)
                            if voice_emotion != 'neutral' and voice_emotion != self.current_emotion:
                                old_emotion = self.current_emotion
                                self.update_emotion(voice_emotion)
                                print(f"Voice emotion: {old_emotion} → {voice_emotion}")
                            
                            self.last_analysis_time = current_time
                        
                        # Keep only last 3 seconds of audio
                        if len(self.audio_buffer) > 66150:
                            self.audio_buffer = self.audio_buffer[-66150:]
                    
                    # Analyze face emotion every 30 minutes
                    current_time = time.time()
                    if not hasattr(self, 'last_face_check'):
                        self.last_face_check = current_time
                    
                    if current_time - self.last_face_check >= 1800:  # 30 minutes = 1800 seconds
                        ret, frame = cap.read()
                        if ret:
                            emotion = self._analyze_face_emotion(frame)
                            if emotion != 'neutral' and emotion != self.current_emotion:
                                old_emotion = self.current_emotion
                                self.update_emotion(emotion)
                                print(f"Face emotion (30min check): {old_emotion} → {emotion}")
                        self.last_face_check = current_time
                    
                    time.sleep(0.05)  # Check voice every 0.05 seconds for better responsiveness
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(1)
            
            cap.release()
            stream.stop_stream()
            stream.close()
            p.terminate()
            
        except Exception as e:
            print(f"Monitor setup error: {e}")
    
    def _analyze_face_emotion(self, frame):
        """Advanced face emotion analysis without API calls"""
        try:
            import cv2
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                
                # Advanced facial feature analysis
                brightness = np.mean(face_roi)
                contrast = np.std(face_roi)
                
                # Edge detection for expression analysis
                edges = cv2.Canny(face_roi, 50, 150)
                edge_density = np.sum(edges > 0) / (w * h)
                
                # Advanced emotion classification
                if brightness > 130 and edge_density < 0.1:
                    return 'happy'
                elif brightness < 70:
                    return 'sad'
                elif edge_density > 0.15:
                    return 'stressed'
                elif contrast > 80:
                    return 'angry'
                else:
                    return 'neutral'
            
            # Fallback for no face detected
            brightness = np.mean(gray)
            contrast = np.std(gray)
            
            if brightness > 130 and contrast > 45:
                return 'happy'
            elif brightness < 70:
                return 'sad'
            elif contrast > 70:
                return 'stressed'
            else:
                return 'neutral'
                
        except Exception as e:
            return 'neutral'
    
    def _analyze_voice_tone(self, audio_data):
        """Advanced voice emotion detection using audio features"""
        try:
            # Calculate advanced audio features
            energy = np.sum(audio_data**2) / len(audio_data)
            zcr = np.sum(np.diff(np.sign(audio_data)) != 0) / len(audio_data)
            
            # Calculate pitch variation (spectral features)
            fft = np.fft.fft(audio_data)
            magnitude = np.abs(fft)
            spectral_centroid = np.sum(magnitude * np.arange(len(magnitude))) / np.sum(magnitude)
            
            # Advanced emotion classification
            if energy > 0.01 and zcr < 0.1 and spectral_centroid > 5000:
                return 'excited'
            elif energy > 0.003 and zcr < 0.15 and spectral_centroid > 3000:
                return 'happy'
            elif energy < 0.001 or spectral_centroid < 1000:
                return 'sad'
            elif zcr > 0.25 and energy > 0.002:
                return 'stressed'
            elif energy > 0.005 and zcr > 0.2:
                return 'angry'
            else:
                return 'neutral'
                
        except Exception as e:
            # Simple fallback
            energy = np.sum(audio_data**2) / len(audio_data)
            if energy > 0.01:
                return 'excited'
            elif energy > 0.003:
                return 'happy'
            elif energy < 0.001:
                return 'sad'
            else:
                return 'neutral'
    
    def get_voice_settings(self):
        """Get TTS settings based on emotion"""
        settings = {
            'happy': {'rate': 200, 'volume': 0.9},
            'excited': {'rate': 220, 'volume': 1.0},
            'sad': {'rate': 140, 'volume': 0.6},
            'stressed': {'rate': 160, 'volume': 0.7},
            'angry': {'rate': 180, 'volume': 0.8},
            'calm': {'rate': 150, 'volume': 0.8},
            'neutral': {'rate': 174, 'volume': 0.9}
        }
        # Silent voice settings
        return settings.get(self.current_emotion, settings['neutral'])
    
    def enable(self):
        self.enabled = True
        self.save_emotion_data()
        self.start_real_time_monitoring()
        return "Emotion detection enabled. I'll now monitor your mood and adapt in real-time."
    
    def disable(self):
        self.enabled = False
        self.save_emotion_data()
        self.stop_real_time_monitoring()
        return "Emotion detection disabled."
    
    def get_status(self):
        if self.enabled:
            return f"Emotion detection active. Current emotion: {self.current_emotion}. Real-time monitoring: {'ON' if self.monitoring else 'OFF'}"
        return "Emotion detection disabled"

# Global emotion system
emotion_system = EmotionSystem()

# Scheduler System
class TaskScheduler:
    def __init__(self):
        self.scheduled_tasks = []
        self.scheduler_thread = None
        self.running = False
        self.tasks_file = 'scheduled_tasks.json'
        self.load_tasks()
    
    def load_tasks(self):
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as f:
                    self.scheduled_tasks = json.load(f)
        except:
            self.scheduled_tasks = []
    
    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.scheduled_tasks, f)
        except Exception as e:
            print(f"Save tasks error: {e}")
    
    def schedule_task(self, task_command, schedule_time):
        try:
            task = {
                'command': task_command,
                'time': schedule_time,
                'created': datetime.now().isoformat(),
                'executed': False
            }
            self.scheduled_tasks.append(task)
            self.save_tasks()
            
            # Parse time and schedule
            time_lower = schedule_time.lower().strip()
            
            if 'am' in time_lower or 'pm' in time_lower:
                # Handle AM/PM format (e.g., "2am", "2:30pm")
                clean_time = time_lower.replace(' ', '')
                schedule.every().day.at(clean_time).do(self._execute_task, task_command)
            elif 'second' in time_lower or 'sec' in time_lower:
                # Handle seconds (e.g., "30 seconds", "5sec")
                import re
                match = re.search(r'(\d+)', time_lower)
                if match:
                    secs = int(match.group(1))
                    schedule.every(secs).seconds.do(self._execute_task, task_command)
            elif 'minute' in time_lower or 'min' in time_lower:
                # Handle minutes (e.g., "5 minutes", "10min")
                import re
                match = re.search(r'(\d+)', time_lower)
                if match:
                    mins = int(match.group(1))
                    schedule.every(mins).minutes.do(self._execute_task, task_command)
            elif 'hour' in time_lower or 'hr' in time_lower:
                # Handle hours (e.g., "2 hours", "1hr")
                import re
                match = re.search(r'(\d+)', time_lower)
                if match:
                    hrs = int(match.group(1))
                    schedule.every(hrs).hours.do(self._execute_task, task_command)
            else:
                # Try to parse as time format (e.g., "14:30", "2:00")
                try:
                    schedule.every().day.at(time_lower).do(self._execute_task, task_command)
                except:
                    return f"Invalid time format: {schedule_time}"
            
            self._start_scheduler()
            return f"Task scheduled: {task_command} at {schedule_time}"
        except Exception as e:
            return f"Schedule error: {e}"
    
    def _execute_task(self, command):
        try:
            print(f"Executing scheduled task: {command}")
            if 'open notepad' in command:
                subprocess.Popen(['notepad.exe'])
                print(f"Opened notepad")
            elif 'open' in command:
                app = command.replace('open ', '')
                subprocess.Popen([app])
                print(f"Opened {app}")
            else:
                # Execute as dual AI command
                from engine.dual_ai import dual_ai
                response = dual_ai.execute(command)
                print(f"Dual AI response: {response}")
                # Speak the response
                try:
                    speak(response)
                except:
                    print("Could not speak response")
            return schedule.CancelJob  # Cancel this job after execution
        except Exception as e:
            print(f"Task execution error: {e}")
            return schedule.CancelJob  # Cancel even on error
    
    def _start_scheduler(self):
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
    
    def _scheduler_loop(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)  # Check every second for better precision
    
    def list_tasks(self):
        if not self.scheduled_tasks:
            return "No scheduled tasks"
        tasks = "Scheduled tasks: "
        for task in self.scheduled_tasks[-5:]:
            tasks += f"{task['command']} at {task['time']}, "
        return tasks

# Global scheduler
task_scheduler = TaskScheduler()

# Continuous listening variables
continuous_active = False
continuous_listener = None
listening_paused = False
jarvis_muted = False

def speak(text):
    global jarvis_muted
    text = str(text)
    
    # Check if Jarvis is muted
    if jarvis_muted:
        print(f"[MUTED] Jarvis: {text}")
        return
    
    # Transform text with personality manager
    try:
        from engine.personality_manager import personality_manager
        text = personality_manager.transform_response(text)
    except Exception as e:
        print(f"Personality transform error: {e}")
    
    # Apply emotion-based adaptation
    try:
        text = emotion_system.get_adaptive_response(text)
    except Exception as e:
        print(f"Emotion adaptation error: {e}")
    
    # Get emotion-based voice settings
    voice_settings = emotion_system.get_voice_settings() if emotion_system.enabled else {'rate': 174, 'volume': 0.9}
    
    # Get current language from multilingual support
    try:
        from engine.multilingual_support import multilingual
        current_language = multilingual.current_language
    except:
        current_language = 'english'
    
    # Update command history with response
    try:
        if hasattr(command_history, 'history') and command_history.history:
            last_entry = command_history.history[-1]
            if last_entry.get('jarvis_response') == "Processing...":
                last_entry['jarvis_response'] = text
                command_history.save_history()
    except Exception as e:
        print(f"History update error: {e}")
    
    try:
        eel.DisplayMessage(text)
    except:
        print(f"Jarvis: {text}")
    
    # Handle TTS based on language
    try:
        # For non-English languages, use gTTS
        if current_language != 'english':
            try:
                from gtts import gTTS
                import pygame
                import io
                import os
                
                # Get language code for gTTS
                lang_codes = {
                    'kannada': 'kn',
                    'hindi': 'hi',
                    'bengali': 'bn',
                    'gujarati': 'gu',
                    'malayalam': 'ml',
                    'marathi': 'mr',
                    'tamil': 'ta',
                    'telugu': 'te',
                    'urdu': 'ur'
                }
                
                lang_code = lang_codes.get(current_language, 'en')
                
                # Generate speech using gTTS
                tts = gTTS(text=text, lang=lang_code, slow=False)
                
                # Save to memory buffer
                mp3_buffer = io.BytesIO()
                tts.write_to_fp(mp3_buffer)
                mp3_buffer.seek(0)
                
                # Play using pygame
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_buffer)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                pygame.mixer.quit()
                
            except Exception as e:
                print(f"gTTS error: {e}")
                # Fallback to voice gender control for non-English
                from engine.voice_gender_control import voice_control
                voice_control.speak_with_gender(text)
        else:
            # For English, use voice gender control with emotion settings
            from engine.voice_gender_control import voice_control
            success = voice_control.speak_with_gender(text)
            if not success:
                # Final fallback to basic pyttsx3 with emotion settings
                engine = pyttsx3.init('sapi5')
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)
                engine.setProperty('rate', voice_settings['rate'])
                engine.setProperty('volume', voice_settings['volume'])
                engine.say(text)
                engine.runAndWait()
                
    except Exception as e:
        print(f"TTS error: {e}")
        # Final fallback to basic pyttsx3 with emotion settings
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', voice_settings['rate'])
            engine.setProperty('volume', voice_settings['volume'])
            engine.say(text)
            engine.runAndWait()
        except:
            print(f"All TTS methods failed for: {text}")
    
    try:
        eel.receiverText(text)
    except:
        pass

def takecommand():
    global listening_paused
    
    # Check if listening is paused
    if listening_paused:
        print("Listening is paused")
        return ""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        try:
            eel.DisplayMessage('listening....')
        except:
            pass
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            return ""

    try:
        print('recognizing')
        try:
            eel.DisplayMessage('recognizing....')
        except:
            pass
        
        # Get current language for speech recognition
        try:
            from engine.multilingual_support import multilingual
            current_language = multilingual.current_language
        except:
            current_language = 'english'
        
        # Set recognition language based on current language
        try:
            from engine.multilingual_support import multilingual
            recognition_language = multilingual.get_speech_recognition_language()
        except:
            recognition_language = 'en-IN'
        
        query = r.recognize_google(audio, language=recognition_language)
        print(f"user said: {query}")
        try:
            eel.DisplayMessage(query)
        except:
            pass
        time.sleep(1)
    except Exception as e:
        print(f"Recognition error: {e}")
        return ""
    
    return query.lower()

# Expose takecommand for chatbot use
@eel.expose
def chatbot_listen():
    return takecommand()

def parse_multiple_commands(query):
    """Parse multiple commands from a single query"""
    import re
    
    # Common separators for multiple commands
    separators = [
        r'\s+and\s+then\s+',
        r'\s+then\s+',
        r'\s+and\s+',
        r'\s*,\s*and\s+',
        r'\s*,\s*then\s+',
        r'\s*,\s*'
    ]
    
    # Try each separator to split the query
    commands = [query.strip()]
    
    for separator in separators:
        temp_commands = []
        for cmd in commands:
            split_cmds = re.split(separator, cmd, flags=re.IGNORECASE)
            if len(split_cmds) > 1:
                temp_commands.extend([c.strip() for c in split_cmds if c.strip()])
            else:
                temp_commands.append(cmd)
        commands = temp_commands
        if len(commands) > 1:
            break
    
    # Filter out empty commands and very short ones
    commands = [cmd for cmd in commands if cmd and len(cmd.strip()) > 2]
    
    return commands

@eel.expose
def allCommands(message=1):
    is_voice_input = False
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
        is_voice_input = True
    else:
        query = message
        try:
            eel.senderText(query)
        except:
            print(f"User: {query}")
        is_voice_input = False
    
    # Store the user command immediately
    if query and query.strip():
        command_history.add_command(query, "Processing...", is_voice_input)
    
    # Check for aura mode at the beginning
    if "aura" in query.lower():
        try:
            from engine.ultimate_ai_executor import ultimate_ai
            print(f"🌟 AURA Mode Activated for: {query}")
          
            
            # Remove "aura" from query and execute with ultimate AI
            clean_query = query.lower().replace("aura", "").strip()
            if clean_query:
                # Execute and get AI-generated response from ultimate AI
                response = ultimate_ai.execute(clean_query)
                if response:
                    speak(response)  # Speak the response from ultimate AI
                    
                    # Wait 1 second then show next move prediction
                    time.sleep(1)
                    
                    # Get next move suggestion from ultimate AI
                    try:
                        suggestions = ultimate_ai.predict_next_move(clean_query)
                        if suggestions and len(suggestions) > 0:
                            suggestion = suggestions[0]
                            print(f"\n🤖 AI Suggestion: {suggestion}")
                            
                            # Get simple yes/no confirmation
                            speak(f"Execute {suggestion}?")
                            confirmation = takecommand()  # Get voice input directly
                            
                            if confirmation and ("yes" in confirmation.lower() or "y" in confirmation.lower()):
                                print(f"🚀 Executing: {suggestion}")
                                speak("Executing suggestion")
                                # Execute suggestion using full Ultimate AI system
                                ultimate_ai.execute(suggestion)
                            else:
                                print("👍 Skipping suggestion")
                                speak("Skipping suggestion")
                    except Exception as e:
                        print(f"Next move error: {e}")
                else:
                    speak("Command completed")
            else:
                speak("Please specify what you want me to do with aura mode")
            
            try:
                eel.ShowHood()
            except:
                pass
            return
            
        except Exception as e:
            print(f"Ultimate AI Error: {e}")
            speak("Aura mode failed. Switching to standard mode.")
            # Continue with normal processing
    
    try:
        print(f"Processing query: '{query}'")
        
        # Detect emotion from user input only if it came from voice
        if emotion_system.enabled and is_voice_input:
            detected_emotion = emotion_system.detect_emotion_from_text(query)
            emotion_system.update_emotion(detected_emotion)
            print(f"Detected emotion: {detected_emotion}")
        elif emotion_system.enabled and not is_voice_input:
            print("Command line input - skipping emotion detection")
        
        # Parse multiple commands
        commands = parse_multiple_commands(query)
        
        if len(commands) > 1:
            print(f"Multiple commands detected: {commands}")
            speak(f"Executing {len(commands)} commands")
            
            # Execute each command sequentially
            for i, cmd in enumerate(commands, 1):
                print(f"Executing command {i}/{len(commands)}: {cmd}")
                try:
                    # Add small delay between commands
                    if i > 1:
                        time.sleep(0.5)
                    
                    # Process each command individually
                    process_single_command(cmd.strip())
                    
                except Exception as e:
                    print(f"Error executing command '{cmd}': {e}")
                    try:
                        speak(f"Error with command {i}")
                    except:
                        print(f"Could not speak error for command {i}")
            
            try:
                speak("All commands completed")
            except:
                print("All commands completed")                
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Single command - use existing logic
        process_single_command(query)
        
    except Exception as e:
        print(f"Error in allCommands: {e}")
        speak("Something went wrong")
    
    try:
        eel.ShowHood()
    except:
        pass

def start_continuous_listen():
    """Start continuous listening mode"""
    global continuous_active, continuous_listener
    try:
        if continuous_listener and continuous_active:
            return "Continuous listening already active"
        
        continuous_active = True
        
        def continuous_loop():
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
            print("✅ Ready for continuous listening")
            
            while continuous_active:
                try:
                    # Check if listening is paused
                    if listening_paused:
                        print("⏸️ Listening paused...")
                        try:
                            eel.updateListenStatus("⏸️ Listening paused...")
                        except:
                            pass
                        time.sleep(1)
                        continue
                    
                    print("🎧 Listening...")
                    try:
                        eel.updateListenStatus("🎤 Listening...")
                    except:
                        pass
                    
                    with microphone as source:
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    print("🔍 Recognizing...")
                    try:
                        eel.updateListenStatus("🔍 Recognizing...")
                    except:
                        pass
                    
                    text = recognizer.recognize_google(audio).lower()
                    if text and len(text.strip()) > 2:
                        print(f"✅ Recognized: {text}")
                        try:
                            eel.updateListenStatus(f"✅ Recognized: {text}")
                            eel.senderText(text)
                        except:
                            pass
                        
                        # Parse and process multiple commands
                        commands = parse_multiple_commands(text)
                        
                        if len(commands) > 1:
                            print(f"Multiple commands detected: {commands}")
                            speak(f"Executing {len(commands)} commands")
                            
                            for i, cmd in enumerate(commands, 1):
                                print(f"Executing command {i}/{len(commands)}: {cmd}")
                                try:
                                    if i > 1:
                                        time.sleep(0.5)
                                    process_single_command(cmd.strip())
                                except Exception as e:
                                    print(f"Error executing command '{cmd}': {e}")
                            
                            speak("All commands completed")
                        else:
                            # Single command
                            process_single_command(text)
                        
                        # Return to listening after response
                        time.sleep(1)
                        try:
                            eel.updateListenStatus("🎤 Listening...")
                        except:
                            pass
                        
                except sr.WaitTimeoutError:
                    print("⏰ Timeout - continuing to listen...")
                except sr.UnknownValueError:
                    print("❓ Could not understand - continuing to listen...")
                except Exception as e:
                    print(f"❌ Continuous listen error: {e}")
                    time.sleep(1)
        
        continuous_listener = threading.Thread(target=continuous_loop, daemon=True)
        continuous_listener.start()
        
        print("[START] Initializing continuous listening thread...")
        return "Continuous listening started - speak commands directly"
        
    except Exception as e:
        return f"Error starting continuous listening: {str(e)}"

def stop_continuous_listen():
    """Stop continuous listening mode"""
    global continuous_active, continuous_listener
    try:
        continuous_active = False
        continuous_listener = None
        return "Continuous listening stopped"
    except Exception as e:
        return f"Error stopping continuous listening: {str(e)}"

def get_continuous_listen_status():
    """Get continuous listening status"""
    global continuous_active
    try:
        if continuous_active:
            return "Continuous listening is active"
        return "Continuous listening is inactive"
    except Exception as e:
        return f"Error checking status: {str(e)}"

def pause_listening():
    """Pause listening mode"""
    global listening_paused
    try:
        listening_paused = True
        save_ui_setting('listening_paused', True)
        print("🎤 Microphone paused")
        return "Listening paused - microphone stopped"
    except Exception as e:
        return f"Error pausing listening: {str(e)}"

def resume_listening():
    """Resume listening mode"""
    global listening_paused
    try:
        listening_paused = False
        save_ui_setting('listening_paused', False)
        print("🎤 Microphone resumed")
        return "Listening resumed - microphone active"
    except Exception as e:
        return f"Error resuming listening: {str(e)}"

def mute_jarvis():
    """Mute Jarvis voice"""
    global jarvis_muted
    try:
        jarvis_muted = True
        save_ui_setting('jarvis_muted', True)
        print("Jarvis muted")
        return "Jarvis muted"
    except Exception as e:
        return f"Error muting Jarvis: {str(e)}"

def unmute_jarvis():
    """Unmute Jarvis voice"""
    global jarvis_muted
    try:
        jarvis_muted = False
        save_ui_setting('jarvis_muted', False)
        print("Jarvis unmuted")
        return "Jarvis unmuted"
    except Exception as e:
        return f"Error unmuting Jarvis: {str(e)}"

def save_ui_setting(key, value):
    """Save setting to ui_config.json"""
    try:
        import json
        config_file = 'ui_config.json'
        
        # Load existing config
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except:
            config = {}
        
        # Update setting
        config[key] = value
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving UI setting: {e}")

def load_ui_settings():
    """Load settings from ui_config.json"""
    global listening_paused, jarvis_muted
    try:
        import json
        with open('ui_config.json', 'r') as f:
            config = json.load(f)
        
        listening_paused = config.get('listening_paused', False)
        jarvis_muted = config.get('jarvis_muted', False)
    except Exception as e:
        print(f"Error loading UI settings: {e}")
        listening_paused = False
        jarvis_muted = False

def process_single_command(query):
    """Process a single command using existing logic"""
    global jarvis_muted
    try:
        print(f"Processing single command: '{query}'")
    
    
        
        # Handle unmute command first to bypass mute check
        if "unmute jarvis" in query or "unmute voice" in query:
       
            jarvis_muted = False
            save_ui_setting('jarvis_muted', False)
            print("Jarvis unmuted")
            speak("Jarvis unmuted")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Direct message command with app, name, and message in one command
        if ("send message to" in query and (" on whatsapp " in query or " on mobile " in query)) or \
           ("whatsapp message to" in query) or ("sms to" in query):
        
            try:
                import re
                from engine.features import findContact, whatsApp, sendMessage
                
                # Extract app, name, and message from query
                app_type = "whatsapp" if ("whatsapp" in query or " on whatsapp " in query) else "mobile"
                
                # Extract contact name and message
                if " on whatsapp " in query:
                    # Pattern: "send message to [name] on whatsapp [message]"
                    match = re.search(r'send message to (\w+) on whatsapp (.+)', query)
                elif " on mobile " in query:
                    # Pattern: "send message to [name] on mobile [message]"
                    match = re.search(r'send message to (\w+) on mobile (.+)', query)
                elif "whatsapp message to" in query:
                    # Pattern: "whatsapp message to [name] [message]"
                    match = re.search(r'whatsapp message to (\w+) (.+)', query)
                elif "sms to" in query:
                    # Pattern: "sms to [name] [message]"
                    match = re.search(r'sms to (\w+) (.+)', query)
                    app_type = "mobile"
                else:
                    match = None
                
                if match:
                    contact_name = match.group(1)
                    message_text = match.group(2)
                    
                    # Find contact
                    contact_no, name = findContact(contact_name)
                    if contact_no != 0:
                        if app_type == "whatsapp":
                            whatsApp(contact_no, message_text, 'message', name)
                        else:
                            sendMessage(message_text, contact_no, name)
                    else:
                        speak(f"Contact {contact_name} not found")
                else:
                    speak("Please use format: send message to name on whatsapp your message")
                    
            except Exception as e:
                print(f"Direct message error: {e}")
                speak("Failed to send message")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Contact-based calling and messaging (existing method)
        elif "send message" in query or "phone call" in query or "video call" in query or "call" in query:
    
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preference = takecommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query or "call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preference:
                    message = ""
                    schedule_time = None
                    
                    if "send message" in query:
                        message = 'message'
                        
                        # Check for scheduling keywords
                        if " in " in query and any(word in query for word in ["second", "minute", "hour", "sec", "min", "hr"]):
                            # Extract schedule time from query
                            import re
                            time_match = re.search(r'in\s+(\d+\s*(?:second|minute|hour|sec|min|hr)s?)', query)
                            if time_match:
                                schedule_time = time_match.group(1)
                                speak(f"what message to send? It will be scheduled for {schedule_time}")
                            else:
                                speak("what message to send")
                        else:
                            speak("what message to send")
                        
                        query = takecommand()
                                        
                    elif "phone call" in query or "call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name, schedule_time)
            eel.ShowHood()
            return
        
        # SMS Test Commands
        elif "test sms" in query or "sms test" in query:
            from engine.features import testSMS
            testSMS()
            eel.ShowHood()
            return
        
        # Phone Commands (must have "on phone" suffix)
        elif "on phone" in query:
            from engine.phone import handle_phone_commands
            if handle_phone_commands(query):
                eel.ShowHood()
                return
        
        # Voice gender switching commands - HIGHER PRIORITY than language switching
        elif any(phrase in query.lower() for phrase in ["switch to male", "switch to female", "male voice", "female voice", "current voice", "voice status"]):
        
            try:
                from engine.voice_gender_control import voice_control
                query_lower = query.lower()
                
                if "female voice" in query_lower or "switch to female" in query_lower:
                    response = voice_control.switch_to_female()
                    speak(response)
                    print(f"Voice switched to female: {response}")
                elif "male voice" in query_lower or "switch to male" in query_lower:
                    response = voice_control.switch_to_male()
                    speak(response)
                    print(f"Voice switched to male: {response}")
                elif "current voice" in query_lower or "voice status" in query_lower:
                    gender = voice_control.get_current_gender()
                    speak(f"Current voice is set to {gender}")
                    print(f"Current voice gender: {gender}")
                    
            except Exception as e:
                print(f"Voice switch error: {e}")
                speak("Voice switching failed")
            print("Voice gender command completed, returning")
            return
        
        # Language switching commands (exclude voice gender commands)
        elif ("switch to" in query or "change language" in query) and not any(voice_term in query.lower() for voice_term in ["male", "female", "voice"]):
            try:
                from engine.multilingual_support import multilingual
                response = multilingual.process_multilingual_command(query)
                speak(response)
            except Exception as e:
                print(f"Language switch error: {e}")
                speak("Language switching is not available")
            eel.ShowHood()
            return
        
        # Add contact command
        elif "add contact" in query:
            try:
                import re
                import sqlite3
                
                # Extract name and number from query
                match = re.search(r'add contact (\w+) (\d+)', query)
                if match:
                    name = match.group(1)
                    number = match.group(2)
                    
                    # Add to database
                    con = sqlite3.connect("jarvis.db")
                    cursor = con.cursor()
                    cursor.execute('INSERT INTO contacts (name, mobile_no) VALUES (?, ?)', (name, number))
                    con.commit()
                    con.close()
                    
                    speak(f"Contact {name} with number {number} added successfully")
                else:
                    speak("Please say add contact name number")
                    
            except Exception as e:
                print(f"Add contact error: {e}")
                speak("Failed to add contact")
            eel.ShowHood()
            return
        
        # Delete contact command
        elif "delete contact" in query:
            try:
                import re
                import sqlite3
                
                # Extract name from query
                match = re.search(r'delete contact (\w+)', query)
                if match:
                    name = match.group(1)
                    
                    con = sqlite3.connect("jarvis.db")
                    cursor = con.cursor()
                    
                    # Check if contact exists
                    cursor.execute('SELECT name FROM contacts WHERE LOWER(name) LIKE ?', ('%' + name.lower() + '%',))
                    result = cursor.fetchone()
                    
                    if result:
                        cursor.execute('DELETE FROM contacts WHERE LOWER(name) LIKE ?', ('%' + name.lower() + '%',))
                        con.commit()
                        speak(f"Contact {name} deleted successfully")
                    else:
                        speak(f"Contact {name} not found")
                    
                    con.close()
                else:
                    speak("Please say delete contact name")
                    
            except Exception as e:
                print(f"Delete contact error: {e}")
                speak("Failed to delete contact")
            eel.ShowHood()
            return
        
        # View contacts command
        elif "view contacts" in query or "show contacts" in query or "list contacts" in query:
            try:
                import sqlite3
                
                con = sqlite3.connect("jarvis.db")
                cursor = con.cursor()
                cursor.execute('SELECT name, mobile_no FROM contacts')
                results = cursor.fetchall()
                con.close()
                
                if results:
                    contact_list = "Your contacts are: "
                    for contact in results:
                        contact_list += f"{contact[0]} {contact[1]}, "
                    speak(contact_list)
                else:
                    speak("No contacts found")
                    
            except Exception as e:
                print(f"View contacts error: {e}")
                speak("Failed to view contacts")
            eel.ShowHood()
            return
        
        # Emotion detection commands
        elif "start emotion" in query or "enable emotion" in query:
            response = emotion_system.enable()
            speak(response)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "stop emotion" in query or "disable emotion" in query:
            response = emotion_system.disable()
            speak(response)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "emotion status" in query or "current emotion" in query:
            response = emotion_system.get_status()
            speak(response)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "encourage me" in query or "cheer me up" in query:
            encouragement = emotion_system.get_encouraging_response()
            speak(encouragement)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "make me laugh" in query or "tell joke" in query:
            humor = emotion_system.get_humor_response()
            speak(humor)
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Calendar event scheduling (for events with "at" time)
        elif "add event" in query or ("add" in query and "event" in query):
            try:
                from engine.voice_advanced_ai import get_voice_advanced_response
                response = get_voice_advanced_response(query)
                speak(response)
            except Exception as e:
                speak(f"Calendar scheduling failed: {e}")
            eel.ShowHood()
            return
        
        # Task scheduling (for system tasks with "in" time)
        elif "schedule" in query and "in" in query and "event" not in query:
            try:
                import re
                # Extract command and time
                parts = query.split(" in ", 1)
                command = parts[0].replace("schedule ", "")
                time_part = parts[1]
                
                response = task_scheduler.schedule_task(command, time_part)
                speak(response)
            except Exception as e:
                speak(f"Task scheduling failed: {e}")
            eel.ShowHood()
            return
        elif "list scheduled" in query or "show scheduled" in query:
            response = task_scheduler.list_tasks()
            speak(response)
            eel.ShowHood()
            return
        
        # Calendar commands
        elif "show calendar" in query or "check calendar" in query or "my events" in query:
            try:
                from engine.voice_advanced_ai import get_voice_advanced_response
                response = get_voice_advanced_response(query)
                speak(response)
            except Exception as e:
                speak(f"Calendar display failed: {e}")
            eel.ShowHood()
            return
        
        # Previous command queries - execute must come first
        elif "execute previous command" in query or "run previous command" in query or "repeat last command" in query:
            try:
                recent = command_history.get_recent_commands(10)
                # Find the last command that's not an "execute" or "what is" command
                prev_cmd = None
                for cmd in reversed(recent):
                    if ("execute previous" not in cmd['user_input'].lower() and 
                        "run previous" not in cmd['user_input'].lower() and
                        "repeat last" not in cmd['user_input'].lower() and
                        "what is previous" not in cmd['user_input'].lower() and
                        "last command" not in cmd['user_input'].lower() and
                        "previous command" not in cmd['user_input'].lower()):
                        prev_cmd = cmd['user_input']
                        break
                
                if prev_cmd:
                    speak(f"Executing previous command: {prev_cmd}")
                    process_single_command(prev_cmd)
                else:
                    speak("No previous command to execute")
            except:
                speak("Cannot execute previous command")
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "what is previous command" in query or "last command" in query or "previous command" in query:
            try:
                recent = command_history.get_recent_commands(10)
                # Find the last command that's not a query command
                prev_cmd = None
                for cmd in reversed(recent):
                    if ("what is previous" not in cmd['user_input'].lower() and 
                        "last command" not in cmd['user_input'].lower() and
                        "previous command" not in cmd['user_input'].lower()):
                        prev_cmd = cmd['user_input']
                        break
                
                if prev_cmd:
                    speak(f"Your previous command was: {prev_cmd}")
                else:
                    speak("No previous command found")
            except:
                speak("Cannot retrieve previous command")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Continuous listening commands
        elif "start continuous" in query or "continuous listen" in query:
            response = start_continuous_listen()
            speak(response)
            eel.ShowHood()
            return
        elif "stop continuous" in query:
            response = stop_continuous_listen()
            speak(response)
            eel.ShowHood()
            return
        elif "continuous status" in query:
            response = get_continuous_listen_status()
            speak(response)
            eel.ShowHood()
            return
        
        # Pause/Resume listening commands
        elif "pause listening" in query:
            response = pause_listening()
            speak(response)
            eel.ShowHood()
            return
        elif "resume listening" in query:
            response = resume_listening()
            speak(response)
            eel.ShowHood()
            return
        
        # Mute/Unmute Jarvis commands
        elif "mute jarvis" in query or "mute voice" in query:
            response = mute_jarvis()
            # Don't speak when muting
            print(response)
            eel.ShowHood()
            return
        # Unmute is handled at the beginning of the function
        
        # Direct website search commands - "open search for ml"
        elif "open" in query and "search for" in query:
            try:
                import webbrowser
                import pyautogui
                import time
                
                # Extract website and search terms
                parts = query.split("search for", 1)
                website_part = parts[0].replace("open", "").strip().lower()
                search_terms = parts[1].strip()
                
                import urllib.parse
                
                # Direct search URLs for specific websites
                search_urls = {
                    'youtube': f'https://www.youtube.com/results?search_query={urllib.parse.quote(search_terms)}',
                    'amazon': f'https://www.amazon.in/s?k={urllib.parse.quote(search_terms)}',
                    'flipkart': f'https://www.flipkart.com/search?q={urllib.parse.quote(search_terms)}',
                    'myntra': f'https://www.myntra.com/{urllib.parse.quote(search_terms)}',
                    'ajio': f'https://www.ajio.com/search/?text={urllib.parse.quote(search_terms)}',
                    'meesho': f'https://www.meesho.com/search?q={urllib.parse.quote(search_terms)}',
                    'wikipedia': f'https://en.wikipedia.org/w/index.php?search={urllib.parse.quote(search_terms)}',
                    'youtube music': f'https://music.youtube.com/search?q={urllib.parse.quote(search_terms)}',
                    'stackoverflow': f'https://stackoverflow.com/search?q={urllib.parse.quote(search_terms)}',
                    'github': f'https://github.com/search?q={urllib.parse.quote(search_terms)}',
                    'npm': f'https://www.npmjs.com/search?q={urllib.parse.quote(search_terms)}',
                    'coursera': f'https://www.coursera.org/search?query={urllib.parse.quote(search_terms)}',
                    'udemy': f'https://www.udemy.com/courses/search/?q={urllib.parse.quote(search_terms)}',
                    'perplexity': f'https://www.perplexity.ai/search?q={urllib.parse.quote(search_terms)}',
                    'linkedin': f'https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(search_terms)}',
                    'linkedin jobs': f'https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(search_terms)}',
                    'google': f'https://www.google.com/search?q={urllib.parse.quote(search_terms)}',
                    'facebook': f'https://www.facebook.com/search/top/?q={urllib.parse.quote(search_terms)}',
                    'twitter': f'https://twitter.com/search?q={urllib.parse.quote(search_terms)}',
                    'instagram': f'https://www.instagram.com/explore/tags/{urllib.parse.quote(search_terms)}',
                    'reddit': f'https://www.reddit.com/search/?q={urllib.parse.quote(search_terms)}',
                    'netflix': f'https://www.netflix.com/search?q={urllib.parse.quote(search_terms)}',
                    'ebay': f'https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(search_terms)}',
                    'pinterest': f'https://www.pinterest.com/search/pins/?q={urllib.parse.quote(search_terms)}',
                    'quora': f'https://www.quora.com/search?q={urllib.parse.quote(search_terms)}',
                    'medium': f'https://medium.com/search?q={urllib.parse.quote(search_terms)}',
                    'dribbble': f'https://dribbble.com/search/{urllib.parse.quote(search_terms)}',
                    'behance': f'https://www.behance.net/search/projects?search={urllib.parse.quote(search_terms)}',
                    'unsplash': f'https://unsplash.com/s/photos/{urllib.parse.quote(search_terms)}',
                    'pixabay': f'https://pixabay.com/images/search/{urllib.parse.quote(search_terms)}',
                    'freepik': f'https://www.freepik.com/search?query={urllib.parse.quote(search_terms)}',
                    'codepen': f'https://codepen.io/search/pens?q={urllib.parse.quote(search_terms)}',
                    'devto': f'https://dev.to/search?q={urllib.parse.quote(search_terms)}',
                    'hashnode': f'https://hashnode.com/search?q={urllib.parse.quote(search_terms)}',
                    'producthunt': f'https://www.producthunt.com/search?q={urllib.parse.quote(search_terms)}',
                    'hackernews': f'https://hn.algolia.com/?q={urllib.parse.quote(search_terms)}',
                    'duckduckgo': f'https://duckduckgo.com/?q={urllib.parse.quote(search_terms)}',
                    'bing': f'https://www.bing.com/search?q={urllib.parse.quote(search_terms)}',
                    'yandex': f'https://yandex.com/search/?text={urllib.parse.quote(search_terms)}',
                    'maps': f'https://www.google.com/maps/search/{urllib.parse.quote(search_terms)}',
                    'zomato': f'https://www.zomato.com/search?q={urllib.parse.quote(search_terms)}',
                    'swiggy': f'https://www.swiggy.com/search?q={urllib.parse.quote(search_terms)}',
                    'bookmyshow': f'https://in.bookmyshow.com/explore/search/{urllib.parse.quote(search_terms)}',
                    'makemytrip': f'https://www.makemytrip.com/search?q={urllib.parse.quote(search_terms)}',
                    'airbnb': f'https://www.airbnb.com/s/{urllib.parse.quote(search_terms)}',
                    'booking': f'https://www.booking.com/searchresults.html?ss={urllib.parse.quote(search_terms)}',
                    'justdial': f'https://www.justdial.com/search/all/{urllib.parse.quote(search_terms)}',
                    'bigbasket': f'https://www.bigbasket.com/ps/?q={urllib.parse.quote(search_terms)}',
                    'nykaa': f'https://www.nykaa.com/search/result/?q={urllib.parse.quote(search_terms)}',
                    'lenskart': f'https://www.lenskart.com/search?q={urllib.parse.quote(search_terms)}',
                    'pharmeasy': f'https://pharmeasy.in/search/all?name={urllib.parse.quote(search_terms)}',
                    'practo': f'https://www.practo.com/search/doctors?results_type=doctor&q={urllib.parse.quote(search_terms)}',
                    'hotstar': f'https://www.hotstar.com/in/search?q={urllib.parse.quote(search_terms)}',
                    'spotify': f'https://open.spotify.com/search/{urllib.parse.quote(search_terms)}',
                    'gaana': f'https://gaana.com/search/{urllib.parse.quote(search_terms)}'
                }
                
                # Regular websites (open and type)
                regular_sites = {
                    'chatgpt': 'https://chat.openai.com',
                    'gemini': 'https://gemini.google.com',
                    'claude': 'https://claude.ai',
                    'bard': 'https://bard.google.com',
                    'copilot': 'https://copilot.microsoft.com'
                }
                
                # Check if website has direct search URL
                if website_part in search_urls:
                    webbrowser.open(search_urls[website_part])
                    speak(f"Searching for {search_terms}")
                elif website_part in regular_sites:
                    webbrowser.open(regular_sites[website_part])
                    speak(f"Opening and typing {search_terms}")
                    time.sleep(3)
                    pyautogui.typewrite(search_terms)
                    pyautogui.press('enter')
                else:
                    # Fallback for unknown websites
                    website_url = f"https://{website_part}.com"
                    webbrowser.open(website_url)
                    speak(f"Opening and typing {search_terms}")
                    time.sleep(3)
                    pyautogui.typewrite(search_terms)
                    pyautogui.press('enter')
                
            except Exception as e:
                print(f"Website search error: {e}")
                speak("Failed to open website")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # General web search with AI
           
        # Browser and Website Management Commands - handle before app management
        elif any(word in query.lower() for word in ['open ', 'launch ', 'run ']) and any(word in query.lower() for word in ['browser', 'web', 'website', 'site']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"Browser/website opener error: {e}")
                speak("Failed to open browser or website")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        elif any(word in query.lower() for word in ['close ', 'quit ', 'exit ', 'kill ']) and any(word in query.lower() for word in ['browser', 'web', 'website', 'site']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"Browser/website closer error: {e}")
                speak("Failed to close browser or website")
            try:
                eel.ShowHood()
            except:
                pass
            return
        

        
        # Direct calculator command - HIGH PRIORITY
        elif "open calculator" in query.lower():
            try:
                import subprocess
                subprocess.Popen('calc', shell=True)
                speak("Calculator opened")
            except Exception as e:
                print(f"Calculator error: {e}")
                speak("Failed to open calculator")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Universal App Management Commands - handle before dual AI
        elif any(word in query.lower() for word in ['open ', 'launch ', 'run ']) and not any(word in query.lower() for word in ['file', 'folder']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"App opener error: {e}")
                speak("Failed to open application")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        elif any(word in query.lower() for word in ['close ', 'quit ', 'exit ', 'kill ']) and not any(word in query.lower() for word in ['file', 'folder', 'browser', 'website']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"App closer error: {e}")
                speak("Failed to close application")
            try:
                eel.ShowHood()
            except:
                pass
            return
        

        
        # Everything else handled by Dual AI (reliable functions only)
        else:
         
            try:
                from engine.dual_ai import dual_ai
                # Use dual_ai.execute instead of get_simple_response for multilingual support
                response = dual_ai.execute(query)
                print(f"Dual AI response: {response}")
                speak(response)
            except Exception as e:
                print(f"Dual AI Error: {e}")
                # Get error message in current language
                try:
                    from engine.multilingual_support import multilingual
                    speak(multilingual.get_response('processing'))
                except:
                    speak("I'm processing your request")
                    
    except Exception as e:
        print(f"Error in process_single_command: {e}")
        speak("Command failed")

# Load UI settings on startup
load_ui_settings()