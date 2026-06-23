import requests
import os
import time
import threading

def create_simple_image(prompt):
    """Create image using free API service"""
    def generate():
        try:
            # Use Pollinations AI (free, no login required)
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
            
            print("[Jarvis] Generating image...")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                os.makedirs("images", exist_ok=True)
                filename = f"images/ai_image_{int(time.time())}.jpg"
                
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                print(f"[Jarvis] Image saved as {filename}")
                
                try:
                    from engine.voice_gender_control import voice_control
                    voice_control.speak_with_gender("Image created and saved successfully")
                except:
                    pass
            else:
                print("[Jarvis] Image generation failed")
                
        except Exception as e:
            print(f"[Jarvis] Error: {e}")
    
    threading.Thread(target=generate, daemon=True).start()
    return "Generating image..."