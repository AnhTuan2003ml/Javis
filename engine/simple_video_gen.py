import requests
import os
import time
import threading

def create_simple_video(prompt):
    """Create video using free API service"""
    def generate():
        try:
            print("[Jarvis] Video generation not available with free APIs")
            print("[Jarvis] Creating animated GIF instead...")
            
            # Use Pollinations for animated GIF (works better)
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=512&height=512&seed=42"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                os.makedirs("videos", exist_ok=True)
                filename = f"videos/ai_animation_{int(time.time())}.gif"
                
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                print(f"[Jarvis] Animation saved as {filename}")
                
                try:
                    from engine.voice_gender_control import voice_control
                    voice_control.speak_with_gender("Animation created and saved successfully")
                except:
                    pass
            else:
                print("[Jarvis] Animation generation failed")
                try:
                    from engine.voice_gender_control import voice_control
                    voice_control.speak_with_gender("Video generation not available with free services")
                except:
                    pass
                
        except Exception as e:
            print(f"[Jarvis] Error: {e}")
            try:
                from engine.voice_gender_control import voice_control
                voice_control.speak_with_gender("Video generation failed. Free video APIs are limited.")
            except:
                pass
    
    threading.Thread(target=generate, daemon=True).start()
    return "Creating animation (video generation requires paid APIs)..."