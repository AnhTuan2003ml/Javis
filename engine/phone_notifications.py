import subprocess
import threading
import time
import json
from datetime import datetime

class PhoneNotificationMonitor:
    def __init__(self):
        self.adb_path = r'C:\platform-tools\adb.exe'
        self.monitoring = False
        self.last_notifications = []
        
    def get_latest_notification(self):
        """Get the latest notification details using logcat"""
        try:
            # Use logcat to get recent notification content
            result = subprocess.run([
                self.adb_path, 'logcat', '-d', '-s', 'NotificationService', '|', 'tail', '-20'
            ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5, shell=True)
            
            if result.returncode == 0 and result.stdout:
                # Try to extract app and content from logcat
                lines = result.stdout.split('\n')
                for line in reversed(lines):  # Check recent entries first
                    if any(app in line.lower() for app in ['whatsapp', 'instagram', 'telegram', 'gmail']):
                        app_name = 'WhatsApp' if 'whatsapp' in line.lower() else \
                                  'Instagram' if 'instagram' in line.lower() else \
                                  'Telegram' if 'telegram' in line.lower() else \
                                  'Gmail' if 'gmail' in line.lower() else 'Phone'
                        
                        return {
                            'app': app_name,
                            'title': f'New {app_name} message',
                            'text': 'You have a new message',
                            'time': datetime.now().strftime('%H:%M')
                        }
            
            # Fallback: try to get app from active notifications
            result2 = subprocess.run([
                self.adb_path, 'shell', 
                'dumpsys notification | grep -A5 "NotificationRecord" | head -20'
            ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5, shell=True)
            
            if result2.returncode == 0 and result2.stdout:
                if 'whatsapp' in result2.stdout.lower():
                    return {'app': 'WhatsApp', 'title': 'New WhatsApp message', 'text': 'You have a new message', 'time': datetime.now().strftime('%H:%M')}
                elif 'instagram' in result2.stdout.lower():
                    return {'app': 'Instagram', 'title': 'New Instagram notification', 'text': 'You have a new notification', 'time': datetime.now().strftime('%H:%M')}
                elif 'gmail' in result2.stdout.lower():
                    return {'app': 'Gmail', 'title': 'New email', 'text': 'You have a new email', 'time': datetime.now().strftime('%H:%M')}
            
            return self.get_fallback_notification()
        except Exception as e:
            return self.get_fallback_notification()
    
    def parse_latest_notification(self, dump_text):
        """Parse the latest notification from dump"""
        try:
            lines = dump_text.split('\n')
            
            # Find the first (latest) NotificationRecord
            current_notification = {}
            in_notification = False
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                if 'NotificationRecord(' in line and not in_notification:
                    in_notification = True
                    current_notification = {'time': datetime.now().strftime('%H:%M')}
                    continue
                
                if in_notification:
                    # Get package name
                    if 'pkg=' in line and 'app' not in current_notification:
                        try:
                            pkg = line.split('pkg=')[1].split()[0]
                            current_notification['app'] = self.get_app_name(pkg)
                        except:
                            pass
                    
                    # Get title
                    elif 'android.title=' in line and 'title' not in current_notification:
                        try:
                            title_part = line.split('android.title=')[1]
                            # Remove String[length=X] wrapper
                            if 'String [length=' in title_part:
                                # Look for the actual content after the length info
                                if ']' in title_part:
                                    title = title_part.split(']', 1)[1].strip()
                                else:
                                    title = title_part.replace('String [length=', '').split(']')[0]
                            else:
                                title = title_part.strip()
                            
                            if title and len(title) > 2:
                                current_notification['title'] = title[:100]
                        except:
                            pass
                    
                    # Get text content
                    elif 'android.text=' in line and 'text' not in current_notification:
                        try:
                            text_part = line.split('android.text=')[1]
                            # Remove String[length=X] wrapper
                            if 'String [length=' in text_part:
                                if ']' in text_part:
                                    text = text_part.split(']', 1)[1].strip()
                                else:
                                    text = text_part.replace('String [length=', '').split(']')[0]
                            else:
                                text = text_part.strip()
                            
                            if text and len(text) > 2:
                                current_notification['text'] = text[:200]
                        except:
                            pass
                    
                    # Get big text (expanded content)
                    elif 'android.bigText=' in line and len(current_notification.get('text', '')) < 10:
                        try:
                            big_text_part = line.split('android.bigText=')[1]
                            if 'String [length=' in big_text_part:
                                if ']' in big_text_part:
                                    big_text = big_text_part.split(']', 1)[1].strip()
                                else:
                                    big_text = big_text_part.replace('String [length=', '').split(']')[0]
                            else:
                                big_text = big_text_part.strip()
                            
                            if big_text and len(big_text) > 2:
                                current_notification['text'] = big_text[:200]
                        except:
                            pass
                    
                    # Stop at next notification or end of current one
                    elif 'NotificationRecord(' in line or (len(current_notification) >= 3):
                        break
            
            # Return the parsed notification or fallback
            if 'app' in current_notification:
                return {
                    'app': current_notification.get('app', 'Phone'),
                    'title': current_notification.get('title', f"New {current_notification.get('app', 'Phone')} notification"),
                    'text': current_notification.get('text', 'Check your phone for details'),
                    'time': current_notification.get('time', datetime.now().strftime('%H:%M'))
                }
            
            return self.get_fallback_notification()
            
        except Exception as e:
            print(f"Parse error: {e}")
            return self.get_fallback_notification()
    
    def get_fallback_notification(self):
        """Fallback notification when parsing fails"""
        return {
            'app': 'Phone',
            'title': 'New notification received',
            'text': 'Check your phone for details',
            'time': datetime.now().strftime('%H:%M')
        }
    
    def parse_notifications(self, dump_text):
        """Parse notification dump for active notifications"""
        if not dump_text:
            return []
            
        notifications = []
        try:
            lines = dump_text.split('\n')
            
            current_notification = {}
            for line in lines:
                line = line.strip()
                
                if 'NotificationRecord(' in line:
                    if current_notification and 'app' in current_notification:
                        notifications.append(current_notification)
                    current_notification = {'time': datetime.now().strftime('%H:%M')}
                
                elif 'pkg=' in line and current_notification:
                    try:
                        pkg = line.split('pkg=')[1].split()[0]
                        current_notification['app'] = self.get_app_name(pkg)
                    except:
                        pass
                
                elif 'android.title=' in line and current_notification:
                    try:
                        title = line.split('android.title=')[1].strip()
                        current_notification['title'] = title[:50] if title else 'Notification'
                    except:
                        current_notification['title'] = 'Notification'
                
                elif 'android.text=' in line and current_notification:
                    try:
                        text = line.split('android.text=')[1].strip()
                        current_notification['text'] = text[:100] if text else ''
                    except:
                        current_notification['text'] = ''
            
            if current_notification and 'app' in current_notification:
                notifications.append(current_notification)
            
            return notifications[:3]  # Return latest 3
        except Exception as e:
            print(f"Parse error: {e}")
            return []
    
    def get_app_name(self, package):
        """Convert package name to readable app name"""
        app_names = {
            'com.whatsapp': 'WhatsApp',
            'com.instagram.android': 'Instagram',
            'com.facebook.katana': 'Facebook',
            'com.google.android.gm': 'Gmail',
            'com.android.mms': 'Messages',
            'com.spotify.music': 'Spotify',
            'com.youtube.android': 'YouTube'
        }
        return app_names.get(package, package.split('.')[-1].title())
    
    def start_monitoring(self):
        """Start monitoring phone notifications"""
        if self.monitoring:
            return
        
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        last_count = 0
        
        while self.monitoring:
            try:
                # Get notification count
                result = subprocess.run([
                    self.adb_path, 'shell', 
                    'dumpsys notification | grep "NotificationRecord" | wc -l'
                ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
                
                if result.returncode == 0 and result.stdout.strip():
                    current_count = int(result.stdout.strip())
                    
                    # Show notification if count increased (new notification)
                    if current_count > last_count and last_count > 0:
                        # Get latest notification details
                        notification_details = self.get_latest_notification()
                        self.show_notification(notification_details)
                    
                    last_count = current_count
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                time.sleep(30)
    
    def show_notification(self, notification):
        """Show notification on Windows"""
        try:
            app = notification.get('app', 'Phone')
            title = notification.get('title', 'New notification')
            text = notification.get('text', '')
            
            print(f"📱 PHONE NOTIFICATION: {app} - {title} - {text}")
            
            # PowerShell toast notification
            try:
                subprocess.run([
                    'powershell', '-Command',
                    f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; '
                    f'$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
                    f'$template.SelectSingleNode("//text[@id=1]").InnerText = "📱 {app}"; '
                    f'$template.SelectSingleNode("//text[@id=2]").InnerText = "{title} - {text}"; '
                    f'$toast = [Windows.UI.Notifications.ToastNotification]::new($template); '
                    f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis Phone").Show($toast)'
                ], shell=True, timeout=3)
            except Exception as toast_error:
                print(f"Toast error: {toast_error}")
                # Fallback to console notification
                print(f"🔔 {app}: {title}")
                print(f"   {text}")
            
        except Exception as e:
            print(f"Notification error: {e}")

# Global instance
phone_monitor = PhoneNotificationMonitor()