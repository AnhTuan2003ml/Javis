import multiprocessing
import subprocess
import time
import sys
import threading
from datetime import datetime
#python -c "from engine.dual_ai import get_simple_response; result = get_simple_response('trivia game'); print(result)"

#  python -c "from engine.command import allCommands; allCommands('open notepad')"

# Method 1 (Step by step):
#   1. Say: 'send message to akshay'
#   2. When asked mode, say: 'whatsapp'
#   3. When asked message, say: 'your message'

#  Method 1: Say 'phone call to akshay' -> choose 'whatsapp'
def startJarvis():
    try:
        from main import start
        start()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def startChatbot():
    try:
        import os
        os.chdir('chatgpt_clone')
        subprocess.run([sys.executable, 'app.py'])
    except Exception as e:
        print(f"Chatbot error: {e}")

# To run hotword with restart capability
def listenHotword():
    max_restarts = 3
    restart_count = 0
    
    while restart_count < max_restarts:
        try:
            from engine.features import hotword
            hotword()
            break
        except Exception as e:
            restart_count += 1
            if restart_count < max_restarts:
                time.sleep(2)
            else:
                break

# Proactive Jarvis background service with popup suggestions
def runProactiveJarvis():
    try:
        from engine.dual_ai import get_simple_response
        
        get_simple_response('enable_proactive_mode')
        print("Proactive Jarvis started in background")
        
        time.sleep(5)
        
        suggestion_count = 0
        start_time = datetime.now()
        
        while True:
            try:
                now = datetime.now()
                elapsed_minutes = (now - start_time).total_seconds() / 60
                
                # Show suggestions after 1 minute, then after 2 minutes, then stop
                if (elapsed_minutes >= 1 and suggestion_count == 0) or (elapsed_minutes >= 2 and suggestion_count == 1):
                    suggestion_count += 1
                    
                    # Get suggestions based on current time patterns
                    try:
                        suggestions = get_simple_response('suggest actions')
                        if suggestions and isinstance(suggestions, list) and len(suggestions) > 0:
                            # Show toast notification for time-based suggestions
                            try:
                                first_suggestion = suggestions[0] if suggestions else "calculator"
                                suggestion_text = f"You usually use: {first_suggestion} (Click notification to open)"
                                
                                # Show notification and ask for confirmation
                                subprocess.run([
                                    'powershell', '-Command',
                                    f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; '
                                    f'$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
                                    f'$template.SelectSingleNode("//text[@id=1]").InnerText = "Jarvis Smart Suggestions"; '
                                    f'$template.SelectSingleNode("//text[@id=2]").InnerText = "You usually use: {first_suggestion}"; '
                                    f'$toast = [Windows.UI.Notifications.ToastNotification]::new($template); '
                                    f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis").Show($toast)'
                                ], shell=True)
                                

                            except:
                                pass
                    except:
                        pass
                
                # Stop showing suggestions after 2 times
                if suggestion_count >= 2:
                    time.sleep(60)  # Just keep running silently
                else:
                    time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                time.sleep(60)
                
    except Exception as e:
        pass

# Start all processes
if __name__ == '__main__':
    try:
        print("Starting JARVIS...")
        
        p1 = multiprocessing.Process(target=startJarvis, name="JarvisMain")
        p2 = multiprocessing.Process(target=listenHotword, name="HotwordDetection")
        p3 = multiprocessing.Process(target=runProactiveJarvis, name="ProactiveJarvis")
        p4 = multiprocessing.Process(target=startChatbot, name="ChatbotServer")
        
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        
        # Silent startup
        
        p1.join()
        
        if p2.is_alive():
            p2.terminate()
            p2.join(timeout=3)
            if p2.is_alive():
                p2.kill()
                p2.join()
        
        if p3.is_alive():
            p3.terminate()
            p3.join(timeout=3)
            if p3.is_alive():
                p3.kill()
                p3.join()
        
        if p4.is_alive():
            p4.terminate()
            p4.join(timeout=3)
            if p4.is_alive():
                p4.kill()
                p4.join()
        
        print("JARVIS stopped")
        
    except KeyboardInterrupt:
        print("\nStopping...")
        
        if 'p1' in locals() and p1.is_alive():
            p1.terminate()
            p1.join(timeout=3)
            
        if 'p2' in locals() and p2.is_alive():
            p2.terminate()
            p2.join(timeout=3)
            
        if 'p3' in locals() and p3.is_alive():
            p3.terminate()
            p3.join(timeout=3)
        
    except Exception as e:
        print(f"System error: {e}")
        
        # Emergency cleanup
        if 'p1' in locals() and p1.is_alive():
            p1.kill()
            
        if 'p2' in locals() and p2.is_alive():
            p2.kill()
            
        if 'p3' in locals() and p3.is_alive():
            p3.kill()
            
        sys.exit(1)





