import time
import os
import base64
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def create_image_gemini(prompt):
    """Create image using Gemini in background"""
    def generate_image():
        try:
            # Configure Chrome headless
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get("https://gemini.google.com/")
            
            print("[Jarvis] Generating image in background...")
            
            # Wait and find text input with multiple attempts
            time.sleep(8)
            
            # Try multiple selectors
            text_box = None
            selectors = [
                (By.CSS_SELECTOR, 'textarea[placeholder*="Enter a prompt"]'),
                (By.CSS_SELECTOR, 'div[contenteditable="true"]'),
                (By.TAG_NAME, "textarea"),
                (By.XPATH, "//textarea"),
                (By.XPATH, "//div[@contenteditable='true']")
            ]
            
            for selector_type, selector in selectors:
                try:
                    text_box = driver.find_element(selector_type, selector)
                    break
                except:
                    continue
            
            if not text_box:
                raise Exception("Could not find input field")
            
            # Click and enter text
            text_box.click()
            time.sleep(1)
            text_box.clear()
            text_box.send_keys(f"Create an image of: {prompt}")
            
            # Try to submit
            try:
                text_box.submit()
            except:
                from selenium.webdriver.common.keys import Keys
                text_box.send_keys(Keys.RETURN)
            
            # Wait for generation
            time.sleep(20)
            
            # Find and save image
            try:
                # Look for generated images
                images = driver.find_elements(By.TAG_NAME, "img")
                saved = False
                
                for img in images[-5:]:  # Check last 5 images
                    try:
                        img_src = img.get_attribute("src")
                        
                        if img_src and (img_src.startswith("data:image") or ("http" in img_src and "logo" not in img_src.lower())):
                            os.makedirs("images", exist_ok=True)
                            
                            if img_src.startswith("data:image"):
                                # Base64 image
                                image_data = base64.b64decode(img_src.split(",")[1])
                                filename = f"images/generated_{int(time.time())}.png"
                                
                                with open(filename, "wb") as f:
                                    f.write(image_data)
                            else:
                                # URL image
                                import requests
                                response = requests.get(img_src)
                                if response.status_code == 200 and len(response.content) > 1000:
                                    filename = f"images/generated_{int(time.time())}.jpg"
                                    with open(filename, "wb") as f:
                                        f.write(response.content)
                                else:
                                    continue
                            
                            print(f"[Jarvis] Image saved as {filename}")
                            saved = True
                            
                            # Voice feedback
                            try:
                                from engine.voice_gender_control import voice_control
                                voice_control.speak_with_gender("Image created successfully and saved to images folder")
                            except:
                                pass
                            break
                    except:
                        continue
                
                if not saved:
                    print("[Jarvis] Could not save generated image - may need login or different approach")
                    
            except Exception as e:
                print(f"[Jarvis] Image generation failed: {str(e)}")
                
            driver.quit()
            
        except Exception as e:
            print(f"[Jarvis] Image creator error: {str(e)}")
            try:
                from engine.voice_gender_control import voice_control
                voice_control.speak_with_gender("Image generation failed. Please try again later.")
            except:
                pass
            if 'driver' in locals():
                try:
                    driver.quit()
                except:
                    pass
    
    # Run in background thread
    threading.Thread(target=generate_image, daemon=True).start()
    return "Starting image generation in background..."