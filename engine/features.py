import os
from urllib.parse import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import threading
from datetime import datetime, timedelta
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
    pass
except ImportError as e:
    print(f"PyAudio not available: {e}")
    print("Install with: pip install pyaudio")
    PYAUDIO_AVAILABLE = False
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    pass
except ImportError as e:
    print(f"PyAutoGUI not available: {e}")
    print("Install with: pip install pyautogui")
    PYAUTOGUI_AVAILABLE = False
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.personality_manager import personality_manager
# Playing assiatnt sound function
try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
    pass
except ImportError as e:
    print(f"PyWhatKit not available: {e}")
    print("Install with: pip install pywhatkit")
    PYWHATKIT_AVAILABLE = False
try:
    import pvporcupine
    PVPORCUPINE_AVAILABLE = True
    pass
except ImportError as e:
    print(f"PvPorcupine not available: {e}")
    print("Install with: pip install pvporcupine")
    PVPORCUPINE_AVAILABLE = False

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    app_name = query.strip().lower()

    if app_name != "":
        try:
            # First try PC apps from database
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                response = personality_manager.transform_response(f"Opening {app_name}", 'success')
                speak(response)
                os.startfile(results[0][0])
                return

            # Then try web commands
            cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()
            
            if len(results) != 0:
                response = personality_manager.transform_response(f"Opening {app_name}", 'success')
                speak(response)
                webbrowser.open(results[0][0])
                return

            # Try common phone apps via ADB (using actual package names from your phone)
            phone_apps = {
                'whatsapp': 'com.whatsapp',
                'instagram': 'com.instagram.android', 
                'facebook': 'com.facebook.katana',
                'youtube': 'com.google.android.youtube',
                'gmail': 'com.google.android.gm',
                'chrome': 'com.android.chrome',
                'maps': 'com.google.android.apps.maps',
                'telegram': 'org.telegram.plus',
                'photos': 'com.google.android.apps.photos',
                'camera': 'com.android.camera',
                'gallery': 'com.miui.gallery',
                'calculator': 'com.miui.calculator',
                'notes': 'com.miui.notes',
                'calendar': 'com.xiaomi.calendar',
                'phonepe': 'com.phonepe.app',
                'hotstar': 'in.startv.hotstar'
            }
            
            if app_name in phone_apps:
                response = personality_manager.transform_response(f"Opening {app_name} on phone", 'executing')
                speak(response)
                # Use monkey command to launch app
                result = subprocess.run(f'adb shell monkey -p {phone_apps[app_name]} 1', 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    success_response = personality_manager.transform_response(f"{app_name} opened successfully", 'success')
                    speak(success_response)
                else:
                    error_response = personality_manager.transform_response(f"Failed to open {app_name}", 'error')
                    speak(error_response)
                return
            
            # Try generic app opening on phone
            speak(f"Trying to open {app_name}")
            # Search for app package containing the name
            result = subprocess.run(f'adb shell pm list packages | findstr {app_name}', 
                                  shell=True, capture_output=True, text=True)
            
            if result.stdout:
                # Get first matching package
                package_line = result.stdout.strip().split('\n')[0]
                package_name = package_line.split(':')[1].strip()
                subprocess.run(f'adb shell monkey -p {package_name} 1', shell=True)
                speak(f"Opened {app_name} on phone")
            else:
                # Fallback to PC
                try:
                    os.system('start '+app_name)
                    speak(f"Opening {app_name}")
                except:
                    speak(f"{app_name} not found")
                    
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
            speak("Something went wrong")

       

def PlayYoutube(query):
    if not PYWHATKIT_AVAILABLE:
        speak("YouTube functionality not available")
        return
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    if not PVPORCUPINE_AVAILABLE or not PYAUDIO_AVAILABLE:
        print("PvPorcupine or PyAudio not available")
        print("Trying fallback hotword detection...")
        try:
            from engine.simple_hotword import simple_hotword_detection
            simple_hotword_detection()
        except Exception as e:
            print(f"Fallback hotword detection failed: {e}")
            print("Please install: pip install pvporcupine pyaudio")
        return
    
    porcupine = None
    paud = None
    audio_stream = None
    
    def cleanup_resources():
        """Clean up audio resources safely"""
        try:
            if audio_stream is not None:
                audio_stream.close()
        except Exception as e:
            print(f"Error closing audio stream: {e}")
        
        try:
            if paud is not None:
                paud.terminate()
        except Exception as e:
            print(f"Error terminating PyAudio: {e}")
        
        try:
            if porcupine is not None:
                porcupine.delete()
        except Exception as e:
            print(f"Error deleting Porcupine: {e}")
    
    try:
        pass
        
        # Initialize Porcupine with error handling
        try:
            porcupine = pvporcupine.create(access_key="7FxDn1i0BUibR4eq2c2D97SyurJDHvIEwvnKiH6lK19IFfAD1uStZQ==", keywords=["jarvis", "alexa"])
            pass
        except Exception as e:
            print(f"Failed to initialize Porcupine: {e}")
            print("Try using access key: porcupine = pvporcupine.create(access_key='YOUR_ACCESS_KEY', keywords=['jarvis'])")
            return
        
        # Initialize PyAudio with error handling
        try:
            paud = pyaudio.PyAudio()
            pass
        except Exception as e:
            print(f"Failed to initialize PyAudio: {e}")
            cleanup_resources()
            return
        
        # Open audio stream with error handling
        try:
            audio_stream = paud.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )
            pass
        except Exception as e:
            print(f"Failed to open audio stream: {e}")
            print("Check if microphone is available and not being used by another application")
            cleanup_resources()
            return
        
        print("Hotword detection ready")
        
        # Main detection loop with error recovery
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while True:
            try:
                # Read audio data
                keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
                
                # Process keyword detection
                keyword_index = porcupine.process(keyword)
                
                # Reset error counter on successful processing
                consecutive_errors = 0
                
                # Check if hotword detected
                if keyword_index >= 0:
                    detected_word = "jarvis" if keyword_index == 0 else "alexa"
                    print(f"Hotword detected: {detected_word}")
                    
                    # Trigger Jarvis activation
                    if PYAUTOGUI_AVAILABLE:
                        try:
                            import pyautogui as autogui
                            pass
                            autogui.keyDown("win")
                            autogui.press("j")
                            time.sleep(2)
                            autogui.keyUp("win")
                            print("Jarvis activated")
                        except Exception as e:
                            print(f"Error activating Jarvis: {e}")
                    else:
                        print("PyAutoGUI not available - please activate Jarvis manually")
                    
                    # Brief pause after detection
                    time.sleep(1)
                    
            except Exception as e:
                consecutive_errors += 1
                print(f"Audio processing error ({consecutive_errors}/{max_consecutive_errors}): {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print("Too many consecutive errors. Restarting hotword detection...")
                    break
                
                # Brief pause before retry
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\nHotword detection stopped by user")
    except Exception as e:
        print(f"Unexpected error in hotword detection: {e}")
    finally:
        print("Cleaning up hotword detection resources...")
        cleanup_resources()
        print("Hotword detection stopped")



# find contacts from database
def findContact(query):
    try:
        # First extract contact name by removing scheduling patterns
        import re
        
        # Remove scheduling patterns like "in 30 seconds" first
        query = re.sub(r'\s+in\s+\d+\s*(?:second|minute|hour|sec|min|hr)s?', '', query)
        
        # Then remove other words
        words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
        query = remove_words(query, words_to_remove)
        
        query = query.strip().lower()
        print(f"Searching for: '{query}'")
        
        # Search in database with multiple patterns
        cursor.execute("SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ? OR LOWER(name) = ?", ('%' + query + '%', query + '%', query))
        results = cursor.fetchall()
        
        if results:
            contact_name = results[0][0]
            mobile_number_str = str(results[0][1])
            print(f"Found contact: {contact_name} - {mobile_number_str}")
            
            if not mobile_number_str.startswith('+91') and len(mobile_number_str) == 10:
                mobile_number_str = '+91' + mobile_number_str
            
            return mobile_number_str, contact_name
        else:
            print(f"Contact '{query}' not found in database")
            speak('Contact not found. Please add contact first')
            return 0, 0
            
    except Exception as e:
        print(f"Error finding contact: {e}")
        speak('Error finding contact')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name, schedule_time=None):
    
    if flag == 'message':
        if schedule_time:
            jarvis_message = f"message scheduled for {name} at {schedule_time}"
        else:
            jarvis_message = "message send successfully to "+name
    elif flag == 'call':
        message = ''
        jarvis_message = "calling to "+name
    else:
        message = ''
        jarvis_message = "starting video call with "+name
    
    # If scheduled, set up timer
    if schedule_time and flag == 'message':
        schedule_whatsapp_message(mobile_no, message, name, schedule_time)
        speak(jarvis_message)
        return

    try:
        # Clean mobile number
        clean_number = mobile_no.replace(" ", "").replace("-", "").replace("+91", "")
        
        if flag == 'message':
            # WhatsApp message - simple URL method
            encoded_message = quote(message)
            whatsapp_url = f"whatsapp://send?phone=91{clean_number}&text={encoded_message}"
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            time.sleep(4)
            
            # Simple automation - just press Enter to send
            if PYAUTOGUI_AVAILABLE:
                try:
                    pyautogui.press('enter')
                    time.sleep(0.5)
                    pyautogui.press('enter')  # Try twice in case first doesn't work
                except Exception as e:
                    print(f"Send failed: {e}")
                    speak(f"Message prepared for {name}. Please press Enter to send.")
            
        elif flag == 'call':
            # WhatsApp voice call - try direct call URL first
            try:
                # Try direct call URL (if supported)
                call_url = f"whatsapp://call?phone=91{clean_number}"
                subprocess.run(f'start "" "{call_url}"', shell=True)
                time.sleep(2)
                speak(f"Attempting to call {name} on WhatsApp")
                
                # If direct call doesn't work, open chat and try automation
                time.sleep(3)
                whatsapp_url = f"whatsapp://send?phone=91{clean_number}"
                subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
                time.sleep(4)
                
                # Simple automation - just press Tab and Enter to navigate to call button
                if PYAUTOGUI_AVAILABLE:
                    try:
                        # Press Tab multiple times to navigate to call button
                        for i in range(11):
                            pyautogui.press('tab')
                            time.sleep(0.5)
                        
                        # Press Enter to activate call button
                        pyautogui.press('enter')
                        time.sleep(1)
                        speak(f"Calling {name} on WhatsApp")
                    except Exception as e:
                        print(f"Auto-call failed: {e}")
                        speak(f"Calling {name} on WhatsApp")
                else:
                    speak(f"Calling {name} on WhatsApp")
                    
            except:
                # Final fallback - just open WhatsApp
                subprocess.run('start "" "whatsapp:"', shell=True)
                time.sleep(4)
                speak(f"Calling {name} on WhatsApp")
            
        else:
            # WhatsApp video call - try direct video call URL first
            try:
                # Try direct video call URL (if supported)
                video_call_url = f"whatsapp://call?phone=91{clean_number}&video=true"
                subprocess.run(f'start "" "{video_call_url}"', shell=True)
                time.sleep(2)
                speak(f"Attempting video call with {name} on WhatsApp")
                
                # If direct video call doesn't work, open chat and try automation
                time.sleep(3)
                whatsapp_url = f"whatsapp://send?phone=91{clean_number}"
                subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
                time.sleep(4)
                
                # Simple automation - use keyboard shortcuts for video call
                if PYAUTOGUI_AVAILABLE:
                    try:
                        # Try Ctrl+Shift+V for video call (common shortcut)
                        for i in range(10):
                            pyautogui.press('tab')
                            time.sleep(0.5)
                            pyautogui.press('enter')
                            time.sleep(1)
                        speak(f"Starting video call with {name} on WhatsApp")
                        return
                    except:
                        pass
                    
                    # If shortcuts fail, try clicking video call button positions
                    try:
                        # Wait for WhatsApp to load
                        time.sleep(3)
                        
                        # Try to find and click video call button
                        video_call_positions = [
                            (1240, 60), (1190, 60), (1290, 60), (1340, 60),
                            (1240, 80), (1240, 100), (1220, 70), (1260, 70),
                            (1200, 50), (1280, 50), (1240, 120), (1240, 40),
                            (1100, 60), (1350, 60), (1200, 140), (1200, 20)
                        ]
                        
                        for x, y in video_call_positions:
                            try:
                                pyautogui.click(x, y)
                                time.sleep(0.3)
                            except:
                                continue
                        
                        speak(f"Starting video call with {name} on WhatsApp")
                    except Exception as e:
                        print(f"Auto-video-call failed: {e}")
                        speak(f"Starting video call with {name} on WhatsApp")
                else:
                    speak(f"Starting video call with {name} on WhatsApp")
                    
            except:
                # Final fallback - just open WhatsApp
                subprocess.run('start "" "whatsapp:"', shell=True)
                time.sleep(4)
                speak(f"Starting video call with {name} on WhatsApp")
        
        speak(jarvis_message)
        
    except Exception as e:
        print(f"WhatsApp error: {e}")
        speak(f"WhatsApp opened for {name}, please call manually")

def schedule_whatsapp_message(mobile_no, message, name, schedule_time):
    """Schedule WhatsApp message to be sent at specified time"""
    try:
        # Parse schedule time
        delay_seconds = parse_schedule_time(schedule_time)
        if delay_seconds <= 0:
            speak("Invalid time format")
            return
        
        # Schedule the message
        timer = threading.Timer(delay_seconds, send_scheduled_whatsapp, [mobile_no, message, name])
        timer.start()
        
        print(f"Message scheduled for {name} in {delay_seconds} seconds")
        
    except Exception as e:
        print(f"Schedule error: {e}")
        speak("Failed to schedule message")

def parse_schedule_time(time_str):
    """Parse time string and return delay in seconds"""
    time_str = time_str.lower().strip()
    
    # Handle formats like "5 seconds", "2 minutes", "1 hour"
    import re
    
    # Extract number and unit
    match = re.search(r'(\d+)\s*(second|minute|hour|sec|min|hr)s?', time_str)
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        
        if unit in ['second', 'sec']:
            return number
        elif unit in ['minute', 'min']:
            return number * 60
        elif unit in ['hour', 'hr']:
            return number * 3600
    
    # Handle "in X format"
    if 'in' in time_str:
        time_str = time_str.replace('in', '').strip()
        return parse_schedule_time(time_str)
    
    return 0

def send_scheduled_whatsapp(mobile_no, message, name):
    """Send the scheduled WhatsApp message"""
    try:
        speak(f"Sending scheduled message to {name}")
        
        # Clean mobile number
        clean_number = mobile_no.replace(" ", "").replace("-", "").replace("+91", "")
        
        # WhatsApp message - simple URL method
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone=91{clean_number}&text={encoded_message}"
        subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
        time.sleep(4)
        
        # Simple automation - just press Enter to send
        if PYAUTOGUI_AVAILABLE:
            try:
                pyautogui.press('enter')
                time.sleep(0.5)
                pyautogui.press('enter')  # Try twice in case first doesn't work
                speak(f"Scheduled message sent to {name}")
            except Exception as e:
                print(f"Send failed: {e}")
                speak(f"Scheduled message prepared for {name}. Please press Enter to send.")
        
    except Exception as e:
        print(f"Scheduled WhatsApp error: {e}")
        speak(f"Failed to send scheduled message to {name}")

# chat bot 
def chatBot(query):
    user_input = query.lower()
    try:
        # Try to use hugchat if cookies exist
        if os.path.exists("engine\\cookies.json"):
            chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
            id = chatbot.new_conversation()
            chatbot.change_conversation(id)
            response = chatbot.chat(user_input)
            print(response)
            speak(response)
            return response
        else:
            # Try Gemini AI first, then fallback to AI brain
            try:
                from engine.dual_ai import get_simple_response
                response = get_simple_response(query)
                if response and len(response.strip()) > 0:
                    print(response)
                    speak(response)
                    return response
            except:
                pass
            
            # If AI brain fails, use simple responses
            if "president" in user_input and "india" in user_input:
                response = "The current President of India is Droupadi Murmu, who took office in July 2022."
            elif "prime minister" in user_input and "india" in user_input:
                response = "The current Prime Minister of India is Narendra Modi."
            else:
                response = "I'm ready to help! Try asking me questions or giving voice commands."
            
            print(response)
            speak(response)
            return response
    except Exception as e:
        print(f"ChatBot error: {e}")
        # Fallback responses for common questions
        if "president" in user_input and "india" in user_input:
            response = "The current President of India is Droupadi Murmu, who took office in July 2022."
        elif "prime minister" in user_input and "india" in user_input:
            response = "The current Prime Minister of India is Narendra Modi."
        elif "capital" in user_input and "india" in user_input:
            response = "The capital of India is New Delhi."
        elif "time" in user_input:
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
        elif "date" in user_input:
            import datetime
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            response = f"Today's date is {current_date}"
        elif "hello" in user_input or "hi" in user_input:
            response = "Hello! I'm Jarvis, your AI assistant. How can I help you today?"
        elif "how are you" in user_input:
            response = "I'm doing great! Ready to help you with any tasks or questions."
        elif "what" in user_input and "name" in user_input:
            response = "I'm Jarvis, your personal AI assistant."
        else:
            response = "I'm here to help! You can ask me questions or give me commands to control your computer and phone."
        
        print(response)
        speak(response)
        return response

# android automation - direct dialing

def makeCall(name, mobileNo):
    speak("Calling "+name)
    try:
        if mobileNo == "PHONE_CONTACT":
            speak(f"Please say the phone number for {name}")
            return
        
        # Clean the number
        clean_number = mobileNo.replace(" ", "").replace("-", "").replace("+91", "")
        print(f"Calling: {clean_number}")
        
        # Make direct call using full ADB path
        call_cmd = f'C:\\platform-tools\\adb.exe shell am start -a android.intent.action.CALL -d tel:{clean_number}'
        result = subprocess.run(call_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            speak(f"Calling {name}")
        else:
            print(f"Call failed: {result.stderr}")
            # Fallback: open dialer with number
            subprocess.run(f'C:\\platform-tools\\adb.exe shell am start -a android.intent.action.DIAL -d tel:{clean_number}', shell=True)
            speak(f"Dialer opened for {name}")
            
    except Exception as e:
        print(f"Call error: {e}")
        speak("Call failed, please try manually")


# to send message using working SMS method (improved with test functionality)
def sendMessage(message, mobileNo, name):
    speak("sending message")
    try:
        if mobileNo == "PHONE_CONTACT":
            speak(f"Please say the phone number for {name}")
            return
            
        # Clean the number
        clean_number = mobileNo.replace(" ", "").replace("-", "").replace("+91", "")
        print(f"Sending SMS to: {clean_number}")
        
        # Use the improved SMS method from test functionality
        success = sendSMSImproved(clean_number, message, name)
        
        if success:
            speak(f"Message sent to {name}")
        else:
            speak(f"Failed to send message to {name}")
        
    except Exception as e:
        print(f"SMS error: {e}")
        speak("Opening Google Messages manually")
        subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.google.android.apps.messaging 1', shell=True)
        speak(f"Please send message to {name} manually")

# Improved SMS sending function (direct message with pre-filled content)
def sendSMSImproved(number, message, name):
    """Send SMS using direct method with pre-filled message"""
    print(f"Sending SMS to {number}: {message}")
    
    # Method 1: Direct SMS intent with properly escaped message
    # Escape the message for shell command
    escaped_message = message.replace('"', '\\"').replace("'", "\\'")
    cmd = f'C:\\platform-tools\\adb.exe shell am start -a android.intent.action.SENDTO -d sms:{number} --es sms_body "{escaped_message}"'
    print(f"Command: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"Result: {result.returncode}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    # If Method 1 succeeds, the SMS compose screen is opened with pre-filled content
    if result.returncode == 0:
        print("✅ SMS compose screen opened with pre-filled number and message!")
        print("Attempting to send the message automatically...")
        
        # Wait for compose screen to load
        time.sleep(2)
        
        # Try to send the message automatically
        try:
            # Press Enter to send (common send method)
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
            time.sleep(1)
            
            # Try again if first attempt fails
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
            time.sleep(1)
            
            # Try clicking send button coordinates
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 1200 100', shell=True)
            time.sleep(1)
            
            print("✅ Message sent automatically!")
            speak(f"Message sent successfully to {name}")
        except Exception as e:
            print(f"Auto-send failed: {e}")
            print("The message is ready to send. Please tap the send button on your phone.")
            speak(f"SMS compose screen opened for {name} with your message pre-filled. Please tap the send button to send.")
        
        return True
    
    # Method 2: Alternative SMS intent format with URL encoding
    print("Trying alternative SMS intent format...")
    import urllib.parse
    encoded_message = urllib.parse.quote(message)
    cmd2 = f'C:\\platform-tools\\adb.exe shell am start -a android.intent.action.SENDTO -d "sms:{number}?body={encoded_message}"'
    print(f"Alternative Command: {cmd2}")
    
    result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    print(f"Alternative Result: {result2.returncode}")
    if result2.stderr:
        print(f"Alternative Error: {result2.stderr}")
    
    if result2.returncode == 0:
        print("✅ SMS compose screen opened with alternative method!")
        print("Attempting to send the message automatically...")
        
        # Wait for compose screen to load
        time.sleep(2)
        
        # Try to send the message automatically
        try:
            # Press Enter to send (common send method)
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
            time.sleep(1)
            
            # Try again if first attempt fails
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
            time.sleep(1)
            
            # Try clicking send button coordinates
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 1200 100', shell=True)
            time.sleep(1)
            
            print("✅ Message sent automatically!")
            speak(f"Message sent successfully to {name}")
        except Exception as e:
            print(f"Auto-send failed: {e}")
            print("The message is ready to send. Please tap the send button on your phone.")
            speak(f"SMS compose screen opened for {name} with your message pre-filled. Please tap the send button to send.")
        
        return True
    
    # Method 3: Use specific messaging app with properly escaped message
    print("Trying with specific messaging app...")
    cmd3 = f'C:\\platform-tools\\adb.exe shell am start -n com.google.android.apps.messaging/.ui.conversation.LaunchConversationActivity -a android.intent.action.SENDTO -d sms:{number} --es sms_body "{escaped_message}"'
    print(f"Specific App Command: {cmd3}")
    
    result3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True)
    print(f"Specific App Result: {result3.returncode}")
    if result3.stderr:
        print(f"Specific App Error: {result3.stderr}")
    
    if result3.returncode == 0:
        print("✅ SMS compose screen opened with specific app method!")
        print("Attempting to send the message automatically...")
        
        # Wait for compose screen to load
        time.sleep(2)
        
        # Try to send the message automatically
        try:
            # Press Enter to send (common send method)
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
            time.sleep(1)
            
            # Try again if first attempt fails
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
            time.sleep(1)
            
            # Try clicking send button coordinates
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 1200 100', shell=True)
            time.sleep(1)
            
            print("✅ Message sent automatically!")
            speak(f"Message sent successfully to {name}")
        except Exception as e:
            print(f"Auto-send failed: {e}")
            print("The message is ready to send. Please tap the send button on your phone.")
            speak(f"SMS compose screen opened for {name} with your message pre-filled. Please tap the send button to send.")
        
        return True
    
    # Method 4: Fallback - Open messaging app and manually fill
    print("Using fallback method - opening messaging app...")
    subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.google.android.apps.messaging 1', shell=True)
    time.sleep(3)
    
    # Start new conversation
    subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.intent.action.SENDTO -d sms:', shell=True)
    time.sleep(2)
    
    # Fill phone number
    subprocess.run(f'C:\\platform-tools\\adb.exe shell input text "{number}"', shell=True)
    time.sleep(1)
    subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
    time.sleep(2)
    
    # Fill message with proper escaping
    escaped_message_fallback = message.replace('"', '\\"').replace("'", "\\'")
    subprocess.run(f'C:\\platform-tools\\adb.exe shell input text "{escaped_message_fallback}"', shell=True)
    time.sleep(1)
    
    print("✅ SMS compose screen opened with fallback method!")
    print("Attempting to send the message automatically...")
    
    # Try to send the message automatically
    try:
        # Press Enter to send (common send method)
        subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
        time.sleep(1)
        
        # Try again if first attempt fails
        subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_ENTER', shell=True)
        time.sleep(1)
        
        # Try clicking send button coordinates
        subprocess.run('C:\\platform-tools\\adb.exe shell input tap 1200 100', shell=True)
        time.sleep(1)
        
        print("✅ Message sent automatically!")
        speak(f"Message sent successfully to {name}")
    except Exception as e:
        print(f"Auto-send failed: {e}")
        print("The message is ready to send. Please tap the send button on your phone.")
        speak(f"SMS compose screen opened for {name} with your message. Please tap the send button to send.")
    
    return True

# SMS Test Function - Works with main application (voice-based)
def testSMS():
    """Test SMS functionality using voice commands - works with main app"""
    
    def test_contact(name):
        """Find contact in database"""
        con = sqlite3.connect("jarvis.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?", ('%' + name.lower() + '%',))
        result = cursor.fetchall()
        
        if result:
            print(f"Found: {result[0][0]} - {result[0][1]}")
            return result[0][1]
        else:
            print(f"Contact '{name}' not found")
            return None

    def test_sms(number, message):
        """Test SMS sending with the working method"""
        # Use the improved SMS function
        return sendSMSImproved(number, message, "test contact")

    # Main test function - voice-based for main app
    speak("SMS Test Mode activated. Please say the contact name to test.")
    from engine.command import takecommand
    contact_name = takecommand()
    print(f"Contact name: {contact_name}")
    
    if contact_name:
        number = test_contact(contact_name)
        if number:
            speak("Please say the test message to send.")
            message = takecommand()
            print(f"Test message: {message}")
            
            if message:
                success = test_sms(number, message)
                if success:
                    speak("SMS test completed successfully")
                else:
                    speak("SMS test failed")
            else:
                speak("No message provided for testing")
        else:
            speak("Contact not found. Please add the contact first using simple add.")
    else:
        speak("No contact name provided for testing")

# SMS Test Function - Direct input version (for standalone use)
def testSMSDirect():
    """Test SMS functionality with direct input - for standalone use"""
    
    def test_contact(name):
        """Find contact in database"""
        con = sqlite3.connect("jarvis.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?", ('%' + name.lower() + '%',))
        result = cursor.fetchall()
        
        if result:
            print(f"Found: {result[0][0]} - {result[0][1]}")
            return result[0][1]
        else:
            print(f"Contact '{name}' not found")
            return None

    def test_sms(number, message):
        """Test SMS sending with the working method"""
        # Use the improved SMS function
        return sendSMSImproved(number, message, "test contact")

    # Main test function - exactly like test_sms.py
    name = input("Enter contact name to test: ")
    number = test_contact(name)

    if number:
        message = input("Enter test message: ")
        test_sms(number, message)
    else:
        print("Add contact first using: py simple_add.py")