"""
Simple hotword detection using speech recognition as fallback
This can be used when PvPorcupine is not available
"""

import speech_recognition as sr
import time
import pyautogui
from engine.config import ASSISTANT_NAME

def simple_hotword_detection():
    """
    Simple hotword detection using continuous speech recognition
    Less efficient than PvPorcupine but works as fallback
    """
    print("Starting simple hotword detection...")
    print("Say 'jarvis', 'hey jarvis', or 'alexa' to activate")
    print("Press Ctrl+C to stop")
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Adjust for ambient noise
    print("Adjusting for ambient noise... Please wait.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    print("Ready for hotword detection!")
    
    hotwords = ["jarvis", "hey jarvis", "alexa", "hey alexa"]
    
    while True:
        try:
            # Listen for audio with shorter timeout
            with microphone as source:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
            
            try:
                # Recognize speech
                text = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"Heard: {text}")
                
                # Check for hotwords
                for hotword in hotwords:
                    if hotword in text:
                        print(f"Hotword '{hotword}' detected!")
                        
                        # Activate Jarvis
                        try:
                            pyautogui.keyDown("win")
                            pyautogui.press("j")
                            time.sleep(2)
                            pyautogui.keyUp("win")
                            print("Jarvis activated!")
                        except Exception as e:
                            print(f"Error activating Jarvis: {e}")
                        
                        # Brief pause after activation
                        time.sleep(3)
                        break
                        
            except sr.UnknownValueError:
                # No speech detected, continue listening
                pass
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                time.sleep(1)
                
        except sr.WaitTimeoutError:
            # Timeout is normal, continue listening
            pass
        except KeyboardInterrupt:
            print("\\nSimple hotword detection stopped")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    simple_hotword_detection()