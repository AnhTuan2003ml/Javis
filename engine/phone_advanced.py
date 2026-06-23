import subprocess
import threading
import time
import json
from datetime import datetime

class AdvancedPhoneIntegration:
    def __init__(self):
        self.adb_path = r'C:\platform-tools\adb.exe'
        self.sms_monitoring = False
        self.call_monitoring = False
        self.last_sms_count = 0
        self.last_call_state = 'idle'
        
    def start_sms_monitoring(self):
        """Start SMS monitoring"""
        if self.sms_monitoring:
            return
        self.sms_monitoring = True
        threading.Thread(target=self._sms_monitor_loop, daemon=True).start()
    
    def stop_sms_monitoring(self):
        """Stop SMS monitoring"""
        self.sms_monitoring = False
    
    def start_call_monitoring(self):
        """Start call monitoring"""
        if self.call_monitoring:
            print("Call monitoring already running")
            return
        
        self.call_monitoring = True
        call_thread = threading.Thread(target=self._call_monitor_loop, daemon=True)
        call_thread.start()
        print(f"Call monitoring thread started: {call_thread.name}")
    
    def stop_call_monitoring(self):
        """Stop call monitoring"""
        self.call_monitoring = False
    
    def get_latest_sms(self):
        """Get latest SMS message"""
        try:
            result = subprocess.run([
                self.adb_path, 'shell',
                'content query --uri content://sms/inbox --projection address,body,date --sort "date DESC" --limit 1'
            ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                if lines and 'address=' in lines[0]:
                    # Parse the SMS data
                    data = lines[0]
                    address = ''
                    body = ''
                    
                    if 'address=' in data:
                        address = data.split('address=')[1].split(',')[0].strip()
                    if 'body=' in data:
                        body = data.split('body=')[1].split(',')[0].strip()
                    
                    return {
                        'sender': address,
                        'message': body,
                        'time': datetime.now().strftime('%H:%M')
                    }
            return None
        except Exception as e:
            return None
    
    def get_call_state(self):
        """Get current call state"""
        try:
            result = subprocess.run([
                self.adb_path, 'shell',
                'dumpsys telephony.registry | grep "mCallState"'
            ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                if 'mCallState=1' in result.stdout:
                    return 'ringing'
                elif 'mCallState=2' in result.stdout:
                    return 'offhook'
                else:
                    return 'idle'
            return 'idle'
        except Exception as e:
            return 'idle'
    
    def get_incoming_call_number(self):
        """Get incoming call number"""
        try:
            result = subprocess.run([
                self.adb_path, 'shell',
                'dumpsys telephony.registry | grep "mCallIncomingNumber"'
            ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'mCallIncomingNumber=' in line:
                        number = line.split('mCallIncomingNumber=')[1].strip()
                        return number if number != 'null' else 'Unknown'
            return 'Unknown'
        except Exception as e:
            return 'Unknown'
    
    def _sms_monitor_loop(self):
        """SMS monitoring loop"""
        while self.sms_monitoring:
            try:
                # Get SMS count
                result = subprocess.run([
                    self.adb_path, 'shell',
                    'content query --uri content://sms/inbox | wc -l'
                ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
                
                if result.returncode == 0 and result.stdout.strip():
                    current_count = int(result.stdout.strip())
                    
                    if current_count > self.last_sms_count and self.last_sms_count > 0:
                        # New SMS received
                        sms_data = self.get_latest_sms()
                        if sms_data:
                            self.handle_new_sms(sms_data)
                    
                    self.last_sms_count = current_count
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                time.sleep(10)
    
    def _call_monitor_loop(self):
        """Call monitoring loop"""
        print("📞 Call monitoring started")
        while self.call_monitoring:
            try:
                current_state = self.get_call_state()
                
                if current_state != self.last_call_state:
                    print(f"📞 Call state change: {self.last_call_state} → {current_state}")
                    
                    if current_state == 'ringing':
                        # Incoming call
                        caller_number = self.get_incoming_call_number()
                        self.handle_incoming_call(caller_number)
                    elif current_state == 'idle' and self.last_call_state in ['ringing', 'offhook']:
                        # Call ended
                        self.handle_call_ended()
                
                self.last_call_state = current_state
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"Call monitor error: {e}")
                time.sleep(10)
        
        print("📞 Call monitoring stopped")
    
    def handle_new_sms(self, sms_data):
        """Handle new SMS message"""
        try:
            sender = sms_data['sender']
            message = sms_data['message']
            
            # Show Windows notification
            subprocess.run([
                'powershell', '-Command',
                f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; '
                f'$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
                f'$template.SelectSingleNode("//text[@id=1]").InnerText = "📱 SMS from {sender}"; '
                f'$template.SelectSingleNode("//text[@id=2]").InnerText = "{message[:100]}"; '
                f'$toast = [Windows.UI.Notifications.ToastNotification]::new($template); '
                f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis SMS").Show($toast)'
            ], shell=True)
            
            # Speak the SMS (if enabled)
            from engine.features import speak
            speak(f"New message from {sender}. {message}")
            
        except Exception as e:
            pass
    
    def handle_incoming_call(self, caller_number):
        """Handle incoming call"""
        try:
            print(f"📞 INCOMING CALL: {caller_number}")
            
            # Show Windows notification
            subprocess.run([
                'powershell', '-Command',
                f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; '
                f'$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
                f'$template.SelectSingleNode("//text[@id=1]").InnerText = "📞 Incoming Call"; '
                f'$template.SelectSingleNode("//text[@id=2]").InnerText = "From: {caller_number}"; '
                f'$toast = [Windows.UI.Notifications.ToastNotification]::new($template); '
                f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis Calls").Show($toast)'
            ], shell=True)
            
            # Announce the call
            from engine.features import speak
            speak(f"Incoming call from {caller_number}")
            
        except Exception as e:
            print(f"Call notification error: {e}")
    
    def handle_call_ended(self):
        """Handle call ended"""
        try:
            print("📞 CALL ENDED")
            from engine.features import speak
            speak("Call ended")
        except Exception as e:
            pass

# Global instance
phone_advanced = AdvancedPhoneIntegration()