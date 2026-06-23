import time
import threading
from datetime import datetime
from engine.voice_advanced_ai import voice_advanced_ai

class ProactiveJarvis:
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start_proactive_mode(self):
        """Start proactive suggestions in background"""
        if self.running:
            print("Proactive mode already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._proactive_loop, daemon=True)
        self.thread.start()
        print("Proactive Jarvis started! Will suggest actions automatically.")
    
    def stop_proactive_mode(self):
        """Stop proactive suggestions"""
        self.running = False
        print("Proactive mode stopped")
    
    def _proactive_loop(self):
        """Main proactive loop"""
        last_check_minute = -1
        
        while self.running:
            try:
                now = datetime.now()
                current_minute = now.minute
                
                # Check every 5 minutes
                if current_minute % 5 == 0 and current_minute != last_check_minute:
                    last_check_minute = current_minute
                    
                    print(f"[{now.strftime('%H:%M')}] Checking for proactive suggestions...")
                    
                    # Check for suggestions
                    suggestion_result = voice_advanced_ai.check_proactive_suggestions()
                    if "Suggested:" in suggestion_result:
                        print(f"SUGGESTION: {suggestion_result}")
                    
                    # Check for high-confidence auto-execution
                    try:
                        auto_result = voice_advanced_ai.auto_execute_if_confident()
                        if "Auto-executed:" in auto_result:
                            print(f"AUTO-EXECUTED: {auto_result}")
                    except:
                        pass  # Method may not exist
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in proactive loop: {e}")
                time.sleep(60)

# Global instance
proactive_jarvis = ProactiveJarvis()

def start_proactive_jarvis():
    """Start proactive Jarvis"""
    proactive_jarvis.start_proactive_mode()

def stop_proactive_jarvis():
    """Stop proactive Jarvis"""
    proactive_jarvis.stop_proactive_mode()

if __name__ == "__main__":
    print("🤖 Starting Proactive Jarvis...")
    print("This will automatically suggest and execute actions based on your patterns.")
    print("Press Ctrl+C to stop.")
    
    start_proactive_jarvis()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping Proactive Jarvis...")
        stop_proactive_jarvis()