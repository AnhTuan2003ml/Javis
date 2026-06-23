"""
New Features Extension - Single file to add features without modifying dual_ai.py
"""

import subprocess
import os
import datetime
import threading
import time
import socket

# Global instance for external access
_new_features_instance = None

def get_new_feature_response(query):
    """External function to access new features"""
    global _new_features_instance
    if _new_features_instance is None:
        _new_features_instance = NewFeatures()
    return _new_features_instance.execute(query)

def task_reminder(query=""):
    """Direct access to task reminder function"""
    global _new_features_instance
    if _new_features_instance is None:
        _new_features_instance = NewFeatures()
    return _new_features_instance.task_reminder(query)

class NewFeatures:
    def __init__(self):
        # Start continuous monitoring
        self._start_continuous_monitoring()
        
        self.features = {
            # Utility Tools
            'weather_forecast': self.weather_forecast,
            'qr_code_generator': self.qr_code_generator,
            'password_generator': self.password_generator,
            'color_picker': self.color_picker,
            # 'text_to_speech_file': self.text_to_speech_file,
            'image_converter': self.image_converter,
            'empty_trash': self.empty_trash,
            
            # Productivity Tools
            'pomodoro_timer': self.pomodoro_timer,
            'pomodoro_test': self.pomodoro_test,
            'break_reminder': self.break_reminder,
            'word_count': self.word_count,
            'text_cleaner': self.text_cleaner,
            'url_shortener': self.url_shortener,
            
            # File Management
            'duplicate_finder': self.duplicate_finder,
            'file_organizer': self.file_organizer,
            'batch_rename': self.batch_rename,
            'folder_size': self.folder_size,
            'recent_files': self.recent_files,
            'compress_files': self.compress_files,
            'extract_archive': self.extract_archive,
            
            # PDF Operations
            'merge_pdf': self.merge_pdf,
            'split_pdf': self.split_pdf,
            'pdf_to_text': self.pdf_to_text,
            'pdf_to_images': self.pdf_to_images,
            'pdf_encrypt': self.pdf_encrypt,
            'pdf_decrypt': self.pdf_decrypt,
            'pdf_compress': self.pdf_compress,
            'pdf_rotate': self.pdf_rotate,
            'pdf_watermark': self.pdf_watermark,
            
            # Document Conversion
            'images_to_pdf': self.images_to_pdf,
            'word_to_pdf': self.word_to_pdf,
            'excel_to_pdf': self.excel_to_pdf,
            'powerpoint_to_pdf': self.powerpoint_to_pdf,
            'html_to_pdf': self.html_to_pdf,
            'text_to_pdf': self.text_to_pdf,
            
            # Advanced Productivity
            'email_templates': self.email_templates,
            'meeting_scheduler': self.meeting_scheduler,
            'task_reminder': self.task_reminder,
            'list_reminders': self.list_reminders,
            
            # Media Tools
            'image_editor': self.image_editor,
            'audio_converter': self.audio_converter,
            'video_downloader': self.video_downloader,
            
            # Recording Tools
            'voice_recorder': self.voice_recorder,
            'screen_recorder': self.screen_recorder,
            
            # Health & Wellness
            'water_reminder': self.water_reminder,
            'exercise_timer': self.exercise_timer,
            'calorie_calculator': self.calorie_calculator,
            'sleep_tracker': self.sleep_tracker,
            'stress_meter': self.stress_meter,
            'mood_tracker': self.mood_tracker,
            'heart_rate_monitor': self.heart_rate_monitor,
            'medication_reminder': self.medication_reminder,
            'bmi_calculator': self.bmi_calculator,
            'system_monitor': self.system_monitor,
            'network_monitor': self.network_monitor,
            
            # Learning & Education
            'language_translator': self.language_translator,
            'dictionary_lookup': self.dictionary_lookup,
            'wikipedia_search': self.wikipedia_search,
            'calculator_advanced': self.calculator_advanced,
            'unit_converter': self.unit_converter,
            'flashcard_system': self.flashcard_system,
            'quiz_generator': self.quiz_generator,
            
            # Creative Tools
            'meme_generator': self.meme_generator,
            'logo_generator': self.logo_generator,
            'color_palette_generator': self.color_palette_generator,
            'font_viewer': self.font_viewer,
            'ascii_art_generator': self.ascii_art_generator,
            'barcode_generator': self.barcode_generator,
            'mind_map_creator': self.mind_map_creator,
            
            # Security & Development Tools
            'password_manager': self.password_manager,
            'startup_manager': self.startup_manager,
            'git_helper': self.git_helper,
            'port_scanner': self.port_scanner,
            'email_sender': self.email_sender,
            'financial_tools': self.financial_tools,
            'speed_test': self.speed_test,
            'battery_health': self.battery_health,
            'thermal_monitor': self.thermal_monitor,
           
            'disk_health_scanner': self.disk_health_scanner,
            'usb_device_manager': self.usb_device_manager,
            'quick_note_taker': self.quick_note_taker,
            'large_file_scanner': self.large_file_scanner,
            'file_search_engine': self.file_search_engine,
            'recent_files_tracker': self.recent_files_tracker,
            'recently_installed_apps': self.recently_installed_apps,
            'python_packages': self.python_packages,
            
            # Universal App Management
            'open_app': self.open_app,
            'close_app': self.close_app,
            
            # Universal Website Management
            'open_website': self.open_website,
            'close_website': self.close_website,
        }
        
        self.natural_mappings = {
            # Utility Tools
            'weather': 'weather_forecast', 'weather forecast': 'weather_forecast',
            'qr code': 'qr_code_generator', 'generate qr': 'qr_code_generator',
            'password': 'password_generator', 'generate password': 'password_generator',
            'color picker': 'color_picker', 'pick color': 'color_picker',
            # 'text to speech': 'text_to_speech_file', 'convert to audio': 'text_to_speech_file',
            'convert image': 'image_converter', 'image format': 'image_converter',
          
            
            # Productivity Tools
            'pomodoro': 'pomodoro_timer', 'work timer': 'pomodoro_timer',
            'pomodoro test': 'pomodoro_test', 'test timer': 'pomodoro_test',
            'break reminder': 'break_reminder', 'remind break': 'break_reminder',
            'word count': 'word_count', 'count words': 'word_count',
            'clean text': 'text_cleaner', 'format text': 'text_cleaner',
            'shorten url': 'url_shortener', 'short link': 'url_shortener',
            
            # File Management
            'find duplicates': 'duplicate_finder', 'duplicate files': 'duplicate_finder',
            'organize files': 'file_organizer', 'organize downloads': 'file_organizer', 'organize documents': 'file_organizer', 'organize desktop': 'file_organizer', 'organize ': 'file_organizer',
            'rename files': 'batch_rename', 'batch rename': 'batch_rename',
            'folder size': 'folder_size', 'calculate size': 'folder_size',
            'recent files': 'recent_files', 'show recent': 'recent_files',
            'compress files': 'compress_files', 'create zip': 'compress_files',
            'extract archive': 'extract_archive', 'extract zip': 'extract_archive',
            
            # PDF Operations
            'merge pdf': 'merge_pdf', 'combine pdf': 'merge_pdf',
            'split pdf': 'split_pdf', 'divide pdf': 'split_pdf',
            'pdf to text': 'pdf_to_text', 'extract text': 'pdf_to_text',
            'pdf to images': 'pdf_to_images', 'convert pdf': 'pdf_to_images',
            'encrypt pdf': 'pdf_encrypt', 'protect pdf': 'pdf_encrypt', 'pdf encrypt': 'pdf_encrypt',
            'decrypt pdf': 'pdf_decrypt', 'unlock pdf': 'pdf_decrypt', 'pdf decrypt': 'pdf_decrypt',
            'compress pdf': 'pdf_compress', 'reduce pdf': 'pdf_compress',
            'rotate pdf': 'pdf_rotate', 'turn pdf': 'pdf_rotate',
            'watermark pdf': 'pdf_watermark', 'add watermark': 'pdf_watermark',
            
            # Document Conversion
            'images to pdf': 'images_to_pdf', 'create pdf': 'images_to_pdf',
            'word to pdf': 'word_to_pdf', 'docx to pdf': 'word_to_pdf',
            'excel to pdf': 'excel_to_pdf', 'xlsx to pdf': 'excel_to_pdf',
            'powerpoint to pdf': 'powerpoint_to_pdf', 'pptx to pdf': 'powerpoint_to_pdf',
            'html to pdf': 'html_to_pdf', 'webpage to pdf': 'html_to_pdf',
            'text to pdf': 'text_to_pdf', 'txt to pdf': 'text_to_pdf',
            
            # Advanced Productivity
            'email templates': 'email_templates', 'email template': 'email_templates',
            'meeting scheduler': 'meeting_scheduler', 'schedule meeting': 'meeting_scheduler',
            'task reminder': 'task_reminder', 'set reminder': 'task_reminder', 'add reminder': 'task_reminder', 'remind me': 'task_reminder',
            'list reminders': 'list_reminders', 'show reminders': 'list_reminders',
            
            # Media Tools
            'image editor': 'image_editor', 'edit image': 'image_editor',
            'audio converter': 'audio_converter', 'convert audio': 'audio_converter',
            'video downloader': 'video_downloader', 'download video': 'video_downloader',
            
            # Recording Tools
            'voice recorder': 'voice_recorder', 'record voice': 'voice_recorder',
            'screen recorder': 'screen_recorder', 'record screen': 'screen_recorder',
            
            # Health & Wellness
            'water reminder': 'water_reminder', 'hydration tracker': 'water_reminder',
            'exercise timer': 'exercise_timer', 'workout timer': 'exercise_timer',
            'calorie calculator': 'calorie_calculator', 'food tracker': 'calorie_calculator',
            'sleep tracker': 'sleep_tracker', 'bedtime reminder': 'sleep_tracker',
            'stress meter': 'stress_meter', 'wellness check': 'stress_meter',
            'mood tracker': 'mood_tracker', 'mood check': 'mood_tracker',
            'heart rate': 'heart_rate_monitor', 'pulse check': 'heart_rate_monitor',
            'medication reminder': 'medication_reminder', 'pill reminder': 'medication_reminder',
            'bmi calculator': 'bmi_calculator', 'body mass index': 'bmi_calculator',
            'system monitor': 'system_monitor', 'system status': 'system_monitor',
            'network monitor': 'network_monitor', 'network status': 'network_monitor',
            
            # Learning & Education
            'translate': 'language_translator', 'translation': 'language_translator',
            'dictionary': 'dictionary_lookup', 'define': 'dictionary_lookup',
            'wikipedia': 'wikipedia_search', 'wiki': 'wikipedia_search',
            'solve': 'calculator_advanced', 'calculate': 'calculator_advanced',
            'convert': 'unit_converter', 'unit conversion': 'unit_converter',
            'flashcard': 'flashcard_system', 'study cards': 'flashcard_system',
            'quiz': 'quiz_generator', 'test me': 'quiz_generator',
            
            # Creative Tools
            'meme': 'meme_generator', 'create meme': 'meme_generator',
            'logo': 'logo_generator', 'create logo': 'logo_generator',
            'color palette': 'color_palette_generator', 'colors': 'color_palette_generator',
            'font': 'font_viewer', 'fonts': 'font_viewer',
            'ascii art': 'ascii_art_generator', 'ascii': 'ascii_art_generator',
            'barcode': 'barcode_generator', 'qr code': 'qr_code_generator',
            'mind map': 'mind_map_creator', 'mindmap': 'mind_map_creator',
            
            # Security & Development Tools
            'password manager': 'password_manager', 'show password': 'password_manager',
            'startup manager': 'startup_manager', 'startup apps': 'startup_manager',
            'git helper': 'git_helper', 'git commit': 'git_helper', 'git push': 'git_helper',
            'port scanner': 'port_scanner', 'scan ports': 'port_scanner',
            'email sender': 'email_sender', 'send email': 'email_sender', 'schedule email': 'email_sender', 'email later': 'email_sender', 'delayed email': 'email_sender',
            'financial tools': 'financial_tools', 'expense': 'financial_tools', 'currency': 'financial_tools', 'stock': 'financial_tools', 'crypto': 'financial_tools', 'spotify': 'financial_tools', 'movie': 'financial_tools', 'news': 'financial_tools', 'joke': 'financial_tools',
            'speed test': 'speed_test', 'internet speed': 'speed_test', 'check speed': 'speed_test',
            'battery health': 'battery_health', 'battery status': 'battery_health', 'battery check': 'battery_health',
            'thermal monitor': 'thermal_monitor', 'temperature check': 'thermal_monitor', 'cpu temperature': 'thermal_monitor',
           
            'disk health': 'disk_health_scanner', 'check disk': 'disk_health_scanner', 'smart data': 'disk_health_scanner',
            'usb devices': 'usb_device_manager', 'usb manager': 'usb_device_manager', 'connected devices': 'usb_device_manager',
            'quick note': 'quick_note_taker', 'note taker': 'quick_note_taker', 'take note': 'quick_note_taker', 'voice note': 'quick_note_taker',
            'large files': 'large_file_scanner', 'big files': 'large_file_scanner', 'file scanner': 'large_file_scanner', 'space usage': 'large_file_scanner',
            'file search': 'file_search_engine', 'search files': 'file_search_engine', 'find files': 'file_search_engine', 'locate files': 'file_search_engine',
            'recent files': 'recent_files_tracker', 'recent items': 'recent_files_tracker', 'file tracker': 'recent_files_tracker', 'latest files': 'recent_files_tracker',
            'recently installed apps': 'recently_installed_apps', 'installed apps': 'recently_installed_apps', 'new apps': 'recently_installed_apps', 'app history': 'recently_installed_apps',
            'python packages': 'python_packages', 'installed packages': 'python_packages', 'pip list': 'python_packages', 'show packages': 'python_packages',
            
           
           
            'open web': 'open_website', 'close web': 'close_website',
            'Empty recycle bin': 'empty_trash', 'clean recycle bin': 'empty_trash',
        }
    
    def _start_continuous_monitoring(self):
        """Start continuous monitoring threads for battery and thermal"""
        try:
            # Start battery monitoring thread
            battery_thread = threading.Thread(target=self._continuous_battery_monitor, daemon=True)
            battery_thread.start()
            
            # Start thermal monitoring thread  
            thermal_thread = threading.Thread(target=self._continuous_thermal_monitor, daemon=True)
            thermal_thread.start()
            
            # Start reminder monitoring thread
            reminder_thread = threading.Thread(target=self._check_pending_reminders, daemon=True)
            reminder_thread.start()
            
        except Exception as e:
            print(f"Error starting continuous monitoring: {e}")
    
    def _continuous_battery_monitor(self):
        """Continuous battery health monitoring"""
        while True:
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery:
                    # Check for overcharging (>95% and plugged in for too long)
                    if battery.percent > 95 and battery.power_plugged:
                        self._show_notification("🔋 Battery Alert", "Battery over 95% - Consider unplugging to preserve battery health")
                    
                    # Check for low battery
                    elif battery.percent < 20 and not battery.power_plugged:
                        self._show_notification("🔋 Low Battery", f"Battery at {battery.percent}% - Please charge soon")
                
                time.sleep(300)  # Check every 5 minutes
            except Exception:
                time.sleep(600)  # Wait 10 minutes on error
    
    def _continuous_thermal_monitor(self):
        """Continuous thermal monitoring"""
        while True:
            try:
                import psutil
                
                # Check CPU temperature
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            for entry in entries:
                                if entry.current > 85:  # Critical temperature
                                    self._show_notification("🌡️ Critical Temperature", f"{entry.label or name}: {entry.current}°C - System may throttle")
                                elif entry.current > 75:  # Warning temperature
                                    self._show_notification("🌡️ High Temperature", f"{entry.label or name}: {entry.current}°C - Monitor system load")
                except:
                    # Fallback: Monitor CPU usage as temperature indicator
                    cpu_percent = psutil.cpu_percent(interval=1)
                    if cpu_percent > 90:
                        self._show_notification("🌡️ High CPU Load", f"CPU at {cpu_percent}% - May cause overheating")
                
                time.sleep(120)  # Check every 2 minutes
            except Exception:
                time.sleep(300)  # Wait 5 minutes on error
    
    def _check_pending_reminders(self):
        """Check for pending reminders on startup and continuously"""
        import json, os
        from datetime import datetime
        
        while True:
            try:
                reminders_file = "reminders.json"
                if os.path.exists(reminders_file):
                    with open(reminders_file, 'r') as f:
                        reminders = json.load(f)
                    
                    now = datetime.now()
                    active_reminders = []
                    
                    for reminder in reminders:
                        reminder_time = datetime.fromisoformat(reminder['reminder_time'])
                        
                        if reminder_time <= now:
                            # Show overdue reminder
                            self._show_notification("Overdue Reminder!", f"Time to: {reminder['task']}")
                        else:
                            # Keep active reminder
                            active_reminders.append(reminder)
                            
                            # Schedule if due within next minute
                            seconds_left = (reminder_time - now).total_seconds()
                            if seconds_left <= 60:
                                def delayed_reminder(task=reminder['task'], delay=seconds_left):
                                    time.sleep(delay)
                                    self._show_notification("Task Reminder!", f"Time to: {task}")
                                
                                threading.Thread(target=delayed_reminder, daemon=True).start()
                    
                    # Update file with only active reminders
                    if len(active_reminders) != len(reminders):
                        with open(reminders_file, 'w') as f:
                            json.dump(active_reminders, f, indent=2)
                
                time.sleep(30)  # Check every 30 seconds
            except Exception:
                time.sleep(60)  # Wait 1 minute on error
    
    def execute(self, query):
        try:
            # Handle dynamic PDF operations with file paths
            import re
            
            # PDF encrypt with file path
            if 'encrypt pdf' in query.lower() or 'pdf encrypt' in query.lower():
                pattern = r'(?:encrypt pdf|pdf encrypt)\s+(.+)'
                file_match = re.search(pattern, query.lower())
                if file_match:
                    pdf_file = file_match.group(1).strip()
                    result = self.pdf_encrypt(pdf_file)
                    print(result)
                    return result
                result = self.pdf_encrypt()
                print(result)
                return result
            
            # PDF decrypt with file path
            if 'decrypt pdf' in query.lower() or 'pdf decrypt' in query.lower():
                pattern = r'(?:decrypt pdf|pdf decrypt)\s+(.+)'
                file_match = re.search(pattern, query.lower())
                if file_match:
                    pdf_file = file_match.group(1).strip()
                    result = self.pdf_decrypt(pdf_file)
                    print(result)
                    return result
                result = self.pdf_decrypt()
                print(result)
                return result
            
            # Split PDF with file path
            if 'split pdf' in query.lower():
                file_match = re.search(r'split pdf\s+([^\s]+)(?:\s+pages?\s+([\d,-]+))?', query.lower())
                if file_match:
                    pdf_file = file_match.group(1).strip()
                    page_range = file_match.group(2).strip() if file_match.group(2) else None
                    result = self.split_pdf(pdf_file, page_range)
                    print(result)
                    return result
                result = self.split_pdf()
                print(result)
                return result
            
            # Other PDF operations with file paths
            pdf_ops = {
                'merge pdf': (r'merge pdf\s+(.+)', self.merge_pdf),
                'pdf to text': (r'pdf to text\s+(.+)', self.pdf_to_text),
                'pdf to images': (r'pdf to images\s+(.+)', self.pdf_to_images),
                'compress pdf': (r'compress pdf\s+(.+)', self.pdf_compress),
                'rotate pdf': (r'rotate pdf\s+(.+)', self.pdf_rotate),
                'watermark pdf': (r'watermark pdf\s+(.+)', self.pdf_watermark)
            }
            
            for cmd, (pattern, func) in pdf_ops.items():
                if cmd in query.lower():
                    file_match = re.search(pattern, query.lower())
                    if file_match:
                        if cmd == 'merge pdf':
                            files = file_match.group(1).strip().split()
                            result = func(files)
                            print(result)
                            return result
                        else:
                            pdf_file = file_match.group(1).strip()
                            result = func(pdf_file)
                            print(result)
                            return result
                    result = func()
                    print(result)
                    return result
            
            # Check for food tracking (only 'add food' keyword)
            if 'add food' in query.lower():
                return self.calorie_calculator(query)
            
            # Check for password manager first (highest priority for password commands)
            if any(phrase in query.lower() for phrase in ['add', 'store', 'show', 'get']) and 'password' in query.lower():
                return self.password_manager(query)
            if 'password manager' in query.lower():
                return self.password_manager(query)
            
            # Check for creative tools first (highest priority)
            if any(word in query.lower() for word in ['meme', 'create meme']):
                return self.meme_generator(query)
            if any(word in query.lower() for word in ['logo', 'create logo']):
                return self.logo_generator(query)
            if any(word in query.lower() for word in ['color palette', 'colors']) and 'calorie' not in query.lower():
                return self.color_palette_generator(query)
            if any(word in query.lower() for word in ['ascii art', 'ascii']):
                return self.ascii_art_generator(query)
            if 'barcode' in query.lower():
                return self.barcode_generator(query)
            if any(word in query.lower() for word in ['mind map', 'mindmap']):
                return self.mind_map_creator(query)
            
            # Check for learning features (high priority)
            if any(word in query.lower() for word in ['translate', 'translation']):
                return self.language_translator(query)
            if any(word in query.lower() for word in ['define', 'dictionary']):
                return self.dictionary_lookup(query)
            if any(word in query.lower() for word in ['wikipedia', 'wiki']):
                return self.wikipedia_search(query)
            if any(word in query.lower() for word in ['calculate']) and not any(word in query.lower() for word in ['calorie', 'food']):
                return self.calculator_advanced(query)
            if 'convert' in query.lower() and any(word in query.lower() for word in ['meters', 'feet', 'kg', 'pounds', 'celsius', 'fahrenheit']):
                return self.unit_converter(query)
            if any(word in query.lower() for word in ['flashcard', 'study']):
                return self.flashcard_system(query)
            if 'quiz' in query.lower():
                return self.quiz_generator(query)
            
            # Check for email commands (high priority)
            if any(word in query.lower() for word in ['email', 'send email', 'schedule email', 'email later']):
                return self.email_sender(query)
            
            # Check for email writing
            if 'write email' in query.lower() or 'compose email' in query.lower():
                return self.email_templates(query)
            
            # Check for close website commands first
            if any(word in query.lower() for word in ['close ', 'quit ', 'exit ', 'kill ']) and any(word in query.lower() for word in ['web', 'website', 'site', 'browser']):
                return self.close_website(query)
            
            # Check for website commands (highest priority)
            if any(word in query.lower() for word in ['website', 'site', 'web', 'browse']) and any(word in query.lower() for word in ['open ', 'launch ', 'start ', 'run ']) and any(word in query.lower() for word in ['website', 'site', '.com', '.org', '.net']):
                return self.open_website(query)
            
            # Check for universal app commands (high priority)
            if any(word in query.lower() for word in ['open ', 'launch ', 'run ']) and not any(word in query.lower() for word in ['file', 'folder', 'browser', 'website',' writing']):
                return self.open_app(query)
            
            if any(word in query.lower() for word in ['close ', 'quit ', 'exit ', 'kill ']) and not any(word in query.lower() for word in ['file', 'folder', 'browser', 'website']):
                return self.close_app(query)
            
            # Check for exact matches first
            query_lower = query.lower().strip()
            if query_lower in self.features:
                func_name = query_lower
            else:
                # Try natural language understanding first
                func_name = self.natural_mappings.get(query_lower)
                
                if not func_name:
                    # Check for partial matches in natural mappings
                    for key, value in self.natural_mappings.items():
                        if key in query_lower:
                            func_name = value
                            break
                
                if not func_name:
                    func_name = None

            if func_name in self.features:
                # Functions that need query parameter
                query_functions = ['weather_forecast', 'qr_code_generator', 'email_templates', 'meeting_scheduler', 'task_reminder', 'list_reminders', 'image_editor', 'audio_converter', 'video_downloader', 'voice_recorder', 'screen_recorder', 'water_reminder', 'exercise_timer', 'calorie_calculator', 'sleep_tracker', 'stress_meter', 'mood_tracker', 'heart_rate_monitor', 'medication_reminder', 'bmi_calculator', 'system_monitor', 'network_monitor', 'language_translator', 'dictionary_lookup', 'wikipedia_search', 'calculator_advanced', 'unit_converter', 'flashcard_system', 'quiz_generator', 'meme_generator', 'logo_generator', 'color_palette_generator', 'font_viewer', 'ascii_art_generator', 'barcode_generator', 'mind_map_creator', 'password_manager', 'startup_manager', 'git_helper', 'port_scanner', 'email_sender', 'financial_tools', 'speed_test', 'battery_health', 'thermal_monitor', 'quick_note_taker', 'large_file_scanner', 'file_search_engine', 'recent_files_tracker', 'file_organizer', 'open_app', 'close_app', 'open_website', 'close_website']
                
                if func_name in query_functions:
                    result = self.features[func_name](query)
                else:
                    result = self.features[func_name]()
                
                # Standardized response: print for terminal, return for UI
                output = result if result else f"{func_name} completed"
                print(output)
                return output
            else:
                return None
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def understand_natural_speech(self, query):
        """Natural language processing for new features functions"""
        query = query.lower().strip()
        
        mappings = {
            # Utility Tools
            'weather_forecast': ['weather', 'weather forecast', 'how is weather'],
            'qr_code_generator': ['qr code', 'generate qr', 'create qr', 'qr generator'],
            'password_generator': ['password', 'generate password', 'create password'],
            'color_picker': ['color picker', 'pick color', 'get color'],
            # 'text_to_speech_file': ['text to speech', 'convert to audio', 'make audio'],
            'image_converter': ['convert image', 'image format', 'change image'],
            'empty_trash': ['empty trash', 'clear trash', 'clean recycle bin'],
            
            # Productivity Tools
            'pomodoro_timer': ['pomodoro', 'work timer', 'focus timer'],
            'pomodoro_test': ['pomodoro test', 'test timer'],
            'break_reminder': ['break reminder', 'remind break', 'set break'],
            'word_count': ['word count', 'count words'],
            'text_cleaner': ['clean text', 'format text'],
            'url_shortener': ['shorten url', 'short link', 'url shortener'],
            
            # File Management
            'duplicate_finder': ['find duplicates', 'duplicate files'],
            'file_organizer': ['organize files', 'organize downloads'],
            'batch_rename': ['rename files', 'batch rename'],
            'folder_size': ['folder size', 'calculate size'],
            'recent_files': ['recent files', 'show recent'],
            'compress_files': ['compress files', 'create zip', 'make archive'],
            'extract_archive': ['extract archive', 'extract zip', 'unzip'],

            
            
            # PDF Operations
            'merge_pdf': ['merge pdf', 'combine pdf', 'join pdf'],
            'split_pdf': ['split pdf', 'divide pdf', 'separate pdf'],
            'pdf_to_text': ['pdf to text', 'extract text'],
            'pdf_to_images': ['pdf to images', 'convert pdf'],
            'pdf_encrypt': ['encrypt pdf', 'protect pdf', 'secure pdf'],
            'pdf_decrypt': ['decrypt pdf', 'unlock pdf'],
            'pdf_compress': ['compress pdf', 'reduce pdf size'],
            'pdf_rotate': ['rotate pdf', 'turn pdf'],
            'pdf_watermark': ['watermark pdf', 'add watermark'],
            
            # Document Conversion
            'images_to_pdf': ['images to pdf', 'create pdf'],
            'word_to_pdf': ['word to pdf', 'doc to pdf', 'docx to pdf'],
            'excel_to_pdf': ['excel to pdf', 'xls to pdf', 'xlsx to pdf'],
            'powerpoint_to_pdf': ['powerpoint to pdf', 'ppt to pdf', 'pptx to pdf'],
            'html_to_pdf': ['html to pdf', 'web to pdf'],
            'text_to_pdf': ['text to pdf', 'txt to pdf'],
            
            # Advanced Productivity
            'email_templates': ['email templates', 'email template', 'create email', 'email draft'],
            'meeting_scheduler': ['meeting scheduler', 'schedule meeting', 'book meeting', 'calendar meeting'],
            'task_reminder': ['task reminder', 'set reminder', 'remind me', 'task alert', 'add reminder'],
            'list_reminders': ['list reminders', 'show reminders', 'what are reminders', 'my reminders'],
            
            # Media Tools
            'image_editor': ['image editor', 'edit image', 'photo editor', 'image filter'],
            'audio_converter': ['audio converter', 'convert audio', 'audio format', 'mp3 converter'],
            'video_downloader': ['video downloader', 'download video', 'youtube download', 'video download'],
            
            # Recording Tools
            'voice_recorder': ['voice recorder', 'record voice', 'audio recorder', 'voice memo', 'record audio'],
            'screen_recorder': ['screen recorder', 'record screen', 'screen capture', 'record desktop', 'capture screen'],
            
            # Health & Wellness
            'water_reminder': ['water reminder', 'hydration tracker', 'drink water', 'water intake', 'hydration alert'],
            'exercise_timer': ['exercise timer', 'workout timer', 'hiit timer', 'fitness timer', 'interval timer'],
            'calorie_calculator': ['calorie calculator', 'food tracker', 'calorie counter', 'nutrition tracker', 'diet tracker', 'ate', 'add food', 'food'],
            'sleep_tracker': ['sleep tracker', 'bedtime reminder', 'sleep schedule', 'sleep timer', 'bedtime alert', 'bedtime', 'set bedtime', 'wake time', 'set wake'],
            'stress_meter': ['stress meter', 'wellness check', 'stress level', 'mental health', 'stress assessment'],
            'mood_tracker': ['mood tracker', 'mood check', 'how feeling', 'emotional state', 'mood log'],
            'heart_rate_monitor': ['heart rate', 'pulse check', 'heart monitor', 'bpm check', 'pulse rate'],
            'medication_reminder': ['medication reminder', 'pill reminder', 'medicine alert', 'drug reminder', 'take pills'],
            'bmi_calculator': ['bmi calculator', 'body mass index', 'weight check', 'health index', 'body weight'],
            
            # Learning & Education
            'language_translator': ['translate', 'translation', 'translate to', 'convert language'],
            'dictionary_lookup': ['define', 'dictionary', 'definition', 'meaning of', 'what is'],
            'wikipedia_search': ['wikipedia', 'wiki', 'search wiki', 'wiki search'],
            'calculator_advanced': ['calculate', 'calculator', 'math', 'solve', 'compute'],
            'unit_converter': ['convert', 'conversion', 'unit convert', 'change unit'],
            'flashcard_system': ['flashcard', 'study cards', 'flash cards', 'study', 'review cards'],
            'quiz_generator': ['quiz', 'test me', 'generate quiz', 'create quiz', 'quiz on'],
            
            # Creative Tools
            'meme_generator': ['meme', 'create meme', 'generate meme', 'meme generator', 'funny meme'],
            'logo_generator': ['logo', 'create logo', 'design logo', 'logo generator', 'company logo'],
            'color_palette_generator': ['color palette', 'colors', 'color scheme', 'palette', 'color generator'],
            'font_viewer': ['font', 'fonts', 'font viewer', 'preview fonts', 'system fonts'],
            'ascii_art_generator': ['ascii art', 'ascii', 'text art', 'ascii generator', 'character art'],
            'barcode_generator': ['barcode', 'generate barcode', 'create barcode', 'barcode generator'],
            'mind_map_creator': ['mind map', 'mindmap', 'create mind map', 'mind mapping', 'brainstorm'],
            
            # Security & Development Tools
            'password_manager': ['password manager', 'show password', 'get password', 'gmail password', 'password for'],
            'startup_manager': ['startup manager', 'startup apps', 'add startup', 'remove startup', 'manage startup'],
            'git_helper': ['git helper', 'git commit', 'git push', 'git status', 'git add', 'git pull'],
            'port_scanner': ['port scanner', 'scan ports', 'security scan', 'network scan', 'check ports'],
            'email_sender': ['email sender', 'send email', 'send message', 'email to', 'compose and send', 'schedule email', 'email later', 'delayed email', 'send email in', 'email scheduler', 'auto reply', 'auto response', 'enable auto reply', 'disable auto reply'],
            
            # Financial Tools
            'financial_tools': ['expense', 'spending', 'currency', 'convert currency', 'stock price', 'crypto price', 'spotify', 'movie', 'imdb', 'news', 'joke', 'financial tools'],
            
            # System Monitoring
            'battery_health': ['battery health', 'battery status', 'battery check', 'battery info', 'battery cycles'],
            'thermal_monitor': ['thermal monitor', 'temperature check', 'cpu temperature', 'system temperature', 'overheating'],
            
            # Quick Note Taker
            'quick_note_taker': ['quick note', 'note taker', 'take note', 'voice note', 'note', 'remember', 'log', 'record'],
            
            # File Management Tools
            'large_file_scanner': ['large files', 'big files', 'file scanner', 'space usage', 'disk space', 'storage usage'],
            'file_search_engine': ['file search', 'search files', 'find files', 'locate files', 'file finder', 'search engine'],
            'recent_files_tracker': ['recent files', 'recent items', 'file tracker', 'latest files', 'recent documents', 'file history'],
            'recently_installed_apps': ['recently installed apps', 'installed apps', 'new apps', 'app history', 'recent apps', 'latest apps'],
            'python_packages': ['python packages', 'installed packages', 'pip list', 'show packages', 'package list', 'pip packages']
        }
        
        # Check for exact phrase matches first
        for func_name, phrases in mappings.items():
            for phrase in phrases:
                if phrase in query:
                    return func_name
        
        # Special handling for weather with location
        if any(word in query.lower() for word in ['weather']):
            return 'weather_forecast'
        
        # Special handling for bedtime/sleep commands
        if any(word in query for word in ['bedtime', 'wake']):
            return 'sleep_tracker'
        
        # Only trigger calorie calculator for specific food keywords
        if 'add food' in query.lower():
            return 'calorie_calculator'
        
        return None
    
    def weather_forecast(self, query=""):
        try:
            import requests
            import re
            
            # Extract location from query
            location = "current location"
            if query:
                # Remove common weather words to get location
                location_match = re.search(r'weather\s+(?:in\s+|for\s+|at\s+)?(.+)', query.lower())
                if location_match:
                    location = location_match.group(1).strip()
            
            # Use free weather API (wttr.in)
            if location == "current location":
                # Try to get location from IP
                try:
                    ip_response = requests.get('https://ipapi.co/json/', timeout=5)
                    if ip_response.status_code == 200:
                        ip_data = ip_response.json()
                        location = f"{ip_data.get('city', 'Unknown')}, {ip_data.get('country_name', 'Unknown')}"
                except:
                    location = "auto"
            
            # Get weather data from wttr.in (free, no API key needed)
            weather_url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(weather_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Current weather
                current = data['current_condition'][0]
                location_info = data['nearest_area'][0]
                
                temp_c = current['temp_C']
                temp_f = current['temp_F']
                humidity = current['humidity']
                description = current['weatherDesc'][0]['value']
                wind_speed = current['windspeedKmph']
                wind_dir = current['winddir16Point']
                feels_like = current['FeelsLikeC']
                visibility = current['visibility']
                pressure = current['pressure']
                
                # Location details
                area_name = location_info['areaName'][0]['value']
                country = location_info['country'][0]['value']
                
                # Today's forecast
                today_forecast = data['weather'][0]
                max_temp = today_forecast['maxtempC']
                min_temp = today_forecast['mintempC']
                
                # Format weather report
                weather_report = f"Weather for {area_name}, {country}:\n"
                weather_report += f"Current: {temp_c}°C ({temp_f}°F) - {description}\n"
                weather_report += f"Feels like: {feels_like}°C\n"
                weather_report += f"Today: {min_temp}°C to {max_temp}°C\n"
                weather_report += f"Humidity: {humidity}%\n"
                weather_report += f"Wind: {wind_speed} km/h {wind_dir}\n"
                weather_report += f"Pressure: {pressure} mb\n"
                weather_report += f"Visibility: {visibility} km"
                
                return weather_report
            else:
                return f"Weather data not available for '{location}'"
                
        except ImportError:
            return "Weather feature requires: pip install requests"
        except requests.exceptions.RequestException:
            return "Weather service unavailable (check internet connection)"
        except Exception as e:
            return f"Weather forecast failed: {e}"
    
    def password_generator(self, length=12):
        import random, string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        return f"Generated password: {password}"
    
    def color_picker(self):
        try:
            import pyautogui
            x, y = pyautogui.position()
            screenshot = pyautogui.screenshot()
            color = screenshot.getpixel((x, y))
            hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
            return f"Color at cursor: RGB{color} | HEX: {hex_color}"
        except Exception as e:
            return f"Color picker failed: {e}"
    
    # def text_to_speech_file(self, text="Hello from Jarvis"):
    #     try:
    #         import pyttsx3
    #         engine = pyttsx3.init()
            
    #         voices = engine.getProperty('voices')
    #         if voices:
    #             engine.setProperty('voice', voices[0].id)
    #         engine.setProperty('rate', 150)
    #         engine.setProperty('volume', 0.9)
            
    #         filename = f"speech_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    #         engine.save_to_file(text, filename)
    #         engine.runAndWait()
            
    #         return f"🔊 Audio file created: '{filename}' | Text: '{text[:50]}...'" if len(text) > 50 else f"🔊 Audio file created: '{filename}' | Text: '{text}'"
    #     except Exception as e:
    #         return f"Text-to-speech failed: {e}"
    
    def image_converter(self, input_file="image.jpg", output_format="png"):
        try:
            from PIL import Image
            if not os.path.exists(input_file):
                return f"Image file '{input_file}' not found"
            
            output_format = output_format.replace('.', '').lower()
            
            img = Image.open(input_file)
            output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
            
            if output_format in ['jpg', 'jpeg']:
                img = img.convert('RGB')
            
            img.save(output_file)
            return f"✅ Converted '{input_file}' to '{output_file}'"
        except Exception as e:
            return f"Image conversion failed: {e}"
    
    def empty_trash(self):
        try:
            subprocess.run('powershell -c "Clear-RecycleBin -Force"', shell=True)
            return "Recycle bin emptied successfully"
        except Exception as e:
            return f"Empty trash failed: {e}"
    
    def pomodoro_timer(self):
        self._show_notification("🍅 Pomodoro Started", "Working for 25 minutes...")
        
        def timer():
            time.sleep(1500)
            self._show_notification("🍅 Pomodoro Complete!", "Take a 5-minute break. Great work!")
        
        threading.Thread(target=timer, daemon=True).start()
        return "🍅 25-minute Pomodoro timer started - Check your notification!"
    
    def break_reminder(self, minutes=30):
        if minutes <= 0 or minutes > 480:
            minutes = 30
        
        self._show_notification("⏰ Break Reminder Set", f"Will remind you in {minutes} minutes")
        
        def reminder():
            time.sleep(minutes * 60)
            self._show_notification("⏰ Break Time!", f"You've been working for {minutes} minutes. Time for a break!")
        
        threading.Thread(target=reminder, daemon=True).start()
        return f"⏰ Break reminder set for {minutes} minutes - Check your notification!"

    def pomodoro_test(self):
        self._show_notification("🍅 TEST: Pomodoro Started", "Will complete in 10 seconds...")
        
        def test_timer():
            time.sleep(10)
            self._show_notification("🍅 TEST: Pomodoro Complete!", "This was a 10-second test.")
        
        threading.Thread(target=test_timer, daemon=True).start()
        return "🍅 TEST: 10-second Pomodoro timer started - Check notifications!"
    
    def _show_notification(self, title, message):
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            messagebox.showinfo(title, message)
            root.destroy()
        except Exception as e:
            print(f"NOTIFICATION: {title} - {message}")
    
    def word_count(self):
        try:
            import pyperclip
            text = pyperclip.paste()
            words = len(text.split())
            chars = len(text)
            return f"Word count: {words} words, {chars} characters"
        except Exception as e:
            return f"Word count failed: {e}"
    
    def text_cleaner(self):
        try:
            import pyperclip, re
            text = pyperclip.paste()
            cleaned = re.sub(r'\s+', ' ', text).strip()
            pyperclip.copy(cleaned)
            return "Text cleaned and copied to clipboard"
        except Exception as e:
            return f"Text cleaner failed: {e}"
    
    def url_shortener(self, url="https://example.com"):
        try:
            import urllib.parse, urllib.request
            
            parsed = urllib.parse.urlparse(url)
            if not parsed.scheme:
                url = 'https://' + url
            
            api_url = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
            response = urllib.request.urlopen(api_url)
            short_url = response.read().decode('utf-8')
            
            try:
                import pyperclip
                pyperclip.copy(short_url)
                clipboard_msg = " (copied to clipboard)"
            except:
                clipboard_msg = ""
            
            return f"🔗 Short URL: {short_url}{clipboard_msg}"
        except Exception as e:
            return f"URL shortener failed: {e}"
    
    def duplicate_finder(self, folder=None):
        try:
            if folder is None:
                folder = "."
            import hashlib
            files = {}
            duplicates = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        if file_hash in files:
                            duplicates.append((filepath, files[file_hash]))
                        else:
                            files[file_hash] = filepath
                    except:
                        continue
            return f"Found {len(duplicates)} duplicate file pairs in {folder}"
        except Exception as e:
            return f"Duplicate finder failed: {e}"
    
    def file_organizer(self, query=""):
        try:
            # Determine target folder based on query
            folder = None
            if 'documents' in query.lower():
                folder = os.path.join(os.path.expanduser("~"), "Documents")
            elif 'downloads' in query.lower():
                folder = os.path.join(os.path.expanduser("~"), "Downloads")
            elif 'desktop' in query.lower():
                folder = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                # Default to Downloads if no specific folder mentioned
                folder = os.path.join(os.path.expanduser("~"), "Downloads")
            
            # Enhanced file type categorization
            extensions = {
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
                'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'Programs': ['.exe', '.msi', '.dmg', '.deb', '.rpm', '.app'],
                'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb']
            }
            
            if not os.path.exists(folder):
                return f"Folder not found: {folder}"
            
            organized = 0
            total_files = 0
            
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    total_files += 1
                    ext = os.path.splitext(filename)[1].lower()
                    
                    for folder_name, exts in extensions.items():
                        if ext in exts:
                            # Create organized folder
                            organized_folder = os.path.join(folder, folder_name)
                            os.makedirs(organized_folder, exist_ok=True)
                            
                            # Move file to organized folder
                            new_path = os.path.join(organized_folder, filename)
                            if not os.path.exists(new_path):
                                os.rename(filepath, new_path)
                                organized += 1
                            break
            
            result = f"📁 File Organization Complete!\n"
            result += f"Folder: {folder}\n"
            result += f"Total files: {total_files}\n"
            result += f"Organized: {organized} files\n"
            result += f"Remaining: {total_files - organized} files (unknown types)"
            
            if organized > 0:
                self._show_notification("Files Organized", f"Organized {organized} files in {os.path.basename(folder)}")
            
            return result
            
        except Exception as e:
            return f"File organizer failed: {e}"
    
    def batch_rename(self, folder=None, prefix="file_"):
        try:
            if folder is None:
                folder = "."
            count = 0
            for i, filename in enumerate(os.listdir(folder)):
                if os.path.isfile(os.path.join(folder, filename)):
                    ext = os.path.splitext(filename)[1]
                    new_name = f"{prefix}{i+1:03d}{ext}"
                    old_path = os.path.join(folder, filename)
                    new_path = os.path.join(folder, new_name)
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        count += 1
            return f"Renamed {count} files with prefix '{prefix}' in {folder}"
        except Exception as e:
            return f"Batch rename failed: {e}"
    
    def folder_size(self, folder=None):
        try:
            if folder is None:
                folder = "."
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        continue
            size_mb = total_size / (1024 * 1024)
            return f"Folder size: {size_mb:.2f} MB ({total_size:,} bytes) in {folder}"
        except Exception as e:
            return f"Folder size calculation failed: {e}"
    
    def recent_files(self, count=10, folder=None):
        try:
            if folder is None:
                folder = "."
            recent = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(filepath)
                        recent.append((filepath, mtime))
                    except:
                        continue
            recent.sort(key=lambda x: x[1], reverse=True)
            result = f"Recent {count} files in {folder}:\n"
            for filepath, mtime in recent[:count]:
                result += f"- {os.path.basename(filepath)}\n"
            return result
        except Exception as e:
            return f"Recent files failed: {e}"
    
    def qr_code_generator(self, query=""):
        try:
            import qrcode
            from PIL import Image
            import re
            
            # Extract text from query
            text = "Hello World"  # default
            if query:
                # Try to extract text after "qr" or "generate qr"
                text_match = re.search(r'(?:qr|generate qr|qr code)\s+(.+)', query.lower())
                if text_match:
                    text = text_match.group(1).strip()
                elif len(query.strip()) > 0:
                    # If no specific pattern, use the whole query as text
                    text = query.strip()
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="#0078FF", back_color="white").convert('RGB')
            
            filename = f"jarvis_qr_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(filename)
            return f"✅ QR Code generated for '{text}': {filename}"
            
        except ImportError:
            return "QR code library not installed. Run: pip install qrcode[pil] pillow"
        except Exception as e:
            return f"QR code generation failed: {str(e)}"
    
    def compress_files(self, folder=None, output_name=None):
        try:
            import zipfile
            if folder is None:
                folder = "."
            if output_name is None:
                output_name = f"archive_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder)
                        zipf.write(file_path, arcname)
            
            return f"📦 Compressed {folder} to {output_name}"
        except Exception as e:
            return f"Compression failed: {e}"
    
    def extract_archive(self, archive_path=None, extract_to=None):
        try:
            if archive_path is None:
                return "Please specify archive path"
            if extract_to is None:
                extract_to = os.path.splitext(archive_path)[0]
            
            os.makedirs(extract_to, exist_ok=True)
            
            if archive_path.lower().endswith('.zip'):
                import zipfile
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(extract_to)
                return f"📂 Extracted ZIP to {extract_to}"
            elif archive_path.lower().endswith('.rar'):
                try:
                    import rarfile
                    with rarfile.RarFile(archive_path, 'r') as rarf:
                        rarf.extractall(extract_to)
                    return f"📂 Extracted RAR to {extract_to}"
                except ImportError:
                    return "RAR support not installed. Run: pip install rarfile"
            else:
                return "Unsupported archive format. Supports ZIP and RAR only."
        except Exception as e:
            return f"Extraction failed: {e}"
    
    def merge_pdf(self, pdf_files=None):
        try:
            from PyPDF2 import PdfMerger
            if not pdf_files:
                return "Please specify PDF files to merge"
            
            merger = PdfMerger()
            for pdf in pdf_files:
                if os.path.exists(pdf):
                    merger.append(pdf)
            
            output_name = f"merged_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            merger.write(output_name)
            merger.close()
            return f"📄 Merged {len(pdf_files)} PDFs into {output_name}"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF merge failed: {e}"
    
    def split_pdf(self, pdf_file=None, page_range=None):
        try:
            from PyPDF2 import PdfReader, PdfWriter
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            reader = PdfReader(pdf_file)
            base_name = os.path.splitext(pdf_file)[0]
            
            if page_range:
                # Parse page range (e.g., "1-3", "2,4,6", "5")
                pages_to_split = []
                if '-' in page_range:
                    start, end = map(int, page_range.split('-'))
                    pages_to_split = list(range(start-1, min(end, len(reader.pages))))
                elif ',' in page_range:
                    pages_to_split = [int(p.strip())-1 for p in page_range.split(',') if int(p.strip())-1 < len(reader.pages)]
                else:
                    page_num = int(page_range) - 1
                    if 0 <= page_num < len(reader.pages):
                        pages_to_split = [page_num]
                
                for i in pages_to_split:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    output_name = f"{base_name}_page_{i+1}.pdf"
                    with open(output_name, 'wb') as output_file:
                        writer.write(output_file)
                
                return f"📄 Split {len(pages_to_split)} pages from PDF"
            else:
                # Split all pages
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    output_name = f"{base_name}_page_{i+1}.pdf"
                    with open(output_name, 'wb') as output_file:
                        writer.write(output_file)
                
                return f"📄 Split PDF into {len(reader.pages)} pages"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF split failed: {e}"
    
    def pdf_to_text(self, pdf_file=None):
        try:
            from PyPDF2 import PdfReader
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            output_name = f"{os.path.splitext(pdf_file)[0]}.txt"
            with open(output_name, 'w', encoding='utf-8') as f:
                f.write(text)
            
            return f"📝 Extracted text to {output_name}"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF to text failed: {e}"
    
    def pdf_to_images(self, pdf_file=None):
        try:
            try:
                import fitz  # PyMuPDF
            except ImportError:
                return "PDF library not installed. Run: pip install PyMuPDF"
            
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            doc = fitz.open(pdf_file)
            base_name = os.path.splitext(pdf_file)[0]
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                output_name = f"{base_name}_page_{page_num+1}.png"
                pix.save(output_name)
            
            doc.close()
            return f"🖼️ Converted PDF to {len(doc)} images"
        except Exception as e:
            return f"PDF to images failed: {e}"
    
    def images_to_pdf(self, image_folder=None):
        try:
            from PIL import Image
            if not image_folder:
                image_folder = "."
            
            images = []
            for file in os.listdir(image_folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    img_path = os.path.join(image_folder, file)
                    img = Image.open(img_path).convert('RGB')
                    images.append(img)
            
            if images:
                output_name = f"images_to_pdf_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                images[0].save(output_name, save_all=True, append_images=images[1:])
                return f"📄 Created PDF from {len(images)} images: {output_name}"
            else:
                return "No images found in folder"
        except ImportError:
            return "PIL library not installed. Run: pip install Pillow"
        except Exception as e:
            return f"Images to PDF failed: {e}"
    
    def word_to_pdf(self, doc_file=None):
        try:
            import win32com.client
            if not doc_file or not os.path.exists(doc_file):
                return "Please specify valid Word document"
            
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(os.path.abspath(doc_file))
            output_name = f"{os.path.splitext(doc_file)[0]}.pdf"
            doc.SaveAs(os.path.abspath(output_name), FileFormat=17)
            doc.Close()
            word.Quit()
            
            return f"📄 Converted Word to PDF: {output_name}"
        except ImportError:
            return "Word automation not available. Install: pip install pywin32"
        except Exception as e:
            return f"Word to PDF failed: {e}"
    
    def excel_to_pdf(self, excel_file=None):
        try:
            import win32com.client
            if not excel_file or not os.path.exists(excel_file):
                return "Please specify valid Excel file"
            
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            wb = excel.Workbooks.Open(os.path.abspath(excel_file))
            output_name = f"{os.path.splitext(excel_file)[0]}.pdf"
            wb.ExportAsFixedFormat(0, os.path.abspath(output_name))
            wb.Close()
            excel.Quit()
            
            return f"📄 Converted Excel to PDF: {output_name}"
        except ImportError:
            return "Excel automation not available. Install: pip install pywin32"
        except Exception as e:
            return f"Excel to PDF failed: {e}"
    
    def powerpoint_to_pdf(self, ppt_file=None):
        try:
            import win32com.client
            if not ppt_file or not os.path.exists(ppt_file):
                return "Please specify valid PowerPoint file"
            
            ppt = win32com.client.Dispatch("PowerPoint.Application")
            ppt.Visible = 1
            presentation = ppt.Presentations.Open(os.path.abspath(ppt_file))
            output_name = f"{os.path.splitext(ppt_file)[0]}.pdf"
            presentation.SaveAs(os.path.abspath(output_name), 32)
            presentation.Close()
            ppt.Quit()
            
            return f"📄 Converted PowerPoint to PDF: {output_name}"
        except ImportError:
            return "PowerPoint automation not available. Install: pip install pywin32"
        except Exception as e:
            return f"PowerPoint to PDF failed: {e}"
    
    def html_to_pdf(self, html_file=None):
        try:
            import pdfkit
            if not html_file or not os.path.exists(html_file):
                return "Please specify valid HTML file"
            
            output_name = f"{os.path.splitext(html_file)[0]}.pdf"
            pdfkit.from_file(html_file, output_name)
            
            return f"📄 Converted HTML to PDF: {output_name}"
        except ImportError:
            return "HTML to PDF library not installed. Run: pip install pdfkit"
        except Exception as e:
            return f"HTML to PDF failed: {e}"
    
    def text_to_pdf(self, text_file=None):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            if not text_file or not os.path.exists(text_file):
                return "Please specify valid text file"
            
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            output_name = f"{os.path.splitext(text_file)[0]}.pdf"
            c = canvas.Canvas(output_name, pagesize=letter)
            
            lines = text.split('\n')
            y = 750
            for line in lines:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, line[:80])
                y -= 15
            
            c.save()
            return f"📄 Converted text to PDF: {output_name}"
        except ImportError:
            return "PDF library not installed. Run: pip install reportlab"
        except Exception as e:
            return f"Text to PDF failed: {e}"
    
    def pdf_encrypt(self, pdf_file=None, password="jarvis123"):
        try:
            from PyPDF2 import PdfReader, PdfWriter
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            output_name = f"{os.path.splitext(pdf_file)[0]}_encrypted.pdf"
            
            with open(output_name, 'wb') as output_file:
                writer.write(output_file)
            
            return f"🔒 Encrypted PDF: {output_name} (password: {password})"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF encryption failed: {e}"
    
    def pdf_decrypt(self, pdf_file=None, password="jarvis123"):
        try:
            from PyPDF2 import PdfReader, PdfWriter
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            reader = PdfReader(pdf_file)
            if reader.is_encrypted:
                reader.decrypt(password)
            
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            output_name = f"{os.path.splitext(pdf_file)[0]}_decrypted.pdf"
            with open(output_name, 'wb') as output_file:
                writer.write(output_file)
            
            return f"🔓 Decrypted PDF: {output_name}"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF decryption failed: {e}"
    
    def pdf_compress(self, pdf_file=None):
        try:
            from PyPDF2 import PdfReader, PdfWriter
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            output_name = f"{os.path.splitext(pdf_file)[0]}_compressed.pdf"
            with open(output_name, 'wb') as output_file:
                writer.write(output_file)
            
            original_size = os.path.getsize(pdf_file)
            compressed_size = os.path.getsize(output_name)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            return f"🗜️ Compressed PDF: {output_name} ({reduction:.1f}% reduction)"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF compression failed: {e}"
    
    def pdf_rotate(self, pdf_file=None, angle=90):
        try:
            from PyPDF2 import PdfReader, PdfWriter
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)
            
            output_name = f"{os.path.splitext(pdf_file)[0]}_rotated.pdf"
            with open(output_name, 'wb') as output_file:
                writer.write(output_file)
            
            return f"🔄 Rotated PDF {angle}°: {output_name}"
        except ImportError:
            return "PDF library not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF rotation failed: {e}"
    
    def pdf_watermark(self, pdf_file=None, watermark_text="JARVIS"):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from PyPDF2 import PdfReader, PdfWriter
            import io
            
            if not pdf_file or not os.path.exists(pdf_file):
                return "Please specify valid PDF file"
            
            # Create watermark
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 50)
            can.setFillAlpha(0.3)
            can.rotate(45)
            can.drawString(200, 200, watermark_text)
            can.save()
            
            packet.seek(0)
            watermark_pdf = PdfReader(packet)
            
            # Apply watermark
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            for page in reader.pages:
                page.merge_page(watermark_pdf.pages[0])
                writer.add_page(page)
            
            output_name = f"{os.path.splitext(pdf_file)[0]}_watermarked.pdf"
            with open(output_name, 'wb') as output_file:
                writer.write(output_file)
            
            return f"💧 Added watermark to PDF: {output_name}"
        except ImportError:
            return "PDF libraries not installed. Run: pip install PyPDF2 reportlab"
        except Exception as e:
            return f"PDF watermark failed: {e}"
    
    def email_templates(self, query=""):
        try:
            # Check if user wants AI-generated email
            if 'write email' in query.lower() or 'compose email' in query.lower():
                return self._generate_ai_email(query)
            
            # Use predefined templates
            templates = {
                'meeting': "Subject: Meeting Request\n\nHi [Name],\n\nI'd like to schedule a meeting to discuss [Topic]. Are you available [Date/Time]?\n\nBest regards,\n[Your Name]",
                'followup': "Subject: Follow-up on [Topic]\n\nHi [Name],\n\nI wanted to follow up on our previous discussion about [Topic]. Please let me know if you need any additional information.\n\nBest regards,\n[Your Name]",
                'thankyou': "Subject: Thank You\n\nHi [Name],\n\nThank you for [Reason]. I really appreciate your time and assistance.\n\nBest regards,\n[Your Name]",
                'apology': "Subject: Apology\n\nHi [Name],\n\nI apologize for [Issue]. I will ensure this doesn't happen again in the future.\n\nBest regards,\n[Your Name]",
                'outofoffice': "Subject: Out of Office\n\nI am currently out of the office from [Start Date] to [End Date]. I will respond to your email when I return.\n\nFor urgent matters, please contact [Contact Person] at [Email/Phone]."
            }
            
            # Extract template type from query
            template_type = "meeting"  # default
            query_lower = query.lower()
            
            if 'apology' in query_lower or 'sorry' in query_lower:
                template_type = 'apology'
            elif 'followup' in query_lower or 'follow up' in query_lower:
                template_type = 'followup'
            elif 'thank' in query_lower:
                template_type = 'thankyou'
            elif 'out of office' in query_lower or 'vacation' in query_lower:
                template_type = 'outofoffice'
            elif 'meeting' in query_lower:
                template_type = 'meeting'
            
            template = templates.get(template_type, templates['meeting'])
            
            try:
                import pyperclip
                pyperclip.copy(template)
                return f"📧 Email template '{template_type}' copied to clipboard\n\n{template}"
            except ImportError:
                return f"📧 Email template '{template_type}':\n\n{template}"
        except Exception as e:
            return f"Email template failed: {e}"
    
    def _generate_ai_email(self, query):
        try:
            import re
            
            # Extract recipient name
            recipient = "there"
            name_patterns = [
                r'write email (?:to |with )?([a-zA-Z]+)',
                r'email (?:to |with )?([a-zA-Z]+)',
                r'compose email (?:to |with )?([a-zA-Z]+)'
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, query.lower())
                if match:
                    recipient = match.group(1).capitalize()
                    break
            
            # Use AI to generate email content
            try:
                from engine.dual_ai import dual_ai
                
                prompt = f"Write a professional email. User request: '{query}'. Recipient name: '{recipient}'. Include subject line and proper email format. Keep it concise and professional."
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    email_content = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(prompt)
                    email_content = response.text.strip()
                
                # Copy to clipboard
                try:
                    import pyperclip
                    pyperclip.copy(email_content)
                    return f"📧 AI-generated email copied to clipboard\n\n{email_content}"
                except ImportError:
                    return f"📧 AI-generated email:\n\n{email_content}"
                    
            except Exception as ai_error:
                # Fallback to simple template
                fallback_email = f"Subject: Message for {recipient}\n\nHi {recipient},\n\nI hope this email finds you well. I wanted to reach out regarding our recent discussion.\n\nPlease let me know if you have any questions or if there's anything I can help you with.\n\nBest regards,\n[Your Name]"
                
                try:
                    import pyperclip
                    pyperclip.copy(fallback_email)
                    return f"📧 Email generated (AI unavailable) copied to clipboard\n\n{fallback_email}"
                except ImportError:
                    return f"📧 Email generated (AI unavailable):\n\n{fallback_email}"
                    
        except Exception as e:
            return f"AI email generation failed: {e}"
    
    def meeting_scheduler(self, query=""):
        try:
            import webbrowser, re
            from datetime import datetime, timedelta
            
            # Extract duration from query
            duration = "1 hour"  # default
            duration_match = re.search(r'(\d+)\s*(hour|hours|minute|minutes)', query.lower())
            if duration_match:
                duration = f"{duration_match.group(1)} {duration_match.group(2)}"
            
            # Extract participants from query
            participants = "team"  # default
            if 'with' in query.lower():
                parts = query.lower().split('with')
                if len(parts) > 1:
                    participants = parts[1].strip()
            
            # Generate meeting details
            now = datetime.now()
            suggested_time = now + timedelta(days=1)
            meeting_link = "https://meet.google.com/new"
            
            meeting_details = f"""Meeting Scheduler
            
Suggested Time: {suggested_time.strftime('%Y-%m-%d %H:%M')}
Duration: {duration}
Participants: {participants}
Meeting Link: {meeting_link}
            
Calendar Integration:
- Google Calendar: https://calendar.google.com
- Outlook: https://outlook.live.com/calendar
            
Meeting opened in browser for scheduling."""
            
            # Open Google Meet in browser
            webbrowser.open(meeting_link)
            
            return meeting_details
        except Exception as e:
            return f"Meeting scheduler failed: {e}"
    
    def task_reminder(self, query=""):
        try:
            import re, json, os
            from datetime import datetime, timedelta
            
            # Create reminders file in current directory
            reminders_file = "reminders.json"
            
            # Extract task from query
            task = "Take a break"  # default
            if 'remind me to' in query.lower():
                task_match = re.search(r'remind me to (.+?)(?:\s+in|$)', query.lower())
                if task_match:
                    task = task_match.group(1).strip()
            elif 'reminder' in query.lower() and len(query.split()) > 2:
                words = query.split()
                if 'reminder' in [w.lower() for w in words]:
                    idx = [w.lower() for w in words].index('reminder')
                    if idx + 1 < len(words):
                        task = ' '.join(words[idx+1:]).strip()
            
            # Extract time from query
            seconds = 1800  # default 30 minutes
            time_match = re.search(r'(\d+)\s*(second|seconds|minute|minutes|hour|hours)', query.lower())
            if time_match:
                num = int(time_match.group(1))
                unit = time_match.group(2)
                if 'hour' in unit:
                    seconds = num * 3600
                elif 'second' in unit:
                    seconds = num
                else:  # minutes
                    seconds = num * 60
            
            if seconds <= 0 or seconds > 201600:  # max 56 hours
                seconds = 1800
            
            # Calculate reminder time
            reminder_time = datetime.now() + timedelta(seconds=seconds)
            
            # Save reminder to JSON
            reminder_data = {
                "task": task,
                "reminder_time": reminder_time.isoformat(),
                "created_at": datetime.now().isoformat(),
                "seconds": seconds
            }
            
            # Load existing reminders
            reminders = []
            if os.path.exists(reminders_file):
                try:
                    with open(reminders_file, 'r') as f:
                        reminders = json.load(f)
                except:
                    reminders = []
            
            reminders.append(reminder_data)
            
            # Save updated reminders
            with open(reminders_file, 'w') as f:
                json.dump(reminders, f, indent=2)
            
            self._show_notification("Task Reminder Set", f"Will remind you to '{task}' in {seconds} seconds")
            
            def reminder():
                time.sleep(seconds)
                self._show_notification("Task Reminder!", f"Time to: {task}")
                
                # Remove completed reminder
                try:
                    if os.path.exists(reminders_file):
                        with open(reminders_file, 'r') as f:
                            current_reminders = json.load(f)
                        updated_reminders = [r for r in current_reminders if r != reminder_data]
                        with open(reminders_file, 'w') as f:
                            json.dump(updated_reminders, f, indent=2)
                except:
                    pass
            
            threading.Thread(target=reminder, daemon=True).start()
            
            return f"Task reminder set: '{task}' at {reminder_time.strftime('%H:%M:%S')} ({seconds} seconds)"
        except Exception as e:
            return f"Task reminder failed: {e}"
    
    def list_reminders(self, query=""):
        try:
            import json, os
            from datetime import datetime
            
            reminders_file = "reminders.json"
            
            if not os.path.exists(reminders_file):
                return "No reminders found. Create your first reminder!"
            
            with open(reminders_file, 'r') as f:
                reminders = json.load(f)
            
            if not reminders:
                return "No active reminders found."
            
            result = "Active Reminders:\n" + "="*30 + "\n"
            
            for i, reminder in enumerate(reminders, 1):
                task = reminder.get('task', 'Unknown task')
                reminder_time = datetime.fromisoformat(reminder.get('reminder_time', ''))
                created_at = datetime.fromisoformat(reminder.get('created_at', ''))
                
                now = datetime.now()
                if reminder_time > now:
                    time_left = reminder_time - now
                    minutes_left = int(time_left.total_seconds() / 60)
                    if minutes_left > 60:
                        hours = minutes_left // 60
                        mins = minutes_left % 60
                        time_str = f"{hours}h {mins}m remaining"
                    else:
                        time_str = f"{minutes_left}m remaining"
                    status = "ACTIVE"
                else:
                    time_str = "OVERDUE"
                    status = "OVERDUE"
                
                result += f"{i}. [{status}] {task}\n"
                result += f"   {time_str}\n"
                result += f"   Due: {reminder_time.strftime('%H:%M')}\n\n"
            
            result += f"Total: {len(reminders)} reminders"
            return result
        except Exception as e:
            return f"Failed to list reminders: {e}"
    
    def image_editor(self, query=""):
        try:
            try:
                from PIL import Image, ImageFilter, ImageEnhance
            except ImportError:
                return "Image library not installed. Run: pip install Pillow"
            
            import re
            
            # Extract file path from query
            file_match = re.search(r'(?:edit|image)\s+(.+?)(?:\s+(?:blur|sharp|bright|contrast|gray|resize)|$)', query.lower())
            if file_match:
                file_path = file_match.group(1).strip()
            else:
                return "Please specify image file: 'image editor filename.jpg blur'"
            
            if not os.path.exists(file_path):
                return f"Image file not found: {file_path}"
            
            img = Image.open(file_path)
            base_name = os.path.splitext(file_path)[0]
            
            # Apply filters based on query
            if 'blur' in query.lower():
                img = img.filter(ImageFilter.BLUR)
                output = f"{base_name}_blur.jpg"
            elif 'sharpen' in query.lower():
                img = img.filter(ImageFilter.SHARPEN)
                output = f"{base_name}_sharp.jpg"
            elif 'bright' in query.lower():
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.5)
                output = f"{base_name}_bright.jpg"
            elif 'contrast' in query.lower():
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
                output = f"{base_name}_contrast.jpg"
            elif 'grayscale' in query.lower() or 'gray' in query.lower():
                img = img.convert('L')
                output = f"{base_name}_gray.jpg"
            elif 'resize' in query.lower():
                img = img.resize((800, 600))
                output = f"{base_name}_resized.jpg"
            else:
                # Default: apply multiple filters
                img = img.filter(ImageFilter.ENHANCE)
                output = f"{base_name}_enhanced.jpg"
            
            img.save(output)
            return f"🖼️ Image edited: {output}"
        except Exception as e:
            return f"Image editor failed: {e}"
    
    def audio_converter(self, query=""):
        try:
            try:
                from pydub import AudioSegment
            except ImportError:
                return "Audio library not installed. Run: pip install pydub"
            
            import re
            
            # Extract file path from query
            file_match = re.search(r'(?:convert|audio)\s+(.+?)(?:\s+(?:to|mp3|wav|flac|aac|ogg)|$)', query.lower())
            if file_match:
                file_path = file_match.group(1).strip()
            else:
                return "Please specify audio file: 'audio converter song.mp3 to wav'"
            
            if not os.path.exists(file_path):
                return f"Audio file not found: {file_path}"
            
            # Detect input format
            input_ext = os.path.splitext(file_path)[1].lower()
            base_name = os.path.splitext(file_path)[0]
            
            # Determine output format from query
            if 'mp3' in query.lower():
                output_format = 'mp3'
            elif 'wav' in query.lower():
                output_format = 'wav'
            elif 'flac' in query.lower():
                output_format = 'flac'
            elif 'aac' in query.lower():
                output_format = 'aac'
            elif 'ogg' in query.lower():
                output_format = 'ogg'
            else:
                output_format = 'mp3'  # default
            
            # Load and convert audio
            audio = AudioSegment.from_file(file_path)
            output_path = f"{base_name}.{output_format}"
            
            # Export with format-specific settings
            if output_format == 'mp3':
                audio.export(output_path, format="mp3", bitrate="192k")
            elif output_format == 'wav':
                audio.export(output_path, format="wav")
            elif output_format == 'flac':
                audio.export(output_path, format="flac")
            else:
                audio.export(output_path, format=output_format)
            
            return f"🎵 Audio converted to {output_format.upper()}: {output_path}"
        except Exception as e:
            return f"Audio converter failed: {e}"
    
    def video_downloader(self, query=""):
        try:
            try:
                import yt_dlp
            except ImportError:
                return "Video downloader not installed. Run: pip install yt-dlp"
            
            import re
            
            # Extract URL from query
            url_pattern = r'https?://[^\s]+'
            url_match = re.search(url_pattern, query)
            
            if not url_match:
                return "Please provide video URL: 'video downloader https://youtube.com/watch?v=...'"
            
            url = url_match.group()
            
            # Configure download options
            ydl_opts = {
                'format': 'best[height<=720]',  # Max 720p for faster download
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
            }
            
            # Determine quality from query
            if 'audio' in query.lower() or 'mp3' in query.lower():
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            elif '1080' in query.lower():
                ydl_opts['format'] = 'best[height<=1080]'
            elif '480' in query.lower():
                ydl_opts['format'] = 'best[height<=480]'
            
            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                
                ydl.download([url])
                
            return f"📹 Downloaded: {title[:50]}..."
        except Exception as e:
            return f"Video download failed: {e}"
    
    def voice_recorder(self, query=""):
        try:
            import pyaudio
            import wave
            import threading
            import time
            from datetime import datetime
            
            # Extract duration from query (default 30 seconds)
            duration = 30
            import re
            duration_match = re.search(r'(\d+)\s*(second|seconds|minute|minutes)', query.lower())
            if duration_match:
                num = int(duration_match.group(1))
                unit = duration_match.group(2)
                if 'minute' in unit:
                    duration = num * 60
                else:
                    duration = num
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"voice_memo_{timestamp}.wav"
            
            # Immediate response with voice feedback
            response_msg = f"Starting voice recording for {duration} seconds"
            
            def record_audio():
                try:
                    print(f"🎤 Recording audio for {duration} seconds...")
                    
                    # Audio settings
                    CHUNK = 1024
                    FORMAT = pyaudio.paInt16
                    CHANNELS = 1
                    RATE = 44100
                    
                    # Initialize PyAudio
                    p = pyaudio.PyAudio()
                    
                    # Start recording
                    stream = p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)
                    
                    frames = []
                    
                    # Record audio
                    for i in range(0, int(RATE / CHUNK * duration)):
                        data = stream.read(CHUNK)
                        frames.append(data)
                    
                    # Stop recording
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    
                    # Save audio file
                    wf = wave.open(filename, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    
                    print(f"🎤 Voice recording saved: {filename}")
                    
                    # Optional: Convert to text using speech recognition
                    if 'text' in query.lower() or 'transcribe' in query.lower():
                        try:
                            print("📝 Converting speech to text...")
                            import speech_recognition as sr
                            r = sr.Recognizer()
                            with sr.AudioFile(filename) as source:
                                audio = r.record(source)
                            text = r.recognize_google(audio)
                            
                            # Save transcription
                            text_filename = f"transcription_{timestamp}.txt"
                            with open(text_filename, 'w', encoding='utf-8') as f:
                                f.write(text)
                            
                            print(f"📝 Transcription saved: {text_filename}")
                            print(f"Text: {text[:100]}..." if len(text) > 100 else f"Text: {text}")
                        except Exception as e:
                            print(f"📝 Transcription failed: {e}")
                        
                except Exception as e:
                    print(f"🎤 Recording failed: {e}")
            
            # Start recording in background thread
            threading.Thread(target=record_audio, daemon=True).start()
            
            return response_msg
            
        except ImportError:
            return "Audio library not installed. Run: pip install pyaudio wave"
        except Exception as e:
            return f"Voice recording failed: {e}"
    
    def screen_recorder(self, query=""):
        try:
            import cv2
            import numpy as np
            import pyautogui
            import threading
            import time
            from datetime import datetime
            
            # Extract duration from query (default 30 seconds)
            duration = 30
            import re
            duration_match = re.search(r'(\d+)\s*(second|seconds|minute|minutes)', query.lower())
            if duration_match:
                num = int(duration_match.group(1))
                unit = duration_match.group(2)
                if 'minute' in unit:
                    duration = num * 60
                else:
                    duration = num
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screen_recording_{timestamp}.mp4"
            
            # Immediate response with voice feedback
            response_msg = f"Starting screen recording for {duration} seconds"
            
            def record_screen():
                try:
                    print(f"📹 Recording screen for {duration} seconds...")
                    
                    # Get screen dimensions
                    screen_size = pyautogui.size()
                    
                    # Define codec and create VideoWriter
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    fps = 20.0
                    out = cv2.VideoWriter(filename, fourcc, fps, screen_size)
                    
                    # Record screen
                    start_time = datetime.now()
                    frames_recorded = 0
                    
                    while (datetime.now() - start_time).seconds < duration:
                        # Capture screenshot
                        img = pyautogui.screenshot()
                        
                        # Convert PIL image to OpenCV format
                        frame = np.array(img)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        
                        # Write frame to video
                        out.write(frame)
                        frames_recorded += 1
                        
                        # Control frame rate
                        time.sleep(1/fps)
                    
                    # Release everything
                    out.release()
                    cv2.destroyAllWindows()
                    
                    print(f"📹 Screen recording saved: {filename} ({frames_recorded} frames)")
                    
                except Exception as e:
                    print(f"📹 Recording failed: {e}")
            
            # Start recording in background thread
            threading.Thread(target=record_screen, daemon=True).start()
            
            return response_msg
            
        except ImportError:
            return "Screen recording libraries not installed. Run: pip install opencv-python pyautogui"
        except Exception as e:
            return f"Screen recording failed: {e}"
    
    def _load_health_data(self):
        """Load health data from JSON file"""
        default_data = {
            'water_intake': {'daily_goal': 8, 'today': 0, 'last_reminder': None, 'history': []},
            'exercise': {'sessions': [], 'weekly_goal': 5, 'current_week': 0},
            'calories': {'daily_goal': 2000, 'today': 0, 'foods': [], 'history': []},
            'sleep': {'bedtime': '22:00', 'wake_time': '06:00', 'reminders': True, 'history': []},
            'stress': {'levels': [], 'last_check': None, 'weekly_average': 0},
            'mood': {'entries': [], 'weekly_average': 0, 'last_check': None},
            'heart_rate': {'readings': [], 'resting_hr': 70, 'last_check': None},
            'medications': {'pills': [], 'reminders': []},
            'bmi': {'height': 170, 'weight': 70, 'history': []}
        }
        
        try:
            import json
            if os.path.exists('health_data.json'):
                with open('health_data.json', 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_data.items():
                        if key not in loaded_data:
                            loaded_data[key] = value
                    return loaded_data
        except:
            pass
        
        return default_data
    
    def _save_health_data(self, data):
        """Save health data to JSON file"""
        try:
            import json
            with open('health_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save health data: {e}")
    
    def water_reminder(self, query=""):
        try:
            import json, re
            from datetime import datetime, timedelta
            
            data = self._load_health_data()
            water_data = data['water_intake']
            
            # Check if user wants to log water intake
            if any(word in query.lower() for word in ['drink', 'drank', 'add', 'had']):
                try:
                    # Use AI to extract water amount and type
                    from engine.dual_ai import dual_ai
                    
                    ai_prompt = f'''Extract water/drink information from: "{query}"
                    
Respond ONLY in this format:
Drink: [drink type]
Amount: [number in ml]
                    
Examples:
Drink: water
Amount: 500

Drink: coffee
Amount: 250

Drink: juice
Amount: 300
                    
Convert glasses/cups to ml (1 glass = 250ml, 1 cup = 240ml, 1 liter = 1000ml).'''
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    
                    # Parse AI response
                    drink_match = re.search(r'Drink:\s*(.+)', ai_response, re.IGNORECASE)
                    amount_match = re.search(r'Amount:\s*(\d+)', ai_response, re.IGNORECASE)
                    
                    if drink_match and amount_match:
                        drink_type = drink_match.group(1).strip().lower()
                        amount = int(amount_match.group(1))
                        
                        # AI hydration analysis
                        hydration_value = amount if drink_type in ['water', 'herbal tea'] else amount * 0.7
                        
                        water_data['today'] += hydration_value
                        water_data['history'].append({
                            'timestamp': datetime.now().isoformat(),
                            'amount': hydration_value,
                            'drink_type': drink_type,
                            'original_amount': amount
                        })
                        
                        glasses_today = water_data['today'] / 250
                        remaining = max(0, water_data['daily_goal'] - glasses_today)
                        
                        self._save_health_data(data)
                        
                        # AI health tip
                        if drink_type not in ['water', 'herbal tea']:
                            tip = f" (Note: {drink_type} provides less hydration than pure water)"
                        else:
                            tip = " (Excellent hydration choice!)"
                        
                        self._show_notification("Hydration Logged", f"{drink_type.title()}: {amount}ml. Hydration: {hydration_value:.0f}ml")
                        
                        return f"Added {amount}ml {drink_type} (hydration value: {hydration_value:.0f}ml). Today: {glasses_today:.1f}/{water_data['daily_goal']} glasses. Remaining: {remaining:.1f}{tip}"
                    
                except Exception:
                    # Fallback to basic parsing
                    amount_match = re.search(r'(\d+)\s*(ml|glass|glasses|cup|cups|liter|liters)', query.lower())
                    if amount_match:
                        amount = int(amount_match.group(1))
                        unit = amount_match.group(2)
                        if 'glass' in unit or 'cup' in unit:
                            amount *= 250
                        elif 'liter' in unit:
                            amount *= 1000
                    else:
                        amount = 250
                    
                    water_data['today'] += amount
                    water_data['history'].append({
                        'timestamp': datetime.now().isoformat(),
                        'amount': amount
                    })
                    
                    glasses_today = water_data['today'] / 250
                    remaining = max(0, water_data['daily_goal'] - glasses_today)
                    
                    self._save_health_data(data)
                    self._show_notification("Water Logged", f"Added {amount}ml. Today: {glasses_today:.1f}/{water_data['daily_goal']} glasses")
                    
                    return f"Water logged: {amount}ml. Today: {glasses_today:.1f}/{water_data['daily_goal']} glasses. Remaining: {remaining:.1f} glasses"
            
            # Set up hourly reminders
            elif 'start' in query.lower() or 'enable' in query.lower():
                def hourly_reminder():
                    while True:
                        time.sleep(3600)  # 1 hour
                        current_data = self._load_health_data()
                        glasses_today = current_data['water_intake']['today'] / 250
                        goal = current_data['water_intake']['daily_goal']
                        
                        if glasses_today < goal:
                            remaining = goal - glasses_today
                            self._show_notification("Hydration Reminder", f"Time to drink water! {remaining:.1f} glasses remaining today")
                
                threading.Thread(target=hourly_reminder, daemon=True).start()
                return "Hourly water reminders started. Stay hydrated!"
            
            # Show current status
            else:
                glasses_today = water_data['today'] / 250
                remaining = max(0, water_data['daily_goal'] - glasses_today)
                
                status = f"Water Intake Today: {glasses_today:.1f}/{water_data['daily_goal']} glasses\n"
                status += f"Remaining: {remaining:.1f} glasses ({remaining * 250:.0f}ml)\n"
                
                if water_data['history']:
                    last_drink = water_data['history'][-1]
                    last_time = datetime.fromisoformat(last_drink['timestamp'])
                    time_ago = datetime.now() - last_time
                    hours_ago = time_ago.total_seconds() / 3600
                    status += f"Last drink: {hours_ago:.1f} hours ago"
                
                return status
                
        except Exception as e:
            return f"Water reminder failed: {e}"
    
    def exercise_timer(self, query=""):
        try:
            import re
            from datetime import datetime, timedelta
            
            data = self._load_health_data()
            exercise_data = data['exercise']
            
            try:
                # Use AI to create personalized workout
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Create a workout plan from: "{query}"
                
Respond ONLY in this format:
Workout: [workout type]
Rounds: [number]
Work: [seconds]
Rest: [seconds]
Intensity: [Low/Medium/High]
                
Examples:
Workout: HIIT
Rounds: 5
Work: 30
Rest: 10
Intensity: High

Workout: Cardio
Rounds: 3
Work: 60
Rest: 30
Intensity: Medium
                
Adjust based on user request or use defaults for HIIT.'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                # Parse AI response
                workout_match = re.search(r'Workout:\s*(.+)', ai_response, re.IGNORECASE)
                rounds_match = re.search(r'Rounds:\s*(\d+)', ai_response, re.IGNORECASE)
                work_match = re.search(r'Work:\s*(\d+)', ai_response, re.IGNORECASE)
                rest_match = re.search(r'Rest:\s*(\d+)', ai_response, re.IGNORECASE)
                intensity_match = re.search(r'Intensity:\s*(.+)', ai_response, re.IGNORECASE)
                
                if all([workout_match, rounds_match, work_match, rest_match]):
                    workout_type = workout_match.group(1).strip()
                    rounds = int(rounds_match.group(1))
                    work_time = int(work_match.group(1))
                    rest_time = int(rest_match.group(1))
                    intensity = intensity_match.group(1).strip() if intensity_match else "Medium"
                else:
                    raise Exception("AI parsing failed")
                    
            except Exception:
                # Fallback to basic parsing
                work_time = 30
                rest_time = 10
                rounds = 5
                workout_type = "HIIT"
                intensity = "Medium"
                
                work_match = re.search(r'work\s+(\d+)\s*(second|seconds|minute|minutes)', query.lower())
                if work_match:
                    work_time = int(work_match.group(1))
                    if 'minute' in work_match.group(2):
                        work_time *= 60
                
                rest_match = re.search(r'rest\s+(\d+)\s*(second|seconds|minute|minutes)', query.lower())
                if rest_match:
                    rest_time = int(rest_match.group(1))
                    if 'minute' in rest_match.group(2):
                        rest_time *= 60
                
                rounds_match = re.search(r'(\d+)\s*rounds?', query.lower())
                if rounds_match:
                    rounds = int(rounds_match.group(1))
            
            # AI-enhanced workout response
            response_msg = f"Starting {workout_type}: {rounds} rounds, {work_time}s work, {rest_time}s rest ({intensity} intensity)"
            
            def hiit_timer():
                try:
                    print(f"🏃 Starting HIIT workout: {rounds} rounds")
                    
                    for round_num in range(1, rounds + 1):
                        # Work phase
                        self._show_notification(f"🏃 Round {round_num}/{rounds}", f"WORK! {work_time} seconds")
                        print(f"🏃 Round {round_num}/{rounds} - WORK! {work_time}s")
                        time.sleep(work_time)
                        
                        # Rest phase (except last round)
                        if round_num < rounds:
                            self._show_notification(f"😴 Rest Time", f"Rest for {rest_time} seconds")
                            print(f"😴 Rest for {rest_time}s")
                            time.sleep(rest_time)
                    
                    # Workout complete
                    total_time = rounds * work_time + (rounds - 1) * rest_time
                    
                    # Log workout
                    exercise_data['sessions'].append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'HIIT',
                        'duration': total_time,
                        'rounds': rounds,
                        'work_time': work_time,
                        'rest_time': rest_time
                    })
                    exercise_data['current_week'] += 1
                    
                    self._save_health_data(data)
                    
                    self._show_notification("🎉 Workout Complete!", f"Great job! {total_time//60}min {total_time%60}s workout finished")
                    print(f"🎉 Workout complete! Total time: {total_time//60}min {total_time%60}s")
                    
                except Exception as e:
                    print(f"🏃 Exercise timer failed: {e}")
            
            threading.Thread(target=hiit_timer, daemon=True).start()
            return response_msg
            
        except Exception as e:
            return f"Exercise timer failed: {e}"
    
    def calorie_calculator(self, query=""):
        try:
            import re
            from datetime import datetime
            
            data = self._load_health_data()
            calorie_data = data['calories']
            
            # Add food using AI
            if any(word in query.lower() for word in ['add', 'ate', 'eat', 'drink', 'had']):
                try:
                    # Use AI to extract food and estimate calories
                    from engine.dual_ai import dual_ai
                    
                    ai_prompt = f'''Extract food information from: "{query}"
                    
Respond ONLY in this exact format (no extra text):
Food: [food name]
Quantity: [number]
Calories: [estimated calories per serving]
                    
Examples:
Food: banana
Quantity: 2
Calories: 105

Food: sushi roll
Quantity: 1
Calories: 200

Food: chocolate cookie
Quantity: 3
Calories: 120
                    
Estimate realistic calories per serving. Always include all three lines.'''
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    
                    # Parse AI response
                    food_match = re.search(r'Food:\s*(.+)', ai_response, re.IGNORECASE)
                    qty_match = re.search(r'Quantity:\s*(\d+)', ai_response, re.IGNORECASE)
                    cal_match = re.search(r'Calories:\s*(\d+)', ai_response, re.IGNORECASE)
                    
                    if food_match and cal_match:
                        food_name = food_match.group(1).strip().lower()
                        quantity = int(qty_match.group(1)) if qty_match else 1
                        calories_per_serving = int(cal_match.group(1))
                        
                        total_calories = calories_per_serving * quantity
                        calorie_data['today'] += total_calories
                        
                        calorie_data['foods'].append({
                            'timestamp': datetime.now().isoformat(),
                            'food': food_name,
                            'quantity': quantity,
                            'calories': total_calories
                        })
                        
                        remaining = max(0, calorie_data['daily_goal'] - calorie_data['today'])
                        
                        self._save_health_data(data)
                        self._show_notification("🍎 Food Logged", f"{food_name.title()}: {total_calories} cal. Today: {calorie_data['today']}/{calorie_data['daily_goal']}")
                        
                        return f"🍎 Added {quantity}x {food_name}: {total_calories} calories. Today: {calorie_data['today']}/{calorie_data['daily_goal']}. Remaining: {remaining}"
                    else:
                        return "🍎 Could not identify food from your message. Try: 'ate 2 apples' or 'add pizza'"
                        
                except Exception as ai_error:
                    # Fallback to basic food database
                    food_db = {
                        'apple': 95, 'banana': 105, 'orange': 62, 'bread': 80, 'rice': 130,
                        'chicken': 165, 'beef': 250, 'fish': 140, 'egg': 70, 'milk': 150,
                        'pizza': 285, 'burger': 540, 'pasta': 220, 'salad': 50, 'yogurt': 100,
                        'coffee': 5, 'tea': 2, 'soda': 140, 'water': 0, 'juice': 110
                    }
                    
                    for food, calories_per_serving in food_db.items():
                        if food in query.lower():
                            qty_match = re.search(rf'(\d+)\s*{food}', query.lower())
                            quantity = int(qty_match.group(1)) if qty_match else 1
                            
                            total_calories = calories_per_serving * quantity
                            calorie_data['today'] += total_calories
                            
                            calorie_data['foods'].append({
                                'timestamp': datetime.now().isoformat(),
                                'food': food,
                                'quantity': quantity,
                                'calories': total_calories
                            })
                            
                            remaining = max(0, calorie_data['daily_goal'] - calorie_data['today'])
                            
                            self._save_health_data(data)
                            self._show_notification("🍎 Food Logged", f"{food.title()}: {total_calories} cal. Today: {calorie_data['today']}/{calorie_data['daily_goal']}")
                            
                            return f"🍎 Added {quantity}x {food}: {total_calories} calories. Today: {calorie_data['today']}/{calorie_data['daily_goal']}. Remaining: {remaining}"
                    
                    return "🍎 Food not recognized. Try: 'ate sandwich' or 'add 2 cookies'"
            
            # Show status
            else:
                remaining = max(0, calorie_data['daily_goal'] - calorie_data['today'])
                over = max(0, calorie_data['today'] - calorie_data['daily_goal'])
                
                status = f"🍎 Calories Today: {calorie_data['today']}/{calorie_data['daily_goal']}\n"
                
                if over > 0:
                    status += f"Over goal by: {over} calories\n"
                else:
                    status += f"Remaining: {remaining} calories\n"
                
                if calorie_data['foods']:
                    status += "\nToday's meals:\n"
                    for food in calorie_data['foods'][-5:]:  # Last 5 items
                        time_str = datetime.fromisoformat(food['timestamp']).strftime('%H:%M')
                        status += f"- {time_str}: {food['quantity']}x {food['food']} ({food['calories']} cal)\n"
                
                return status
                
        except Exception as e:
            return f"Calorie calculator failed: {e}"
    
    def sleep_tracker(self, query=""):
        try:
            import re
            from datetime import datetime, timedelta, time
            
            data = self._load_health_data()
            sleep_data = data['sleep']
            
            # AI-powered sleep optimization
            if 'bedtime' in query.lower() or 'set' in query.lower():
                try:
                    # Use AI to optimize sleep schedule
                    from engine.dual_ai import dual_ai
                    
                    ai_prompt = f'''Optimize sleep schedule from: "{query}"
                    
Respond ONLY in this format:
Bedtime: [HH:MM in 24h format]
Wake: [HH:MM in 24h format]
Optimal: [Yes/No]
Advice: [sleep optimization tip]
                    
Examples:
Bedtime: 22:30
Wake: 06:30
Optimal: Yes
Advice: Perfect 8-hour sleep cycle

Bedtime: 01:00
Wake: 07:00
Optimal: No
Advice: Try sleeping earlier for better recovery
                    
Recommend 7-9 hours of sleep for optimal health.'''
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_response)
                        ai_response = response.text.strip()
                    
                    # Parse AI response
                    bedtime_match = re.search(r'Bedtime:\s*(\d{1,2}:\d{2})', ai_response, re.IGNORECASE)
                    wake_match = re.search(r'Wake:\s*(\d{1,2}:\d{2})', ai_response, re.IGNORECASE)
                    optimal_match = re.search(r'Optimal:\s*(Yes|No)', ai_response, re.IGNORECASE)
                    advice_match = re.search(r'Advice:\s*(.+)', ai_response, re.IGNORECASE)
                    
                    if bedtime_match:
                        sleep_data['bedtime'] = bedtime_match.group(1)
                        if wake_match:
                            sleep_data['wake_time'] = wake_match.group(1)
                        
                        optimal = optimal_match.group(1) if optimal_match else "Unknown"
                        advice = advice_match.group(1) if advice_match else "Maintain consistent sleep schedule"
                        
                        sleep_data['ai_advice'] = advice
                        self._save_health_data(data)
                        
                        return f"😴 AI-optimized schedule set\nBedtime: {sleep_data['bedtime']}\nWake: {sleep_data['wake_time']}\nOptimal: {optimal}\nAI Advice: {advice}"
                        
                except Exception:
                    # Fallback to basic parsing
                    time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(pm|am)?', query.lower())
                    if time_match:
                        hour = int(time_match.group(1))
                        minute = int(time_match.group(2)) if time_match.group(2) else 0
                        period = time_match.group(3)
                        
                        if period == 'pm' and hour != 12:
                            hour += 12
                        elif period == 'am' and hour == 12:
                            hour = 0
                        
                        sleep_data['bedtime'] = f"{hour:02d}:{minute:02d}"
                        self._save_health_data(data)
                        
                        return f"😴 Bedtime set to {sleep_data['bedtime']}. Sleep reminders enabled."
            
            # Set wake time
            elif 'wake' in query.lower():
                time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(pm|am)?', query.lower())
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2)) if time_match.group(2) else 0
                    period = time_match.group(3)
                    
                    if period == 'pm' and hour != 12:
                        hour += 12
                    elif period == 'am' and hour == 12:
                        hour = 0
                    
                    sleep_data['wake_time'] = f"{hour:02d}:{minute:02d}"
                    self._save_health_data(data)
                    
                    return f"⏰ Wake time set to {sleep_data['wake_time']}"
            
            # Start sleep reminders
            elif 'start' in query.lower() or 'enable' in query.lower():
                def sleep_reminder():
                    while True:
                        try:
                            current_data = self._load_health_data()
                            bedtime_str = current_data['sleep']['bedtime']
                            bedtime_hour, bedtime_min = map(int, bedtime_str.split(':'))
                            
                            now = datetime.now()
                            bedtime_today = now.replace(hour=bedtime_hour, minute=bedtime_min, second=0, microsecond=0)
                            
                            # If bedtime has passed today, set for tomorrow
                            if now > bedtime_today:
                                bedtime_today += timedelta(days=1)
                            
                            # Calculate time until bedtime
                            time_until = bedtime_today - now
                            
                            # Remind 30 minutes before bedtime
                            if time_until.total_seconds() <= 1800:  # 30 minutes
                                self._show_notification("😴 Bedtime Soon", f"Bedtime in {int(time_until.total_seconds()//60)} minutes. Start winding down!")
                                time.sleep(1800)  # Wait 30 minutes before next check
                            else:
                                time.sleep(900)  # Check every 15 minutes
                                
                        except Exception as e:
                            time.sleep(3600)  # Wait 1 hour on error
                
                threading.Thread(target=sleep_reminder, daemon=True).start()
                return f"😴 Sleep reminders started. Bedtime: {sleep_data['bedtime']}, Wake: {sleep_data['wake_time']}"
            
            # Show sleep schedule
            else:
                bedtime_hour, bedtime_min = map(int, sleep_data['bedtime'].split(':'))
                wake_hour, wake_min = map(int, sleep_data['wake_time'].split(':'))
                
                # Calculate sleep duration
                bedtime_minutes = bedtime_hour * 60 + bedtime_min
                wake_minutes = wake_hour * 60 + wake_min
                
                if wake_minutes < bedtime_minutes:
                    wake_minutes += 24 * 60  # Next day
                
                sleep_duration = (wake_minutes - bedtime_minutes) / 60
                
                status = f"😴 Sleep Schedule:\n"
                status += f"Bedtime: {sleep_data['bedtime']}\n"
                status += f"Wake time: {sleep_data['wake_time']}\n"
                status += f"Sleep duration: {sleep_duration:.1f} hours\n"
                
                if sleep_duration < 7:
                    status += "⚠️ Consider getting more sleep (7-9 hours recommended)"
                elif sleep_duration > 9:
                    status += "⚠️ You might be sleeping too much (7-9 hours recommended)"
                else:
                    status += "✅ Good sleep duration!"
                
                return status
                
        except Exception as e:
            return f"Sleep tracker failed: {e}"
    
    def stress_meter(self, query=""):
        try:
            import re
            from datetime import datetime, timedelta
            
            data = self._load_health_data()
            stress_data = data['stress']
            
            # AI-powered stress analysis
            if any(word in query.lower() for word in ['level', 'feel', 'stressed', 'rate', 'anxious', 'overwhelmed']):
                try:
                    # Use AI to analyze stress from description
                    from engine.dual_ai import dual_ai
                    
                    ai_prompt = f'''Analyze stress level from: "{query}"
                    
Respond ONLY in this format:
Stress: [1-10]
Cause: [main stress cause]
Recommendation: [specific advice]
                    
Examples:
Stress: 7
Cause: work pressure
Recommendation: Take 5-minute breathing break

Stress: 3
Cause: mild fatigue
Recommendation: Stay hydrated and rest
                    
Rate 1-10 where 1=very calm, 10=extremely stressed.'''
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    
                    # Parse AI response
                    stress_match = re.search(r'Stress:\s*(\d+)', ai_response, re.IGNORECASE)
                    cause_match = re.search(r'Cause:\s*(.+)', ai_response, re.IGNORECASE)
                    rec_match = re.search(r'Recommendation:\s*(.+)', ai_response, re.IGNORECASE)
                    
                    if stress_match:
                        stress_level = int(stress_match.group(1))
                        cause = cause_match.group(1).strip() if cause_match else "general stress"
                        ai_recommendation = rec_match.group(1).strip() if rec_match else "Take deep breaths"
                    else:
                        raise Exception("AI parsing failed")
                        
                except Exception:
                    # Fallback to manual input
                    level_match = re.search(r'(\d+)', query)
                    if level_match:
                        stress_level = int(level_match.group(1))
                        cause = "user reported"
                        ai_recommendation = "Basic stress management"
                    else:
                        return "🧘 Please describe your stress or rate it 1-10. Example: 'stress level 5' or 'feeling overwhelmed'"
                
                if 1 <= stress_level <= 10:
                    stress_data['levels'].append({
                        'timestamp': datetime.now().isoformat(),
                        'level': stress_level,
                        'cause': cause,
                        'ai_recommendation': ai_recommendation
                    })
                    
                    # AI-enhanced weekly analysis
                    week_ago = datetime.now() - timedelta(days=7)
                    recent_levels = [
                        entry['level'] for entry in stress_data['levels']
                        if datetime.fromisoformat(entry['timestamp']) > week_ago
                    ]
                    
                    if recent_levels:
                        stress_data['weekly_average'] = sum(recent_levels) / len(recent_levels)
                        
                        # AI trend analysis
                        if len(recent_levels) >= 3:
                            trend = "increasing" if recent_levels[-1] > recent_levels[-3] else "decreasing" if recent_levels[-1] < recent_levels[-3] else "stable"
                            trend_msg = f" (Trend: {trend})"
                        else:
                            trend_msg = ""
                    else:
                        trend_msg = ""
                    
                    stress_data['last_check'] = datetime.now().isoformat()
                    self._save_health_data(data)
                    
                    # AI-enhanced recommendations
                    if stress_level >= 8:
                        self._show_notification("🧘 High Stress Alert", f"Cause: {cause}. {ai_recommendation}")
                    elif stress_level >= 6:
                        self._show_notification("🧘 Stress Notice", f"Moderate stress from {cause}")
                    
                    return f"🧘 Stress logged: {stress_level}/10\nCause: {cause}\nWeekly average: {stress_data['weekly_average']:.1f}{trend_msg}\nAI Advice: {ai_recommendation}"
                else:
                    return "🧘 Please rate stress level 1-10 (1=very calm, 10=very stressed)"
            
            # Quick stress assessment
            elif 'check' in query.lower() or 'assess' in query.lower():
                questions = [
                    "Rate your current stress (1-10):",
                    "1 = Very calm and relaxed",
                    "5 = Moderate stress",
                    "10 = Extremely stressed"
                ]
                
                assessment = "🧘 Quick Stress Assessment:\n" + "\n".join(questions)
                assessment += "\n\nBreathing Exercise: Inhale 4 counts → Hold 4 → Exhale 4 → Repeat 5 times"
                
                return assessment
            
            # Show stress history
            else:
                if not stress_data['levels']:
                    return "🧘 No stress data yet. Try: 'stress level 5' to log your current stress."
                
                # Recent stress levels
                recent = stress_data['levels'][-7:]  # Last 7 entries
                
                status = f"🧘 Stress Overview:\n"
                status += f"Weekly average: {stress_data['weekly_average']:.1f}/10\n"
                
                if stress_data['last_check']:
                    last_time = datetime.fromisoformat(stress_data['last_check'])
                    hours_ago = (datetime.now() - last_time).total_seconds() / 3600
                    status += f"Last check: {hours_ago:.1f} hours ago\n"
                
                status += "\nRecent levels:\n"
                for entry in recent:
                    time_str = datetime.fromisoformat(entry['timestamp']).strftime('%m/%d %H:%M')
                    level = entry['level']
                    status += f"- {time_str}: {level}/10\n"
                
                # Stress management tips
                if stress_data['weekly_average'] >= 7:
                    status += "\n⚠️ High stress detected. Consider: meditation, exercise, or talking to someone."
                elif stress_data['weekly_average'] >= 5:
                    status += "\n💡 Moderate stress. Try: regular breaks, deep breathing, or light exercise."
                else:
                    status += "\n✅ Good stress management! Keep it up."
                
                return status
                
        except Exception as e:
            return f"Stress meter failed: {e}"
    
    def mood_tracker(self, query=""):
        try:
            import re
            from datetime import datetime, timedelta
            
            data = self._load_health_data()
            mood_data = data['mood']
            
            # AI-powered mood analysis
            if any(word in query.lower() for word in ['feel', 'mood', 'happy', 'sad', 'angry', 'anxious', 'excited', 'tired']):
                try:
                    from engine.dual_ai import dual_ai
                    
                    ai_prompt = f'''Analyze mood from: "{query}"
                    
Respond ONLY in this format:
Mood: [1-10]
Emotion: [primary emotion]
Trigger: [what caused this mood]
Suggestion: [mood improvement tip]
                    
Examples:
Mood: 8
Emotion: happy
Trigger: good news
Suggestion: Share your joy with others

Mood: 4
Emotion: stressed
Trigger: work pressure
Suggestion: Take a short walk
                    
Rate 1-10 where 1=very negative, 10=very positive.'''
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    
                    # Parse AI response
                    mood_match = re.search(r'Mood:\s*(\d+)', ai_response, re.IGNORECASE)
                    emotion_match = re.search(r'Emotion:\s*(.+)', ai_response, re.IGNORECASE)
                    trigger_match = re.search(r'Trigger:\s*(.+)', ai_response, re.IGNORECASE)
                    suggestion_match = re.search(r'Suggestion:\s*(.+)', ai_response, re.IGNORECASE)
                    
                    if mood_match:
                        mood_score = int(mood_match.group(1))
                        emotion = emotion_match.group(1).strip() if emotion_match else "neutral"
                        trigger = trigger_match.group(1).strip() if trigger_match else "general"
                        suggestion = suggestion_match.group(1).strip() if suggestion_match else "Stay positive"
                    else:
                        raise Exception("AI parsing failed")
                        
                except Exception:
                    # Fallback mood detection
                    positive_words = ['happy', 'great', 'good', 'excited', 'amazing', 'wonderful']
                    negative_words = ['sad', 'bad', 'angry', 'tired', 'stressed', 'awful']
                    
                    mood_score = 5  # neutral
                    emotion = "neutral"
                    
                    for word in positive_words:
                        if word in query.lower():
                            mood_score = 8
                            emotion = word
                            break
                    
                    for word in negative_words:
                        if word in query.lower():
                            mood_score = 3
                            emotion = word
                            break
                    
                    trigger = "user reported"
                    suggestion = "Practice mindfulness"
                
                if 1 <= mood_score <= 10:
                    mood_data['entries'].append({
                        'timestamp': datetime.now().isoformat(),
                        'score': mood_score,
                        'emotion': emotion,
                        'trigger': trigger,
                        'suggestion': suggestion
                    })
                    
                    # Calculate weekly average
                    week_ago = datetime.now() - timedelta(days=7)
                    recent_moods = [
                        entry['score'] for entry in mood_data['entries']
                        if datetime.fromisoformat(entry['timestamp']) > week_ago
                    ]
                    
                    if recent_moods:
                        mood_data['weekly_average'] = sum(recent_moods) / len(recent_moods)
                    
                    mood_data['last_check'] = datetime.now().isoformat()
                    self._save_health_data(data)
                    
                    # Mood-based notifications
                    if mood_score <= 3:
                        self._show_notification("Mood Alert", f"Low mood detected. {suggestion}")
                    elif mood_score >= 8:
                        self._show_notification("Great Mood!", f"You're feeling {emotion}! Keep it up!")
                    
                    return f"Mood logged: {mood_score}/10 ({emotion})\nTrigger: {trigger}\nWeekly average: {mood_data['weekly_average']:.1f}\nSuggestion: {suggestion}"
                else:
                    return "Please rate mood 1-10 or describe how you feel"
            
            # Show mood history
            else:
                if not mood_data['entries']:
                    return "No mood data yet. Try: 'feeling happy' or 'mood 7'"
                
                recent = mood_data['entries'][-7:]
                
                status = f"Mood Overview:\n"
                status += f"Weekly average: {mood_data['weekly_average']:.1f}/10\n"
                
                if mood_data['last_check']:
                    last_time = datetime.fromisoformat(mood_data['last_check'])
                    hours_ago = (datetime.now() - last_time).total_seconds() / 3600
                    status += f"Last check: {hours_ago:.1f} hours ago\n"
                
                status += "\nRecent moods:\n"
                for entry in recent:
                    time_str = datetime.fromisoformat(entry['timestamp']).strftime('%m/%d %H:%M')
                    score = entry['score']
                    emotion = entry['emotion']
                    status += f"- {time_str}: {score}/10 ({emotion})\n"
                
                return status
                
        except Exception as e:
            return f"Mood tracker failed: {e}"
    
    def heart_rate_monitor(self, query=""):
        try:
            import re
            from datetime import datetime, timedelta
            
            data = self._load_health_data()
            hr_data = data['heart_rate']
            
            # Log heart rate
            if any(word in query.lower() for word in ['bpm', 'rate', 'pulse', 'beat']):
                hr_match = re.search(r'(\d+)\s*(?:bpm|beats?)', query.lower())
                if hr_match:
                    heart_rate = int(hr_match.group(1))
                    
                    if 40 <= heart_rate <= 200:
                        hr_data['readings'].append({
                            'timestamp': datetime.now().isoformat(),
                            'bpm': heart_rate,
                            'type': 'manual'
                        })
                        
                        # Calculate resting HR average
                        recent_readings = hr_data['readings'][-10:]  # Last 10 readings
                        if len(recent_readings) >= 3:
                            avg_hr = sum(r['bpm'] for r in recent_readings) / len(recent_readings)
                            hr_data['resting_hr'] = int(avg_hr)
                        
                        hr_data['last_check'] = datetime.now().isoformat()
                        self._save_health_data(data)
                        
                        # Heart rate analysis
                        if heart_rate > 100:
                            status = "High (may indicate stress or activity)"
                            self._show_notification("High Heart Rate", f"{heart_rate} BPM detected")
                        elif heart_rate < 60:
                            status = "Low (athletic or resting)"
                        else:
                            status = "Normal range"
                        
                        return f"Heart rate logged: {heart_rate} BPM\nStatus: {status}\nResting HR: {hr_data['resting_hr']} BPM"
                    else:
                        return "Please enter valid heart rate (40-200 BPM)"
                else:
                    return "Please specify heart rate: 'heart rate 75 bpm'"
            
            # Show heart rate history
            else:
                if not hr_data['readings']:
                    return "No heart rate data yet. Try: 'heart rate 72 bpm'"
                
                recent = hr_data['readings'][-7:]
                
                status = f"Heart Rate Monitor:\n"
                status += f"Resting HR: {hr_data['resting_hr']} BPM\n"
                
                if hr_data['last_check']:
                    last_time = datetime.fromisoformat(hr_data['last_check'])
                    hours_ago = (datetime.now() - last_time).total_seconds() / 3600
                    status += f"Last reading: {hours_ago:.1f} hours ago\n"
                
                status += "\nRecent readings:\n"
                for reading in recent:
                    time_str = datetime.fromisoformat(reading['timestamp']).strftime('%m/%d %H:%M')
                    bpm = reading['bpm']
                    status += f"- {time_str}: {bpm} BPM\n"
                
                return status
                
        except Exception as e:
            return f"Heart rate monitor failed: {e}"
    
    def medication_reminder(self, query=""):
        try:
            import re, json
            from datetime import datetime, timedelta
            
            data = self._load_health_data()
            med_data = data['medications']
            
            # Add medication
            if 'add' in query.lower() or 'take' in query.lower():
                # Extract medication name and schedule
                med_match = re.search(r'(?:add|take)\s+(.+?)(?:\s+(?:every|at|daily)|$)', query.lower())
                if med_match:
                    med_name = med_match.group(1).strip()
                    
                    # Extract schedule
                    schedule = "daily"
                    time_match = re.search(r'(?:at|every)\s+(\d{1,2}):?(\d{2})?\s*(am|pm)?', query.lower())
                    if time_match:
                        hour = int(time_match.group(1))
                        minute = int(time_match.group(2)) if time_match.group(2) else 0
                        period = time_match.group(3)
                        
                        if period == 'pm' and hour != 12:
                            hour += 12
                        elif period == 'am' and hour == 12:
                            hour = 0
                        
                        schedule = f"{hour:02d}:{minute:02d}"
                    
                    medication = {
                        'name': med_name,
                        'schedule': schedule,
                        'added': datetime.now().isoformat(),
                        'last_taken': None
                    }
                    
                    med_data['pills'].append(medication)
                    self._save_health_data(data)
                    
                    # Set up reminder
                    def med_reminder():
                        while True:
                            try:
                                if schedule != "daily":
                                    # Parse time
                                    hour, minute = map(int, schedule.split(':'))
                                    now = datetime.now()
                                    reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                                    
                                    if now > reminder_time:
                                        reminder_time += timedelta(days=1)
                                    
                                    time_until = (reminder_time - now).total_seconds()
                                    time.sleep(time_until)
                                    
                                    self._show_notification("💊 Medication Reminder", f"Time to take {med_name}")
                                    time.sleep(86400)  # Wait 24 hours for next reminder
                                else:
                                    time.sleep(86400)  # Daily reminder at same time
                            except Exception:
                                time.sleep(3600)  # Wait 1 hour on error
                    
                    threading.Thread(target=med_reminder, daemon=True).start()
                    
                    return f"Medication added: {med_name}\nSchedule: {schedule}\nReminders enabled"
                else:
                    return "Please specify medication: 'add aspirin at 8am'"
            
            # Mark as taken
            elif 'taken' in query.lower() or 'took' in query.lower():
                med_match = re.search(r'(?:taken|took)\s+(.+)', query.lower())
                if med_match:
                    med_name = med_match.group(1).strip()
                    
                    for med in med_data['pills']:
                        if med_name.lower() in med['name'].lower():
                            med['last_taken'] = datetime.now().isoformat()
                            self._save_health_data(data)
                            return f"Marked {med['name']} as taken"
                    
                    return f"Medication '{med_name}' not found in your list"
                else:
                    return "Please specify which medication you took"
            
            # List medications
            else:
                if not med_data['pills']:
                    return "No medications added yet. Try: 'add vitamin D at 9am'"
                
                status = "Medication Schedule:\n" + "="*30 + "\n"
                
                for i, med in enumerate(med_data['pills'], 1):
                    status += f"{i}. {med['name']}\n"
                    status += f"   Schedule: {med['schedule']}\n"
                    
                    if med['last_taken']:
                        last_taken = datetime.fromisoformat(med['last_taken'])
                        hours_ago = (datetime.now() - last_taken).total_seconds() / 3600
                        status += f"   Last taken: {hours_ago:.1f} hours ago\n"
                    else:
                        status += f"   Last taken: Never\n"
                    
                    status += "\n"
                
                return status
                
        except Exception as e:
            return f"Medication reminder failed: {e}"
    
    def bmi_calculator(self, query=""):
        try:
            import re
            from datetime import datetime
            
            data = self._load_health_data()
            bmi_data = data['bmi']
            
            # Update weight/height
            if 'weight' in query.lower() or 'height' in query.lower():
                weight_match = re.search(r'weight\s+(\d+(?:\.\d+)?)\s*(?:kg|kilos?)?', query.lower())
                height_match = re.search(r'height\s+(\d+(?:\.\d+)?)\s*(?:cm|centimeters?)?', query.lower())
                
                if weight_match:
                    bmi_data['weight'] = float(weight_match.group(1))
                
                if height_match:
                    bmi_data['height'] = float(height_match.group(1))
                
                self._save_health_data(data)
            
            # Calculate BMI
            weight = bmi_data['weight']
            height = bmi_data['height'] / 100  # Convert cm to meters
            
            bmi = weight / (height * height)
            
            # BMI categories
            if bmi < 18.5:
                category = "Underweight"
                advice = "Consider consulting a nutritionist for healthy weight gain"
            elif bmi < 25:
                category = "Normal weight"
                advice = "Great! Maintain your current lifestyle"
            elif bmi < 30:
                category = "Overweight"
                advice = "Consider regular exercise and balanced diet"
            else:
                category = "Obese"
                advice = "Consult a healthcare provider for weight management"
            
            # Log BMI history
            bmi_data['history'].append({
                'timestamp': datetime.now().isoformat(),
                'bmi': round(bmi, 1),
                'weight': weight,
                'height': bmi_data['height'],
                'category': category
            })
            
            self._save_health_data(data)
            
            result = f"BMI Calculator:\n"
            result += f"Height: {bmi_data['height']} cm\n"
            result += f"Weight: {weight} kg\n"
            result += f"BMI: {bmi:.1f}\n"
            result += f"Category: {category}\n"
            result += f"Advice: {advice}"
            
            return result
            
        except Exception as e:
            return f"BMI calculator failed: {e}"
    
    def system_monitor(self, query=""):
        try:
            import psutil
            from datetime import datetime
            
            # CPU and Memory usage
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # System temperatures (if available)
            try:
                temps = psutil.sensors_temperatures()
                temp_info = ""
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            temp_info += f"{entry.label or name}: {entry.current}°C "
            except:
                temp_info = "Temperature sensors not available"
            
            # Network activity
            net_io = psutil.net_io_counters()
            
            # Battery info (for laptops)
            try:
                battery = psutil.sensors_battery()
                battery_info = f"Battery: {battery.percent}% ({'Charging' if battery.power_plugged else 'Discharging'})" if battery else "No battery"
            except:
                battery_info = "Battery info unavailable"
            
            status = f"System Monitor:\n"
            status += f"CPU Usage: {cpu_percent}%\n"
            status += f"Memory: {memory.percent}% ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)\n"
            status += f"Disk: {disk.percent}% ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB)\n"
            status += f"Network: {net_io.bytes_sent//1024//1024}MB sent, {net_io.bytes_recv//1024//1024}MB received\n"
            status += f"{battery_info}\n"
            status += f"Temperature: {temp_info}"
            
            # Alerts for high usage
            if cpu_percent > 80:
                self._show_notification("High CPU Usage", f"CPU at {cpu_percent}%")
            if memory.percent > 85:
                self._show_notification("High Memory Usage", f"RAM at {memory.percent}%")
            
            return status
            
        except ImportError:
            return "System monitoring requires: pip install psutil"
        except Exception as e:
            return f"System monitor failed: {e}"
    
    def network_monitor(self, query=""):
        try:
            import socket
            import subprocess
            import re
            
            # Get local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Check internet connectivity
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                internet_status = "Connected"
            except:
                internet_status = "Disconnected"
            
            # Get WiFi info (Windows)
            try:
                wifi_result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                           capture_output=True, text=True, timeout=10)
                wifi_profiles = len(re.findall(r'All User Profile\s*:\s*(.+)', wifi_result.stdout))
                
                # Current WiFi connection
                current_wifi = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                            capture_output=True, text=True, timeout=10)
                ssid_match = re.search(r'SSID\s*:\s*(.+)', current_wifi.stdout)
                current_ssid = ssid_match.group(1).strip() if ssid_match else "Not connected"
                
                signal_match = re.search(r'Signal\s*:\s*(\d+)%', current_wifi.stdout)
                signal_strength = signal_match.group(1) + "%" if signal_match else "Unknown"
                
            except:
                wifi_profiles = "Unknown"
                current_ssid = "Unknown"
                signal_strength = "Unknown"
            
            # Network speed test (simple ping)
            try:
                ping_result = subprocess.run(['ping', '-n', '4', '8.8.8.8'], 
                                           capture_output=True, text=True, timeout=15)
                avg_match = re.search(r'Average = (\d+)ms', ping_result.stdout)
                ping_time = avg_match.group(1) + "ms" if avg_match else "Failed"
            except:
                ping_time = "Failed"
            
            status = f"Network Monitor:\n"
            status += f"Local IP: {local_ip}\n"
            status += f"Internet: {internet_status}\n"
            status += f"Current WiFi: {current_ssid}\n"
            status += f"Signal Strength: {signal_strength}\n"
            status += f"Ping to Google: {ping_time}\n"
            status += f"Saved WiFi Networks: {wifi_profiles}"
            
            # Alert for connection issues
            if internet_status == "Disconnected":
                self._show_notification("Network Alert", "Internet connection lost")
            
            return status
            
        except Exception as e:
            return f"Network monitor failed: {e}"
    
    def language_translator(self, query=""):
        try:
            import re
            
            # Extract text and target language
            if 'translate' in query.lower():
                # Parse: "translate hello to spanish" or "translate 'bonjour' from french to english"
                translate_match = re.search(r'translate\s+["\']?(.+?)["\']?\s+(?:to|into)\s+(\w+)', query.lower())
                if translate_match:
                    text = translate_match.group(1).strip()
                    target_lang = translate_match.group(2).strip()
                else:
                    return "Usage: 'translate hello to spanish' or 'translate bonjour to english'"
            else:
                return "Please specify translation: 'translate [text] to [language]'"
            
            # Use AI for translation
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Translate this text to {target_lang}: "{text}"
                
Respond ONLY in this format:
Original: [original text]
Language: [target language]
Translation: [translated text]
Pronunciation: [how to pronounce if applicable]
                
Example:
Original: hello
Language: spanish
Translation: hola
Pronunciation: OH-lah'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                # Parse AI response
                translation_match = re.search(r'Translation:\s*(.+)', ai_response, re.IGNORECASE)
                pronunciation_match = re.search(r'Pronunciation:\s*(.+)', ai_response, re.IGNORECASE)
                
                if translation_match:
                    translation = translation_match.group(1).strip()
                    pronunciation = pronunciation_match.group(1).strip() if pronunciation_match else ""
                    
                    result = f"Translation:\n"
                    result += f"'{text}' -> '{translation}' ({target_lang})"
                    if pronunciation:
                        result += f"\nPronunciation: {pronunciation}"
                    
                    return result
                else:
                    return f"Could not translate '{text}' to {target_lang}"
                    
            except Exception:
                # Fallback to basic translation service
                try:
                    import requests
                    
                    # Use Google Translate API (free tier)
                    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        translation = result_data[0][0][0]
                        return f"Translation: '{text}' -> '{translation}' ({target_lang})"
                    else:
                        return "Translation service unavailable"
                        
                except Exception:
                    return f"Translation failed for '{text}' to {target_lang}"
                    
        except Exception as e:
            return f"Language translator failed: {e}"
    
    def dictionary_lookup(self, query=""):
        try:
            import re
            
            # Extract word to define
            if 'define' in query.lower():
                word_match = re.search(r'define\s+(\w+)', query.lower())
                if word_match:
                    word = word_match.group(1).strip()
                else:
                    return "Usage: 'define [word]' - Example: 'define computer'"
            elif 'dictionary' in query.lower():
                word_match = re.search(r'dictionary\s+(\w+)', query.lower())
                if word_match:
                    word = word_match.group(1).strip()
                else:
                    return "Usage: 'dictionary [word]' - Example: 'dictionary science'"
            else:
                # Extract any word from query
                words = re.findall(r'\b[a-zA-Z]{3,}\b', query)
                if words:
                    word = words[-1]  # Take last significant word
                else:
                    return "Please specify a word to define"
            
            # Use AI for comprehensive definition
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Provide a comprehensive definition for the word: "{word}"
                
Respond ONLY in this format:
Word: [word]
Pronunciation: [phonetic pronunciation]
Part of Speech: [noun/verb/adjective/etc.]
Definition: [clear definition]
Example: [example sentence]
Synonyms: [similar words]
Etymology: [word origin if known]
                
Example:
Word: computer
Pronunciation: kuhm-PYOO-ter
Part of Speech: noun
Definition: An electronic device that processes data and performs calculations
Example: I use my computer for work and entertainment
Synonyms: PC, machine, device
Etymology: From Latin "computare" meaning to calculate'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                # Format the response nicely
                lines = ai_response.split('\n')
                formatted_def = f"Dictionary Lookup: {word.upper()}\n" + "="*40 + "\n"
                
                for line in lines:
                    if ':' in line:
                        formatted_def += line + "\n"
                
                return formatted_def
                
            except Exception:
                # Fallback to simple definition
                return f"Definition of '{word}': A word requiring dictionary lookup. Please check online dictionary for detailed definition."
                
        except Exception as e:
            return f"Dictionary lookup failed: {e}"
    
    def wikipedia_search(self, query=""):
        try:
            import re
            import requests
            
            # Extract search term - fix the parsing issue
            search_term = ""
            if 'wikipedia search for' in query.lower():
                search_match = re.search(r'wikipedia search for\s+(.+)', query.lower())
                if search_match:
                    search_term = search_match.group(1).strip()
            elif 'wikipedia' in query.lower() or 'wiki' in query.lower():
                search_match = re.search(r'(?:wikipedia|wiki)\s+(?:search\s+(?:for\s+)?)?(.+)', query.lower())
                if search_match:
                    search_term = search_match.group(1).strip()
            else:
                search_term = query.strip()
            
            if not search_term:
                return "Please specify a topic to search"
            
            # Search Wikipedia API
            try:
                # Get page summary
                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_term.replace(' ', '_')}"
                response = requests.get(wiki_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    title = data.get('title', search_term)
                    extract = data.get('extract', 'No summary available')
                    page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
                    
                    # Limit extract length
                    if len(extract) > 500:
                        extract = extract[:500] + "..."
                    
                    result = f"Wikipedia: {title}\n" + "="*50 + "\n"
                    result += f"{extract}\n\n"
                    result += f"Full article: {page_url}"
                    
                    return result
                else:
                    # Try search if direct lookup fails
                    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_term}&format=json&srlimit=3"
                    search_response = requests.get(search_url, timeout=10)
                    
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        if search_data['query']['search']:
                            results = search_data['query']['search']
                            if len(results) == 1:
                                page_title = results[0]['title']
                                # Try to get the actual page content
                                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title.replace(' ', '_')}"
                                page_response = requests.get(wiki_url, timeout=10)
                                if page_response.status_code == 200:
                                    page_data = page_response.json()
                                    extract = page_data.get('extract', 'No summary available')
                                    page_url = page_data.get('content_urls', {}).get('desktop', {}).get('page', '')
                                    
                                    if len(extract) > 500:
                                        extract = extract[:500] + "..."
                                    
                                    result = f"Wikipedia: {page_title}\n" + "="*50 + "\n"
                                    result += f"{extract}\n\n"
                                    result += f"Full article: {page_url}"
                                    return result
                                else:
                                    return f"Found: {page_title}. Try: 'wikipedia {page_title}'"
                            else:
                                # Multiple results found
                                result = f"Multiple Wikipedia articles found for '{search_term}':\n"
                                for i, item in enumerate(results[:3], 1):
                                    result += f"{i}. {item['title']}\n"
                                result += f"\nTry: 'wikipedia {results[0]['title']}' for the first result"
                                return result
                    
                    return f"No Wikipedia article found for '{search_term}'. Try searching with more specific terms."
                    
            except Exception:
                return f"Wikipedia search failed for '{search_term}'"
                
        except Exception as e:
            return f"Wikipedia search failed: {e}"
    
    def calculator_advanced(self, query=""):
        try:
            import re
            import math
            
            # Extract mathematical expression
            if 'calculate' in query.lower():
                calc_match = re.search(r'calculate\s+(.+)', query.lower())
                if calc_match:
                    expression = calc_match.group(1).strip()
                else:
                    return "Usage: 'calculate [expression]' - Example: 'calculate sin(45) + log(10)'"
            else:
                expression = query.strip()
            
            if not expression:
                return "Please provide a mathematical expression"
            
            # Use AI for complex calculations
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Solve this mathematical expression: "{expression}"
                
Respond ONLY in this format:
Expression: [original expression]
Result: [numerical result]
Steps: [calculation steps if complex]
Explanation: [brief explanation]
                
Support: basic arithmetic (+,-,*,/), powers (^,**), roots (sqrt), trigonometry (sin,cos,tan), logarithms (log,ln), constants (pi,e)
                
Example:
Expression: sin(45) + log(10)
Result: 0.707 + 1.000 = 1.707
Steps: sin(45°) = 0.707, log₁₀(10) = 1.000
Explanation: Sine of 45 degrees plus logarithm base 10 of 10'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Advanced Calculator:\n{ai_response}"
                
            except Exception:
                # Fallback to basic Python evaluation
                try:
                    # Replace common math functions
                    safe_expr = expression.lower()
                    safe_expr = safe_expr.replace('^', '**')
                    safe_expr = safe_expr.replace('sin', 'math.sin')
                    safe_expr = safe_expr.replace('cos', 'math.cos')
                    safe_expr = safe_expr.replace('tan', 'math.tan')
                    safe_expr = safe_expr.replace('log', 'math.log10')
                    safe_expr = safe_expr.replace('ln', 'math.log')
                    safe_expr = safe_expr.replace('sqrt', 'math.sqrt')
                    safe_expr = safe_expr.replace('pi', 'math.pi')
                    safe_expr = safe_expr.replace('e', 'math.e')
                    
                    # Evaluate safely
                    result = eval(safe_expr, {"__builtins__": {}, "math": math})
                    return f"Calculator: {expression} = {result}"
                    
                except Exception:
                    return f"Invalid mathematical expression: '{expression}'"
                    
        except Exception as e:
            return f"Calculator failed: {e}"
    
    def unit_converter(self, query=""):
        try:
            import re
            
            # Extract conversion request
            convert_match = re.search(r'convert\s+(\d+(?:\.\d+)?)\s*(\w+)\s+(?:to|into)\s+(\w+)', query.lower())
            if convert_match:
                value = float(convert_match.group(1))
                from_unit = convert_match.group(2).strip()
                to_unit = convert_match.group(3).strip()
            else:
                return "Usage: 'convert 100 meters to feet' or 'convert 32 fahrenheit to celsius'"
            
            # Use AI for intelligent unit conversion
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Convert {value} {from_unit} to {to_unit}
                
Respond ONLY in this format:
Original: [value] [from_unit]
Converted: [result] [to_unit]
Formula: [conversion formula]
Category: [length/weight/temperature/etc.]
                
Support common units: meters/feet/inches, kg/pounds/ounces, celsius/fahrenheit/kelvin, liters/gallons/cups, etc.
                
Example:
Original: 100 meters
Converted: 328.08 feet
Formula: meters × 3.28084 = feet
Category: length'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Unit Converter:\n{ai_response}"
                
            except Exception:
                # Fallback to basic conversions
                conversions = {
                    ('meters', 'feet'): 3.28084,
                    ('feet', 'meters'): 0.3048,
                    ('kg', 'pounds'): 2.20462,
                    ('pounds', 'kg'): 0.453592,
                    ('celsius', 'fahrenheit'): lambda c: c * 9/5 + 32,
                    ('fahrenheit', 'celsius'): lambda f: (f - 32) * 5/9,
                }
                
                key = (from_unit.lower(), to_unit.lower())
                if key in conversions:
                    factor = conversions[key]
                    if callable(factor):
                        result = factor(value)
                    else:
                        result = value * factor
                    
                    return f"Unit Conversion: {value} {from_unit} = {result:.4f} {to_unit}"
                else:
                    return f"Conversion from {from_unit} to {to_unit} not supported"
                    
        except Exception as e:
            return f"Unit converter failed: {e}"
    
    def flashcard_system(self, query=""):
        try:
            import json
            import random
            import re
            
            flashcards_file = "flashcards.json"
            
            # Load existing flashcards
            try:
                with open(flashcards_file, 'r') as f:
                    flashcards = json.load(f)
            except:
                flashcards = {'decks': {}}
            
            # Add new flashcard
            if 'add' in query.lower() and 'flashcard' in query.lower():
                # Parse: "add flashcard python: programming language"
                add_match = re.search(r'add flashcard\s+(.+?):\s*(.+)', query.lower())
                if add_match:
                    question = add_match.group(1).strip()
                    answer = add_match.group(2).strip()
                    
                    deck_name = "general"
                    if 'deck' in query.lower():
                        deck_match = re.search(r'deck\s+(\w+)', query.lower())
                        if deck_match:
                            deck_name = deck_match.group(1)
                    
                    if deck_name not in flashcards['decks']:
                        flashcards['decks'][deck_name] = []
                    
                    from datetime import datetime
                    flashcards['decks'][deck_name].append({
                        'question': question,
                        'answer': answer,
                        'created': datetime.now().isoformat()
                    })
                    
                    with open(flashcards_file, 'w') as f:
                        json.dump(flashcards, f, indent=2)
                    
                    return f"Flashcard added to '{deck_name}' deck: {question} -> {answer}"
                else:
                    return "Usage: 'add flashcard [question]: [answer]' - Example: 'add flashcard capital of france: paris'"
            
            # Study flashcards
            elif 'study' in query.lower() or 'flashcard' in query.lower():
                if not flashcards['decks']:
                    return "No flashcards available. Add some first: 'add flashcard [question]: [answer]'"
                
                # Select deck
                deck_name = "general"
                if 'deck' in query.lower():
                    deck_match = re.search(r'deck\s+(\w+)', query.lower())
                    if deck_match:
                        deck_name = deck_match.group(1)
                
                if deck_name not in flashcards['decks'] or not flashcards['decks'][deck_name]:
                    available_decks = list(flashcards['decks'].keys())
                    return f"Deck '{deck_name}' not found. Available decks: {', '.join(available_decks)}"
                
                # Get random flashcard
                cards = flashcards['decks'][deck_name]
                card = random.choice(cards)
                
                return f"Flashcard Study - {deck_name.title()} Deck:\nQuestion: {card['question']}\n\n(Say 'answer' to reveal the answer)"
            
            # Show answer
            elif 'answer' in query.lower():
                return "Feature: Show last flashcard answer (implement session tracking)"
            
            # List decks
            else:
                if not flashcards['decks']:
                    return "No flashcard decks available. Create your first: 'add flashcard [question]: [answer]'"
                
                result = "Flashcard Decks:\n" + "="*30 + "\n"
                for deck_name, cards in flashcards['decks'].items():
                    result += f"{deck_name.title()}: {len(cards)} cards\n"
                
                result += "\nUsage: 'study flashcard deck [name]' or 'add flashcard [question]: [answer]'"
                return result
                
        except Exception as e:
            return f"Flashcard system failed: {e}"
    
    def quiz_generator(self, query=""):
        try:
            import re
            
            # Extract quiz topic
            if 'quiz' in query.lower():
                topic_match = re.search(r'quiz\s+(?:on\s+|about\s+)?(.+)', query.lower())
                if topic_match:
                    topic = topic_match.group(1).strip()
                else:
                    topic = "general knowledge"
            else:
                topic = query.strip() or "general knowledge"
            
            # Use AI to generate quiz questions
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Generate a quiz about: "{topic}"
                
Create 5 multiple choice questions. Respond ONLY in this format:

QUIZ: {topic.upper()}

Q1: [question]
A) [option A]
B) [option B] 
C) [option C]
D) [option D]
Correct: [A/B/C/D]

Q2: [question]
A) [option A]
B) [option B]
C) [option C] 
D) [option D]
Correct: [A/B/C/D]

[Continue for Q3, Q4, Q5]

Make questions educational and appropriate difficulty level.'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Quiz Generator:\n{ai_response}\n\nSay 'quiz answers' to see the correct answers!"
                
            except Exception:
                # Fallback to simple quiz
                sample_questions = {
                    "general": [
                        "What is the capital of France? A) London B) Berlin C) Paris D) Madrid",
                        "What is 2+2? A) 3 B) 4 C) 5 D) 6",
                        "Which planet is closest to the Sun? A) Venus B) Mercury C) Earth D) Mars"
                    ],
                    "science": [
                        "What is H2O? A) Hydrogen B) Oxygen C) Water D) Carbon",
                        "Speed of light? A) 300,000 km/s B) 150,000 km/s C) 450,000 km/s D) 600,000 km/s"
                    ]
                }
                
                questions = sample_questions.get("general", sample_questions["general"])
                
                result = f"Quiz: {topic.title()}\n" + "="*30 + "\n"
                for i, q in enumerate(questions[:3], 1):
                    result += f"Q{i}: {q}\n\n"
                
                return result
                
        except Exception as e:
            return f"Quiz generator failed: {e}"
    
    def meme_generator(self, query=""):
        try:
            import re
            
            # Extract meme request
            if 'meme' in query.lower():
                meme_match = re.search(r'meme\s+(.+)', query.lower())
                if meme_match:
                    meme_request = meme_match.group(1).strip()
                else:
                    meme_request = "funny programming joke"
            else:
                meme_request = query.strip() or "random funny meme"
            
            # Use AI to generate meme concept
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Create a meme concept for: "{meme_request}"
                
Respond ONLY in this format:
Template: [meme template name]
Top Text: [text for top]
Bottom Text: [text for bottom]
Style: [humor style]
Description: [visual description]
                
Examples:
Template: Drake Pointing
Top Text: Using print() for debugging
Bottom Text: Using proper debugger
Style: Programming humor
Description: Drake disapproving of print, approving debugger
                
Make it funny and relatable!'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Meme Generator:\n{ai_response}\n\nNote: Use online meme generators like imgflip.com to create the actual image!"
                
            except Exception:
                # Fallback meme concepts
                templates = {
                    "programming": "Template: Distracted Boyfriend\nTop: Me\nGirlfriend: Current project\nOther woman: New framework",
                    "work": "Template: This is Fine\nTop: Everything is under control\nBottom: (while everything burns)",
                    "study": "Template: Drake Pointing\nTop: Studying early\nBottom: Cramming last minute"
                }
                
                concept_type = "programming" if any(word in meme_request for word in ['code', 'programming', 'developer']) else "work"
                concept = templates.get(concept_type, templates["work"])
                
                return f"Meme Generator:\n{concept}\n\nUse imgflip.com or similar to create the image!"
                
        except Exception as e:
            return f"Meme generator failed: {e}"
    
    def logo_generator(self, query=""):
        try:
            import re
            
            # Extract logo requirements
            company_match = re.search(r'logo\s+(?:for\s+)?(.+?)(?:\s+(?:blue|red|green|black|white|color))?', query.lower())
            if company_match:
                company_name = company_match.group(1).strip()
            else:
                company_name = "MyCompany"
            
            # Extract colors
            colors = []
            color_words = ['blue', 'red', 'green', 'black', 'white', 'yellow', 'purple', 'orange']
            for color in color_words:
                if color in query.lower():
                    colors.append(color)
            
            if not colors:
                colors = ['blue', 'white']
            
            # Use AI to generate logo concept
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Design a logo concept for: "{company_name}" using colors: {', '.join(colors)}
                
Respond ONLY in this format:
Company: [company name]
Concept: [logo concept]
Colors: [color scheme]
Font: [font style]
Symbol: [icon/symbol idea]
Style: [modern/classic/minimalist/etc]
Description: [detailed visual description]
                
Example:
Company: TechCorp
Concept: Tech innovation and reliability
Colors: Blue (#0066CC) and White (#FFFFFF)
Font: Modern sans-serif, bold
Symbol: Stylized circuit pattern forming a "T"
Style: Modern, minimalist
Description: Clean geometric design with tech elements
                
Make it professional and memorable!'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Logo Generator:\n{ai_response}\n\nRecommended tools: Canva, Figma, or Adobe Illustrator"
                
            except Exception:
                # Fallback logo concept
                return f"Logo Generator:\nCompany: {company_name.title()}\nConcept: Professional and modern\nColors: {', '.join(colors)}\nFont: Clean sans-serif\nSymbol: Abstract geometric shape\nStyle: Minimalist\nDescription: Simple, scalable design with company initials"
                
        except Exception as e:
            return f"Logo generator failed: {e}"
    
    def color_palette_generator(self, query=""):
        try:
            import re
            import random
            
            # Extract theme
            theme_match = re.search(r'(?:color|palette)\s+(.+)', query.lower())
            if theme_match:
                theme = theme_match.group(1).strip()
            else:
                theme = "modern"
            
            # Use AI to generate color palette
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Generate a color palette for theme: "{theme}"
                
Respond ONLY in this format:
Theme: [theme name]
Primary: [color name] (#HEXCODE)
Secondary: [color name] (#HEXCODE)
Accent: [color name] (#HEXCODE)
Neutral: [color name] (#HEXCODE)
Background: [color name] (#HEXCODE)
Mood: [emotional description]
Use Case: [where to use this palette]
                
Example:
Theme: Ocean Sunset
Primary: Deep Blue (#1E3A8A)
Secondary: Coral Orange (#FF7F50)
Accent: Golden Yellow (#FFD700)
Neutral: Warm Gray (#8B7355)
Background: Cream White (#FFF8DC)
Mood: Calm, warm, inspiring
Use Case: Website, branding, presentations
                
Provide harmonious, professional colors!'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Color Palette Generator:\n{ai_response}\n\nTip: Use tools like Coolors.co or Adobe Color for visualization"
                
            except Exception:
                # Fallback color palettes
                palettes = {
                    "modern": ["#2563EB", "#64748B", "#F59E0B", "#EF4444", "#F8FAFC"],
                    "nature": ["#16A34A", "#84CC16", "#EAB308", "#92400E", "#F7FEE7"],
                    "ocean": ["#0EA5E9", "#06B6D4", "#3B82F6", "#1E40AF", "#F0F9FF"]
                }
                
                colors = palettes.get(theme, palettes["modern"])
                result = f"Color Palette: {theme.title()}\n"
                for i, color in enumerate(colors):
                    labels = ["Primary", "Secondary", "Accent", "Neutral", "Background"]
                    result += f"{labels[i]}: {color}\n"
                
                return result
                
        except Exception as e:
            return f"Color palette generator failed: {e}"
    
    def font_viewer(self, query=""):
        try:
            import platform
            
            # Get system info
            system = platform.system()
            
            # Use AI to recommend fonts
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Recommend fonts for: "{query or 'general use'}"
                
Respond ONLY in this format:
Purpose: [use case]
Heading Font: [font name] - [description]
Body Font: [font name] - [description]
Display Font: [font name] - [description]
Monospace: [font name] - [description]
System Fonts: [list of common system fonts]
Web Safe: [web-safe alternatives]
Google Fonts: [free alternatives]
                
Example:
Purpose: Professional presentation
Heading Font: Arial Black - Bold, impactful
Body Font: Calibri - Clean, readable
Display Font: Impact - Strong presence
Monospace: Consolas - Code and data
System Fonts: Arial, Times New Roman, Verdana
Web Safe: Helvetica, Georgia, Courier
Google Fonts: Roboto, Open Sans, Lato
                
Focus on readability and professionalism!'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Font Viewer ({system}):\n{ai_response}\n\nUse Character Map (Windows) or Font Book (Mac) to preview fonts"
                
            except Exception:
                # Fallback font recommendations
                common_fonts = {
                    "Windows": ["Arial", "Calibri", "Times New Roman", "Verdana", "Consolas"],
                    "Darwin": ["Helvetica", "San Francisco", "Times", "Menlo", "Monaco"],
                    "Linux": ["DejaVu Sans", "Liberation Sans", "Ubuntu", "Noto Sans"]
                }
                
                fonts = common_fonts.get(system, common_fonts["Windows"])
                result = f"Font Viewer ({system}):\n"
                result += f"Common System Fonts:\n"
                for font in fonts:
                    result += f"- {font}\n"
                
                return result
                
        except Exception as e:
            return f"Font viewer failed: {e}"
    
    def ascii_art_generator(self, query=""):
        try:
            import re
            
            # Extract text to convert
            text_match = re.search(r'ascii\s+(?:art\s+)?(.+)', query.lower())
            if text_match:
                text = text_match.group(1).strip()
            else:
                text = "HELLO"
            
            # Use AI to generate ASCII art
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Create ASCII art for text: "{text}"
                
Respond ONLY with ASCII art using characters like: # * - = + | \\ / _ ^
                
Make it readable and artistic. Example for "HI":

#   #  ###
#   #   #
#####   #
#   #   #
#   #  ###
                
Create similar art for the given text.'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"ASCII Art Generator:\n{ai_response}"
                
            except Exception:
                # Fallback simple ASCII
                simple_ascii = {
                    "hello": "#   # ##### #     #     #####\n#   # #     #     #     #    \n##### ##### #     #     #####\n#   # #     #     #     #    \n#   # ##### ##### ##### #####",
                    "hi": "#   #  ###\n#   #   #\n#####   #\n#   #   #\n#   #  ###"
                }
                
                art = simple_ascii.get(text.lower(), f"ASCII: {text.upper()}")
                return f"ASCII Art Generator:\n{art}"
                
        except Exception as e:
            return f"ASCII art generator failed: {e}"
    
    def barcode_generator(self, query=""):
        try:
            import re
            
            # Extract data to encode
            data_match = re.search(r'barcode\s+(.+)', query.lower())
            if data_match:
                data = data_match.group(1).strip()
            else:
                data = "123456789"
            
            # Use AI to generate barcode info
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Generate barcode information for: "{data}"
                
Respond ONLY in this format:
Data: [input data]
Type: [barcode type - Code128/EAN/QR/etc]
Format: [numeric/alphanumeric/text]
Use Case: [where this would be used]
Pattern: [simplified visual pattern]
Tools: [recommended generators]
                
Example:
Data: 123456789
Type: Code128
Format: Numeric
Use Case: Product identification
Pattern: |||| | || ||| | |||| |
Tools: Online generators, ZXing, python-barcode
                
Choose appropriate barcode type for the data!'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Barcode Generator:\n{ai_response}\n\nRecommended: Use online barcode generators or python-barcode library"
                
            except Exception:
                # Fallback barcode info
                barcode_type = "QR Code" if len(data) > 20 else "Code128"
                return f"Barcode Generator:\nData: {data}\nType: {barcode_type}\nUse online generators like barcode-generator.org"
                
        except Exception as e:
            return f"Barcode generator failed: {e}"
    
    def mind_map_creator(self, query=""):
        try:
            import re
            
            # Extract topic
            topic_match = re.search(r'mind\s*map\s+(.+)', query.lower())
            if topic_match:
                topic = topic_match.group(1).strip()
            else:
                topic = "project planning"
            
            # Use AI to generate mind map structure
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Create a mind map structure for: "{topic}"
                
Respond ONLY in this format:
Central Topic: [main topic]
Branch 1: [subtopic]
  - [detail 1]
  - [detail 2]
Branch 2: [subtopic]
  - [detail 1]
  - [detail 2]
Branch 3: [subtopic]
  - [detail 1]
  - [detail 2]
Connections: [how branches relate]
Colors: [suggested color scheme]
Tools: [recommended mind mapping tools]
                
Example:
Central Topic: Learning Python
Branch 1: Basics
  - Variables and data types
  - Control structures
Branch 2: Advanced
  - Object-oriented programming
  - Libraries and frameworks
Branch 3: Practice
  - Projects
  - Problem solving
Connections: Basics → Advanced → Practice
Colors: Blue for basics, Green for advanced, Orange for practice
Tools: XMind, MindMeister, Lucidchart
                
Make it comprehensive and logical!'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                return f"Mind Map Creator:\n{ai_response}\n\nRecommended tools: XMind, MindMeister, or draw.io for digital creation"
                
            except Exception:
                # Fallback mind map structure
                return f"Mind Map Creator:\nCentral Topic: {topic.title()}\nBranch 1: Planning\n  - Goals\n  - Timeline\nBranch 2: Resources\n  - Tools\n  - People\nBranch 3: Implementation\n  - Steps\n  - Milestones\n\nUse XMind or similar tools to create visual mind map"
                
        except Exception as e:
            return f"Mind map creator failed: {e}"
    
    def password_manager(self, query=""):
        try:
            import json
            import os
            import re
            
            try:
                from cryptography.fernet import Fernet  # type: ignore
            except ImportError:
                return "🔐 Password manager requires: pip install cryptography"
            
            # Password storage file
            password_file = "passwords.json"
            key_file = "password_key.key"
            
            # Generate or load encryption key
            if not os.path.exists(key_file):
                key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(key)
            else:
                with open(key_file, 'rb') as f:
                    key = f.read()
            
            cipher = Fernet(key)
            
            # Load existing passwords
            passwords = {}
            if os.path.exists(password_file):
                try:
                    with open(password_file, 'r') as f:
                        encrypted_data = json.load(f)
                    for service, encrypted_pass in encrypted_data.items():
                        passwords[service] = cipher.decrypt(encrypted_pass.encode()).decode()
                except:
                    passwords = {}
            
            # Show password command
            if 'show' in query.lower() or 'get' in query.lower():
                service_match = re.search(r'(?:show|get)\s+(?:my\s+)?(\w+)\s+password', query.lower())
                if service_match:
                    service = service_match.group(1).lower()
                    if service in passwords:
                        return f"🔐 {service.title()} password: {passwords[service]}"
                    else:
                        return f"🔐 No password stored for {service}. Available: {', '.join(passwords.keys())}"
                else:
                    return f"🔐 Stored passwords: {', '.join(passwords.keys()) if passwords else 'None'}\nUsage: 'show gmail password'"
            
            # Add password command
            elif 'add' in query.lower() or 'store' in query.lower():
                add_match = re.search(r'(?:add|store)\s+(\w+)\s+password\s+(.+)', query.lower())
                if add_match:
                    service = add_match.group(1).lower()
                    password = add_match.group(2).strip()
                    
                    passwords[service] = password
                    
                    # Encrypt and save
                    encrypted_data = {}
                    for svc, pwd in passwords.items():
                        encrypted_data[svc] = cipher.encrypt(pwd.encode()).decode()
                    
                    with open(password_file, 'w') as f:
                        json.dump(encrypted_data, f)
                    
                    return f" Password for {service} stored securely"
                else:
                    return " Usage: 'add gmail password mypassword123'"
            
            # List passwords
            else:
                if passwords:
                    return f" Password Manager - Stored accounts: {', '.join(passwords.keys())}\nSay 'show [service] password' to retrieve"
                else:
                    return " Password Manager - No passwords stored yet\nUsage: 'add gmail password mypassword123'"
                    
        except Exception as e:
            return f" Password manager failed: {e}"
    
    def startup_manager(self, query=""):
        try:
            import subprocess
            import os
            import re
            
            # Add startup app
            if 'add' in query.lower():
                app_match = re.search(r'add\s+(?:startup\s+)?(\w+)', query.lower())
                if app_match:
                    app_name = app_match.group(1)
                    
                    # Windows startup registry
                    try:
                        import winreg
                        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                        
                        # For demo, we'll add notepad as example
                        app_path = "notepad.exe" if app_name.lower() == "notepad" else f"{app_name}.exe"
                        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
                        winreg.CloseKey(key)
                        
                        return f"Added {app_name} to startup programs"
                    except Exception as e:
                        return f"Failed to add {app_name} to startup: {e}"
                else:
                    return "Usage: 'add startup notepad' or 'add chrome to startup'"
            
            # Remove startup app
            elif 'remove' in query.lower():
                app_match = re.search(r'remove\s+(?:startup\s+)?(\w+)', query.lower())
                if app_match:
                    app_name = app_match.group(1)
                    
                    try:
                        import winreg
                        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                        
                        winreg.DeleteValue(key, app_name)
                        winreg.CloseKey(key)
                        
                        return f"Removed {app_name} from startup programs"
                    except FileNotFoundError:
                        return f"{app_name} not found in startup programs"
                    except Exception as e:
                        return f"Failed to remove {app_name}: {e}"
                else:
                    return "Usage: 'remove startup notepad'"
            
            # List startup apps
            else:
                try:
                    import winreg
                    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                    
                    startup_apps = []
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_apps.append(f"{name}: {value}")
                            i += 1
                        except WindowsError:
                            break
                    
                    winreg.CloseKey(key)
                    
                    if startup_apps:
                        result = "Startup Programs:\n" + "\n".join(startup_apps)
                    else:
                        result = "No custom startup programs found"
                    
                    return result
                    
                except Exception as e:
                    return f"Failed to list startup programs: {e}"
                    
        except Exception as e:
            return f"Startup manager failed: {e}"
    
    def git_helper(self, query=""):
        try:
            import subprocess
            import os
            import re
            
            # Check if in git repository
            try:
                subprocess.run(['git', 'status'], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                return "Not in a git repository. Navigate to a git project first."
            
            # Git commit
            if 'commit' in query.lower():
                message_match = re.search(r'commit\s+["\']?(.+?)["\']?$', query)
                if message_match:
                    commit_message = message_match.group(1).strip()
                else:
                    commit_message = "Auto commit via Jarvis"
                
                try:
                    # Add all changes
                    subprocess.run(['git', 'add', '.'], check=True)
                    
                    # Commit with message
                    result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                          capture_output=True, text=True, check=True)
                    
                    return f"Git commit successful: '{commit_message}'\n{result.stdout}"
                except subprocess.CalledProcessError as e:
                    return f"Git commit failed: {e.stderr}"
            
            # Git push
            elif 'push' in query.lower():
                try:
                    result = subprocess.run(['git', 'push'], capture_output=True, text=True, check=True)
                    return f"Git push successful\n{result.stdout}"
                except subprocess.CalledProcessError as e:
                    # Try with upstream setup if no upstream branch
                    if "no upstream branch" in e.stderr:
                        try:
                            result = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'], 
                                                  capture_output=True, text=True, check=True)
                            return f"Git push successful (upstream set)\n{result.stdout}"
                        except subprocess.CalledProcessError as e2:
                            return f"Git push failed: {e2.stderr}"
                    return f"Git push failed: {e.stderr}"
            
            # Git status
            elif 'status' in query.lower():
                try:
                    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, check=True)
                    if result.stdout.strip():
                        return f"Git status:\n{result.stdout}"
                    else:
                        return "Git status: Working directory clean"
                except subprocess.CalledProcessError as e:
                    return f"Git status failed: {e.stderr}"
            
            # Default: show git status
            else:
                try:
                    status_result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
                    branch_result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
                    
                    current_branch = branch_result.stdout.strip()
                    status = status_result.stdout.strip()
                    
                    result = f"Git Helper - Branch: {current_branch}\n"
                    if status:
                        result += f"Changes:\n{status}\n"
                    else:
                        result += "Working directory clean\n"
                    
                    result += "\nCommands: 'git commit message', 'git push', 'git status'"
                    return result
                    
                except subprocess.CalledProcessError:
                    return "Git Helper - Repository status unavailable"
                    
        except FileNotFoundError:
            return "Git not installed. Please install Git first."
        except Exception as e:
            return f"Git helper failed: {e}"
    
    def open_app(self, query=""):
        """Universal app opener - works with any application"""
        try:
            import re
            
            # Extract app name from query
            app_match = re.search(r'(?:open|launch|start|run)\s+(.+)', query.lower())
            if app_match:
                app_name = app_match.group(1).strip()
            else:
                return "Usage: 'open [app name]' - Example: 'open notepad' or 'open chrome'"
            
            # COMPLETE Windows App Mappings - ALL Available Applications
            app_mappings = {
                # === MICROSOFT OFFICE SUITE ===
                'word': 'winword', 'microsoft word': 'winword', 'ms word': 'winword',
                'excel': 'excel', 'microsoft excel': 'excel', 'ms excel': 'excel',
                'powerpoint': 'powerpnt', 'microsoft powerpoint': 'powerpnt', 'ms powerpoint': 'powerpnt', 'ppt': 'powerpnt',
                'outlook': 'OUTLOOK', 'microsoft outlook': 'OUTLOOK', 'ms outlook': 'OUTLOOK',
                'onenote': 'onenote', 'microsoft onenote': 'onenote', 'ms onenote': 'onenote',
                'access': 'msaccess', 'microsoft access': 'msaccess', 'ms access': 'msaccess',
                'publisher': 'mspub', 'microsoft publisher': 'mspub', 'ms publisher': 'mspub',
                'visio': 'visio', 'microsoft visio': 'visio', 'ms visio': 'visio',
                'project': 'winproj', 'microsoft project': 'winproj', 'ms project': 'winproj',
                'teams': 'teams', 'microsoft teams': 'teams', 'ms teams': 'teams',
                'sharepoint': 'sharepoint', 'onedrive': 'onedrive',
                
                # === WEB BROWSERS ===
                'chrome': 'chrome', 'google chrome': 'chrome', 'googlechrome': 'chrome',
                'firefox': 'firefox', 'mozilla firefox': 'firefox', 'mozilla': 'firefox',
                'edge': 'msedge', 'microsoft edge': 'msedge', 'ms edge': 'msedge',
                'opera': 'opera', 'opera gx': 'opera',
                'brave': 'brave', 'brave browser': 'brave',
                'safari': 'safari', 'internet explorer': 'iexplore', 'ie': 'iexplore',
                'tor': 'tor', 'tor browser': 'tor',
                'vivaldi': 'vivaldi', 'waterfox': 'waterfox',
                
                # === WINDOWS BUILT-IN APPS ===
                'camera': 'microsoft.windows.camera:', 'windows camera': 'microsoft.windows.camera:',
                'photos': 'microsoft.windows.photos:', 'windows photos': 'microsoft.windows.photos:',
                'mail': 'hxoutlook', 'windows mail': 'hxoutlook', 'mail app': 'hxoutlook',
                'calendar': 'hxcalendarappimm', 'windows calendar': 'hxcalendarappimm', 'calendar app': 'hxcalendarappimm',
                'calculator': 'calculator', 'calc': 'calculator', 'windows calculator': 'calculator',
                'notepad': 'notepad', 'text editor': 'notepad',
                'wordpad': 'wordpad', 'rich text editor': 'wordpad',
                'paint': 'mspaint', 'microsoft paint': 'mspaint', 'ms paint': 'mspaint',
                'paint 3d': 'ms-paint:', 'microsoft paint 3d': 'ms-paint:', 'paint3d': 'ms-paint:',
                'snipping tool': 'snippingtool', 'screenshot': 'snippingtool', 'snip': 'snippingtool',
                'sticky notes': 'stickynotes', 'notes': 'stickynotes',
                'voice recorder': 'soundrecorder', 'sound recorder': 'soundrecorder', 'recorder': 'soundrecorder',
                'movies tv': 'microsoft.zunevideo:', 'movies and tv': 'microsoft.zunevideo:', 'video player': 'microsoft.zunevideo:',
                'groove music': 'microsoft.zunemusic:', 'music': 'microsoft.zunemusic:', 'music player': 'microsoft.zunemusic:',
                'maps': 'microsoft.windowsmaps:', 'windows maps': 'microsoft.windowsmaps:', 'map': 'microsoft.windowsmaps:',
                'weather': 'microsoft.bingweather:', 'windows weather': 'microsoft.bingweather:', 'weather app': 'microsoft.bingweather:',
                'news': 'microsoft.bingnews:', 'microsoft news': 'microsoft.bingnews:', 'news app': 'microsoft.bingnews:',
                'store': 'ms-windows-store:', 'microsoft store': 'ms-windows-store:', 'windows store': 'ms-windows-store:',
                'xbox': 'microsoft.xboxapp:', 'xbox app': 'microsoft.xboxapp:', 'xbox console companion': 'microsoft.xboxapp:',
                'cortana': 'searchui', 'search': 'searchui',
                'people': 'microsoft.people:', 'contacts': 'microsoft.people:',
                'alarms': 'microsoft.windowsalarms:', 'clock': 'microsoft.windowsalarms:', 'timer': 'microsoft.windowsalarms:',
                'feedback hub': 'microsoft.windowsfeedbackhub:', 'feedback': 'microsoft.windowsfeedbackhub:',
                'get help': 'microsoft.gethelp:', 'help': 'microsoft.gethelp:',
                'tips': 'microsoft.getstarted:', 'get started': 'microsoft.getstarted:',
                'mixed reality portal': 'microsoft.windows.holographic.firstrun:', 'mr portal': 'microsoft.windows.holographic.firstrun:',
                'your phone': 'microsoft.yourphone:', 'phone companion': 'microsoft.yourphone:',
                
                # === SYSTEM TOOLS & UTILITIES ===
                'cmd': 'cmd', 'command prompt': 'cmd', 'command line': 'cmd', 'terminal': 'cmd',
                'powershell': 'powershell', 'windows powershell': 'powershell', 'ps': 'powershell',
                'task manager': 'taskmgr', 'taskmgr': 'taskmgr', 'process manager': 'taskmgr',
                'control panel': 'control', 'control': 'control', 'system settings': 'control',
                'settings': 'ms-settings:', 'windows settings': 'ms-settings:', 'pc settings': 'ms-settings:',
                'file explorer': 'explorer', 'explorer': 'explorer', 'files': 'explorer', 'folder': 'explorer',
                'registry editor': 'regedit', 'regedit': 'regedit', 'registry': 'regedit',
                'device manager': 'devmgmt.msc', 'devices': 'devmgmt.msc',
                'disk management': 'diskmgmt.msc', 'disk manager': 'diskmgmt.msc',
                'services': 'services.msc', 'windows services': 'services.msc',
                'event viewer': 'eventvwr.msc', 'events': 'eventvwr.msc', 'logs': 'eventvwr.msc',
                'system information': 'msinfo32', 'system info': 'msinfo32', 'sysinfo': 'msinfo32',
                'system configuration': 'msconfig', 'msconfig': 'msconfig', 'boot config': 'msconfig',
                'resource monitor': 'resmon', 'resmon': 'resmon', 'performance': 'resmon',
                'performance monitor': 'perfmon', 'perfmon': 'perfmon',
                'computer management': 'compmgmt.msc', 'management console': 'compmgmt.msc',
                'disk cleanup': 'cleanmgr', 'cleanup': 'cleanmgr',
                'defragment': 'dfrgui', 'disk defragmenter': 'dfrgui',
                'character map': 'charmap', 'charmap': 'charmap', 'symbols': 'charmap',
                'magnifier': 'magnify', 'zoom': 'magnify', 'screen magnifier': 'magnify',
                'narrator': 'narrator', 'screen reader': 'narrator',
                'on screen keyboard': 'osk', 'virtual keyboard': 'osk', 'osk': 'osk',
                'remote desktop': 'mstsc', 'rdp': 'mstsc', 'remote connection': 'mstsc',
                'windows defender': 'msascuil', 'defender': 'msascuil', 'antivirus': 'msascuil',
                'firewall': 'wf.msc', 'windows firewall': 'wf.msc',
                'group policy': 'gpedit.msc', 'gpedit': 'gpedit.msc', 'policy editor': 'gpedit.msc',
                'local users': 'lusrmgr.msc', 'user manager': 'lusrmgr.msc',
                'certificate manager': 'certmgr.msc', 'certificates': 'certmgr.msc',
                'component services': 'dcomcnfg', 'dcom': 'dcomcnfg',
                'iis manager': 'inetmgr', 'internet information services': 'inetmgr',
                
                # === DEVELOPMENT TOOLS ===
                'vscode': 'code', 'vs code': 'code', 'visual studio code': 'code', 'code': 'code',
                'visual studio': 'devenv', 'vs': 'devenv', 'visual studio 2022': 'devenv', 'visual studio 2019': 'devenv',
                'git bash': 'git-bash', 'git': 'git-bash', 'bash': 'git-bash',
                'github desktop': 'githubdesktop', 'github': 'githubdesktop',
                'android studio': 'studio64', 'android': 'studio64',
                'intellij': 'idea64', 'intellij idea': 'idea64', 'idea': 'idea64',
                'pycharm': 'pycharm64', 'pycharm community': 'pycharm64', 'pycharm professional': 'pycharm64',
                'sublime text': 'sublime_text', 'sublime': 'sublime_text',
                'atom': 'atom', 'atom editor': 'atom',
                'brackets': 'brackets', 'adobe brackets': 'brackets',
                'notepad++': 'notepad++', 'notepadplusplus': 'notepad++', 'npp': 'notepad++',
                'eclipse': 'eclipse', 'eclipse ide': 'eclipse',
                'netbeans': 'netbeans', 'netbeans ide': 'netbeans',
                'webstorm': 'webstorm', 'phpstorm': 'phpstorm', 'clion': 'clion',
                'xampp': 'xampp-control', 'wamp': 'wampmanager', 'laragon': 'laragon',
                'docker': 'docker desktop', 'docker desktop': 'docker desktop',
                'postman': 'postman', 'insomnia': 'insomnia',
                'sourcetree': 'sourcetree', 'gitkraken': 'gitkraken',
                'unity': 'unity', 'unity hub': 'unity hub', 'unreal engine': 'unrealengine',
                
                # === MEDIA & ENTERTAINMENT ===
                'spotify': 'spotify', 'spotify music': 'spotify',
                'vlc': 'vlc', 'vlc media player': 'vlc', 'vlc player': 'vlc',
                'windows media player': 'wmplayer', 'media player': 'wmplayer', 'wmp': 'wmplayer',
                'itunes': 'itunes', 'apple music': 'itunes',
                'audacity': 'audacity', 'audio editor': 'audacity',
                'obs': 'obs64', 'obs studio': 'obs64', 'streaming': 'obs64',
                'handbrake': 'handbrake', 'video converter': 'handbrake',
                'kodi': 'kodi', 'media center': 'kodi',
                'plex': 'plex', 'plex media server': 'plex',
                'netflix': 'microsoft.netflix:', 'youtube': 'microsoft.youtube:',
                'amazon prime': 'primevideo', 'disney plus': 'disney+',
                'twitch': 'twitch', 'youtube music': 'youtube music',
                'foobar2000': 'foobar2000', 'winamp': 'winamp',
                'mpc': 'mpc-hc64', 'media player classic': 'mpc-hc64',
                'potplayer': 'potplayermini64', 'kmplayer': 'kmplayer',
                'adobe premiere': 'premiere', 'premiere pro': 'premiere',
                'adobe after effects': 'afterfx', 'after effects': 'afterfx',
                'davinci resolve': 'resolve', 'final cut': 'final cut pro',
                'camtasia': 'camtasia', 'bandicam': 'bandicam',
                
                # === COMMUNICATION ===
                'discord': 'discord', 'discord app': 'discord',
                'skype': 'skype', 'skype for business': 'lync',
                'zoom': 'zoom', 'zoom meetings': 'zoom',
                'whatsapp': 'whatsapp', 'whatsapp desktop': 'whatsapp',
                'telegram': 'telegram', 'telegram desktop': 'telegram',
                'slack': 'slack', 'slack desktop': 'slack',
                'signal': 'signal', 'signal desktop': 'signal',
                'viber': 'viber', 'viber desktop': 'viber',
                'line': 'line', 'wechat': 'wechat', 'qq': 'qq',
                'facebook messenger': 'messenger', 'messenger': 'messenger',
                'google meet': 'meet', 'google hangouts': 'hangouts',
                'webex': 'webex', 'cisco webex': 'webex',
                'gotomeeting': 'gotomeeting', 'teamviewer': 'teamviewer',
                
                # === GAMING ===
                'steam': 'steam', 'steam client': 'steam',
                'epic games': 'epicgameslauncher', 'epic': 'epicgameslauncher', 'epic launcher': 'epicgameslauncher',
                'origin': 'origin', 'ea origin': 'origin', 'ea desktop': 'eadesktop',
                'uplay': 'uplay', 'ubisoft connect': 'ubisoftconnect',
                'battle.net': 'battle.net', 'battlenet': 'battle.net', 'blizzard': 'battle.net',
                'gog galaxy': 'goggalaxy', 'gog': 'goggalaxy',
                'minecraft': 'minecraft', 'minecraft launcher': 'minecraftlauncher',
                'roblox': 'roblox', 'roblox player': 'robloxplayerbeta',
                'xbox game bar': 'gamebar', 'game bar': 'gamebar',
                'nvidia geforce': 'geforce experience', 'geforce experience': 'geforce experience',
                'amd radeon': 'radeon software', 'radeon software': 'radeon software',
                'msi afterburner': 'msiafterburner', 'afterburner': 'msiafterburner',
                'fraps': 'fraps', 'bandicam': 'bandicam',
                
                # === CREATIVE & DESIGN ===
                'photoshop': 'photoshop', 'adobe photoshop': 'photoshop', 'ps': 'photoshop',
                'illustrator': 'illustrator', 'adobe illustrator': 'illustrator', 'ai': 'illustrator',
                'indesign': 'indesign', 'adobe indesign': 'indesign', 'id': 'indesign',
                'lightroom': 'lightroom', 'adobe lightroom': 'lightroom', 'lr': 'lightroom',
                'acrobat': 'acrobat', 'adobe acrobat': 'acrobat', 'pdf reader': 'acrobat',
                'dreamweaver': 'dreamweaver', 'adobe dreamweaver': 'dreamweaver',
                'animate': 'animate', 'adobe animate': 'animate', 'flash': 'animate',
                'xd': 'adobe xd', 'adobe xd': 'adobe xd',
                'gimp': 'gimp', 'gnu image manipulation': 'gimp',
                'blender': 'blender', '3d modeling': 'blender',
                'figma': 'figma', 'sketch': 'sketch',
                'canva': 'canva', 'canva desktop': 'canva',
                'coreldraw': 'coreldraw', 'corel': 'coreldraw',
                'paint.net': 'paintdotnet', 'paintnet': 'paintdotnet',
                'krita': 'krita', 'inkscape': 'inkscape',
                'autodesk maya': 'maya', 'maya': 'maya',
                'autocad': 'autocad', 'autodesk autocad': 'autocad',
                '3ds max': '3dsmax', 'autodesk 3ds max': '3dsmax',
                'solidworks': 'solidworks', 'fusion 360': 'fusion360',
                
                # === PRODUCTIVITY ===
                'notion': 'notion', 'notion desktop': 'notion',
                'evernote': 'evernote', 'evernote desktop': 'evernote',
                'trello': 'trello', 'trello desktop': 'trello',
                'todoist': 'todoist', 'todoist desktop': 'todoist',
                'asana': 'asana', 'monday': 'monday',
                'clickup': 'clickup', 'airtable': 'airtable',
                'obsidian': 'obsidian', 'roam research': 'roam',
                'logseq': 'logseq', 'remnote': 'remnote',
                'anki': 'anki', 'flashcards': 'anki',
                'zotero': 'zotero', 'mendeley': 'mendeley',
                
                # === CLOUD STORAGE ===
                'dropbox': 'dropbox', 'dropbox desktop': 'dropbox',
                'google drive': 'googledrivefs', 'drive': 'googledrivefs',
                'icloud': 'icloud', 'apple icloud': 'icloud',
                'box': 'box', 'box sync': 'box sync',
                'mega': 'megasync', 'megasync': 'megasync',
                'pcloud': 'pcloud', 'sync.com': 'sync',
                
                # === UTILITIES & TOOLS ===
                'winrar': 'winrar', 'rar': 'winrar',
                '7zip': '7zfm', '7-zip': '7zfm', 'seven zip': '7zfm',
                'winzip': 'winzip32', 'zip': 'winzip32',
                'peazip': 'peazip', 'bandizip': 'bandizip',
                'ccleaner': 'ccleaner', 'system cleaner': 'ccleaner',
                'malwarebytes': 'malwarebytes', 'mbam': 'malwarebytes',
                'avast': 'avastui', 'avg': 'avgui', 'norton': 'norton',
                'kaspersky': 'kaspersky', 'bitdefender': 'bitdefender',
                'anydesk': 'anydesk', 'remote access': 'anydesk',
                'putty': 'putty', 'ssh client': 'putty',
                'filezilla': 'filezilla', 'ftp client': 'filezilla',
                'wireshark': 'wireshark', 'network analyzer': 'wireshark',
                'nmap': 'nmap', 'network scanner': 'nmap',
                'virtualbox': 'virtualbox', 'vm': 'virtualbox',
                'vmware': 'vmware', 'vmware workstation': 'vmware',
                'hyper-v': 'virtmgmt.msc', 'hyperv': 'virtmgmt.msc',
                'cpu-z': 'cpuz', 'gpu-z': 'gpuz',
                'hwinfo': 'hwinfo64', 'speccy': 'speccy',
                'crystaldiskinfo': 'diskinfo64', 'crystaldiskmark': 'diskmark64',
                'process explorer': 'procexp64', 'process monitor': 'procmon',
                'autoruns': 'autoruns64', 'sysinternals': 'procexp64',
                'everything': 'everything', 'file search': 'everything',
                'powertoys': 'powertoys', 'microsoft powertoys': 'powertoys',
                'f.lux': 'flux', 'blue light filter': 'flux',
                'rainmeter': 'rainmeter', 'desktop customization': 'rainmeter',
                'wallpaper engine': 'wallpaper32', 'animated wallpaper': 'wallpaper32',
                
                # === BROWSERS WITH MODES ===
                'chrome incognito': 'chrome --incognito',
                'firefox private': 'firefox -private-window',
                'edge inprivate': 'msedge --inprivate',
                'chrome dev tools': 'chrome --auto-open-devtools-for-tabs',
                
                # === SYSTEM SHORTCUTS ===
                'run': 'explorer shell:AppsFolder\\Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy!App',
                'startup folder': 'shell:startup',
                'temp folder': 'temp',
                'system32': 'system32',
                'program files': 'explorer "C:\\Program Files"',
                'documents': 'explorer shell:MyComputerFolder',
                'downloads': 'explorer shell:Downloads',
                'desktop': 'explorer shell:Desktop',
                'pictures': 'explorer shell:MyPictures',
                'music folder': 'explorer shell:MyMusic',
                'videos': 'explorer shell:MyVideo'
            }
            
            # Use mapped name if available (check exact match first, then partial)
            actual_app_name = app_mappings.get(app_name.lower(), app_name)
            
            # If no exact match, try partial matching
            if actual_app_name == app_name:
                for key, value in app_mappings.items():
                    if app_name.lower() in key or key in app_name.lower():
                        actual_app_name = value
                        break
            
            # AI fallback if no mapping found
            if actual_app_name == app_name:
                try:
                    from engine.dual_ai import dual_ai
                    ai_prompt = f'What is the exact executable name for "{app_name}" on Windows? Respond with ONLY the executable name (like "notepad" or "chrome"), no explanations.'
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant",
                            max_tokens=20
                        )
                        ai_app_name = response.choices[0].message.content.strip().lower()
                        if ai_app_name and len(ai_app_name) < 50:
                            actual_app_name = ai_app_name
                except Exception:
                    pass
            
            # Try multiple methods to open the app
            opened = False
            
            # Method 1: Windows start command with mapped name
            try:
                subprocess.run(f'start "" "{actual_app_name}"', shell=True, check=True)
                opened = True
            except:
                pass
            
            # Method 1.1: Try original app name with start
            if not opened:
                try:
                    subprocess.run(f'start "" "{app_name}"', shell=True, check=True)
                    opened = True
                except:
                    pass
            
            # Method 1.5: Comprehensive Office app detection
            if not opened and app_name.lower() in ['outlook', 'word', 'excel', 'powerpoint', 'onenote', 'access', 'publisher']:
                # All possible Office installation paths
                office_versions = ['Office16', 'Office15', 'Office14', 'Office12']
                office_roots = [
                    'C:\\Program Files\\Microsoft Office\\root',
                    'C:\\Program Files (x86)\\Microsoft Office\\root',
                    'C:\\Program Files\\Microsoft Office',
                    'C:\\Program Files (x86)\\Microsoft Office'
                ]
                
                # Try all combinations
                for root in office_roots:
                    for version in office_versions:
                        office_path = f"{root}\\{version}\\{actual_app_name}.exe"
                        if os.path.exists(office_path):
                            try:
                                subprocess.Popen(office_path)
                                opened = True
                                break
                            except:
                                pass
                    if opened:
                        break
                
                # Also try direct Office folder
                if not opened:
                    direct_paths = [
                        f"C:\\Program Files\\Microsoft Office\\{actual_app_name}.exe",
                        f"C:\\Program Files (x86)\\Microsoft Office\\{actual_app_name}.exe"
                    ]
                    for path in direct_paths:
                        if os.path.exists(path):
                            try:
                                subprocess.Popen(path)
                                opened = True
                                break
                            except:
                                pass
            
            # Method 2: PowerShell Get-Command to find executable
            if not opened:
                try:
                    result = subprocess.run(f'powershell "Get-Command {actual_app_name} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source"', 
                                          shell=True, capture_output=True, text=True)
                    if result.stdout.strip():
                        exe_path = result.stdout.strip()
                        subprocess.Popen(exe_path)
                        opened = True
                except:
                    pass
            
            # Method 2.1: Try with original name
            if not opened:
                try:
                    result = subprocess.run(f'powershell "Get-Command {app_name} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source"', 
                                          shell=True, capture_output=True, text=True)
                    if result.stdout.strip():
                        exe_path = result.stdout.strip()
                        subprocess.Popen(exe_path)
                        opened = True
                except:
                    pass
            
            # Method 3: Where command to locate executable
            if not opened:
                try:
                    result = subprocess.run(f'where {actual_app_name}', shell=True, capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        exe_path = result.stdout.strip().split('\n')[0]
                        subprocess.Popen(exe_path)
                        opened = True
                except:
                    pass
            
            # Method 3.1: Where with .exe extension
            if not opened:
                try:
                    result = subprocess.run(f'where {actual_app_name}.exe', shell=True, capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        exe_path = result.stdout.strip().split('\n')[0]
                        subprocess.Popen(exe_path)
                        opened = True
                except:
                    pass
            
            # Method 4: Try original name if mapping failed
            if not opened and actual_app_name != app_name:
                try:
                    subprocess.run(f'start {app_name}', shell=True, check=True)
                    opened = True
                except:
                    pass
            
            # Method 5: Search system and program files
            if not opened:
                search_paths = [
                    f"C:\\Windows\\System32\\{actual_app_name}.exe",
                    f"C:\\Windows\\{actual_app_name}.exe",
                    f"C:\\Program Files\\{app_name}\\{actual_app_name}.exe",
                    f"C:\\Program Files (x86)\\{app_name}\\{actual_app_name}.exe",
                    f"C:\\Program Files\\{actual_app_name}\\{actual_app_name}.exe",
                    f"C:\\Program Files (x86)\\{actual_app_name}\\{actual_app_name}.exe"
                ]
                
                for path in search_paths:
                    if os.path.exists(path):
                        try:
                            subprocess.Popen(path)
                            opened = True
                            break
                        except:
                            pass
            
            # Method 6: Use Windows Registry to find Office apps
            if not opened and app_name.lower() in ['outlook', 'word', 'excel', 'powerpoint']:
                try:
                    import winreg
                    
                    # Check registry for Office installation
                    reg_paths = [
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{}.exe".format(actual_app_name),
                        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\{}.exe".format(actual_app_name)
                    ]
                    
                    for reg_path in reg_paths:
                        try:
                            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                            exe_path = winreg.QueryValue(key, "")
                            winreg.CloseKey(key)
                            
                            if exe_path and os.path.exists(exe_path):
                                subprocess.Popen(exe_path)
                                opened = True
                                break
                        except:
                            continue
                            
                except Exception:
                    pass
            
            if opened:
                return f"Opened {app_name} successfully"
            else:
                return f"Could not open {app_name}. Try the full application name or check if it's installed."
                        
        except Exception as e:
            return f"App opener failed: {e}"
    
    def close_app(self, query=""):
        """Universal app closer - works with any running application"""
        try:
            import re
            
            # Extract app name from query
            app_match = re.search(r'(?:close|quit|exit|kill)\s+(.+)', query.lower())
            if app_match:
                app_name = app_match.group(1).strip()
            else:
                return "Usage: 'close [app name]' - Example: 'close notepad' or 'close chrome'"
            
            # COMPLETE Process Name Mappings for Closing ALL Applications
            app_mappings = {
                # === MICROSOFT OFFICE SUITE ===
                'word': 'WINWORD', 'microsoft word': 'WINWORD', 'ms word': 'WINWORD',
                'excel': 'EXCEL', 'microsoft excel': 'EXCEL', 'ms excel': 'EXCEL',
                'powerpoint': 'POWERPNT', 'microsoft powerpoint': 'POWERPNT', 'ms powerpoint': 'POWERPNT', 'ppt': 'POWERPNT',
                'outlook': 'OUTLOOK', 'microsoft outlook': 'OUTLOOK', 'ms outlook': 'OUTLOOK',
                'onenote': 'ONENOTE', 'microsoft onenote': 'ONENOTE', 'ms onenote': 'ONENOTE',
                'access': 'MSACCESS', 'microsoft access': 'MSACCESS', 'ms access': 'MSACCESS',
                'publisher': 'MSPUB', 'microsoft publisher': 'MSPUB', 'ms publisher': 'MSPUB',
                'visio': 'VISIO', 'microsoft visio': 'VISIO', 'ms visio': 'VISIO',
                'project': 'WINPROJ', 'microsoft project': 'WINPROJ', 'ms project': 'WINPROJ',
                'teams': 'Teams', 'microsoft teams': 'Teams', 'ms teams': 'Teams',
                'sharepoint': 'sharepoint', 'onedrive': 'OneDrive',
                
                # === WEB BROWSERS ===
                'chrome': 'chrome', 'google chrome': 'chrome', 'googlechrome': 'chrome',
                'firefox': 'firefox', 'mozilla firefox': 'firefox', 'mozilla': 'firefox',
                'edge': 'msedge', 'microsoft edge': 'msedge', 'ms edge': 'msedge',
                'opera': 'opera', 'opera gx': 'opera',
                'brave': 'brave', 'brave browser': 'brave',
                'safari': 'safari', 'internet explorer': 'iexplore', 'ie': 'iexplore',
                'tor': 'tor', 'tor browser': 'tor',
                'vivaldi': 'vivaldi', 'waterfox': 'waterfox',
                
                # === WINDOWS BUILT-IN APPS ===
                'camera': 'WindowsCamera', 'windows camera': 'WindowsCamera',
                'photos': 'Microsoft.Photos', 'windows photos': 'Microsoft.Photos',
                'mail': 'HxOutlook', 'windows mail': 'HxOutlook', 'mail app': 'HxOutlook',
                'calendar': 'HxCalendarAppImm', 'windows calendar': 'HxCalendarAppImm', 'calendar app': 'HxCalendarAppImm',
                'calculator': 'Calculator', 'calc': 'Calculator', 'windows calculator': 'Calculator',
                'notepad': 'notepad', 'text editor': 'notepad',
                'wordpad': 'wordpad', 'rich text editor': 'wordpad',
                'paint': 'mspaint', 'microsoft paint': 'mspaint', 'ms paint': 'mspaint',
                'paint 3d': 'PaintStudio.View', 'microsoft paint 3d': 'PaintStudio.View', 'paint3d': 'PaintStudio.View',
                'snipping tool': 'SnippingTool', 'screenshot': 'SnippingTool', 'snip': 'SnippingTool',
                'sticky notes': 'StickyNotes', 'notes': 'StickyNotes',
                'voice recorder': 'SoundRecorder', 'sound recorder': 'SoundRecorder', 'recorder': 'SoundRecorder',
                'movies tv': 'Video.UI', 'movies and tv': 'Video.UI', 'video player': 'Video.UI',
                'groove music': 'Music.UI', 'music': 'Music.UI', 'music player': 'Music.UI',
                'maps': 'Maps', 'windows maps': 'Maps', 'map': 'Maps',
                'weather': 'Microsoft.BingWeather', 'windows weather': 'Microsoft.BingWeather', 'weather app': 'Microsoft.BingWeather',
                'news': 'Microsoft.BingNews', 'microsoft news': 'Microsoft.BingNews', 'news app': 'Microsoft.BingNews',
                'store': 'WinStore.App', 'microsoft store': 'WinStore.App', 'windows store': 'WinStore.App',
                'xbox': 'XboxApp', 'xbox app': 'XboxApp', 'xbox console companion': 'XboxApp',
                'cortana': 'SearchUI', 'search': 'SearchUI',
                'people': 'Microsoft.People', 'contacts': 'Microsoft.People',
                'alarms': 'Microsoft.WindowsAlarms', 'clock': 'Microsoft.WindowsAlarms', 'timer': 'Microsoft.WindowsAlarms',
                'feedback hub': 'Microsoft.WindowsFeedbackHub', 'feedback': 'Microsoft.WindowsFeedbackHub',
                'get help': 'Microsoft.GetHelp', 'help': 'Microsoft.GetHelp',
                'tips': 'Microsoft.Getstarted', 'get started': 'Microsoft.Getstarted',
                'mixed reality portal': 'MixedRealityPortal', 'mr portal': 'MixedRealityPortal',
                'your phone': 'YourPhone', 'phone companion': 'YourPhone',
                
                # === SYSTEM TOOLS & UTILITIES ===
                'cmd': 'cmd', 'command prompt': 'cmd', 'command line': 'cmd', 'terminal': 'cmd',
                'powershell': 'powershell', 'windows powershell': 'powershell', 'ps': 'powershell',
                'task manager': 'Taskmgr', 'taskmgr': 'Taskmgr', 'process manager': 'Taskmgr',
                'control panel': 'control', 'control': 'control', 'system settings': 'control',
                'file explorer': 'explorer', 'explorer': 'explorer', 'files': 'explorer', 'folder': 'explorer',
                'registry editor': 'regedit', 'regedit': 'regedit', 'registry': 'regedit',
                'device manager': 'mmc', 'devices': 'mmc',
                'disk management': 'mmc', 'disk manager': 'mmc',
                'services': 'mmc', 'windows services': 'mmc',
                'event viewer': 'mmc', 'events': 'mmc', 'logs': 'mmc',
                'system information': 'msinfo32', 'system info': 'msinfo32', 'sysinfo': 'msinfo32',
                'system configuration': 'msconfig', 'msconfig': 'msconfig', 'boot config': 'msconfig',
                'resource monitor': 'resmon', 'resmon': 'resmon', 'performance': 'resmon',
                'performance monitor': 'perfmon', 'perfmon': 'perfmon',
                'computer management': 'mmc', 'management console': 'mmc',
                'disk cleanup': 'cleanmgr', 'cleanup': 'cleanmgr',
                'defragment': 'dfrgui', 'disk defragmenter': 'dfrgui',
                'character map': 'charmap', 'charmap': 'charmap', 'symbols': 'charmap',
                'magnifier': 'Magnify', 'zoom': 'Magnify', 'screen magnifier': 'Magnify',
                'narrator': 'Narrator', 'screen reader': 'Narrator',
                'on screen keyboard': 'osk', 'virtual keyboard': 'osk', 'osk': 'osk',
                'remote desktop': 'mstsc', 'rdp': 'mstsc', 'remote connection': 'mstsc',
                'windows defender': 'MsMpEng', 'defender': 'MsMpEng', 'antivirus': 'MsMpEng',
                'firewall': 'mmc', 'windows firewall': 'mmc',
                'group policy': 'mmc', 'gpedit': 'mmc', 'policy editor': 'mmc',
                'local users': 'mmc', 'user manager': 'mmc',
                'certificate manager': 'mmc', 'certificates': 'mmc',
                'component services': 'dcomcnfg', 'dcom': 'dcomcnfg',
                'iis manager': 'inetmgr', 'internet information services': 'inetmgr',
                
                # === DEVELOPMENT TOOLS ===
                'vscode': 'Code', 'vs code': 'Code', 'visual studio code': 'Code', 'code': 'Code',
                'visual studio': 'devenv', 'vs': 'devenv', 'visual studio 2022': 'devenv', 'visual studio 2019': 'devenv',
                'git bash': 'mintty', 'git': 'mintty', 'bash': 'mintty',
                'github desktop': 'GitHubDesktop', 'github': 'GitHubDesktop',
                'android studio': 'studio64', 'android': 'studio64',
                'intellij': 'idea64', 'intellij idea': 'idea64', 'idea': 'idea64',
                'pycharm': 'pycharm64', 'pycharm community': 'pycharm64', 'pycharm professional': 'pycharm64',
                'sublime text': 'sublime_text', 'sublime': 'sublime_text',
                'atom': 'atom', 'atom editor': 'atom',
                'brackets': 'Brackets', 'adobe brackets': 'Brackets',
                'notepad++': 'notepad++', 'notepadplusplus': 'notepad++', 'npp': 'notepad++',
                'eclipse': 'eclipse', 'eclipse ide': 'eclipse',
                'netbeans': 'netbeans', 'netbeans ide': 'netbeans',
                'webstorm': 'webstorm', 'phpstorm': 'phpstorm', 'clion': 'clion',
                'xampp': 'xampp-control', 'wamp': 'wampmanager', 'laragon': 'laragon',
                'docker': 'Docker Desktop', 'docker desktop': 'Docker Desktop',
                'postman': 'Postman', 'insomnia': 'Insomnia',
                'sourcetree': 'SourceTree', 'gitkraken': 'GitKraken',
                'unity': 'Unity', 'unity hub': 'Unity Hub', 'unreal engine': 'UnrealEngine',
                
                # === MEDIA & ENTERTAINMENT ===
                'spotify': 'Spotify', 'spotify music': 'Spotify',
                'vlc': 'vlc', 'vlc media player': 'vlc', 'vlc player': 'vlc',
                'windows media player': 'wmplayer', 'media player': 'wmplayer', 'wmp': 'wmplayer',
                'itunes': 'iTunes', 'apple music': 'iTunes',
                'audacity': 'audacity', 'audio editor': 'audacity',
                'obs': 'obs64', 'obs studio': 'obs64', 'streaming': 'obs64',
                'handbrake': 'HandBrake', 'video converter': 'HandBrake',
                'kodi': 'Kodi', 'media center': 'Kodi',
                'plex': 'Plex Media Server', 'plex media server': 'Plex Media Server',
                'netflix': 'Netflix', 'youtube': 'chrome',
                'amazon prime': 'PrimeVideo', 'disney plus': 'Disney+',
                'twitch': 'Twitch', 'youtube music': 'YouTube Music',
                'foobar2000': 'foobar2000', 'winamp': 'winamp',
                'mpc': 'mpc-hc64', 'media player classic': 'mpc-hc64',
                'potplayer': 'PotPlayerMini64', 'kmplayer': 'KMPlayer',
                'adobe premiere': 'Adobe Premiere Pro', 'premiere pro': 'Adobe Premiere Pro',
                'adobe after effects': 'AfterFX', 'after effects': 'AfterFX',
                'davinci resolve': 'Resolve', 'final cut': 'Final Cut Pro',
                'camtasia': 'CamtasiaStudio', 'bandicam': 'bandicam',
                
                # === COMMUNICATION ===
                'discord': 'Discord', 'discord app': 'Discord',
                'skype': 'Skype', 'skype for business': 'lync',
                'zoom': 'Zoom', 'zoom meetings': 'Zoom',
                'whatsapp': 'WhatsApp', 'whatsapp desktop': 'WhatsApp',
                'telegram': 'Telegram', 'telegram desktop': 'Telegram',
                'slack': 'slack', 'slack desktop': 'slack',
                'signal': 'Signal', 'signal desktop': 'Signal',
                'viber': 'Viber', 'viber desktop': 'Viber',
                'line': 'LINE', 'wechat': 'WeChat', 'qq': 'QQ',
                'facebook messenger': 'Messenger', 'messenger': 'Messenger',
                'google meet': 'Meet', 'google hangouts': 'Hangouts',
                'webex': 'CiscoWebexMeetings', 'cisco webex': 'CiscoWebexMeetings',
                'gotomeeting': 'GoToMeeting', 'teamviewer': 'TeamViewer',
                
                # === GAMING ===
                'steam': 'steam', 'steam client': 'steam',
                'epic games': 'EpicGamesLauncher', 'epic': 'EpicGamesLauncher', 'epic launcher': 'EpicGamesLauncher',
                'origin': 'Origin', 'ea origin': 'Origin', 'ea desktop': 'EADesktop',
                'uplay': 'upc', 'ubisoft connect': 'UbisoftConnect',
                'battle.net': 'Battle.net', 'battlenet': 'Battle.net', 'blizzard': 'Battle.net',
                'gog galaxy': 'GalaxyClient', 'gog': 'GalaxyClient',
                'minecraft': 'Minecraft', 'minecraft launcher': 'MinecraftLauncher',
                'roblox': 'RobloxPlayerBeta', 'roblox player': 'RobloxPlayerBeta',
                'xbox game bar': 'GameBar', 'game bar': 'GameBar',
                'nvidia geforce': 'NVIDIA GeForce Experience', 'geforce experience': 'NVIDIA GeForce Experience',
                'amd radeon': 'RadeonSoftware', 'radeon software': 'RadeonSoftware',
                'msi afterburner': 'MSIAfterburner', 'afterburner': 'MSIAfterburner',
                'fraps': 'fraps', 'bandicam': 'bandicam',
                
                # === CREATIVE & DESIGN ===
                'photoshop': 'Photoshop', 'adobe photoshop': 'Photoshop', 'ps': 'Photoshop',
                'illustrator': 'Illustrator', 'adobe illustrator': 'Illustrator', 'ai': 'Illustrator',
                'indesign': 'InDesign', 'adobe indesign': 'InDesign', 'id': 'InDesign',
                'lightroom': 'Lightroom', 'adobe lightroom': 'Lightroom', 'lr': 'Lightroom',
                'acrobat': 'Acrobat', 'adobe acrobat': 'Acrobat', 'pdf reader': 'Acrobat',
                'dreamweaver': 'Dreamweaver', 'adobe dreamweaver': 'Dreamweaver',
                'animate': 'Animate', 'adobe animate': 'Animate', 'flash': 'Animate',
                'xd': 'Adobe XD', 'adobe xd': 'Adobe XD',
                'gimp': 'gimp', 'gnu image manipulation': 'gimp',
                'blender': 'blender', '3d modeling': 'blender',
                'figma': 'Figma', 'sketch': 'Sketch',
                'canva': 'Canva', 'canva desktop': 'Canva',
                'coreldraw': 'CorelDRAW', 'corel': 'CorelDRAW',
                'paint.net': 'PaintDotNet', 'paintnet': 'PaintDotNet',
                'krita': 'krita', 'inkscape': 'inkscape',
                'autodesk maya': 'maya', 'maya': 'maya',
                'autocad': 'acad', 'autodesk autocad': 'acad',
                '3ds max': '3dsmax', 'autodesk 3ds max': '3dsmax',
                'solidworks': 'SLDWORKS', 'fusion 360': 'Fusion360',
                
                # === PRODUCTIVITY ===
                'notion': 'Notion', 'notion desktop': 'Notion',
                'evernote': 'Evernote', 'evernote desktop': 'Evernote',
                'trello': 'Trello', 'trello desktop': 'Trello',
                'todoist': 'Todoist', 'todoist desktop': 'Todoist',
                'asana': 'Asana', 'monday': 'Monday',
                'clickup': 'ClickUp', 'airtable': 'Airtable',
                'obsidian': 'Obsidian', 'roam research': 'Roam',
                'logseq': 'Logseq', 'remnote': 'RemNote',
                'anki': 'anki', 'flashcards': 'anki',
                'zotero': 'zotero', 'mendeley': 'Mendeley Desktop',
                
                # === CLOUD STORAGE ===
                'dropbox': 'Dropbox', 'dropbox desktop': 'Dropbox',
                'google drive': 'GoogleDriveFS', 'drive': 'GoogleDriveFS',
                'icloud': 'iCloudServices', 'apple icloud': 'iCloudServices',
                'box': 'Box', 'box sync': 'Box Sync',
                'mega': 'MEGAsync', 'megasync': 'MEGAsync',
                'pcloud': 'pCloud', 'sync.com': 'Sync',
                
                # === UTILITIES & TOOLS ===
                'winrar': 'WinRAR', 'rar': 'WinRAR',
                '7zip': '7zFM', '7-zip': '7zFM', 'seven zip': '7zFM',
                'winzip': 'WINZIP32', 'zip': 'WINZIP32',
                'peazip': 'peazip', 'bandizip': 'Bandizip',
                'ccleaner': 'CCleaner64', 'system cleaner': 'CCleaner64',
                'malwarebytes': 'mbam', 'mbam': 'mbam',
                'avast': 'AvastUI', 'avg': 'AVGUI', 'norton': 'Norton',
                'kaspersky': 'Kaspersky', 'bitdefender': 'Bitdefender',
                'anydesk': 'AnyDesk', 'remote access': 'AnyDesk',
                'putty': 'putty', 'ssh client': 'putty',
                'filezilla': 'filezilla', 'ftp client': 'filezilla',
                'wireshark': 'Wireshark', 'network analyzer': 'Wireshark',
                'nmap': 'nmap', 'network scanner': 'nmap',
                'virtualbox': 'VirtualBox', 'vm': 'VirtualBox',
                'vmware': 'vmware', 'vmware workstation': 'vmware-vmx',
                'hyper-v': 'vmms', 'hyperv': 'vmms',
                'cpu-z': 'cpuz', 'gpu-z': 'GPU-Z',
                'hwinfo': 'HWiNFO64', 'speccy': 'Speccy64',
                'crystaldiskinfo': 'DiskInfo64', 'crystaldiskmark': 'DiskMark64',
                'process explorer': 'procexp64', 'process monitor': 'Procmon',
                'autoruns': 'Autoruns64', 'sysinternals': 'procexp64',
                'everything': 'Everything', 'file search': 'Everything',
                'powertoys': 'PowerToys', 'microsoft powertoys': 'PowerToys',
                'f.lux': 'flux', 'blue light filter': 'flux',
                'rainmeter': 'Rainmeter', 'desktop customization': 'Rainmeter',
                'wallpaper engine': 'wallpaper32', 'animated wallpaper': 'wallpaper32'
            }
            
            # Get actual process name
            actual_app_name = app_mappings.get(app_name.lower(), app_name)
            
            # If no exact match, try partial matching
            if actual_app_name == app_name:
                for key, value in app_mappings.items():
                    if app_name.lower() in key or key in app_name.lower():
                        actual_app_name = value
                        break
            
            # AI fallback for process name
            if actual_app_name == app_name:
                try:
                    from engine.dual_ai import dual_ai
                    ai_prompt = f'What is the exact process name for "{app_name}" on Windows? Respond with ONLY the process name (like "notepad" or "chrome"), no explanations.'
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant",
                            max_tokens=20
                        )
                        ai_process_name = response.choices[0].message.content.strip()
                        if ai_process_name and len(ai_process_name) < 50:
                            actual_app_name = ai_process_name
                except Exception:
                    pass
            
            # Try multiple methods to close the app
            success_count = 0
            
            try:
                # Method 1: Kill by mapped process name with .exe
                result = subprocess.run(f'taskkill /f /im "{actual_app_name}.exe"', 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0 and "SUCCESS" in result.stdout:
                    success_count += 1
            except:
                pass
            
            try:
                # Method 2: Kill by mapped process name without .exe
                result = subprocess.run(f'taskkill /f /im "{actual_app_name}"', 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0 and "SUCCESS" in result.stdout:
                    success_count += 1
            except:
                pass
            
            try:
                # Method 3: Kill by original name with .exe
                result = subprocess.run(f'taskkill /f /im "{app_name}.exe"', 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0 and "SUCCESS" in result.stdout:
                    success_count += 1
            except:
                pass
            
            try:
                # Method 4: Kill by original name without .exe
                result = subprocess.run(f'taskkill /f /im "{app_name}"', 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0 and "SUCCESS" in result.stdout:
                    success_count += 1
            except:
                pass
            
            try:
                # Method 5: Kill by window title (partial match)
                result = subprocess.run(f'taskkill /f /fi "WINDOWTITLE eq *{app_name}*"', 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0 and "SUCCESS" in result.stdout:
                    success_count += 1
            except:
                pass
            
            if success_count > 0:
                return f"Closed {app_name} successfully"
            else:
                return f"Could not close {app_name}. App may not be running or name not recognized."
                
        except Exception as e:
            return f"App closer failed: {e}"
    
    def port_scanner(self, query=""):
        try:
            import threading
            import re
            from datetime import datetime
            
            # Extract target and port range
            target = "127.0.0.1"  # localhost default
            start_port = 1
            end_port = 1000
            
            # Parse target IP/hostname
            ip_match = re.search(r'scan\s+([\d\.]+|\w+\.\w+)', query.lower())
            if ip_match:
                target = ip_match.group(1)
            
            # Parse port range
            port_match = re.search(r'port[s]?\s+(\d+)(?:-(\d+))?', query.lower())
            if port_match:
                start_port = int(port_match.group(1))
                end_port = int(port_match.group(2)) if port_match.group(2) else start_port
            
            # Limit scan range for safety
            if end_port - start_port > 1000:
                end_port = start_port + 1000
            
            open_ports = []
            
            def scan_port(host, port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
            
            # Start scanning
            start_time = datetime.now()
            threads = []
            
            for port in range(start_port, end_port + 1):
                thread = threading.Thread(target=scan_port, args=(target, port))
                threads.append(thread)
                thread.start()
                
                # Limit concurrent threads
                if len(threads) >= 50:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for thread in threads:
                thread.join()
            
            end_time = datetime.now()
            scan_duration = (end_time - start_time).total_seconds()
            
            # Common port services
            port_services = {
                21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP"
            }
            
            result = f"🔍 Port Scanner Results\n"
            result += f"Target: {target}\n"
            result += f"Scanned: {start_port}-{end_port}\n"
            result += f"Duration: {scan_duration:.2f}s\n\n"
            
            if open_ports:
                result += f"Open Ports ({len(open_ports)} found):\n"
                for port in sorted(open_ports):
                    service = port_services.get(port, "Unknown")
                    result += f"  {port}/tcp - {service}\n"
            else:
                result += "No open ports found\n"
            
            return result
            
        except Exception as e:
            return f"🔍 Port scanner failed: {e}"
    
    def _setup_auto_response(self, query):
        """Setup AI auto-response for incoming emails"""
        try:
            import threading
            import time
            import imaplib
            import email
            from email.header import decode_header
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
            
            if 'enable' in query.lower() or 'start' in query.lower():
                # Extract custom message from query
                import re
                import json
                import os
                
                # Extract meeting info and time
                custom_message = ""
                if 'meeting' in query.lower():
                    # Extract time info
                    time_match = re.search(r'(\d{1,2}\s*(?:am|pm|:\d{2}))', query.lower())
                    meeting_time = time_match.group(1) if time_match else "later"
                    
                    custom_message = f"Thank you for your email. I am currently in a meeting and will respond after {meeting_time}. Your message is important to me and I will get back to you as soon as possible."
                elif 'busy' in query.lower() or 'unavailable' in query.lower():
                    custom_message = "Thank you for your email. I am currently unavailable but will respond as soon as possible."
                
                # Save custom message
                with open('auto_reply_message.txt', 'w') as f:
                    f.write(custom_message)
                
                replied_emails = set()
                
                # Clear previous tracking
                if os.path.exists('replied_emails.json'):
                    os.remove('replied_emails.json')
                
                def auto_response_monitor():
                    while True:
                        try:
                            # Connect to Gmail IMAP
                            mail = imaplib.IMAP4_SSL('imap.gmail.com')
                            mail.login(SENDER_EMAIL, SENDER_PASSWORD)
                            mail.select('inbox')
                            
                            # Search for unread emails
                            status, messages = mail.search(None, 'UNSEEN')
                            
                            if messages[0]:
                                for msg_id in messages[0].split():
                                    # Fetch email
                                    status, msg_data = mail.fetch(msg_id, '(RFC822)')
                                    msg = email.message_from_bytes(msg_data[0][1])
                                    
                                    # Get sender and subject
                                    sender = msg['From']
                                    subject = msg['Subject']
                                    msg_id_str = msg_id.decode()
                                    
                                    # Skip if already replied to this email
                                    if msg_id_str in replied_emails:
                                        continue
                                    
                                    # Skip promotional/newsletter emails
                                    promotional_keywords = ['unsubscribe', 'newsletter', 'promotion', 'offer', 'deal', 'sale', 'marketing', 'noreply', 'no-reply']
                                    sender_lower = sender.lower()
                                    subject_lower = subject.lower() if subject else ''
                                    
                                    if any(keyword in sender_lower or keyword in subject_lower for keyword in promotional_keywords):
                                        print(f"SKIPPED PROMOTIONAL: {sender} - {subject}")
                                        mail.store(msg_id, '+FLAGS', '\\Seen')
                                        continue
                                    
                                    replied_emails.add(msg_id_str)
                                    
                                    # Get email body with error handling
                                    body = ""
                                    try:
                                        if msg.is_multipart():
                                            for part in msg.walk():
                                                if part.get_content_type() == "text/plain":
                                                    payload = part.get_payload(decode=True)
                                                    if payload:
                                                        body = payload.decode('utf-8', errors='ignore')
                                                        break
                                        else:
                                            payload = msg.get_payload(decode=True)
                                            if payload:
                                                body = payload.decode('utf-8', errors='ignore')
                                    except:
                                        body = "[Email content could not be decoded]"
                                    
                                    # Generate AI response
                                    try:
                                        # Check for custom message
                                        custom_msg = ""
                                        if os.path.exists('auto_reply_message.txt'):
                                            with open('auto_reply_message.txt', 'r') as f:
                                                custom_msg = f.read().strip()
                                        
                                        if custom_msg:
                                            ai_response = custom_msg
                                        else:
                                            from engine.dual_ai import dual_ai
                                            
                                            ai_prompt = f'''Generate a professional auto-reply for this email:
                                            From: {sender}
                                            Subject: {subject}
                                            Content: {body[:500]}...
                                            
                                            Respond with a helpful, professional auto-reply message (max 100 words).'''
                                            
                                            if dual_ai.ai_provider == 'groq':
                                                response = dual_ai.groq_client.chat.completions.create(
                                                    messages=[{"role": "user", "content": ai_prompt}],
                                                    model="llama-3.1-8b-instant"
                                                )
                                                ai_response = response.choices[0].message.content.strip()
                                            else:
                                                response = dual_ai.gemini_model.generate_content(ai_prompt)
                                                ai_response = response.text.strip()

                                        
                                        # Send auto-reply
                                        reply_msg = MIMEMultipart()
                                        reply_msg['From'] = SENDER_EMAIL
                                        reply_msg['To'] = sender
                                        reply_msg['Subject'] = f"Re: {subject}"
                                        reply_msg.attach(MIMEText(ai_response, 'plain'))
                                        
                                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                                        server.starttls()
                                        server.login(SENDER_EMAIL, SENDER_PASSWORD)
                                        server.sendmail(SENDER_EMAIL, sender, reply_msg.as_string())
                                        server.quit()
                                        
                                        # Log auto-reply activity
                                        print(f"AUTO-REPLY SENT: To {sender} - Subject: Re: {subject}")
                                        
                                        # Mark as read
                                        mail.store(msg_id, '+FLAGS', '\\Seen')
                                        
                                    except Exception as e:
                                        print(f"Auto-reply failed for {sender}: {e}")
                            
                            mail.close()
                            mail.logout()
                            
                        except Exception as e:
                            print(f"Email monitoring error: {e}")
                        
                        time.sleep(30)  # Check every 30 seconds
                
                threading.Thread(target=auto_response_monitor, daemon=True).start()
                return "EMAIL: AI Auto-response enabled - monitoring inbox every 30 seconds"
            
            elif 'disable' in query.lower() or 'stop' in query.lower():
                return "EMAIL: Auto-response disabled (restart to re-enable)"
            
            else:
                return "EMAIL: Auto-response commands - 'enable auto reply' or 'disable auto reply'"
                
        except Exception as e:
            return f"Auto-response setup failed: {e}"
    
    def _schedule_email(self, query):
        """Schedule email for later sending"""
        try:
            import re
            import json
            import os
            import threading
            import time
            from datetime import datetime, timedelta
            
            # Extract email details and timing - support multiple formats
            # Format 1: "send mail to user@email.com sub hello test in 5second"
            email_match = re.search(r'(?:send\s+mail\s+to|schedule\s+email\s+to)\s+([\w\.-]+@[\w\.-]+)\s+sub(?:ject)?\s+(.+?)\s+in\s+(\d+)\s*(second|seconds|minute|minutes|hour|hours)', query.lower())
            if not email_match:
                return "Usage: 'send mail to user@email.com sub Hello test in 5second'"
            
            recipient = email_match.group(1)
            subject = email_match.group(2).strip()
            delay_num = int(email_match.group(3))
            delay_unit = email_match.group(4)
            
            # Convert to seconds
            if 'hour' in delay_unit:
                delay_seconds = delay_num * 3600
            elif 'minute' in delay_unit:
                delay_seconds = delay_num * 60
            else:  # seconds
                delay_seconds = delay_num
            
            # Schedule the email
            schedule_time = datetime.now() + timedelta(seconds=delay_seconds)
            
            def send_scheduled_email():
                time.sleep(delay_seconds)
                # Send the actual email using existing email_sender logic
                from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                try:
                    msg = MIMEMultipart()
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = recipient
                    msg['Subject'] = subject
                    msg.attach(MIMEText(f"Scheduled message: {subject}", 'plain'))
                    
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
                    server.quit()
                except:
                    pass
            
            threading.Thread(target=send_scheduled_email, daemon=True).start()
            
            return f"EMAIL: Scheduled for {schedule_time.strftime('%Y-%m-%d %H:%M')} to {recipient} - Subject: {subject}"
            
        except Exception as e:
            return f"Email scheduling failed: {e}"
    
    def email_sender(self, query=""):
        try:
            import smtplib
            import re
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
            
            # Check for auto-response setup
            if 'auto reply' in query.lower() or 'auto response' in query.lower():
                return self._setup_auto_response(query)
            
            # Check for scheduling - detect 'in X seconds/minutes/hours'
            if 'schedule' in query.lower() or 'later' in query.lower() or re.search(r'\s+in\s+\d+\s*(second|seconds|minute|minutes|hour|hours)', query.lower()):
                return self._schedule_email(query)
            
            # Parse multiple email formats
            # Format 1: "send email to user@email.com subject hello message test"
            email_pattern1 = r'send\s+email\s+to\s+([\w\.-]+@[\w\.-]+)\s+subject\s+(.+?)\s+message\s+(.+)'
            # Format 2: "user@email.com sub hello test" (your format)
            email_pattern2 = r'([\w\.-]+@[\w\.-]+)\s+sub\s+(.+?)\s+(.+)'
            
            match = re.search(email_pattern1, query.lower()) or re.search(email_pattern2, query.lower())
            
            if not match:
                return "EMAIL: Formats - 1. 'send email to user@email.com subject Hello message Test' 2. 'user@email.com sub Hello Test'"
            
            recipient = match.group(1)
            subject = match.group(2).strip()
            message = match.group(3).strip()
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Send email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, recipient, text)
            server.quit()
            
            return f"EMAIL: Sent successfully to {recipient} - Subject: {subject} - Message: {message}"
            
        except Exception as e:
            return f"EMAIL: Failed - {str(e)} - Check your email_config.py settings"
    
    def financial_tools(self, query=""):
        try:
            from engine.dual_ai import dual_ai
            import requests
            import json
            import re
            from datetime import datetime
            
            # AI-powered expense tracker
            if "expense" in query.lower() or "spending" in query.lower():
                try:
                    ai_prompt = f'Extract expense info from: "{query}"\nRespond: Amount: [number]\nCategory: [category]\nAction: [add/show/total]'
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    
                    amount_match = re.search(r'Amount:\s*(\d+(?:\.\d{2})?)', ai_response)
                    category_match = re.search(r'Category:\s*(\w+)', ai_response)
                    action_match = re.search(r'Action:\s*(\w+)', ai_response)
                    
                    if amount_match and action_match and action_match.group(1).lower() == 'add':
                        amount = float(amount_match.group(1))
                        category = category_match.group(1) if category_match else "general"
                        
                        expense_file = "expenses.json"
                        try:
                            with open(expense_file, 'r') as f:
                                expenses = json.load(f)
                        except:
                            expenses = []
                        
                        expenses.append({
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "amount": amount,
                            "category": category,
                            "description": query
                        })
                        
                        with open(expense_file, 'w') as f:
                            json.dump(expenses, f, indent=2)
                        
                        return f"AI Expense Tracker: Added ${amount} for {category}"
                    
                    elif action_match and action_match.group(1).lower() in ['show', 'total']:
                        try:
                            with open("expenses.json", 'r') as f:
                                expenses = json.load(f)
                            total = sum(exp['amount'] for exp in expenses)
                            return f"AI Expense Analysis: Total ${total:.2f} across {len(expenses)} transactions"
                        except:
                            return "No expenses recorded yet"
                    
                except Exception:
                    pass
                
                return "AI Expense Tracker: Say 'add expense 50 on food' or 'show total expenses'"
            
            # Real-time currency converter
            elif "convert" in query.lower() and "currency" in query.lower():
                try:
                    amount_match = re.search(r'(\d+(?:\.\d{2})?)', query)
                    currency_match = re.search(r'(\w{3})\s+to\s+(\w{3})', query.upper())
                    
                    if amount_match and currency_match:
                        amount = float(amount_match.group(1))
                        from_curr = currency_match.group(1)
                        to_curr = currency_match.group(2)
                        
                        # Real-time API
                        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
                        response = requests.get(url, timeout=5)
                        
                        if response.status_code == 200:
                            data = response.json()
                            rate = data['rates'].get(to_curr)
                            
                            if rate:
                                converted = amount * rate
                                return f"Real-time Currency: {amount} {from_curr} = {converted:.2f} {to_curr}\nLive Rate: 1 {from_curr} = {rate:.4f} {to_curr}"
                    
                    return "Format: 'convert 100 USD to EUR'"
                except Exception as e:
                    return f"Currency API error: {e}"
            
            # Real-time stock/crypto prices
            elif "stock" in query.lower() or "crypto" in query.lower() or "price" in query.lower():
                symbol_match = re.search(r'(\w+)\s+(?:stock|price|crypto)', query.lower())
                
                if symbol_match:
                    symbol = symbol_match.group(1).upper()
                    
                    try:
                        # Try real crypto API first
                        if symbol in ['BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'DOGE']:
                            crypto_url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
                            response = requests.get(crypto_url, timeout=5)
                            if response.status_code == 200:
                                data = response.json()
                                if symbol.lower() in data:
                                    price = data[symbol.lower()]['usd']
                                    return f"Live Crypto: {symbol} = ${price:,.2f} USD"
                        
                        # Indian stocks mapping
                        indian_stocks = {
                            'TATA': 'TATAMOTORS.NS',
                            'TCS': 'TCS.NS', 
                            'RELIANCE': 'RELIANCE.NS',
                            'INFY': 'INFY.NS',
                            'HDFC': 'HDFCBANK.NS',
                            'ICICI': 'ICICIBANK.NS',
                            'SBI': 'SBIN.NS',
                            'ITC': 'ITC.NS',
                            'WIPRO': 'WIPRO.NS',
                            'BHARTI': 'BHARTIARTL.NS'
                        }
                        
                        # Check if it's an Indian stock
                        yahoo_symbol = symbol
                        if symbol in indian_stocks:
                            yahoo_symbol = indian_stocks[symbol]
                        
                        # Try Yahoo Finance API
                        stock_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
                        response = requests.get(stock_url, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if 'chart' in data and data['chart']['result'] and len(data['chart']['result']) > 0:
                                result = data['chart']['result'][0]
                                if 'meta' in result and 'regularMarketPrice' in result['meta']:
                                    price = result['meta']['regularMarketPrice']
                                    currency = result['meta'].get('currency', 'USD')
                                    
                                    if symbol in indian_stocks:
                                        return f"Live Indian Stock: {symbol} = Rs.{price:.2f} INR"
                                    else:
                                        return f"Live Stock: {symbol} = ${price:.2f} {currency}"
                        
                        # Use Gemini AI for stock information
                        try:
                            ai_prompt = f'Get current stock information for {symbol}. Provide: Current Price, Market Cap, 52-week high/low, and brief analysis. Format as: Stock: {symbol}\nPrice: $X.XX\nMarket Cap: $X.XB\nAnalysis: [brief market insight]'
                            
                            if dual_ai.ai_provider == 'groq':
                                response = dual_ai.groq_client.chat.completions.create(
                                    messages=[{"role": "user", "content": ai_prompt}],
                                    model="llama-3.1-8b-instant"
                                )
                                ai_response = response.choices[0].message.content.strip()
                            else:
                                response = dual_ai.gemini_model.generate_content(ai_prompt)
                                ai_response = response.text.strip()
                            
                            return f"AI Stock Analysis:\n{ai_response}"
                        
                        except Exception as e:
                            return f"AI stock analysis failed: {e}"
                    
                    except Exception as e:
                        return f"Price API error: {e}"
                else:
                    return "Format: 'AAPL stock price', 'TATA stock price', or 'BTC crypto price'"
            
            # Real-time movie info
            elif "movie" in query.lower() or "imdb" in query.lower():
                movie_match = re.search(r'movie\s+(.+?)(?:\s+rating|$)', query.lower())
                
                if movie_match:
                    movie_name = movie_match.group(1).strip()
                    
                    try:
                        # Try OMDB API (free with demo key)
                        omdb_url = f"http://www.omdbapi.com/?t={movie_name}&apikey=demo"
                        response = requests.get(omdb_url, timeout=5)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if data.get('Response') == 'True':
                                title = data.get('Title', 'Unknown')
                                year = data.get('Year', 'Unknown')
                                rating = data.get('imdbRating', 'N/A')
                                genre = data.get('Genre', 'Unknown')
                                plot = data.get('Plot', 'No plot available')
                                
                                result = f"Live Movie Info:\n"
                                result += f"Title: {title}\n"
                                result += f"Year: {year}\n"
                                result += f"IMDb Rating: {rating}/10\n"
                                result += f"Genre: {genre}\n"
                                result += f"Plot: {plot[:100]}..."
                                
                                return result
                        
                        # Try TMDB API alternative
                        tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key=demo&query={movie_name}"
                        response = requests.get(tmdb_url, timeout=5)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if data.get('results'):
                                movie = data['results'][0]
                                title = movie.get('title', 'Unknown')
                                year = movie.get('release_date', 'Unknown')[:4] if movie.get('release_date') else 'Unknown'
                                rating = movie.get('vote_average', 'N/A')
                                overview = movie.get('overview', 'No overview available')
                                
                                result = f"Live Movie Info (TMDB):\n"
                                result += f"Title: {title}\n"
                                result += f"Year: {year}\n"
                                result += f"Rating: {rating}/10\n"
                                result += f"Overview: {overview[:100]}..."
                                
                                return result
                        
                        return f"Movie '{movie_name}' not found in databases. Check spelling or try another title."
                    
                    except Exception as e:
                        return f"Movie API error: {e}"
                else:
                    return "Format: 'movie inception' or 'imdb avatar'"
            
            # AI-powered location-specific news
            # AI-powered location-specific news
            elif "news" in query.lower():
                try:
                    # Extract location and count from query
                    location_match = re.search(r'news\s+on\s+(\w+)', query.lower())
                    count_match = re.search(r'(\d+)\s+news', query.lower())
                    
                    location = location_match.group(1) if location_match else "general"
                    count = int(count_match.group(1)) if count_match else 5
                    
                    # Use Gemini for real-time news, Groq as fallback
                    from engine.dual_ai import dual_ai
                    
                    try:
                        ai_prompt = f'Get latest {count} real-time news headlines about {location}. Include brief descriptions.'
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    except:
                        ai_prompt = f'Generate {count} news headlines about {location}. Format: 1. [Headline]\n   [Description]'
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    
                    return f"News for {location.title()}:\n{ai_response}"
                
                except Exception as e:
                    return f"News error: {e}"


                    

            
            # AI joke generator
            elif "joke" in query.lower():
                try:
                    ai_prompt = 'Generate a funny, clean joke. Make it original and clever.'
                    
                    if dual_ai.ai_provider == 'groq':
                        response = dual_ai.groq_client.chat.completions.create(
                            messages=[{"role": "user", "content": ai_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        ai_response = response.choices[0].message.content.strip()
                    else:
                        response = dual_ai.gemini_model.generate_content(ai_prompt)
                        ai_response = response.text.strip()
                    
                    return f"AI Joke: {ai_response}"
                
                except Exception as e:
                    return f"AI joke failed: {e}"
            
            # Spotify with AI
            elif "spotify" in query.lower():
                try:
                    import subprocess
                    
                    if "play" in query.lower():
                        subprocess.run(['nircmd', 'sendkeypress', 'media_play_pause'], check=False)
                        return "Spotify: Playing music"
                    elif "pause" in query.lower():
                        subprocess.run(['nircmd', 'sendkeypress', 'media_play_pause'], check=False)
                        return "Spotify: Paused"
                    elif "next" in query.lower():
                        subprocess.run(['nircmd', 'sendkeypress', 'media_next_track'], check=False)
                        return "Spotify: Next track"
                    elif "previous" in query.lower():
                        subprocess.run(['nircmd', 'sendkeypress', 'media_prev_track'], check=False)
                        return "Spotify: Previous track"
                    else:
                        return "Spotify AI: Commands - play, pause, next, previous"
                
                except Exception as e:
                    return f"Spotify control failed: {e}"
            
            else:
                return "AI Financial Tools: expense tracker, real-time currency, live stock/crypto prices, spotify control, AI movie info, live news, AI jokes"
        
        except Exception as e:
            return f"Financial AI tools error: {e}"
    
    def speed_test(self, query=""):
        try:
            import time
            import requests
            import subprocess
            
            def ping_test():
                try:
                    result = subprocess.run(['ping', '-n', '4', '8.8.8.8'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        import re
                        avg_match = re.search(r'Average = (\d+)ms', result.stdout)
                        return int(avg_match.group(1)) if avg_match else 0
                    return 0
                except:
                    return 0
            
            def download_test():
                try:
                    start_time = time.time()
                    test_url = "http://speedtest.ftp.otenet.gr/files/test1Mb.db"
                    response = requests.get(test_url, timeout=30)
                    download_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        file_size_mb = len(response.content) / (1024 * 1024)
                        download_speed = (file_size_mb / download_time) * 8
                        return download_speed
                    return 0
                except:
                    return 0
            
            def upload_test():
                try:
                    start_time = time.time()
                    test_data = b'0' * (100 * 1024)
                    response = requests.post('https://httpbin.org/post', data=test_data, timeout=10)
                    upload_time = time.time() - start_time
                    upload_speed = (0.1 / upload_time) * 8 if upload_time > 0 else 0
                    return upload_speed
                except:
                    return 0
            
            ping = ping_test()
            download_speed = download_test()
            upload_speed = upload_test()
            
            result = f"Internet Speed Test Results:\n"
            result += f"Download: {download_speed:.1f} Mbps\n"
            result += f"Upload: {upload_speed:.1f} Mbps\n"
            result += f"Ping: {ping} ms\n"
            
            if download_speed > 25:
                result += "Status: Excellent connection"
            elif download_speed > 10:
                result += "Status: Good connection"
            elif download_speed > 5:
                result += "Status: Average connection"
            else:
                result += "Status: Slow connection"
            
            return result
        
        except Exception as e:
            return f"Speed test failed: {e}"
    
    def battery_health(self, query=""):
        try:
            import psutil
            import subprocess
            from datetime import datetime
            
            # Get battery information
            battery = psutil.sensors_battery()
            if not battery:
                return "Battery not detected (desktop computer or battery unavailable)"
            
            # Basic battery info
            percent = battery.percent
            plugged = battery.power_plugged
            
            # Get detailed battery info (Windows)
            try:
                result = subprocess.run(['powercfg', '/batteryreport', '/output', 'battery_report.html'], 
                                      capture_output=True, text=True, timeout=10)
                report_generated = result.returncode == 0
            except:
                report_generated = False
            
            # Battery health analysis
            health_status = "Good"
            warnings = []
            
            if percent < 20 and not plugged:
                warnings.append("Low battery - charge soon")
                health_status = "Needs charging"
            
            if plugged and percent > 95:
                warnings.append("Overcharging detected - unplug to preserve battery")
            
            # Estimate cycles (simplified)
            try:
                # Get battery design capacity vs current capacity
                wmi_result = subprocess.run(['wmic', 'path', 'Win32_Battery', 'get', 'DesignCapacity,FullChargeCapacity'], 
                                          capture_output=True, text=True, timeout=5)
                if wmi_result.returncode == 0:
                    lines = wmi_result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        data = lines[1].split()
                        if len(data) >= 2:
                            design_cap = int(data[0]) if data[0].isdigit() else 0
                            current_cap = int(data[1]) if data[1].isdigit() else 0
                            if design_cap > 0 and current_cap > 0:
                                health_percent = (current_cap / design_cap) * 100
                                if health_percent < 80:
                                    warnings.append(f"Battery degraded to {health_percent:.1f}% of original capacity")
                                    health_status = "Degraded"
            except:
                pass
            
            # Create result
            result = f"Battery Health Monitor:\n"
            result += f"Current charge: {percent}%\n"
            result += f"Power adapter: {'Connected' if plugged else 'Disconnected'}\n"
            result += f"Health status: {health_status}\n"
            
            if warnings:
                result += f"\nWarnings:\n"
                for warning in warnings:
                    result += f"⚠️ {warning}\n"
            
            if report_generated:
                result += f"\nDetailed report: battery_report.html"
            
            # Show notification for critical issues
            if percent < 15 and not plugged:
                self._show_notification("🔋 Critical Battery", f"Battery at {percent}% - Charge immediately!")
            elif warnings:
                self._show_notification("🔋 Battery Alert", warnings[0])
            
            return result
            
        except Exception as e:
            return f"Battery health check failed: {e}"
    
    def thermal_monitor(self, query=""):
        try:
            import psutil
            import subprocess
            from datetime import datetime
            
            # Get CPU temperature and usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Try to get temperature sensors
            temperatures = {}
            alerts = []
            
            try:
                # Windows: Try WMI for temperature
                wmi_result = subprocess.run(['wmic', '/namespace:\\\\root\\wmi', 'PATH', 'MSAcpi_ThermalZoneTemperature', 'get', 'CurrentTemperature'], 
                                          capture_output=True, text=True, timeout=5)
                if wmi_result.returncode == 0:
                    lines = wmi_result.stdout.strip().split('\n')
                    for line in lines[1:]:
                        if line.strip().isdigit():
                            # Convert from tenths of Kelvin to Celsius
                            temp_kelvin = int(line.strip()) / 10
                            temp_celsius = temp_kelvin - 273.15
                            temperatures['CPU'] = temp_celsius
                            break
            except:
                pass
            
            # Try psutil sensors (Linux/some Windows systems)
            try:
                sensors = psutil.sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        for entry in entries:
                            label = entry.label or name
                            temp = entry.current
                            temperatures[label] = temp
            except:
                pass
            
            # If no temperature sensors, estimate from CPU usage
            if not temperatures:
                estimated_temp = 30 + (cpu_percent * 0.5)  # Rough estimation
                temperatures['CPU (estimated)'] = estimated_temp
            
            # Analyze temperatures and generate alerts
            critical_temp = 85
            warning_temp = 75
            
            for component, temp in temperatures.items():
                if temp > critical_temp:
                    alerts.append(f"🔥 CRITICAL: {component} at {temp:.1f}°C - System may shutdown!")
                elif temp > warning_temp:
                    alerts.append(f"⚠️ WARNING: {component} at {temp:.1f}°C - High temperature")
            
            # Check CPU usage for thermal correlation
            if cpu_percent > 90:
                alerts.append(f"🔥 High CPU usage ({cpu_percent}%) may cause overheating")
            
            # Create result
            result = f"Thermal Monitor:\n"
            result += f"CPU Usage: {cpu_percent}%\n"
            
            if temperatures:
                result += f"\nTemperatures:\n"
                for component, temp in temperatures.items():
                    status = "🔥" if temp > critical_temp else "⚠️" if temp > warning_temp else "✅"
                    result += f"{status} {component}: {temp:.1f}°C\n"
            else:
                result += "\nTemperature sensors not available\n"
            
            # Add thermal guidelines
            result += f"\nThermal Guidelines:\n"
            result += f"✅ Normal: < 75°C\n"
            result += f"⚠️ Warning: 75-85°C\n"
            result += f"🔥 Critical: > 85°C\n"
            
            if alerts:
                result += f"\nAlerts:\n"
                for alert in alerts:
                    result += f"{alert}\n"
                
                # Show notification for critical temperatures
                if any("CRITICAL" in alert for alert in alerts):
                    self._show_notification("🔥 OVERHEATING ALERT", "Critical temperature detected! Check cooling system.")
                elif any("WARNING" in alert for alert in alerts):
                    self._show_notification("⚠️ Temperature Warning", "High temperature detected - monitor system")
            
            return result
            
        except Exception as e:
            return f"Thermal monitoring failed: {e}"
    
    def disk_health_scanner(self, query=""):
        try:
            import subprocess
            import re
            from datetime import datetime
            
            # Get disk information using WMIC (Windows)
            try:
                # Get disk health using SMART data
                smart_result = subprocess.run(['wmic', 'diskdrive', 'get', 'status,size,model'], 
                                            capture_output=True, text=True, timeout=10)
                
                if smart_result.returncode == 0:
                    lines = smart_result.stdout.strip().split('\n')
                    disk_info = []
                    
                    for line in lines[1:]:  # Skip header
                        if line.strip():
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                disk_info.append(line.strip())
                
                # Get disk space information
                space_result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], 
                                            capture_output=True, text=True, timeout=10)
                
                disk_space = []
                if space_result.returncode == 0:
                    lines = space_result.stdout.strip().split('\n')
                    for line in lines[1:]:
                        if line.strip() and 'Caption' not in line:
                            parts = line.strip().split()
                            if len(parts) >= 3:
                                caption = parts[0]
                                free_space = int(parts[1]) if parts[1].isdigit() else 0
                                total_space = int(parts[2]) if parts[2].isdigit() else 0
                                
                                if total_space > 0:
                                    used_space = total_space - free_space
                                    usage_percent = (used_space / total_space) * 100
                                    
                                    disk_space.append({
                                        'drive': caption,
                                        'total_gb': total_space // (1024**3),
                                        'free_gb': free_space // (1024**3),
                                        'used_percent': usage_percent
                                    })
                
                # Create health report
                result = f"Disk Health Scanner:\n"
                result += f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                # Disk status
                if disk_info:
                    result += "Physical Disks:\n"
                    for info in disk_info[:3]:  # Show first 3 disks
                        result += f"- {info}\n"
                else:
                    result += "Physical Disks: Status OK\n"
                
                # Disk space analysis
                if disk_space:
                    result += "\nDisk Space Analysis:\n"
                    warnings = []
                    
                    for disk in disk_space:
                        drive = disk['drive']
                        total = disk['total_gb']
                        free = disk['free_gb']
                        used_pct = disk['used_percent']
                        
                        status = "✅ Good"
                        if used_pct > 90:
                            status = "🔴 Critical"
                            warnings.append(f"Drive {drive} is {used_pct:.1f}% full - Clean up space immediately!")
                        elif used_pct > 80:
                            status = "⚠️ Warning"
                            warnings.append(f"Drive {drive} is {used_pct:.1f}% full - Consider cleanup")
                        
                        result += f"Drive {drive}: {free}GB free / {total}GB total ({used_pct:.1f}% used) {status}\n"
                    
                    # Show warnings
                    if warnings:
                        result += "\nWarnings:\n"
                        for warning in warnings:
                            result += f"⚠️ {warning}\n"
                        
                        # Show critical notification
                        if any("Critical" in w for w in warnings):
                            self._show_notification("🔴 Disk Space Critical", "One or more drives are critically full!")
                        elif warnings:
                            self._show_notification("⚠️ Disk Space Warning", "Some drives are getting full")
                
                # Health recommendations
                result += "\nHealth Recommendations:\n"
                result += "✅ Run disk cleanup regularly\n"
                result += "✅ Check for disk errors: chkdsk /f\n"
                result += "✅ Defragment HDDs monthly\n"
                result += "✅ Monitor SMART data for early warnings\n"
                
                return result
                
            except subprocess.TimeoutExpired:
                return "Disk health scan timed out - system may be busy"
            except Exception as scan_error:
                return f"Disk scan error: {scan_error}"
                
        except Exception as e:
            return f"Disk health scanner failed: {e}"
    
    def usb_device_manager(self, query=""):
        try:
            import subprocess
            import re
            from datetime import datetime
            
            # Get USB device information (Windows)
            try:
                # Get USB devices using WMIC
                usb_result = subprocess.run(['wmic', 'path', 'Win32_USBHub', 'get', 'Name,DeviceID,Status'], 
                                          capture_output=True, text=True, timeout=10)
                
                usb_devices = []
                if usb_result.returncode == 0:
                    lines = usb_result.stdout.strip().split('\n')
                    for line in lines[1:]:
                        if line.strip() and 'DeviceID' not in line:
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                usb_devices.append(line.strip())
                
                # Get removable drives
                drives_result = subprocess.run(['wmic', 'logicaldisk', 'where', 'drivetype=2', 'get', 'caption,label,size'], 
                                             capture_output=True, text=True, timeout=10)
                
                removable_drives = []
                if drives_result.returncode == 0:
                    lines = drives_result.stdout.strip().split('\n')
                    for line in lines[1:]:
                        if line.strip() and 'Caption' not in line:
                            parts = line.strip().split()
                            if len(parts) >= 1:
                                removable_drives.append(line.strip())
                
                # Create device report
                result = f"USB Device Manager:\n"
                result += f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                # USB Hubs and Controllers
                if usb_devices:
                    result += f"USB Controllers ({len(usb_devices)}):\n"
                    for device in usb_devices[:5]:  # Show first 5
                        result += f"- {device}\n"
                else:
                    result += "USB Controllers: None detected\n"
                
                # Removable drives
                if removable_drives:
                    result += f"\nRemovable Drives ({len(removable_drives)}):\n"
                    for drive in removable_drives:
                        result += f"- {drive}\n"
                else:
                    result += "\nRemovable Drives: None connected\n"
                
                # USB Safety tips
                result += "\nUSB Safety Tips:\n"
                result += "✅ Safely eject before removing\n"
                result += "✅ Scan for malware regularly\n"
                result += "✅ Use trusted devices only\n"
                result += "✅ Keep drivers updated\n"
                
                # Quick actions
                result += "\nQuick Actions:\n"
                result += "- 'eject usb' - Safely eject all removable drives\n"
                result += "- 'scan usb' - Check for malware\n"
                
                return result
                
            except subprocess.TimeoutExpired:
                return "USB device scan timed out"
            except Exception as scan_error:
                return f"USB scan error: {scan_error}"
                
        except Exception as e:
            return f"USB device manager failed: {e}"
    
    def quick_note_taker(self, query=""):
        try:
            import json
            import os
            from datetime import datetime
            
            notes_file = "quick_notes.json"
            
            # Load existing notes
            notes = []
            if os.path.exists(notes_file):
                try:
                    with open(notes_file, 'r', encoding='utf-8') as f:
                        notes = json.load(f)
                except:
                    notes = []
            
            # List recent notes first
            if 'list' in query.lower() or 'show' in query.lower():
                if not notes:
                    return "[NOTE] No notes found. Create your first: 'quick note [your note]'"
                
                # Show last 10 notes
                recent_notes = notes[-10:]
                result = f"[NOTE] Quick Notes ({len(notes)} total):\n" + "="*40 + "\n"
                
                for note in reversed(recent_notes):
                    result += f"#{note['id']} [{note['time']}] {note['text']}\n"
                
                return result
            
            # Add new note
            elif any(word in query.lower() for word in ['note', 'remember', 'log', 'record']) or query.strip():
                # Extract note content
                note_text = ""
                if 'note' in query.lower():
                    import re
                    note_match = re.search(r'(?:note|take note|quick note)\s+(.+)', query, re.IGNORECASE)
                    if note_match:
                        note_text = note_match.group(1).strip()
                elif len(query.strip()) > 0:
                    note_text = query.strip()
                
                if not note_text:
                    return "[NOTE] Usage: 'quick note [your note]' or 'note meeting at 3pm'"
                
                # Create timestamped note
                timestamp = datetime.now()
                note_entry = {
                    'id': len(notes) + 1,
                    'text': note_text,
                    'timestamp': timestamp.isoformat(),
                    'date': timestamp.strftime('%Y-%m-%d'),
                    'time': timestamp.strftime('%H:%M:%S')
                }
                
                notes.append(note_entry)
                
                # Save notes
                with open(notes_file, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, indent=2, ensure_ascii=False)
                
                self._show_notification("Note Saved", f"Note #{note_entry['id']}: {note_text[:50]}..." if len(note_text) > 50 else f"Note #{note_entry['id']}: {note_text}")
                
                return f"[NOTE] #{note_entry['id']} saved at {note_entry['time']}\n'{note_text}'"
            
            # Search notes
            elif 'search' in query.lower():
                import re
                search_match = re.search(r'search\s+(.+)', query, re.IGNORECASE)
                if search_match:
                    search_term = search_match.group(1).strip().lower()
                    
                    matching_notes = [note for note in notes if search_term in note['text'].lower()]
                    
                    if matching_notes:
                        result = f"[NOTE] Found {len(matching_notes)} notes for '{search_term}':\n"
                        for note in matching_notes[-5:]:  # Last 5 matches
                            result += f"#{note['id']} [{note['time']}] {note['text']}\n"
                        return result
                    else:
                        return f"[NOTE] No notes found containing '{search_term}'"
                else:
                    return "[NOTE] Usage: 'search [keyword]'"
            
            # Delete note
            elif 'delete' in query.lower():
                import re
                delete_match = re.search(r'delete\s+(?:note\s+)?(\d+)', query, re.IGNORECASE)
                if delete_match:
                    note_id = int(delete_match.group(1))
                    
                    # Find and remove note
                    for i, note in enumerate(notes):
                        if note['id'] == note_id:
                            deleted_note = notes.pop(i)
                            
                            # Save updated notes
                            with open(notes_file, 'w', encoding='utf-8') as f:
                                json.dump(notes, f, indent=2, ensure_ascii=False)
                            
                            return f" Deleted note #{note_id}: '{deleted_note['text']}'"
                    
                    return f"Note #{note_id} not found"
                else:
                    return " Usage: 'delete note [number]'"
            
            # Default help
            else:
                return " Quick Note Taker Commands:\n• 'quick note [text]' - Add note\n• 'list notes' - Show recent notes\n• 'search [keyword]' - Find notes\n• 'delete note [number]' - Remove note"
                
        except Exception as e:
            return f"Quick note taker failed: {e}"
    
    def large_file_scanner(self, query=""):
        try:
            import os
            from datetime import datetime
            
            # Default scan path
            scan_path = "C:\\" if os.path.exists("C:\\") else os.path.expanduser("~")
            
            # Extract custom path if provided
            if 'scan' in query.lower() and (':\\' in query or '/' in query):
                import re
                path_match = re.search(r'([A-Za-z]:\\[^\s]+|/[^\s]+)', query)
                if path_match:
                    custom_path = path_match.group(1)
                    if os.path.exists(custom_path):
                        scan_path = custom_path
            
            large_files = []
            min_size = 100 * 1024 * 1024  # 100MB threshold
            
            # Scan for large files
            for root, dirs, files in os.walk(scan_path):
                # Skip system directories
                dirs[:] = [d for d in dirs if d not in ['System Volume Information', '$Recycle.Bin', 'Windows']]
                
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        
                        if size > min_size:
                            size_mb = size / (1024 * 1024)
                            large_files.append({
                                'path': file_path,
                                'size': size,
                                'size_mb': round(size_mb, 1),
                                'name': file
                            })
                        
                        # Limit scan to prevent timeout
                        if len(large_files) >= 20:
                            break
                    except (OSError, PermissionError):
                        continue
                
                if len(large_files) >= 20:
                    break
            
            # Sort by size (largest first)
            large_files.sort(key=lambda x: x['size'], reverse=True)
            
            result = f"Large File Scanner - {scan_path}\n"
            result += f"Scan Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            if large_files:
                result += f"Found {len(large_files)} files >100MB:\n"
                for file in large_files[:10]:  # Show top 10
                    result += f"• {file['size_mb']}MB - {file['name']}\n"
            else:
                result += "No large files (>100MB) found\n"
            
            return result
            
        except Exception as e:
            return f"Large file scanner failed: {e}"
    
    def file_search_engine(self, query=""):
        try:
            import os
            import re
            from datetime import datetime
            
            # Extract search term
            search_term = ""
            if 'search' in query.lower():
                search_match = re.search(r'search\s+(?:for\s+)?(.+)', query, re.IGNORECASE)
                if search_match:
                    search_term = search_match.group(1).strip()
            elif query.strip():
                search_term = query.strip()
            
            if not search_term:
                return "File Search Engine\nUsage: 'search [filename]' or 'find [keyword]'"
            
            # Search locations
            search_paths = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads"),
                "C:\\Users\\Hp\\Videos\\inp"  # Current workspace
            ]
            
            found_files = []
            
            for search_path in search_paths:
                if not os.path.exists(search_path):
                    continue
                
                try:
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            if search_term.lower() in file.lower():
                                file_path = os.path.join(root, file)
                                try:
                                    size = os.path.getsize(file_path)
                                    modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                                    
                                    found_files.append({
                                        'name': file,
                                        'path': file_path,
                                        'size': size,
                                        'modified': modified.strftime('%Y-%m-%d %H:%M')
                                    })
                                except (OSError, PermissionError):
                                    continue
                        
                        # Limit results
                        if len(found_files) >= 15:
                            break
                except (OSError, PermissionError):
                    continue
            
            # Sort by modification time (newest first)
            found_files.sort(key=lambda x: x['modified'], reverse=True)
            
            result = f"File Search Results for '{search_term}'\n"
            result += f"Found {len(found_files)} files:\n\n"
            
            if found_files:
                for file in found_files[:10]:  # Show top 10
                    size_kb = file['size'] / 1024
                    result += f"📄 {file['name']}\n"
                    result += f"   📁 {file['path']}\n"
                    result += f"   📅 {file['modified']} | {size_kb:.1f}KB\n\n"
            else:
                result += f"No files found containing '{search_term}'\n"
            
            return result
            
        except Exception as e:
            return f"File search engine failed: {e}"
    
    def recent_files_tracker(self, query=""):
        try:
            import os
            import json
            import subprocess
            from datetime import datetime, timedelta
            
            recent_file = "recent_files.json"
            
            # Parse query for number and open command
            show_count = 12  # default
            open_file = False
            
            if query:
                # Extract number if specified
                import re
                numbers = re.findall(r'\d+', query)
                if numbers:
                    show_count = min(int(numbers[0]), 20)  # max 20
                
                # Check for open command
                if 'open' in query.lower():
                    open_file = True
            
            # Load existing recent files
            recent_files = []
            if os.path.exists(recent_file):
                try:
                    with open(recent_file, 'r', encoding='utf-8') as f:
                        recent_files = json.load(f)
                except:
                    recent_files = []
            
            # Auto-scan common directories for recent files
            scan_paths = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads"),
                "C:\\Users\\Hp\\Videos\\inp"
            ]
            
            current_files = []
            cutoff_time = datetime.now() - timedelta(days=7)
            
            for scan_path in scan_paths:
                if not os.path.exists(scan_path):
                    continue
                
                try:
                    for root, dirs, files in os.walk(scan_path):
                        if root.count(os.sep) - scan_path.count(os.sep) > 2:
                            continue
                        
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                                
                                if modified_time > cutoff_time:
                                    current_files.append({
                                        'name': file,
                                        'path': file_path,
                                        'modified': modified_time.isoformat(),
                                        'modified_str': modified_time.strftime('%Y-%m-%d %H:%M'),
                                        'size': os.path.getsize(file_path)
                                    })
                                
                                if len(current_files) >= 25:
                                    break
                            except (OSError, PermissionError):
                                continue
                        
                        if len(current_files) >= 25:
                            break
                except (OSError, PermissionError):
                    continue
            
            # Sort by modification time (newest first)
            current_files.sort(key=lambda x: x['modified'], reverse=True)
            recent_files = current_files[:20]
            
            # Save updated list
            try:
                with open(recent_file, 'w', encoding='utf-8') as f:
                    json.dump(recent_files, f, indent=2, ensure_ascii=False)
            except:
                pass
            
            # Open file if requested
            if open_file and recent_files:
                try:
                    os.startfile(recent_files[0]['path'])
                    return f"Opening: {recent_files[0]['name']}"
                except Exception as e:
                    return f"Failed to open file: {e}"
            
            result = f"Recent Files (Last 7 days) - Showing {min(show_count, len(recent_files))}\n"
            result += f"Updated: {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            if recent_files:
                for i, file in enumerate(recent_files[:show_count], 1):
                    size_kb = file['size'] / 1024
                    result += f"{i}. 📄 {file['name']}\n"
                    result += f"   📅 {file['modified_str']} | {size_kb:.1f}KB\n\n"
            else:
                result += "No recent files found\n"
            
            return result
            
        except Exception as e:
            return f"Recent files tracker failed: {e}"
    
    def recently_installed_apps(self, query=""):
        try:
            import subprocess
            import re
            from datetime import datetime, timedelta
            
            # Parse query for number
            show_count = 10  # default
            if query:
                numbers = re.findall(r'\d+', query)
                if numbers:
                    show_count = min(int(numbers[0]), 50)  # max 50
            
            # Get installed apps using PowerShell
            cmd = "Get-WmiObject -Class Win32_Product | Select-Object Name, InstallDate | Sort-Object InstallDate -Descending"
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return "Failed to retrieve installed apps"
            
            lines = result.stdout.strip().split('\n')
            apps = []
            
            for line in lines[3:]:  # Skip header lines
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        date_str = parts[-1]
                        name = ' '.join(parts[:-1])
                        
                        if date_str and date_str != 'InstallDate':
                            try:
                                # Parse date format YYYYMMDD
                                if len(date_str) == 8 and date_str.isdigit():
                                    install_date = datetime.strptime(date_str, '%Y%m%d')
                                    apps.append({
                                        'name': name,
                                        'date': install_date.strftime('%Y-%m-%d'),
                                        'days_ago': (datetime.now() - install_date).days
                                    })
                            except:
                                continue
            
            # Sort by install date (newest first)
            apps.sort(key=lambda x: x['date'], reverse=True)
            
            output = f"Recently Installed Apps - Showing {min(show_count, len(apps))}\n"
            output += f"Updated: {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            if apps:
                for i, app in enumerate(apps[:show_count], 1):
                    days_text = "today" if app['days_ago'] == 0 else f"{app['days_ago']} days ago"
                    output += f"{i}. 📱 {app['name']}\n"
                    output += f"   📅 {app['date']} ({days_text})\n\n"
            else:
                output += "No recently installed apps found\n"
            
            return output
            
        except Exception as e:
            return f"Recently installed apps failed: {e}"
    


    
    def open_website(self, query=""):
        """Universal website opener with comprehensive mappings and AI fallback"""
        try:
            import webbrowser
            import re
            
            # Comprehensive website mappings
            website_mappings = {
                # Search Engines
                'google': 'https://www.google.com',
                'bing': 'https://www.bing.com',
                'yahoo': 'https://www.yahoo.com',
                'duckduckgo': 'https://duckduckgo.com',
                'yandex': 'https://yandex.com',
                'baidu': 'https://www.baidu.com',
                
                # Social Media
                'facebook': 'https://www.facebook.com',
                'twitter': 'https://www.twitter.com',
                'x': 'https://www.x.com',
                'instagram': 'https://www.instagram.com',
                'linkedin': 'https://www.linkedin.com',
                'tiktok': 'https://www.tiktok.com',
                'snapchat': 'https://www.snapchat.com',
                'pinterest': 'https://www.pinterest.com',
                'reddit': 'https://www.reddit.com',
                'discord': 'https://discord.com',
                'telegram': 'https://web.telegram.org',
                'whatsapp': 'https://web.whatsapp.com',
                'youtube': 'https://www.youtube.com',
                
                # Entertainment & Media
                'netflix': 'https://www.netflix.com',
                'amazon prime': 'https://www.primevideo.com',
                'disney plus': 'https://www.disneyplus.com',
                'hulu': 'https://www.hulu.com',
                'spotify': 'https://open.spotify.com',
                'apple music': 'https://music.apple.com',
                'soundcloud': 'https://soundcloud.com',
                'twitch': 'https://www.twitch.tv',
                'vimeo': 'https://vimeo.com',
                'dailymotion': 'https://www.dailymotion.com',
                
                # Shopping & E-commerce
                'amazon': 'https://www.amazon.com',
                'ebay': 'https://www.ebay.com',
                'alibaba': 'https://www.alibaba.com',
                'aliexpress': 'https://www.aliexpress.com',
                'walmart': 'https://www.walmart.com',
                'target': 'https://www.target.com',
                'bestbuy': 'https://www.bestbuy.com',
                'etsy': 'https://www.etsy.com',
                'shopify': 'https://www.shopify.com',
                
                # News & Information
                'cnn': 'https://www.cnn.com',
                'bbc': 'https://www.bbc.com',
                'reuters': 'https://www.reuters.com',
                'nytimes': 'https://www.nytimes.com',
                'guardian': 'https://www.theguardian.com',
                'wikipedia': 'https://www.wikipedia.org',
                'wikimedia': 'https://www.wikimedia.org',
                
                # Technology & Development
                'github': 'https://github.com',
                'stackoverflow': 'https://stackoverflow.com',
                'gitlab': 'https://gitlab.com',
                'bitbucket': 'https://bitbucket.org',
                'codepen': 'https://codepen.io',
                'jsfiddle': 'https://jsfiddle.net',
                'replit': 'https://replit.com',
                'codesandbox': 'https://codesandbox.io',
                'npm': 'https://www.npmjs.com',
                'pypi': 'https://pypi.org',
                
                # Cloud & Productivity
                'google drive': 'https://drive.google.com',
                'dropbox': 'https://www.dropbox.com',
                'onedrive': 'https://onedrive.live.com',
                'icloud': 'https://www.icloud.com',
                'gmail': 'https://mail.google.com',
                'outlook': 'https://outlook.live.com',
                'yahoo mail': 'https://mail.yahoo.com',
                'google docs': 'https://docs.google.com',
                'google sheets': 'https://sheets.google.com',
                'google slides': 'https://slides.google.com',
                'office 365': 'https://office.com',
                'notion': 'https://www.notion.so',
                'trello': 'https://trello.com',
                'slack': 'https://slack.com',
                'zoom': 'https://zoom.us',
                'teams': 'https://teams.microsoft.com',
                
                # Education & Learning
                'coursera': 'https://www.coursera.org',
                'udemy': 'https://www.udemy.com',
                'edx': 'https://www.edx.org',
                'khan academy': 'https://www.khanacademy.org',
                'codecademy': 'https://www.codecademy.com',
                'freecodecamp': 'https://www.freecodecamp.org',
                'duolingo': 'https://www.duolingo.com',
                
                # Finance & Banking
                'paypal': 'https://www.paypal.com',
                'stripe': 'https://stripe.com',
                'coinbase': 'https://www.coinbase.com',
                'binance': 'https://www.binance.com',
                'robinhood': 'https://robinhood.com',
                
                # Travel & Maps
                'google maps': 'https://maps.google.com',
                'booking': 'https://www.booking.com',
                'airbnb': 'https://www.airbnb.com',
                'expedia': 'https://www.expedia.com',
                'tripadvisor': 'https://www.tripadvisor.com',
                
                # Health & Fitness
                'webmd': 'https://www.webmd.com',
                'mayo clinic': 'https://www.mayoclinic.org',
                'fitbit': 'https://www.fitbit.com',
                'myfitnesspal': 'https://www.myfitnesspal.com',
                
                # Gaming
                'steam': 'https://store.steampowered.com',
                'epic games': 'https://www.epicgames.com',
                'origin': 'https://www.origin.com',
                'battle.net': 'https://www.battle.net',
                'xbox': 'https://www.xbox.com',
                'playstation': 'https://www.playstation.com',
                'nintendo': 'https://www.nintendo.com',
                
                # Design & Creative
                'behance': 'https://www.behance.net',
                'dribbble': 'https://dribbble.com',
                'figma': 'https://www.figma.com',
                'canva': 'https://www.canva.com',
                'adobe': 'https://www.adobe.com',
                'unsplash': 'https://unsplash.com',
                'pexels': 'https://www.pexels.com',
                
                # Communication
                'skype': 'https://web.skype.com',
                'viber': 'https://www.viber.com',
                'messenger': 'https://www.messenger.com',
                
                # Food & Delivery
                'ubereats': 'https://www.ubereats.com',
                'doordash': 'https://www.doordash.com',
                'grubhub': 'https://www.grubhub.com',
                'zomato': 'https://www.zomato.com',
                
                # Weather
                'weather': 'https://weather.com',
                'accuweather': 'https://www.accuweather.com',
                
                # Miscellaneous
                'craigslist': 'https://craigslist.org',
                'indeed': 'https://www.indeed.com',
                'glassdoor': 'https://www.glassdoor.com',
                'quora': 'https://www.quora.com',
                'medium': 'https://medium.com',
                'tumblr': 'https://www.tumblr.com',
                'flickr': 'https://www.flickr.com',
                'imdb': 'https://www.imdb.com',
                'rottentomatoes': 'https://www.rottentomatoes.com'
            }
            
            # Extract website name from query
            website_name = ""
            query_lower = query.lower().strip()
            
            # Remove common prefixes
            for prefix in ['open ', 'launch ', 'start ', 'run ', 'website ', 'site ', 'web ', 'browse ', 'go to ']:
                if query_lower.startswith(prefix):
                    query_lower = query_lower[len(prefix):].strip()
                    break
            
            # Check if it's already a URL
            if any(protocol in query_lower for protocol in ['http://', 'https://', 'www.']):
                url = query_lower
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                webbrowser.open(url)
                return f"🌐 Opened website: {url}"
            
            # Check direct mappings first
            website_name = query_lower
            if website_name in website_mappings:
                url = website_mappings[website_name]
                webbrowser.open(url)
                return f"🌐 Opened {website_name.title()}: {url}"
            
            # Check partial matches
            for site, url in website_mappings.items():
                if site in query_lower or query_lower in site:
                    webbrowser.open(url)
                    return f"🌐 Opened {site.title()}: {url}"
            
            # AI fallback for unknown websites
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Find the correct website URL for: "{query}"
                
Respond ONLY in this format:
Website: [website name]
URL: [full https URL]
Description: [brief description]
                
Examples:
Website: OpenAI
URL: https://www.openai.com
Description: AI research company

Website: Microsoft
URL: https://www.microsoft.com
Description: Technology corporation
                
If unsure, provide the most likely official website URL.'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                # Parse AI response
                url_match = re.search(r'URL:\s*(https?://[^\s]+)', ai_response, re.IGNORECASE)
                name_match = re.search(r'Website:\s*(.+)', ai_response, re.IGNORECASE)
                
                if url_match:
                    url = url_match.group(1).strip()
                    name = name_match.group(1).strip() if name_match else query
                    
                    webbrowser.open(url)
                    return f"🌐 AI found and opened {name}: {url}"
                else:
                    # Fallback: construct likely URL
                    clean_name = re.sub(r'[^a-zA-Z0-9]', '', query_lower)
                    fallback_url = f"https://www.{clean_name}.com"
                    webbrowser.open(fallback_url)
                    return f"🌐 Opened best guess: {fallback_url}"
                    
            except Exception as ai_error:
                print(f"AI website lookup failed: {ai_error}")
                
                # Final fallback: Google search
                search_query = query.replace(' ', '+')
                google_search = f"https://www.google.com/search?q={search_query}+official+website"
                webbrowser.open(google_search)
                return f"🌐 Opened Google search for '{query}' official website"
                
        except Exception as e:
            return f"Website opening failed: {e}"


  
    def close_website(self, query=""):
        """Close browser or specific website tabs"""
        try:
            import subprocess
            import re
            
            # Website mappings for recognition
            website_mappings = {
                'google': 'Google', 'bing': 'Bing', 'yahoo': 'Yahoo', 'duckduckgo': 'DuckDuckGo',
                'facebook': 'Facebook', 'twitter': 'Twitter', 'x': 'X', 'instagram': 'Instagram',
                'linkedin': 'LinkedIn', 'tiktok': 'TikTok', 'youtube': 'YouTube', 'netflix': 'Netflix',
                'amazon': 'Amazon', 'ebay': 'eBay', 'github': 'GitHub', 'stackoverflow': 'Stack Overflow',
                'gmail': 'Gmail', 'outlook': 'Outlook', 'zoom': 'Zoom', 'teams': 'Microsoft Teams',
                'spotify': 'Spotify', 'discord': 'Discord', 'slack': 'Slack', 'reddit': 'Reddit'
            }
            
            browsers = {
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe', 
                'edge': 'msedge.exe',
                'safari': 'safari.exe',
                'opera': 'opera.exe'
            }
            
            if not query:
                for browser in browsers.values():
                    subprocess.run(['taskkill', '/f', '/im', browser], capture_output=True)
                return "Closed all browsers"
            
            query_lower = query.lower().strip()
            
            # Remove common prefixes
            for prefix in ['close ', 'quit ', 'exit ', 'stop ']:
                if query_lower.startswith(prefix):
                    query_lower = query_lower[len(prefix):].strip()
                    break
            
            # Close specific browser
            if query_lower in browsers:
                subprocess.run(['taskkill', '/f', '/im', browsers[query_lower]], capture_output=True)
                return f" Closed {query_lower}"
            
            # Close all browsers if "browser" mentioned
            if 'browser' in query_lower:
                for browser in browsers.values():
                    subprocess.run(['taskkill', '/f', '/im', browser], capture_output=True)
                return " Closed all browsers"
            
            # Check website mappings
            if query_lower in website_mappings:
                for browser in browsers.values():
                    subprocess.run(['taskkill', '/f', '/im', browser], capture_output=True)
                return f" Closed browsers (was viewing {website_mappings[query_lower]})"
            
            # AI fallback
            try:
                from engine.dual_ai import dual_ai
                
                ai_prompt = f'''Identify if "{query}" is a website or browser name.
                
Respond ONLY:
Type: [website/browser/unknown]
Action: [close_browser/close_all/unknown]
                
Examples:
Type: website
Action: close_browser

Type: browser
Action: close_browser'''
                
                if dual_ai.ai_provider == 'groq':
                    response = dual_ai.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": ai_prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    ai_response = response.choices[0].message.content.strip()
                else:
                    response = dual_ai.gemini_model.generate_content(ai_prompt)
                    ai_response = response.text.strip()
                
                if 'close_browser' in ai_response.lower():
                    for browser in browsers.values():
                        subprocess.run(['taskkill', '/f', '/im', browser], capture_output=True)
                    return f" AI closed browsers (was viewing {query})"
                    
            except Exception:
                pass
            
            # Final fallback - close all browsers
            for browser in browsers.values():
                subprocess.run(['taskkill', '/f', '/im', browser], capture_output=True)
            return f" Closed browsers for '{query}'"
            
        except Exception as e:
            return f"Failed to close: {e}"
        
    def python_packages(self, query=""):
        import subprocess
        import re
        
        limit = 10
        numbers = re.findall(r'\d+', query)
        if numbers:
            limit = int(numbers[0])
        
        try:
            result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')[2:]
            
            packages = []
            for line in lines[:limit]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append(f"{parts[0]} ({parts[1]})")
            
            return f"Top {len(packages)} installed packages:\n" + "\n".join(packages)
        
        except Exception as e:
            return f"Error getting packages: {e}"



new_features = NewFeatures()

def get_new_feature_response(query):
    return new_features.execute(query)