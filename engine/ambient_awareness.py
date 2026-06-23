import threading
import time
import numpy as np

class AmbientAwareness:
    def __init__(self):
        self.active = False
        self.thread = None
        
    def start(self):
        """Start ambient sound detection"""
        if self.active:
            return "Ambient awareness already running"
        
        try:
            import pyaudio
            
            self.active = True
            
            def listen_background():
                try:
                    # Audio config
                    CHUNK = 1024
                    FORMAT = pyaudio.paInt16
                    CHANNELS = 1
                    RATE = 44100
                    THRESHOLD = 5  # Very low threshold for sensitive detection
                    
                    p = pyaudio.PyAudio()
                    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                                  input=True, frames_per_buffer=CHUNK)
                    
                    doorbell_count = 0
                    alarm_count = 0
                    crying_count = 0
                    
                    while self.active:
                        try:
                            data = stream.read(CHUNK, exception_on_overflow=False)
                            audio_data = np.frombuffer(data, dtype=np.int16)
                            # Fix volume calculation
                            mean_square = np.mean(audio_data.astype(np.float64)**2)
                            volume = np.sqrt(max(0, mean_square)) if mean_square > 0 else 0
                            
                            if volume > THRESHOLD:
                                high_freq = np.mean(np.abs(audio_data[audio_data > np.mean(audio_data)]))
                                
                                # Doorbell (short, high-pitched)
                                if high_freq > 50 and volume > 20:
                                    doorbell_count += 1
                                    if doorbell_count >= 3:
                                        self._alert("Doorbell detected! Someone is at the door.")
                                        doorbell_count = 0
                                        time.sleep(5)
                                
                                # Alarm (sustained loud)
                                elif volume > 30:
                                    alarm_count += 1
                                    if alarm_count >= 5:
                                        self._alert("Alarm detected! Please check for emergencies.")
                                        alarm_count = 0
                                        time.sleep(10)
                                
                                # Baby crying (variable pitch)
                                elif 20 < high_freq < 100 and volume > 15:
                                    crying_count += 1
                                    if crying_count >= 5:
                                        self._alert("Baby crying detected! The baby may need attention.")
                                        crying_count = 0
                                        time.sleep(15)
                                
                                # General sound detection
                                elif volume > 10:
                                    print(f"Sound: Vol={volume:.1f}, Freq={high_freq:.1f}")
                            
                            # Reset counters gradually
                            if volume < THRESHOLD:
                                doorbell_count = max(0, doorbell_count - 1)
                                alarm_count = max(0, alarm_count - 1)
                                crying_count = max(0, crying_count - 1)
                            
                            # Debug output for testing
                            if volume > 2:
                                print(f"Audio: {volume:.1f}", end=" ", flush=True)
                            
                            time.sleep(0.1)
                            
                        except Exception as e:
                            continue
                    
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    
                except Exception as e:
                    self.active = False
            
            self.thread = threading.Thread(target=listen_background, daemon=True)
            self.thread.start()
            
            return "Ambient awareness started - listening for doorbell, alarms, baby crying"
            
        except ImportError:
            return "PyAudio not installed. Run: pip install pyaudio numpy"
        except Exception as e:
            return f"Failed to start: {str(e)}"
    
    def stop(self):
        """Stop ambient detection"""
        self.active = False
        if self.thread:
            self.thread.join(timeout=2)
        return "Ambient awareness stopped"
    
    def status(self):
        """Get status"""
        return f"Ambient awareness: {'Active' if self.active else 'Inactive'}"
    
    def _alert(self, message):
        """Alert user"""
        print(f"🔊 AMBIENT ALERT: {message}")
        
        try:
            from engine.features import speak
            speak(message)
        except:
            pass

# Global instance
ambient_awareness = AmbientAwareness()