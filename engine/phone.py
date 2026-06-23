import subprocess
import time
from engine.command import speak

# Use the main app's speak (routes to frontend via eel)

def check_adb_connection():
    """Check if ADB device is connected"""
    try:
        result = subprocess.run('C:\\platform-tools\\adb.exe devices', shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        connected_devices = [line for line in lines[1:] if line.strip() and 'device' in line]
        return len(connected_devices) > 0
    except:
        return False

def handle_phone_commands(query):
    """Handle all phone-related commands"""
    
    # Basic swipe commands
    if "swipe up" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 1500 500 500', shell=True)
            speak("Swiped up")
        else:
            speak("Phone not connected")
    
    elif "swipe down" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 500 500 1500', shell=True)
            speak("Swiped down")
        else:
            speak("Phone not connected")
    
    elif "swipe left" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 800 800 200 800', shell=True)
            speak("Swiped left")
        else:
            speak("Phone not connected")
    
    elif "swipe right" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 200 800 800 800', shell=True)
            speak("Swiped right")
        else:
            speak("Phone not connected")
    
    elif "back" in query or "go back" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_BACK', shell=True)
            speak("Going back")
        else:
            speak("Phone not connected")
    
    elif "home" in query or "go home" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_HOME', shell=True)
            speak("Going home")
        else:
            speak("Phone not connected")
    
    elif "tap" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 800', shell=True)
            speak("Screen tapped")
        else:
            speak("Phone not connected")
    
    # Phone control commands
    elif "unlock" in query or "wake up" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_POWER', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 1500 500 500', shell=True)
            speak("Phone unlocked")
        else:
            speak("Phone not connected")
        
    elif "lock" in query or "sleep" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_POWER', shell=True)
            speak("Phone locked")
        else:
            speak("Phone not connected")
        
    elif "volume up" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_VOLUME_UP', shell=True)
            speak("Volume increased")
        else:
            speak("Phone not connected")
        
    elif "volume down" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_VOLUME_DOWN', shell=True)
            speak("Volume decreased")
        else:
            speak("Phone not connected")
        
    elif "mute" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_VOLUME_MUTE', shell=True)
            speak("Phone muted")
        else:
            speak("Phone not connected")
        
    elif "screenshot" in query or "capture screen" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell screencap -p /sdcard/screenshot.png', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe pull /sdcard/screenshot.png .', shell=True)
            speak("Screenshot taken")
        else:
            speak("Phone not connected")
    
    # Screen mirroring
    elif "mirror" in query or "show screen" in query or "display screen" in query:
        if check_adb_connection():
            speak("Starting phone mirroring")
            subprocess.Popen('C:\\scrcpy-win64-v3.3.2\\scrcpy.exe --stay-awake', shell=True)
            speak("Phone screen mirrored")
        else:
            speak("Phone not connected")
    
    elif "stop mirroring" in query or "close screen" in query:
        speak("Stopping screen mirroring")
        subprocess.run('taskkill /f /im scrcpy.exe', shell=True)
        speak("Screen mirroring stopped")
    
    # URL open on phone - handle before generic "open" app routing
    elif "open url on phone" in query or "open link on phone" in query:
        if check_adb_connection():
            import re
            m = re.search(r'(https?://\S+)', query)
            if m:
                url = m.group(1)
                subprocess.run(f'C\\platform-tools\\adb.exe shell am start -a android.intent.action.VIEW -d "{url}"', shell=True)
                speak("Opened link on phone")
            else:
                speak("Please say: open URL on phone followed by the link")
        else:
            speak("Phone not connected")

    # App opening
    elif "open" in query:
        app_name = query.replace("open", "").strip()
        
        phone_apps = {
            'whatsapp': 'com.whatsapp',
            'instagram': 'com.instagram.android', 
            'facebook': 'com.facebook.katana',
            'youtube': 'com.google.android.youtube',
            'gmail': 'com.google.android.gm',
            'chrome': 'com.android.chrome',
            'maps': 'com.google.android.apps.maps',
            'camera': 'com.android.camera',
            'gallery': 'com.miui.gallery',
            'settings': 'com.android.settings'
        }
        
        if app_name in phone_apps:
            if check_adb_connection():
                speak(f"Opening {app_name}")
                subprocess.run(f'C:\\platform-tools\\adb.exe shell monkey -p {phone_apps[app_name]} 1', shell=True)
                speak(f"{app_name} opened")
            else:
                speak("Phone not connected")
        else:
            speak(f"{app_name} not found")
    
    # Advanced gesture controls
    elif "double tap" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 800', shell=True)
            time.sleep(0.1)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 800', shell=True)
            speak("Double tap performed")
        else:
            speak("Phone not connected")
    
    elif "long press" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 800 500 800 1000', shell=True)
            speak("Long press performed")
        else:
            speak("Phone not connected")
    
    elif "scroll up" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 1200 500 800', shell=True)
            speak("Scrolled up")
        else:
            speak("Phone not connected")
    
    elif "scroll down" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 800 500 1200', shell=True)
            speak("Scrolled down")
        else:
            speak("Phone not connected")
    
    elif "zoom in" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 400 600 300 500 & C:\\platform-tools\\adb.exe shell input swipe 600 600 700 700', shell=True)
            speak("Zoomed in")
        else:
            speak("Phone not connected")
    
    elif "zoom out" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 300 500 400 600 & C:\\platform-tools\\adb.exe shell input swipe 700 700 600 600', shell=True)
            speak("Zoomed out")
        else:
            speak("Phone not connected")
    
    # System controls
    elif "wifi on" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell svc wifi enable', shell=True)
            speak("WiFi enabled")
        else:
            speak("Phone not connected")
    
    elif "wifi off" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell svc wifi disable', shell=True)
            speak("WiFi disabled")
        else:
            speak("Phone not connected")
    
    # Removed generic "wifi" handler to avoid duplication; use "wifi on/off" instead
    
    elif "bluetooth on" in query:
        if check_adb_connection():
            # Modern Android supports cmd bluetooth enable
            subprocess.run('C:\\platform-tools\\adb.exe shell cmd bluetooth enable', shell=True)
            speak("Bluetooth enabled")
        else:
            speak("Phone not connected")
    
    elif "bluetooth off" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell cmd bluetooth disable', shell=True)
            speak("Bluetooth disabled")
        else:
            speak("Phone not connected")
    
    # Removed generic "bluetooth" handler to avoid duplication; use "bluetooth on/off" instead
    
    elif "flashlight on" in query or "torch on" in query:
        if check_adb_connection():
            # Try direct torch command first (Android 13+)
            result = subprocess.run('C:\\platform-tools\\adb.exe shell cmd torch on', shell=True)
            if result.returncode != 0:
                # Fallback to quick settings tile
                subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 0 500 800', shell=True)
                time.sleep(1)
                subprocess.run('C:\\platform-tools\\adb.exe shell input tap 200 200', shell=True)
            speak("Flashlight turned on")
        else:
            speak("Phone not connected")
    
    elif "flashlight off" in query or "torch off" in query:
        if check_adb_connection():
            # Try direct torch command first (Android 13+)
            result = subprocess.run('C:\\platform-tools\\adb.exe shell cmd torch off', shell=True)
            if result.returncode != 0:
                # Fallback to quick settings tile
                subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 0 500 800', shell=True)
                time.sleep(1)
                subprocess.run('C:\\platform-tools\\adb.exe shell input tap 200 200', shell=True)
            speak("Flashlight turned off")
        else:
            speak("Phone not connected")
    
    elif "brightness up" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 0 500 800', shell=True)
            time.sleep(1)
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 200 600 700 600', shell=True)
            speak("Brightness increased")
        else:
            speak("Phone not connected")
    
    elif "brightness down" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 0 500 800', shell=True)
            time.sleep(1)
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 700 600 200 600', shell=True)
            speak("Brightness decreased")
        else:
            speak("Phone not connected")
    
    # Media controls
    elif "play music" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_MEDIA_PLAY', shell=True)
            speak("Music playing")
        else:
            speak("Phone not connected")
    
    elif "pause music" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_MEDIA_PAUSE', shell=True)
            speak("Music paused")
        else:
            speak("Phone not connected")
    
    elif "next song" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_MEDIA_NEXT', shell=True)
            speak("Next song")
        else:
            speak("Phone not connected")
    
    elif "previous song" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_MEDIA_PREVIOUS', shell=True)
            speak("Previous song")
        else:
            speak("Phone not connected")
    
    # Smart modes
    elif "bedtime mode" in query or "sleep mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global zen_mode 1', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put system screen_brightness 50', shell=True)
            speak("Bedtime mode activated")
        else:
            speak("Phone not connected")
    
    elif "morning mode" in query or "wake up mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global zen_mode 0', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put system screen_brightness 200', shell=True)
            speak("Morning mode activated")
        else:
            speak("Phone not connected")
    
    elif "driving mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global zen_mode 1', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.google.android.apps.maps 1', shell=True)
            speak("Driving mode activated")
        else:
            speak("Phone not connected")
    
    # Battery and performance
    elif "battery" in query:
        if check_adb_connection():
            result = subprocess.run('C:\\platform-tools\\adb.exe shell dumpsys battery | findstr level', shell=True, capture_output=True, text=True)
            if result.stdout:
                level = result.stdout.split(':')[1].strip()
                speak(f"Battery is at {level} percent")
            else:
                speak("Could not get battery info")
        else:
            speak("Phone not connected")
    
    elif "battery saver" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global low_power 1', shell=True)
            speak("Battery saver enabled")
        else:
            speak("Phone not connected")
    
    elif "dark mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell cmd uimode night yes', shell=True)
            speak("Dark mode enabled")
        else:
            speak("Phone not connected")
    
    elif "light mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell cmd uimode night no', shell=True)
            speak("Light mode enabled")
        else:
            speak("Phone not connected")
    
    # Text input
    elif "type" in query:
        from engine.command import takecommand
        if check_adb_connection():
            speak("What text do you want to type?")
            text = takecommand()
            if text:
                subprocess.run(f'C:\\platform-tools\\adb.exe shell input text "{text}"', shell=True)
                speak("Text entered")
        else:
            speak("Phone not connected")
    
    # Emergency and utility
    elif "find phone" in query or "locate phone" in query:
        if check_adb_connection():
            # Disable DND and raise volumes
            try:
                subprocess.run('C:\\platform-tools\\adb.exe shell settings put global zen_mode 0', shell=True)
            except:
                pass
            try:
                for _ in range(15):
                    subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_VOLUME_UP', shell=True)
                    time.sleep(0.08)
            except:
                pass
            try:
                subprocess.run('C:\\platform-tools\\adb.exe shell cmd audio set-master-mute false', shell=True)
            except:
                pass

            # Try to trigger an alarm/alert activity (varies by OEM)
            alarm_intents = [
                'am start -n com.google.android.deskclock/com.android.deskclock.alerting.AlertFullscreenActivity',
                'am start -n com.google.android.deskclock/com.android.deskclock.AlarmActivity',
                'am start -n com.android.deskclock/.AlarmAlertFullScreen',
                'am start -a com.android.deskclock.ALARM_ALERT'
            ]
            for intent in alarm_intents:
                try:
                    subprocess.run(f'C:\\platform-tools\\adb.exe shell {intent}', shell=True)
                    time.sleep(0.4)
                except:
                    continue

            # Post multiple high-priority notifications (some ROMs play default sound)
            try:
                for _ in range(4):
                    subprocess.run('C:\\platform-tools\\adb.exe shell cmd notification post -t "Find Phone" "jarvis.find" "Phone is here"', shell=True)
                    time.sleep(0.6)
            except:
                pass

            # Try to play a built-in ringtone file via media viewer
            ringtone_candidates = [
                'file:///sdcard/Download/jarvis_ring.ogg',
                'file:///system/media/audio/ringtones/Ring_Synth_04.ogg',
                'file:///system/media/audio/ringtones/Basic_tone.ogg',
                'file:///system/media/audio/ringtones/Orion.ogg',
                'file:///system/media/audio/notifications/Argon.ogg'
            ]
            for uri in ringtone_candidates:
                try:
                    subprocess.run(f'C\\platform-tools\\adb.exe shell am start -a android.intent.action.VIEW -d {uri} -t audio/*', shell=True)
                    time.sleep(0.4)
                    # Try to force playback
                    for _ in range(3):
                        subprocess.run('C\\platform-tools\\adb.exe shell input keyevent KEYCODE_MEDIA_PLAY', shell=True)
                        time.sleep(0.2)
                    # Also try media dispatch play (Android 13+)
                    subprocess.run('C\\platform-tools\\adb.exe shell cmd media dispatch play', shell=True)
                    # Boost volume again just in case
                    for _ in range(3):
                        subprocess.run('C\\platform-tools\\adb.exe shell input keyevent KEYCODE_VOLUME_UP', shell=True)
                        time.sleep(0.1)
                except:
                    continue

            # Removed web URL fallback to avoid opening Chrome
            speak("Phone is ringing to help you find it")
        else:
            speak("Phone not connected")
    
    elif "restart" in query or "reboot" in query:
        if check_adb_connection():
            speak("Restarting phone")
            subprocess.run('C:\\platform-tools\\adb.exe shell reboot', shell=True)
        else:
            speak("Phone not connected")
    
    elif "connection" in query or "status" in query:
        if check_adb_connection():
            speak("Phone is connected and ready")
        else:
            speak("Phone not connected")
    
    # MIUI Specific Features for Redmi 12 5G
    elif "game mode" in query or "gaming mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.gamebooster.ui.GameBoosterMainActivity', shell=True)
            speak("Game mode activated")
        else:
            speak("Phone not connected")
    
    elif "game turbo" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.xiaomi.gamecenter.sdk.service/.GameCenterService', shell=True)
            speak("Game turbo enabled")
        else:
            speak("Phone not connected")
    
    elif "security center" in query or "security app" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.miui.securitycenter 1', shell=True)
            speak("Security center opened")
        else:
            speak("Phone not connected")
    
    elif "cleaner" in query or "clean phone" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.optimizecenter.MainActivity', shell=True)
            speak("Phone cleaner opened")
        else:
            speak("Phone not connected")
    
    elif "boost performance" in query or "performance boost" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.powercenter.PowerCenterActivity', shell=True)
            speak("Performance boost activated")
        else:
            speak("Phone not connected")
    
    elif "mi mover" in query or "clone phone" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.miui.huanji 1', shell=True)
            speak("Mi Mover opened")
        else:
            speak("Phone not connected")
    
    elif "themes" in query or "theme store" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.android.thememanager 1', shell=True)
            speak("Theme store opened")
        else:
            speak("Phone not connected")
    
    elif "mi remote" in query or "infrared" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.duokan.phone.remotecontroller 1', shell=True)
            speak("Mi Remote opened")
        else:
            speak("Phone not connected")
    
    elif "compass" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.miui.compass 1', shell=True)
            speak("Compass opened")
        else:
            speak("Phone not connected")
    
    elif "scanner" in query or "qr scanner" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.xiaomi.scanner 1', shell=True)
            speak("Scanner opened")
        else:
            speak("Phone not connected")
    
    elif "recorder" in query or "voice recorder" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.android.soundrecorder 1', shell=True)
            speak("Voice recorder opened")
        else:
            speak("Phone not connected")
    
    elif "file manager" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.mi.android.globalFileexplorer 1', shell=True)
            speak("File manager opened")
        else:
            speak("Phone not connected")
    
    elif "downloads" in query or "download manager" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.intent.action.VIEW_DOWNLOADS', shell=True)
            speak("Downloads opened")
        else:
            speak("Phone not connected")
    
    # Clipboard and URL handoff
    elif "send clipboard to phone" in query or "clipboard to phone" in query:
        if check_adb_connection():
            try:
                pc_clip = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Clipboard'], capture_output=True, text=True)
                clip_text = (pc_clip.stdout or "").strip()
            except Exception:
                clip_text = ""
            if clip_text:
                safe_text = clip_text.replace('"', '\\"')
                subprocess.run(f'C:\\platform-tools\\adb.exe shell cmd clipboard set "{safe_text}"', shell=True)
                speak("Clipboard sent to phone")
            else:
                speak("PC clipboard is empty")
        else:
            speak("Phone not connected")

    elif "copy from phone clipboard" in query or "get phone clipboard" in query:
        if check_adb_connection():
            result = subprocess.run('C:\\platform-tools\\adb.exe shell cmd clipboard get', shell=True, capture_output=True, text=True)
            phone_clip = (result.stdout or "").strip()
            if phone_clip:
                try:
                    # Use PowerShell here-string to preserve content
                    subprocess.run(['powershell', '-NoProfile', '-Command', f'Set-Clipboard -Value @"\n{phone_clip}\n"@'], shell=False)
                except Exception:
                    pass
                speak("Copied phone clipboard to computer")
            else:
                speak("Phone clipboard is empty")
        else:
            speak("Phone not connected")

    elif "open url on phone" in query or "open link on phone" in query:
        if check_adb_connection():
            import re
            m = re.search(r'(https?://\S+)', query)
            if m:
                url = m.group(1)
                subprocess.run(f'C:\\platform-tools\\adb.exe shell am start -a android.intent.action.VIEW -d "{url}"', shell=True)
                speak("Opened link on phone")
            else:
                speak("Please say: open URL on phone followed by the link")
        else:
            speak("Phone not connected")
    
    # File/Image transfer helpers
    elif "pull latest photo" in query or "get latest photo" in query:
        if check_adb_connection():
            # Try Camera folder first
            result = subprocess.run('C:\\platform-tools\\adb.exe shell ls -t /sdcard/DCIM/Camera | head -1', shell=True, capture_output=True, text=True)
            latest = (result.stdout or "").strip().splitlines()[0] if result.stdout else ""
            if latest:
                subprocess.run(f'C:\\platform-tools\\adb.exe pull /sdcard/DCIM/Camera/{latest} .', shell=True)
                speak("Latest photo saved to computer")
            else:
                speak("Could not find latest photo")
        else:
            speak("Phone not connected")
    
    elif "pull latest screenshot" in query or "get latest screenshot" in query:
        if check_adb_connection():
            result = subprocess.run('C:\\platform-tools\\adb.exe shell ls -t /sdcard/Pictures/Screenshots | head -1', shell=True, capture_output=True, text=True)
            latest = (result.stdout or "").strip().splitlines()[0] if result.stdout else ""
            if latest:
                subprocess.run(f'C:\\platform-tools\\adb.exe pull /sdcard/Pictures/Screenshots/{latest} .', shell=True)
                speak("Latest screenshot saved to computer")
            else:
                speak("Could not find latest screenshot")
        else:
            speak("Phone not connected")
    
    elif "pull recent photos" in query or "get recent photos" in query:
        if check_adb_connection():
            # Pull top 3 recent camera images
            result = subprocess.run('C:\\platform-tools\\adb.exe shell ls -t /sdcard/DCIM/Camera | head -3', shell=True, capture_output=True, text=True)
            files = [f.strip() for f in (result.stdout or "").splitlines() if f.strip()]
            if files:
                for f in files:
                    subprocess.run(f'C:\\platform-tools\\adb.exe pull /sdcard/DCIM/Camera/{f} .', shell=True)
                speak("Recent photos saved to computer")
            else:
                speak("Could not find recent photos")
        else:
            speak("Phone not connected")
    
    elif "push download" in query or "send to phone" in query:
        if check_adb_connection():
            # Expect a filename spoken after the phrase, e.g., "send to phone sample.jpg"
            parts = query.split()
            candidate = None
            for p in parts[::-1]:
                if "." in p and len(p) <= 64:
                    candidate = p
                    break
            if candidate:
                # Push from current directory to phone Downloads
                subprocess.run(f'C:\\platform-tools\\adb.exe push "{candidate}" /sdcard/Download/', shell=True)
                speak("File sent to phone Downloads")
            else:
                speak("Say: send to phone <filename with extension>")
        else:
            speak("Phone not connected")
    
    # Phone calling feature
    elif "call" in query:
        if check_adb_connection():
            from engine.command import takecommand
            speak("What number do you want to call?")
            number = takecommand()
            if number:
                # Extract digits from speech
                import re
                digits = re.findall(r'\d+', number)
                if digits:
                    phone_number = ''.join(digits)
                    subprocess.run(f'C:\\platform-tools\\adb.exe shell am start -a android.intent.action.CALL -d tel:{phone_number}', shell=True)
                    speak(f"Calling {phone_number}")
                else:
                    speak("Could not understand the number")
        else:
            speak("Phone not connected")
    
    # Advanced Camera Controls for Redmi 12 5G
    elif "portrait mode" in query or "portrait camera" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.camera/.Camera', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 150 1800', shell=True)  # Portrait mode
            speak("Portrait mode activated")
        else:
            speak("Phone not connected")
    
    elif "night mode" in query or "night camera" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.camera/.Camera', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 300 1800', shell=True)  # Night mode
            speak("Night mode activated")
        else:
            speak("Phone not connected")
    
    elif "pro mode" in query or "manual camera" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.camera/.Camera', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 450 1800', shell=True)  # Pro mode
            speak("Pro mode activated")
        else:
            speak("Phone not connected")
    
    elif "video mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.camera/.Camera', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 600 1800', shell=True)  # Video mode
            speak("Video mode activated")
        else:
            speak("Phone not connected")
    
    elif "macro mode" in query or "macro camera" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.camera/.Camera', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 750 1800', shell=True)  # Macro mode
            speak("Macro mode activated")
        else:
            speak("Phone not connected")
    
    elif "ultra wide" in query or "wide angle" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.camera/.Camera', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 100 1000', shell=True)  # Ultra wide
            speak("Ultra wide camera activated")
        else:
            speak("Phone not connected")
    
    elif "zoom in camera" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 900 1000', shell=True)  # 2x zoom
            speak("Camera zoomed in")
        else:
            speak("Phone not connected")
    
    elif "flash on" in query or "camera flash on" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 100 200', shell=True)  # Flash toggle
            speak("Camera flash enabled")
        else:
            speak("Phone not connected")
    
    elif "flash off" in query or "camera flash off" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 100 200', shell=True)  # Flash toggle
            speak("Camera flash disabled")
        else:
            speak("Phone not connected")
    
    # MIUI Control Center and Quick Settings
    elif "control center" in query or "quick panel" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 1000 0 1000 800', shell=True)  # Right swipe for control center
            speak("Control center opened")
        else:
            speak("Phone not connected")
    
    elif "notification panel" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 0 500 800', shell=True)  # Left swipe for notifications
            speak("Notification panel opened")
        else:
            speak("Phone not connected")
    
    elif "close panels" in query or "hide panels" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 800 500 0', shell=True)
            speak("Panels closed")
        else:
            speak("Phone not connected")
    
    # MIUI Gestures and Navigation
    elif "recent apps" in query or "app switcher" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_APP_SWITCH', shell=True)
            speak("Recent apps opened")
        else:
            speak("Phone not connected")
    
    elif "clear recent" in query or "close all apps" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_APP_SWITCH', shell=True)
            time.sleep(1)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 1800', shell=True)  # Clear all button
            speak("All apps cleared")
        else:
            speak("Phone not connected")
    
    elif "split screen" in query or "multi window" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell input keyevent KEYCODE_APP_SWITCH', shell=True)
            time.sleep(1)
            subprocess.run('C:\\platform-tools\\adb.exe shell input swipe 500 600 500 300', shell=True)  # Drag app up
            speak("Split screen activated")
        else:
            speak("Phone not connected")
    
    # MIUI System Optimizations
    elif "memory cleanup" in query or "ram cleanup" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am broadcast -a miui.intent.action.CLEAN_MEMORY', shell=True)
            speak("Memory cleaned")
        else:
            speak("Phone not connected")
    
    elif "deep clean" in query or "storage cleanup" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.optimizecenter.MainActivity', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 600', shell=True)  # Deep clean
            speak("Deep cleaning started")
        else:
            speak("Phone not connected")
    
    elif "virus scan" in query or "security scan" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.antivirus.activity.ScanActivity', shell=True)
            speak("Security scan started")
        else:
            speak("Phone not connected")
    
    elif "app lock" in query or "privacy protection" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.applock.AppLockMainActivity', shell=True)
            speak("App lock settings opened")
        else:
            speak("Phone not connected")
    
    elif "dual apps" in query or "clone apps" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.xspace.ui.activity.XSpaceSettingActivity', shell=True)
            speak("Dual apps settings opened")
        else:
            speak("Phone not connected")
    
    # MIUI Connectivity Features
    elif "cast screen" in query or "screen cast" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.CAST_SETTINGS', shell=True)
            speak("Screen cast settings opened")
        else:
            speak("Phone not connected")
    
    elif "mi share" in query or "nearby share" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.miui.mishare.connectivity 1', shell=True)
            speak("Mi Share opened")
        else:
            speak("Phone not connected")
    
    elif "mobile hotspot" in query or "personal hotspot" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.TETHER_SETTINGS', shell=True)
            speak("Mobile hotspot settings opened")
        else:
            speak("Phone not connected")
    
    elif "usb tethering" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.TETHER_SETTINGS', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 400', shell=True)  # USB tethering toggle
            speak("USB tethering toggled")
        else:
            speak("Phone not connected")
    
    # MIUI Display and Sound Enhancements
    elif "reading mode" in query or "eye protection" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put secure night_display_activated 1', shell=True)
            speak("Reading mode enabled")
        else:
            speak("Phone not connected")
    
    elif "disable reading mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put secure night_display_activated 0', shell=True)
            speak("Reading mode disabled")
        else:
            speak("Phone not connected")
    
    elif "refresh rate" in query or "display refresh" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.DISPLAY_SETTINGS', shell=True)
            speak("Display settings opened for refresh rate")
        else:
            speak("Phone not connected")
    
    elif "dolby atmos" in query or "audio enhancement" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.SOUND_SETTINGS', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 800', shell=True)  # Audio effects
            speak("Audio enhancement settings opened")
        else:
            speak("Phone not connected")
    
    # MIUI Battery and Performance
    elif "ultra battery saver" in query or "extreme battery" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global low_power 1', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.powercenter.PowerCenterActivity', shell=True)
            speak("Ultra battery saver enabled")
        else:
            speak("Phone not connected")
    
    elif "performance mode" in query or "high performance" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.powercenter.PowerCenterActivity', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 400', shell=True)  # Performance mode
            speak("Performance mode activated")
        else:
            speak("Phone not connected")
    
    elif "balanced mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.powercenter.PowerCenterActivity', shell=True)
            time.sleep(2)
            subprocess.run('C:\\platform-tools\\adb.exe shell input tap 500 600', shell=True)  # Balanced mode
            speak("Balanced mode activated")
        else:
            speak("Phone not connected")
    
    # MIUI Automation and Smart Features
    elif "shortcuts" in query or "mi shortcuts" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell monkey -p com.miui.mishare.connectivity 1', shell=True)
            speak("Shortcuts opened")
        else:
            speak("Phone not connected")
    
    elif "second space" in query or "private space" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.xspace.ui.activity.XSpaceSettingActivity', shell=True)
            speak("Second space settings opened")
        else:
            speak("Phone not connected")
    
    elif "kids mode" in query or "child mode" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.miui.securitycenter/com.miui.childrenmode.ChildrenModeActivity', shell=True)
            speak("Kids mode activated")
        else:
            speak("Phone not connected")
    
    elif "focus mode" in query or "do not disturb focus" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global zen_mode 3', shell=True)  # Priority only
            speak("Focus mode activated")
        else:
            speak("Phone not connected")
    
    elif "sleep mode" in query or "bedtime focus" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put global zen_mode 1', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put system screen_brightness 30', shell=True)
            subprocess.run('C:\\platform-tools\\adb.exe shell settings put secure night_display_activated 1', shell=True)
            speak("Sleep mode activated")
        else:
            speak("Phone not connected")
    
    # Advanced MIUI System Controls
    elif "developer options" in query or "dev options" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -n com.android.settings/.DevelopmentSettings', shell=True)
            speak("Developer options opened")
        else:
            speak("Phone not connected")
    
    elif "about phone" in query or "phone info" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.DEVICE_INFO_SETTINGS', shell=True)
            speak("About phone opened")
        else:
            speak("Phone not connected")
    
    elif "miui version" in query or "system version" in query:
        if check_adb_connection():
            result = subprocess.run('C:\\platform-tools\\adb.exe shell getprop ro.miui.ui.version.name', shell=True, capture_output=True, text=True)
            if result.stdout:
                version = result.stdout.strip()
                speak(f"MIUI version is {version}")
            else:
                speak("Could not get MIUI version")
        else:
            speak("Phone not connected")
    
    elif "system update" in query or "miui update" in query:
        if check_adb_connection():
            subprocess.run('C:\\platform-tools\\adb.exe shell am start -a android.settings.SYSTEM_UPDATE_SETTINGS', shell=True)
            speak("System update opened")
        else:
            speak("Phone not connected")
    

    
    else:
        return False  # Command not handled
    
    return True  # Command handled