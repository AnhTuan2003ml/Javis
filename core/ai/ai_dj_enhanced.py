import subprocess
import pyautogui
import time
from datetime import datetime

def ai_dj_mode_enhanced(command=""):
    try:
        if not command:
            return start_dj_session()
        
        command_lower = command.lower()
        if "party" in command_lower or "upbeat" in command_lower:
            return dj_party_mode()
        elif "chill" in command_lower or "relax" in command_lower:
            return dj_chill_mode()
        elif "focus" in command_lower or "work" in command_lower:
            return dj_focus_mode()
        elif "stop" in command_lower or "off" in command_lower:
            return stop_dj_session()
        else:
            return ai_music_selection(command)
    except Exception as e:
        return f"DJ mode error: {str(e)}"

def start_dj_session():
    try:
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 12:
            return dj_focus_mode()
        elif 13 <= current_hour <= 18:
            return dj_auto_mode()
        elif 19 <= current_hour <= 23:
            return dj_party_mode()
        else:
            return dj_chill_mode()
    except Exception as e:
        return f"DJ session error: {str(e)}"

def dj_party_mode():
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)  # Search box
        time.sleep(1)
        pyautogui.typewrite('party music mix 2024')
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)  # First video
        time.sleep(2)
        return "AI DJ: Party mode activated! Playing YouTube party mix"
    except Exception as e:
        return f"Party mode error: {str(e)}"

def dj_chill_mode():
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite('lofi hip hop study chill music')
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return "AI DJ: Chill mode activated! Playing YouTube lofi mix"
    except Exception as e:
        return f"Chill mode error: {str(e)}"

def dj_focus_mode():
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite('focus music instrumental ambient study')
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return "AI DJ: Focus mode activated! Playing YouTube focus music"
    except Exception as e:
        return f"Focus mode error: {str(e)}"

def dj_auto_mode():
    try:
        playlists = ['top hits 2024', 'pop music mix', 'rock classics', 'indie music', 'electronic dance']
        import random
        playlist = random.choice(playlists)
        
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite(playlist)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return f"AI DJ: Auto mode activated! Playing YouTube {playlist}"
    except Exception as e:
        return f"Auto mode error: {str(e)}"

def ai_music_selection(request):
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite(request[:50])
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return f"AI DJ: Playing YouTube {request}"
    except Exception as e:
        return f"Music selection error: {str(e)}"

def stop_dj_session():
    try:
        pyautogui.press('space')
        return "AI DJ: Session ended. Music paused."
    except Exception as e:
        return f"Stop DJ error: {str(e)}"