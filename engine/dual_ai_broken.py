import subprocess
import pyautogui
import psutil
from datetime import datetime, timedelta
import json
import os
import shutil
import socket
import time
import random
import requests
import winreg
import base64
import hashlib
import sqlite3
from collections import Counter
from typing import Optional, Dict, Any, List
import zipfile
import re
import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Import multilingual support
try:
    from engine.multilingual_support import multilingual
except:
    multilingual = None

class DualAI:
    def __init__(self):
        self.ai_provider = self._get_ai_provider()
        self._init_ai_models()
        # Initialize multilingual support
        from engine.multilingual_support import multilingual
        self.multilingual = multilingual
        
        # Initialize personality manager
        try:
            from engine.personality_manager import personality_manager
            self.personality_manager = personality_manager
        except:
            self.personality_manager = None
        
        # All system functions
        self.functions = {
            # Power
            'shutdown': lambda: subprocess.run('shutdown /s /t 5', shell=True),
            'restart': lambda: subprocess.run('shutdown /r /t 5', shell=True),
            'sleep': lambda: subprocess.run('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True),
            'lock': lambda: subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True),
            'hibernate': lambda: subprocess.run('shutdown /h', shell=True),
            
            # Apps
            'calculator': lambda: subprocess.Popen('calc', shell=True),
            'notepad': lambda: subprocess.Popen('notepad', shell=True),
            'chrome': lambda: subprocess.Popen('start chrome', shell=True),
            'edge': lambda: subprocess.Popen('start msedge', shell=True),
            'explorer': lambda: subprocess.Popen('explorer', shell=True),
            'settings': lambda: subprocess.Popen('start ms-settings:', shell=True),
            'taskmanager': lambda: subprocess.Popen('taskmgr', shell=True),
            'cmd': lambda: subprocess.Popen('cmd', shell=True),
            'paint': lambda: subprocess.Popen('mspaint', shell=True),
            'firefox': lambda: subprocess.Popen('start firefox', shell=True),
            'word': lambda: subprocess.Popen('start winword', shell=True),
            'excel': lambda: subprocess.Popen('start excel', shell=True),
            'powerpoint': lambda: subprocess.Popen('start powerpnt', shell=True),
            'vlc': lambda: subprocess.Popen('start vlc', shell=True),
            'vscode': lambda: subprocess.Popen('start code', shell=True),
            'spotify': lambda: subprocess.Popen('start spotify:', shell=True),
            'steam': lambda: subprocess.Popen('start steam', shell=True),
            
            # Websites
            'google': lambda: subprocess.Popen('start chrome https://www.google.com', shell=True),
            'youtube': lambda: subprocess.Popen('start chrome https://www.youtube.com', shell=True),
            'wikipedia': lambda: subprocess.Popen('start chrome https://www.wikipedia.org', shell=True),
            'stackoverflow': lambda: subprocess.Popen('start chrome https://stackoverflow.com', shell=True),
            'github': lambda: subprocess.Popen('start chrome https://github.com', shell=True),
            'amazon': lambda: subprocess.Popen('start chrome https://www.amazon.in', shell=True),
            'flipkart': lambda: subprocess.Popen('start chrome https://www.flipkart.com', shell=True),
            'instagram': lambda: subprocess.Popen('start chrome https://www.instagram.com', shell=True),
            'facebook': lambda: subprocess.Popen('start chrome https://www.facebook.com', shell=True),
            'twitter': lambda: subprocess.Popen('start chrome https://www.twitter.com', shell=True),
            'linkedin': lambda: subprocess.Popen('start chrome https://www.linkedin.com', shell=True),
            'whatsapp_web': lambda: subprocess.Popen('start chrome https://web.whatsapp.com', shell=True),
            'gmail': lambda: subprocess.Popen('start chrome https://mail.google.com', shell=True),
            'netflix': lambda: subprocess.Popen('start chrome https://www.netflix.com', shell=True),
            
            # Volume
            'volume_up': lambda: pyautogui.press('volumeup'),
            'volume_down': lambda: pyautogui.press('volumedown'),
            'mute': lambda: pyautogui.press('volumemute'),
            
            # Screen
            'screenshot': lambda: pyautogui.screenshot().save(f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'),
            'desktop': lambda: pyautogui.hotkey('win', 'd'),
            'minimize_all': lambda: pyautogui.hotkey('win', 'm'),
            'brightness_up': self._brightness_up,
            'brightness_down': self._brightness_down,
            
            # Keyboard
            'alt_tab': lambda: pyautogui.hotkey('alt', 'tab'),
            'copy': lambda: pyautogui.hotkey('ctrl', 'c'),
            'paste': lambda: pyautogui.hotkey('ctrl', 'v'),
            'save': lambda: pyautogui.hotkey('ctrl', 's'),
            'undo': lambda: pyautogui.hotkey('ctrl', 'z'),
            'select_all': lambda: pyautogui.hotkey('ctrl', 'a'),
            
            # Close apps
            'close_chrome': lambda: subprocess.run('taskkill /f /im chrome.exe', shell=True),
            'close_edge': lambda: subprocess.run('taskkill /f /im msedge.exe', shell=True),
            'close_notepad': lambda: subprocess.run('taskkill /f /im notepad.exe', shell=True),
            
            # Folders
            'downloads': lambda: subprocess.run('explorer shell:Downloads', shell=True),
            'documents': lambda: subprocess.run('explorer shell:Personal', shell=True),
            'pictures': lambda: subprocess.run('explorer shell:MyPictures', shell=True),
            
            # System info
            'cpu': lambda: psutil.cpu_percent(interval=1),
            'memory': lambda: psutil.virtual_memory().percent,
            'battery': lambda: psutil.sensors_battery().percent if psutil.sensors_battery() else None,
            'time': lambda: datetime.now().strftime('%I:%M %p'),
            'date': lambda: datetime.now().strftime('%A, %B %d, %Y'),
            
            # AI Control
            'switch_to_gemini': self._switch_to_gemini,
            'switch_to_groq': self._switch_to_groq,
            'current_ai': self._get_current_ai,
            'switch_language_hindi': self._switch_to_hindi,
            'switch_language_kannada': self._switch_to_kannada,
            'switch_language_english': self._switch_to_english,
            
            # Calendar
            'schedule': self._schedule_event,
            'show_calendar': self._show_calendar,
            
            # Advanced AI Features
            'daily_briefing': self._daily_briefing,
            'predictive_assistance': self._predictive_assistance,
            'context_memory_store': self._context_memory_store,
            'context_memory_recall': self._context_memory_recall,
            'recall': self._context_memory_recall,
            
            # Security & Authentication
            'file_vault_encrypt': self._file_vault_encrypt,
            'file_vault_decrypt': self._file_vault_decrypt,
            'anomaly_detection': self._anomaly_detection,
            'phishing_scan': self._phishing_scan,
            'parental_control': self._parental_control,
            
            # Cloud & Multi-Device
            'cloud_backup': self._cloud_backup,
            'email_summarize': self._email_summarize,
            'sync_devices': self._sync_devices,
            
            # AI Productivity
            'realtime_transcription': self._realtime_transcription,
            'summarize_meeting': self._summarize_meeting,
            'smart_clipboard': self._smart_clipboard,
            'document_qa': self._document_qa,
            'ai_presentation': self._ai_presentation,
            
            # Smart Home
            'smart_home_control': self._smart_home_control,
            'set_home_scene': self._set_home_scene,
            'security_camera': self._security_camera,
            'energy_monitoring': self._energy_monitoring,
            
            # Entertainment Plus
            'ai_dj_mode': self._ai_dj_mode,
            'trivia_game': self._trivia_game,
            'storytelling': self._storytelling,
            'fitness_coach': self._fitness_coach,
            
            # Health & Wellness
            'posture_detection': self._posture_detection,
            'eye_care_mode': self._eye_care_mode,
            'daily_health_log': self._daily_health_log,
            'mood_tracker': self._mood_tracker,
            'meditation_prompt': self._meditation_prompt,
            
            # System Monitoring
            'system_monitor_live': self._system_monitor_live,
            'auto_fix_system': self._auto_fix_system,
            
            # All Advanced AI Features Integration
            'manage_package': self._manage_package,
            'docker_control': self._docker_control,
            'context_memory_store': self._context_memory_store,
            'context_memory_recall': self._context_memory_recall,
            'adaptive_learning': self._adaptive_learning,
            'check_proactive': self._check_proactive,
            'enable_proactive_mode': self._enable_proactive_mode,
            'enable proactive mode': self._enable_proactive_mode,
            'disable_proactive_mode': self._disable_proactive_mode,
            'disable proactive mode': self._disable_proactive_mode,
            'manual_learn': self._manual_learn,
            'file_vault_encrypt': self._file_vault_encrypt,
            'file_vault_decrypt': self._file_vault_decrypt,
            'anomaly_detection': self._anomaly_detection,
            'phishing_scan': self._phishing_scan,
            'parental_control': self._parental_control,
            'calendar_schedule': self._calendar_schedule,
            'cloud_backup': self._cloud_backup,
            'realtime_transcription': self._realtime_transcription,
            'summarize_meeting': self._summarize_meeting,
            'smart_clipboard': self._smart_clipboard,
            'document_qa': self._document_qa,
            'ai_presentation': self._ai_presentation,
            'smart_home_control': self._smart_home_control,
            'set_home_scene': self._set_home_scene,
            'security_camera': self._security_camera,
            'energy_monitoring': self._energy_monitoring,
            'ai_dj_mode': self._ai_dj_mode,
            'trivia_game': self._trivia_game,
            'storytelling': self._storytelling,
            'fitness_coach': self._fitness_coach,
            'debug_screen': self._debug_screen_code,
            'fix_my_code': self._debug_screen_code,
            'check_code': self._debug_screen_code,
            'code_agent': self._code_agent,
            'research_agent': self._research_agent,
            'organizer_agent': self._organizer_agent,
            'multi_agent_collab': self._multi_agent_collab,
            'scholar_search': self._scholar_search,
            'stock_updates': self._stock_updates,
            'crypto_updates': self._crypto_updates,
            'realtime_translation': self._realtime_translation,
            'posture_detection': self._posture_detection,
            'eye_care_mode': self._eye_care_mode,
            'daily_health_log': self._daily_health_log,
            'mood_tracker': self._mood_tracker,
            'meditation_prompt': self._meditation_prompt,
            
            # Face Auth
            'enable_face_auth': self._enable_face_auth,
            'disable_face_auth': self._disable_face_auth,
            'face_auth_status': self._get_face_auth_status,
            
            # Voice Gender Control
            'switch_to_male_voice': self._switch_to_male_voice,
            'switch_to_female_voice': self._switch_to_female_voice,
            'male_voice': self._switch_to_male_voice,
            'female_voice': self._switch_to_female_voice,
            'current_voice_gender': self._get_current_voice_gender,
            'voice_status': self._get_current_voice_gender,
            

            
            # Media Controls
            'play_pause': self._play_pause,
            'next_track': self._next_track,
            'previous_track': self._previous_track,
            'stop_media': self._stop_media,
            
            # Window Management
            'maximize_window': self._maximize_window,
            'minimize_window': self._minimize_window,
            'split_screen_left': self._split_screen_left,
            'split_screen_right': self._split_screen_right,
            'close_window': self._close_window,
            'switch_window': self._switch_window,
            
            # Text Operations
            'find_text': self._find_text,
            'replace_text': self._replace_text,
            'new_document': self._new_document,
            'print_document': self._print_document,
            'zoom_in': self._zoom_in,
            'zoom_out': self._zoom_out,
            
            # Security Features
            'clear_clipboard': self._clear_clipboard,
            'clear_history': self._clear_browser_history,
            'empty_recycle_bin': self._empty_recycle_bin,
            'lock_screen': self._lock_screen,
            
            # Automation
            'set_reminder': self._set_reminder,
            'schedule_shutdown': self._schedule_shutdown,
            'auto_backup': self._backup_files,
            'clean_temp': self._clean_temp_files,
            
            # Entertainment
            'play_music': self._play_music,
            'random_wallpaper': self._change_wallpaper,
            'joke': self._tell_joke,
   
            'news': self._get_news,
            'quote': self._get_quote,
            
            # Voice Mouse Control
            'move_mouse_up': self._move_mouse_up,
            'move_mouse_down': self._move_mouse_down,
            'move_mouse_left': self._move_mouse_left,
            'move_mouse_right': self._move_mouse_right,
            'move_mouse_center': self._move_mouse_center,
            'left_click': self._left_click,
            'right_click': self._right_click,
            'double_click': self._double_click,
            'start_drag': self._start_drag,
            'drop_here': self._drop_here,
            'scroll_up': self._scroll_up,
            'scroll_down': self._scroll_down,
            'scroll_to_top': self._scroll_to_top,
            
            # Voice Keyboard Control
            'type_text': self._type_text,
            'press_enter': self._press_enter,
            'press_tab': self._press_tab,
            'press_escape': self._press_escape,
            'press_backspace': self._press_backspace,
            'press_delete': self._press_delete,
            'go_to_beginning': self._go_to_beginning,
            'go_to_end': self._go_to_end,
            
            # ALL ADVANCED FEATURES INTEGRATED
            # File Operations
            'create_folder': self._create_folder,
            'delete_file': self._delete_file,
            'search_files': self._search_files,
            'copy_file': self._copy_file,
            'move_file': self._move_file,
            
            # Network & Internet
            'check_internet': self._ping_test,
            'ip_address': self._get_ip,
            'wifi_password': self._get_wifi_password,
            'network_speed': self._speed_test,
            
            # System Monitoring
            'disk_space': self._get_disk_space,
            'running_processes': self._list_processes,
            'system_uptime': self._get_uptime,
            'temperature': self._get_cpu_temp,
            
            # Advanced Window Management
            'next_window': self._next_window,
            'previous_window': self._previous_window,
            'close_all_windows': self._close_all_windows,
            'snap_left': self._snap_left,
            'snap_right': self._snap_right,
            'full_screen': self._full_screen,
            'restore_window': self._restore_window,
            
            # Advanced File Operations
            'open_recent_file': self._open_recent_file,
            'create_new_file': self._create_new_file,
            'rename_file': self._rename_file,
            'duplicate_file': self._duplicate_file,
            'compress_file': self._compress_file,
            'extract_archive': self._extract_archive,
            
            # Web Browsing Control
            'open_new_tab': self._open_new_tab,
            'close_current_tab': self._close_current_tab,
            'switch_to_next_tab': self._switch_to_next_tab,
            'switch_to_previous_tab': self._switch_to_previous_tab,
            'refresh_page': self._refresh_page,
            'go_back': self._go_back,
            'go_forward': self._go_forward,
            'bookmark_page': self._bookmark_page,
            'open_bookmarks': self._open_bookmarks,
            'search_web': self._search_web,
            
            # Advanced Media Control
            'skip_forward': self._skip_forward,
            'skip_backward': self._skip_backward,
            'increase_speed': self._increase_speed,
            'decrease_speed': self._decrease_speed,
            'toggle_fullscreen': self._toggle_fullscreen,
            'toggle_subtitles': self._toggle_subtitles,
            
            # System Information
            'show_system_info': self._show_system_info,
            'check_updates': self._check_updates,
            'show_installed_programs': self._show_installed_programs,
            'show_startup_programs': self._show_startup_programs,
            'show_network_info': self._show_network_info,
            
            # Voice Dictation
            'start_dictation': self._start_dictation,
            'stop_dictation': self._stop_dictation,
            'dictate_email': self._dictate_email,
            'dictate_document': self._dictate_document,
            
            # Screen Control
            'take_screenshot_window': self._take_screenshot_window,
            'take_screenshot_area': self._take_screenshot_area,
            'start_screen_recording': self._start_screen_recording,
            'stop_screen_recording': self._stop_screen_recording,
            
            # Power Management
            'hibernate_computer': self._hibernate_computer,
            'log_off': self._log_off,
            'switch_user': self._switch_user,
            'enable_airplane_mode': self._enable_airplane_mode,
            'disable_airplane_mode': self._disable_airplane_mode,
            
            # Accessibility Features
            'enable_narrator': self._enable_narrator,
            'disable_narrator': self._disable_narrator,
            'enable_magnifier': self._enable_magnifier,
            'disable_magnifier': self._disable_magnifier,
            'high_contrast_mode': self._high_contrast_mode,
            
            # Network Control
            'connect_wifi': self._connect_wifi,
            'disconnect_wifi': self._disconnect_wifi,
            'show_wifi_networks': self._show_wifi_networks,
            'enable_hotspot': self._enable_hotspot,
            'disable_hotspot': self._disable_hotspot,
            
            # Advanced Search
            'search_files_content': self._search_files_content,
            'search_registry': self._search_registry,
            'search_installed_software': self._search_installed_software,
            'find_large_files': self._find_large_files,
            'find_duplicate_files': self._find_duplicate_files,
            
            # Smart Home Integration
            'smart_lights': self._control_smart_lights,
            'smart_fan': self._control_smart_fan,
            'smart_ac': self._control_smart_ac,
            'home_scene': self._set_home_scene,
            
            # Advanced AI Capabilities
            'generate_code': self._generate_code,
            'debug_code': self._debug_code,
            'translate_text': self._translate_text,
            'summarize_text': self._summarize_text,
            'analyze_image': self._analyze_image,
            
            # Productivity & Office
            'send_email': self._send_email,
            'schedule_meeting': self._schedule_meeting,
            'create_task': self._create_task,
            'convert_document': self._convert_document,
            'merge_pdf': self._merge_pdf,
            
            # Developer Tools
            'git_status': self._git_status,
            'git_commit': self._git_commit,
            'run_tests': self._run_tests,
            'format_code': self._format_code,
            'api_test': self._api_test,
            
            # Health & Wellness
            'water_reminder': self._water_reminder,
            'break_reminder': self._break_reminder,
            'eye_care': self._eye_care_reminder,
            'fitness_track': self._fitness_track,
            
            # Advanced System Control
            'registry_edit': self._registry_edit,
            'service_control': self._service_control,
            'driver_update': self._driver_update,
            'system_optimize': self._system_optimize,
            'performance_monitor': self._performance_monitor,
            
            # Communication & Social
            'social_post': self._social_post,
            'compose_email': self._compose_email,
            'message_template': self._message_template,
            'contact_search': self._contact_search,
            
            # Learning & Education
            'wikipedia_search': self._wikipedia_search,
            'dictionary_lookup': self._dictionary_lookup,
            'unit_convert': self._unit_convert,
            'math_calculate': self._math_calculate,
            'language_learn': self._language_learn,
            
            # Entertainment Plus
            'movie_recommend': self._movie_recommend,
            'book_suggest': self._book_suggest,
            'game_launch': self._game_launch,
            'streaming_control': self._streaming_control,
            'playlist_manage': self._playlist_manage,
            
            # Advanced Automation
            'workflow_automate': self._workflow_automate,
            'batch_operations': self._batch_operations,
            'scheduled_tasks': self._scheduled_tasks,
            'system_maintenance': self._system_maintenance,
            'auto_updates': self._auto_updates,
            
            # Built-in Entertainment
            'tell_joke': self._tell_joke,
            'get_quote': self._get_quote,
       
            'get_news': self._get_news,
            
            # YouTube Automation
            'youtube_play': self._youtube_play,
            'youtube_pause': self._youtube_pause,
            'youtube_next': self._youtube_next,
            'youtube_previous': self._youtube_previous,
            'youtube_fullscreen': self._youtube_fullscreen,
            'youtube_volume_up': self._youtube_volume_up,
            'youtube_volume_down': self._youtube_volume_down,
            'youtube_mute': self._youtube_mute,
            'youtube_speed_up': self._youtube_speed_up,
            'youtube_speed_down': self._youtube_speed_down,
            'youtube_skip_forward': self._youtube_skip_forward,
            'youtube_skip_backward': self._youtube_skip_backward,
            'youtube_search': self._youtube_search,
            'youtube_subscribe': self._youtube_subscribe,
            'youtube_like': self._youtube_like,
            'youtube_dislike': self._youtube_dislike,
            'youtube_comment': self._youtube_comment,
            'youtube_share': self._youtube_share,
            'youtube_theater_mode': self._youtube_theater_mode,
            'youtube_miniplayer': self._youtube_miniplayer,
            'youtube_captions': self._youtube_captions,
            'play_video': self._play_video,
            'play_movie': self._play_movie,
            'play_song': self._play_song,
            'search_and_play': self._search_and_play,
            
            # Multiple App/Website Opening
     
            
            # Chrome Automation
            'chrome_new_tab': self._chrome_new_tab,
            'chrome_close_tab': self._chrome_close_tab,
            'chrome_next_tab': self._chrome_next_tab,
            'chrome_previous_tab': self._chrome_previous_tab,
            'chrome_reload': self._chrome_reload,
            'chrome_back': self._chrome_back,
            'chrome_forward': self._chrome_forward,
            'chrome_home': self._chrome_home,
            'chrome_bookmark': self._chrome_bookmark,
            'chrome_history': self._chrome_history,
            'chrome_downloads': self._chrome_downloads,
            'chrome_incognito': self._chrome_incognito,
            'chrome_developer_tools': self._chrome_developer_tools,
            'chrome_zoom_in': self._chrome_zoom_in,
            'chrome_zoom_out': self._chrome_zoom_out,
            'chrome_zoom_reset': self._chrome_zoom_reset,
            'chrome_find': self._chrome_find,
            'chrome_print': self._chrome_print,
            'chrome_save_page': self._chrome_save_page,
            'chrome_view_source': self._chrome_view_source,
            'chrome_extensions': self._chrome_extensions,
            'chrome_settings': self._chrome_settings,
            'chrome_clear_data': self._chrome_clear_data,
            
            # Proactive mode commands
            'enable proactive mode': self._enable_proactive_mode,
            'disable proactive mode': self._disable_proactive_mode,
            
            # Gesture Control
            'start_gesture_control': self._start_gesture_control,
            'stop_gesture_control': self._stop_gesture_control,
            'hand_control': self._start_gesture_control,
            'eye_control': self._start_gesture_control,
            'head_control': self._start_gesture_control,
            'gesture_control': self._start_gesture_control,
            'start gesture control': self._start_gesture_control,
            'stop gesture control': self._stop_gesture_control,
            
            # Code Review Functions
            'code_review': self._code_review,
            'folder_review': self._folder_review,
            'file_review': self._file_review,
            'live_code_review': self._live_code_review,
            'start_live_review': self._start_live_review,
            'stop_live_review': self._stop_live_review,
            
            # Continuous Listening Functions
         
            

        }
    
    def _get_ai_provider(self):
        try:
            with open('ai_config.json', 'r') as f:
                config = json.load(f)
                return config.get('ai_provider', 'groq')
        except:
            return 'groq'
    
    def _set_ai_provider(self, provider):
        try:
            config = {'ai_provider': provider}
            with open('ai_config.json', 'w') as f:
                json.dump(config, f)
            self.ai_provider = provider
            self._init_ai_models()
            return True
        except:
            return False
    
    def _init_ai_models(self):
        if self.ai_provider == 'groq':
            try:
                from groq import Groq
                from engine.groq_config import GROQ_API_KEY
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                # Test the API key with a simple request
                test_response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
            except Exception as e:
                print(f"Groq failed: {e}, switching to Gemini")
                self.ai_provider = 'gemini'
                self._init_gemini()
        else:
            self._init_gemini()
    
    def _init_gemini(self):
        try:
            import google.generativeai as genai
            from engine.gemini_config import GEMINI_API_KEY
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            print("Using Gemini AI")
        except Exception as e:
            print(f"AI init error: {e}")
    
    def execute(self, query):
        try:
            # Handle voice gender switching commands FIRST (highest priority)
            query_lower = query.lower().strip()
            
            # Exact voice command matching
            if 'female voice' in query_lower:
                return self._switch_to_female_voice()
            elif 'male voice' in query_lower:
                return self._switch_to_male_voice()
            elif 'switch to female' in query_lower:
                return self._switch_to_female_voice()
            elif 'switch to male' in query_lower:
                return self._switch_to_male_voice()
            elif 'current voice' in query_lower or 'voice status' in query_lower:
                return self._get_current_voice_gender()
            
            # Process multilingual commands AFTER English commands
            # Skip multilingual processing for basic English "open" commands
            if not query.lower().startswith('open ') and self.multilingual:
                # Check if it's a language switching command
                if any(word in query.lower() for word in ['switch to', 'change language', 'भाषा', 'ভাষা', 'ભાষા', 'ಭಾಷೆ', 'ഭാഷ', 'भाषा', 'மொழி', 'భాష', 'زبان']):
                    response = self.multilingual.process_multilingual_command(query)
                    return response
                
                # Process command in current language context only for non-English commands
                detected_lang = self.multilingual.detect_language(query)
                if detected_lang != 'english':
                    response = self.multilingual.process_command_in_language(query, self.multilingual.current_language)
                    if response != self.multilingual.get_response('processing'):
                        return response
            # Handle continuous listening commands FIRST
            query_clean = query.lower().strip()
          
            
            # Handle code review commands FIRST to prevent interference
            if query_clean == 'code review':
                return self._code_review()
            
            if query_clean == 'folder review' or query_clean == 'review':
                return self._folder_review()
            
            if query_clean.startswith('folder review '):
                folder_name = query[14:].strip()
                return self._folder_review(folder_name)
            
            if query_clean.startswith('file review '):
                file_path = query[12:].strip()
                return self._file_review(file_path)
            
            if query_clean == 'start live review':
                return self._start_live_review()
            
            if query_clean == 'stop live review':
                return self._stop_live_review()
            
            if query_clean == 'live code review':
                return self._live_code_review()
            
            # Skip all other processing for review commands
            if 'review' in query_clean and not query_clean.startswith('folder review ') and not query_clean.startswith('live'):
                return self._folder_review()
            
            # Check for dynamic commands - HIGHEST PRIORITY
            import re
            
            # Volume/brightness with numbers - PROCESS IMMEDIATELY
            volume_match = re.search(r'(?:set )?volume (?:to )?([0-9]+)', query.lower())
            brightness_match = re.search(r'(?:set )?brightness (?:to )?([0-9]+)', query.lower())
            
            if volume_match:
                level = int(volume_match.group(1))
                self._set_volume(level)
                return f"Volume set to {level}%"
            
            if brightness_match:
                level = int(brightness_match.group(1))
                self._set_brightness(level)
                return f"Brightness set to {level}%"
            
            # Handle "open" commands - HIGHEST PRIORITY
            if query.lower().startswith('open '):
                content = query[5:].strip().lower()  # Remove 'open '
                
                # Direct mappings for open commands
                direct_mappings = {
                    'facebook': 'facebook',
                    'instagram': 'instagram',
                    'google': 'google',
                    'youtube': 'youtube',
                    'gmail': 'gmail',
                    'twitter': 'twitter',
                    'linkedin': 'linkedin',
                    'whatsapp': 'whatsapp_web',
                    'netflix': 'netflix',
                    'amazon': 'amazon',
                    'flipkart': 'flipkart',
                    'wikipedia': 'wikipedia',
                    'stackoverflow': 'stackoverflow',
                    'github': 'github',
                    'notepad': 'notepad',
                    'calculator': 'calculator',
                    'chrome': 'chrome',
                    'edge': 'edge',
                    'firefox': 'firefox',
                    'word': 'word',
                    'excel': 'excel',
                    'powerpoint': 'powerpoint',
                    'vlc': 'vlc',
                    'vscode': 'vscode',
                    'spotify': 'spotify',
                    'steam': 'steam',
                    'explorer': 'explorer',
                    'settings': 'settings',
                    'taskmanager': 'taskmanager',
                    'cmd': 'cmd',
                    'paint': 'paint'
                }
                
                # Check for exact single command match first
                if content in direct_mappings:
                    func_name = direct_mappings[content]
                    try:
                        result = self.functions[func_name]()
                        return self._get_response(func_name, result)
                    except Exception as e:
                        return f"Error opening {content}"
                
            
                
                # If not found in direct mappings, try original function check
                if content in self.functions:
                    result = self.functions[content]()
                    return self._get_response(content, result)
            
            # Handle volume commands with better parsing
            if 'volume' in query.lower():
                if 'up' in query.lower() or 'increase' in query.lower():
                    result = self.functions['volume_up']()
                    return self._get_response('volume_up', result)
                elif 'down' in query.lower() or 'decrease' in query.lower():
                    result = self.functions['volume_down']()
                    return self._get_response('volume_down', result)
                elif 'mute' in query.lower():
                    result = self.functions['mute']()
                    return self._get_response('mute', result)
            
        
            
            # Handle brightness commands
            if 'brightness' in query.lower():
                if 'up' in query.lower() or 'increase' in query.lower():
                    result = self.functions['brightness_up']()
                    return self._get_response('brightness_up', result)
                elif 'down' in query.lower() or 'decrease' in query.lower():
                    result = self.functions['brightness_down']()
                    return self._get_response('brightness_down', result)
            
            # Chrome automation commands
            if query.lower().startswith('chrome '):
                chrome_cmd = query.lower().replace('chrome ', '').strip().replace(' ', '_')
                chrome_function = f'chrome_{chrome_cmd}'
                if chrome_function in self.functions:
                    result = self.functions[chrome_function]()
                    return self._get_response(chrome_function, result)
            
            # YouTube automation commands  
            if query.lower().startswith('youtube '):
                youtube_cmd = query.lower().replace('youtube ', '').strip().replace(' ', '_')
                youtube_function = f'youtube_{youtube_cmd}'
                if youtube_function in self.functions:
                    result = self.functions[youtube_function]()
                    return self._get_response(youtube_function, result)
            
            # Email summarization with content
            if query.lower().startswith('summarize email '):
                email_content = query[16:].strip()  # Remove 'summarize email '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.email_summarize(email_content)
                except:
                    return "Error summarizing email"
            
            # Calendar commands - force use of voice_advanced_ai
            if 'show calendar' in query.lower() or 'check calendar' in query.lower() or 'add event' in query.lower():
                try:
                    from engine.voice_advanced_ai import get_voice_advanced_response
                    return get_voice_advanced_response(query)
                except:
                    pass
            
            # Package management commands
            if query.lower().startswith('install '):
                package = query[8:].strip()  # Remove 'install '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.install_package(package)
                except:
                    return "Error installing package"
            
            if query.lower() == 'list packages':
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.list_packages()
                except:
                    return "Error listing packages"
            
            # Check for research agent before search patterns
            if 'research agent' in query.lower() or 'research help' in query.lower():
                return self._research_agent()
            
            # Health & Wellness dynamic commands
            if query.lower().startswith('health log '):
                entry = query[11:].strip()  # Remove 'health log '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.daily_health_log(entry)
                except:
                    return "Error logging health data"
            
            if query.lower().startswith('mood tracker ') or query.lower().startswith('track mood '):
                if query.lower().startswith('mood tracker '):
                    mood = query[13:].strip()  # Remove 'mood tracker '
                else:
                    mood = query[11:].strip()  # Remove 'track mood '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.mood_tracker(mood)
                except:
                    return "Error tracking mood"
            
            if query.lower().startswith('meditate ') or query.lower().startswith('meditation '):
                if query.lower().startswith('meditate '):
                    duration = query[9:].strip()  # Remove 'meditate '
                else:
                    duration = query[11:].strip()  # Remove 'meditation '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    if duration and duration.isdigit():
                        return voice_advanced_ai.meditation_prompt(duration)
                    return voice_advanced_ai.meditation_prompt()
                except:
                    return "Error starting meditation"
            
            # Security & Authentication dynamic commands
            if query.lower().startswith('encrypt file '):
                file_path = query[13:].strip()  # Remove 'encrypt file '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.file_vault_encrypt(file_path)
                except:
                    return "Error encrypting file"
            
            if query.lower().startswith('decrypt file '):
                file_path = query[13:].strip()  # Remove 'decrypt file '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.file_vault_decrypt(file_path)
                except:
                    return "Error decrypting file"
            
            if query.lower().startswith('phishing scan '):
                url = query[14:].strip()  # Remove 'phishing scan '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.phishing_malware_scan_link(url)
                except:
                    return "Error scanning URL"
            
            if query.lower().startswith('parental control '):
                action = query[17:].strip()  # Remove 'parental control '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.parental_control_set(action)
                except:
                    return "Error with parental control"
            
            # Adaptive Learning dynamic commands
            if query.lower().startswith('adaptive learning '):
                action = query[18:].strip()  # Remove 'adaptive learning '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.adaptive_learning(action)
                except:
                    return "Error with adaptive learning"
            
            if query.lower().startswith('manual learn '):
                action = query[13:].strip()  # Remove 'manual learn '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.manual_learn(action)
                except:
                    return "Error with manual learning"
            
            if query.lower().startswith('teach jarvis '):
                action = query[14:].strip()  # Remove 'teach jarvis '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.manual_learn(action)
                except:
                    return "Error teaching Jarvis"
            
            # Check new features FIRST before any other processing
            new_feature_result = self._check_new_features(query)
            if new_feature_result:
                return new_feature_result
            
            # Dynamic search and play commands - more flexible detection
            play_patterns = [
                r'(?:play|search)\s+(?:video|movie|song|music|on youtube)?\s*(.+)',
                r'youtube\s+(?:play|search)\s+(.+)',
                r'(?:play|search)\s+(.+?)\s+(?:on youtube|video|song|music)',
                r'(?:play|search)\s+(.+)'
            ]
            
            for pattern in play_patterns:
                play_match = re.search(pattern, query.lower())
                if play_match:
                    search_term = play_match.group(1).strip()
                    # Check if it's likely a media search
                    media_keywords = ['youtube', 'video', 'movie', 'song', 'music', 'play', 'search']
                    if any(keyword in query.lower() for keyword in media_keywords) and search_term:
                        # Exclude system commands
                        system_commands = ['notepad', 'calculator', 'chrome', 'word', 'excel']
                        if not any(cmd in search_term.lower() for cmd in system_commands):
                            return self._search_and_play(search_term)
                    break
            
            # Face auth commands - handle before general on/off
            if 'face auth' in query.lower() or 'face recognition' in query.lower():
                if 'enable' in query.lower() or 'turn on' in query.lower():
                    result = self._enable_face_auth()
                    return self._get_response('enable_face_auth', result)
                elif 'disable' in query.lower() or 'turn off' in query.lower():
                    result = self._disable_face_auth()
                    return self._get_response('disable_face_auth', result)
                elif 'status' in query.lower() or 'check' in query.lower():
                    result = self._get_face_auth_status()
                    return self._get_response('face_auth_status', result)
            
            # Dynamic on/off commands using AI
            on_off_match = re.search(r'(?:turn (on|off)|(?:enable|disable)) (.+)', query.lower())
            if on_off_match:
                action = on_off_match.group(1) if on_off_match.group(1) else ('on' if 'enable' in query.lower() else 'off')
                feature = on_off_match.group(2).strip()
                # Skip face auth as it's handled above
                if 'face' not in feature:
                    return self._handle_on_off(feature, action)
            
            if volume_match:
                level = int(volume_match.group(1))
                self._set_volume(level)
                return f"Volume set to {level}%"
            
            if brightness_match:
                level = int(brightness_match.group(1))
                self._set_brightness(level)
                return f"Brightness set to {level}%"
            

            
            if self._is_question(query):
                return self._answer_question(query)
            
            # Enhanced command matching with better natural language processing
            query_lower = query.lower().strip()
            
            # First try exact matches
            if query_lower in self.functions:
                func_name = query_lower
            else:
                # Try natural language understanding with enhanced matching
                func_name = self.understand_natural_speech(query)
                
                # If still no match, try fuzzy matching for common commands
                if not func_name:
                    func_name = self._fuzzy_match_command(query_lower)
                
                if not func_name:
                    # Fallback to advanced AI functions
                    try:
                        from engine.voice_advanced_ai import get_voice_advanced_response
                        advanced_response = get_voice_advanced_response(query)
                        if advanced_response and "Voice command not recognized" not in advanced_response and "Error:" not in advanced_response:
                            return advanced_response
                    except:
                        pass
                    
                    # Final fallback to AI model for function selection
                    prompt = f'User said: "{query}"\nAvailable functions: {list(self.functions.keys())}\nRespond with ONLY the function name or "none":'
                    
                    try:
                        if self.ai_provider == 'groq':
                            response = from engine.ai_fallback_system import try_all_ai_providers
func_name = try_all_ai_providers(prompt)
if not func_name:
    func_name = self._simple_fallback_match(query)
                        else:
                            response = self.gemini_model.generate_content(prompt)
                            func_name = response.text.strip()
                    except Exception as e:
                        print(f"AI API error: {e}")
                        # Fallback to simple command matching
                        func_name = self._simple_fallback_match(query)

            if func_name in self.functions:
                result = self.functions[func_name]()
                # For advanced features, return the actual result
                advanced_result_features = ['joke', 'quote', 'disk_space', 'ip_address', 'system_uptime', 'temperature', 'running_processes', 'check_internet', 'wifi_password', 'network_speed', 'create_folder', 'delete_file', 'search_files', 'set_reminder', 'schedule_shutdown', 'auto_backup', 'clean_temp', 'move_mouse_up', 'move_mouse_down', 'move_mouse_left', 'move_mouse_right', 'move_mouse_center', 'left_click', 'right_click', 'double_click', 'start_drag', 'drop_here', 'scroll_up', 'scroll_down', 'scroll_to_top', 'type_text', 'press_enter', 'press_tab', 'press_escape', 'press_backspace', 'press_delete', 'go_to_beginning', 'go_to_end', 'play_video', 'play_movie', 'play_song', 'search_and_play', 'open_multiple', 'daily_briefing', 'predictive_assistance', 'context_memory_recall', 'show_calendar', 'schedule', 'email_summarize', 'sync_devices', 'system_monitor_live', 'auto_fix_system', 'manage_package', 'docker_control', 'adaptive_learning', 'check_proactive', 'enable_proactive_mode', 'disable_proactive_mode', 'manual_learn', 'file_vault_encrypt', 'file_vault_decrypt', 'anomaly_detection', 'phishing_scan', 'parental_control', 'calendar_schedule', 'cloud_backup', 'realtime_transcription', 'summarize_meeting', 'smart_clipboard', 'document_qa', 'ai_presentation', 'smart_home_control', 'set_home_scene', 'security_camera', 'energy_monitoring', 'ai_dj_mode', 'trivia_game', 'storytelling', 'fitness_coach', 'code_agent', 'research_agent', 'organizer_agent', 'multi_agent_collab', 'scholar_search', 'stock_updates', 'crypto_updates', 'realtime_translation', 'posture_detection', 'eye_care_mode', 'daily_health_log', 'mood_tracker', 'meditation_prompt', 'start_gesture_control', 'stop_gesture_control']
                if func_name in advanced_result_features:
                    return result
                response = self._get_response(func_name, result)
                return response
            else:
                if self._is_question(query):
                    response = self._answer_question(query)
                    return response
                # Try multilingual processing as fallback
                if self.multilingual:
                    ml_response = self.multilingual.process_command_in_language(query, self.multilingual.current_language)
                    if ml_response != self.multilingual.get_response('processing'):
                        return ml_response
                
                if self.multilingual:
                    response = self.multilingual.get_response('not_understood')
                else:
                    response = "I can help with commands or questions!"
                return response
                
        except Exception as e:
            print(f"Error: {e}")
            # Try simple fallback for basic commands
            fallback_result = self._simple_fallback_match(query)
            if fallback_result and fallback_result in self.functions:
                try:
                    result = self.functions[fallback_result]()
                    return self._get_response(fallback_result, result)
                except:
                    pass
            
            if self.multilingual:
                response = self.multilingual.get_response('error')
            else:
                response = "Something went wrong."
            return response
    
    def understand_natural_speech(self, query):
        """Complete natural language processing for ALL functions"""
        query = query.lower().strip()
        
        mappings = {
            'shutdown': ['shut down', 'turn off computer', 'power off', 'shutdown computer'],
            'restart': ['restart', 'reboot', 'restart computer', 'reboot system'],
            'sleep': ['sleep', 'put to sleep', 'sleep mode'],
            'lock': ['lock', 'lock screen', 'secure screen'],
            'hibernate': ['hibernate', 'deep sleep', 'hibernation'],
            'volume_up': ['volume up', 'louder', 'increase volume', 'make it louder', 'turn up sound', 'increase the volume'],
            'volume_down': ['volume down', 'quieter', 'decrease volume', 'make it quieter', 'turn down sound'],
            'mute': ['mute', 'silence', 'turn off sound', 'mute audio'],
            'screenshot': ['screenshot', 'take screenshot', 'capture screen', 'take a picture of screen'],
            'brightness_up': ['brightness up', 'brighter', 'increase brightness', 'brighten screen'],
            'brightness_down': ['brightness down', 'dimmer', 'decrease brightness', 'my screen is too bright'],
            'desktop': ['show desktop', 'go to desktop', 'minimize all'],
            'calculator': ['calculator', 'calc', 'open calculator'],
            'notepad': ['notepad', 'text editor', 'open notepad'],
            'chrome': ['chrome', 'browser', 'open chrome', 'web browser'],
            'edge': ['edge', 'microsoft edge', 'open edge'],
            'firefox': ['firefox', 'open firefox', 'mozilla'],
            'word': ['word', 'microsoft word', 'document editor'],
            'excel': ['excel', 'spreadsheet', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'presentation', 'slides'],
            'vlc': ['vlc', 'video player', 'media player'],
            'vscode': ['vscode', 'code editor', 'visual studio'],
            'spotify': ['spotify', 'music', 'music player'],
            'steam': ['steam', 'games', 'gaming'],
            'explorer': ['explorer', 'file manager', 'files'],
            'settings': ['settings', 'system settings', 'control panel'],
            'taskmanager': ['task manager', 'processes', 'taskmanager'],
            'cmd': ['command prompt', 'cmd', 'terminal'],
            'paint': ['paint', 'drawing', 'mspaint'],
            'google': ['google', 'search', 'google search'],
            'youtube': ['youtube', 'videos', 'watch videos'],
            'wikipedia': ['wikipedia', 'wiki', 'encyclopedia'],
            'stackoverflow': ['stackoverflow', 'programming help', 'coding help'],
            'github': ['github', 'git', 'code repository'],
            'amazon': ['amazon', 'shopping', 'buy online'],
            'flipkart': ['flipkart', 'shopping india'],
            'instagram': ['instagram', 'insta', 'photos'],
            'facebook': ['facebook', 'fb', 'social media'],
            'twitter': ['twitter', 'tweets', 'social'],
            'linkedin': ['linkedin', 'professional network'],
            'whatsapp_web': ['whatsapp', 'messaging', 'chat'],
            'gmail': ['gmail', 'email', 'mail'],
            'netflix': ['netflix', 'movies', 'streaming'],
            'copy': ['copy', 'copy text', 'copy this'],
            'paste': ['paste', 'paste text', 'paste here'],
            'save': ['save', 'save file', 'save document'],
            'undo': ['undo', 'undo last action', 'go back'],
            'select_all': ['select all', 'select everything'],
            'alt_tab': ['switch window', 'alt tab', 'change window'],
            'time': ['time', 'what time is it', 'current time', 'tell me the time'],
            'date': ['date', 'what date is it', 'current date', 'today'],
            'cpu': ['cpu usage', 'processor usage', 'cpu load'],
            'memory': ['memory usage', 'ram usage', 'memory load'],
            'battery': ['battery', 'battery level', 'battery percentage'],
            'downloads': ['downloads', 'download folder'],
            'documents': ['documents', 'my documents'],
            'pictures': ['pictures', 'photos', 'image folder'],
            'switch_to_gemini': ['switch to gemini', 'use gemini', 'gemini ai'],
            'switch_to_groq': ['switch to groq', 'use groq', 'groq ai'],
            'current_ai': ['current ai', 'which ai', 'ai status'],
            'switch_language_hindi': ['hindi', 'switch to hindi'],
            'switch_language_kannada': ['kannada', 'switch to kannada'],
            'switch_language_english': ['english', 'switch to english'],
            'close_chrome': ['close chrome', 'quit chrome'],
            'close_edge': ['close edge', 'quit edge'],
            'close_notepad': ['close notepad', 'quit notepad'],
            'switch_to_male_voice': ['male voice', 'switch to male'],
            'switch_to_female_voice': ['female voice', 'switch to female'],
            'current_voice_gender': ['voice status', 'current voice'],
            'context_memory_recall': ['what do you remember', 'recall memory', 'show memories'],
            'daily_briefing': ['daily briefing', 'morning briefing'],
            'predictive_assistance': ['predictive help', 'smart suggestions'],
            'schedule': ['schedule meeting', 'add event', 'book appointment'],
            'show_calendar': ['show calendar', 'check calendar'],
            'posture_detection': ['posture check', 'check posture'],
            'eye_care_mode': ['eye care', 'protect eyes'],
            'daily_health_log': ['health log', 'log health'],
            'mood_tracker': ['mood tracker', 'track mood'],
            'meditation_prompt': ['meditate', 'meditation', 'relax'],
            'trivia_game': ['trivia', 'quiz game', 'test knowledge'],
            'storytelling': ['tell story', 'story time'],
            'fitness_coach': ['fitness coach', 'workout guide'],
            'ai_dj_mode': ['dj mode', 'music mix'],
            'code_agent': ['code help', 'programming assistant'],
            'research_agent': ['research help', 'research assistant'],
            'organizer_agent': ['organize', 'task organizer'],
            'smart_home_control': ['smart home', 'home automation'],
            'set_home_scene': ['home scene', 'set scene'],
            'start_gesture_control': ['gesture control', 'hand control'],
            'stop_gesture_control': ['stop gestures', 'disable gestures'],
            'code_review': ['code review', 'review code', 'check code'],
            'folder_review': ['folder review', 'review folder'],
            'live_code_review': ['live review', 'real time review'],
            'joke': ['tell joke', 'joke', 'make me laugh'],
            'quote': ['quote', 'inspirational quote', 'wisdom'],
    
            'news': ['news', 'latest news', 'headlines'],
            'disk_space': ['disk space', 'storage space', 'free space'],
            'system_uptime': ['uptime', 'system uptime', 'how long running'],
            'temperature': ['temperature', 'cpu temperature', 'system temp'],
            'running_processes': ['processes', 'running programs', 'active processes'],
            'check_internet': ['internet', 'check internet', 'connection test'],
            'ip_address': ['ip address', 'my ip', 'network address'],
            'wifi_password': ['wifi password', 'network password'],
            'network_speed': ['speed test', 'internet speed', 'connection speed'],
            'create_folder': ['create folder', 'new folder', 'make folder'],
            'delete_file': ['delete file', 'remove file'],
            'search_files': ['search files', 'find files'],
            'copy_file': ['copy file', 'duplicate file'],
            'move_file': ['move file', 'relocate file'],
            'maximize_window': ['maximize', 'maximize window', 'make bigger'],
            'minimize_window': ['minimize', 'minimize window', 'hide window'],
            'close_window': ['close window', 'close this'],
            'split_screen_left': ['split left', 'snap left', 'window left'],
            'split_screen_right': ['split right', 'snap right', 'window right'],
            'full_screen': ['full screen', 'fullscreen'],
            'play_pause': ['play', 'pause', 'play pause'],
            'next_track': ['next', 'next song', 'skip'],
            'previous_track': ['previous', 'previous song', 'back'],
            'stop_media': ['stop', 'stop playing'],
            'find_text': ['find', 'search text', 'find text'],
            'replace_text': ['replace', 'find replace'],
            'new_document': ['new document', 'new file'],
            'print_document': ['print', 'print document'],
            'zoom_in': ['zoom in', 'magnify', 'make bigger'],
            'zoom_out': ['zoom out', 'make smaller'],
            'clear_clipboard': ['clear clipboard', 'empty clipboard'],
            'clear_history': ['clear history', 'delete history'],
            'empty_recycle_bin': ['empty recycle bin', 'clear trash'],
            'lock_screen': ['lock screen', 'secure computer'],
            'set_reminder': ['set reminder', 'remind me'],
            'schedule_shutdown': ['schedule shutdown', 'auto shutdown'],
            'auto_backup': ['backup', 'backup files'],
            'clean_temp': ['clean temp', 'delete temp files'],
            'play_music': ['play music', 'start music'],
            'random_wallpaper': ['change wallpaper', 'new wallpaper'],
            'move_mouse_up': ['mouse up', 'move mouse up', 'cursor up'],
            'move_mouse_down': ['mouse down', 'move mouse down', 'cursor down'],
            'move_mouse_left': ['mouse left', 'move mouse left', 'cursor left'],
            'move_mouse_right': ['mouse right', 'move mouse right', 'cursor right'],
            'move_mouse_center': ['mouse center', 'center mouse'],
            'left_click': ['left click', 'click', 'mouse click'],
            'right_click': ['right click', 'context menu'],
            'double_click': ['double click', 'double tap'],
            'scroll_up': ['scroll up', 'page up'],
            'scroll_down': ['scroll down', 'page down'],
            'press_enter': ['press enter', 'hit enter', 'enter key'],
            'press_tab': ['press tab', 'tab key'],
            'press_escape': ['press escape', 'escape key'],
            'press_backspace': ['backspace', 'delete back'],
            'press_delete': ['delete key', 'delete forward'],
            'youtube_play': ['youtube play', 'play video'],
            'youtube_pause': ['youtube pause', 'pause video'],
            'youtube_next': ['youtube next', 'next video'],
            'youtube_previous': ['youtube previous', 'previous video'],
            'youtube_fullscreen': ['youtube fullscreen', 'video fullscreen'],
            'youtube_volume_up': ['youtube louder', 'video volume up'],
            'youtube_volume_down': ['youtube quieter', 'video volume down'],
            'youtube_mute': ['youtube mute', 'mute video'],
            'youtube_speed_up': ['youtube faster', 'speed up video'],
            'youtube_speed_down': ['youtube slower', 'slow down video'],
            'youtube_skip_forward': ['youtube skip', 'skip ahead'],
            'youtube_skip_backward': ['youtube back', 'skip back'],
            'youtube_search': ['youtube search', 'search video'],
            'youtube_subscribe': ['youtube subscribe', 'subscribe channel'],
            'youtube_like': ['youtube like', 'like video'],
            'youtube_theater_mode': ['theater mode', 'cinema mode'],
            'youtube_captions': ['captions', 'subtitles'],
            'chrome_new_tab': ['new tab', 'open tab'],
            'chrome_close_tab': ['close tab', 'close current tab'],
            'chrome_next_tab': ['next tab', 'switch tab'],
            'chrome_previous_tab': ['previous tab', 'last tab'],
            'chrome_reload': ['reload', 'refresh'],
            'chrome_back': ['go back', 'back page'],
            'chrome_forward': ['go forward', 'forward page'],
            'chrome_bookmark': ['bookmark', 'save bookmark'],
            'chrome_history': ['history', 'browser history'],
            'chrome_downloads': ['downloads', 'download history'],
            'chrome_incognito': ['incognito', 'private browsing'],
            'chrome_settings': ['chrome settings', 'browser settings'],
            'enable_face_auth': ['enable face auth', 'face recognition on'],
            'disable_face_auth': ['disable face auth', 'face recognition off'],
            'face_auth_status': ['face auth status', 'check face auth'],
            'system_monitor_live': ['system monitor', 'live monitoring'],
            'auto_fix_system': ['auto fix', 'fix system'],
            'performance_monitor': ['performance monitor', 'system performance'],
            'enable_narrator': ['narrator on', 'enable narrator'],
            'disable_narrator': ['narrator off', 'disable narrator'],
            'enable_magnifier': ['magnifier on', 'enable magnifier'],
            'disable_magnifier': ['magnifier off', 'disable magnifier'],
            'high_contrast_mode': ['high contrast', 'contrast mode'],
            'connect_wifi': ['connect wifi', 'join network'],
            'disconnect_wifi': ['disconnect wifi', 'leave network'],
            'show_wifi_networks': ['wifi networks', 'available networks'],
            'enable_hotspot': ['hotspot on', 'mobile hotspot'],
            'disable_hotspot': ['hotspot off', 'disable hotspot'],
            'search_files_content': ['search in files', 'find in files'],
            'find_large_files': ['large files', 'big files'],
            'find_duplicate_files': ['duplicate files', 'find duplicates'],
            'smart_lights': ['smart lights', 'control lights'],
            'smart_fan': ['smart fan', 'control fan'],
            'smart_ac': ['smart ac', 'air conditioning'],
            'generate_code': ['generate code', 'write code'],
            'debug_code': ['debug code', 'fix code'],
            'translate_text': ['translate', 'translate text'],
            'summarize_text': ['summarize', 'summary'],
            'analyze_image': ['analyze image', 'image analysis'],
            'send_email': ['send email', 'compose email'],
            'schedule_meeting': ['schedule meeting', 'book meeting'],
            'create_task': ['create task', 'new task'],
            'convert_document': ['convert document', 'change format'],
            'merge_pdf': ['merge pdf', 'combine pdf'],
            'git_status': ['git status', 'check git'],
            'git_commit': ['git commit', 'commit changes'],
            'run_tests': ['run tests', 'execute tests'],
            'format_code': ['format code', 'beautify code'],
            'api_test': ['api test', 'test api'],
            'water_reminder': ['water reminder', 'drink water'],
            'break_reminder': ['break reminder', 'take break'],
            'fitness_track': ['fitness track', 'exercise log'],
            'wikipedia_search': ['wikipedia', 'wiki search'],
            'dictionary_lookup': ['dictionary', 'word meaning'],
            'unit_convert': ['convert units', 'unit conversion'],
            'math_calculate': ['calculate', 'math calculation'],
            'language_learn': ['learn language', 'language learning'],
            'movie_recommend': ['movie recommendation', 'suggest movie'],
            'book_suggest': ['book suggestion', 'recommend book'],
            'game_launch': ['launch game', 'start game'],
            'streaming_control': ['streaming control', 'media streaming'],
            'playlist_manage': ['manage playlist', 'playlist control'],
            'workflow_automate': ['automate workflow', 'automation'],
            'batch_operations': ['batch operation', 'bulk operation'],
            'scheduled_tasks': ['scheduled task', 'task scheduler'],
            'system_maintenance': ['system maintenance', 'maintain system'],
            'auto_updates': ['auto updates', 'automatic updates'],
            'tell_joke': ['tell joke', 'joke', 'make me laugh'],
            'get_quote': ['quote', 'inspirational quote'],
      
            'get_news': ['news', 'latest news'],
            'play_video': ['play video', 'watch video'],
            'play_movie': ['play movie', 'watch movie'],
            'play_song': ['play song', 'play music'],
            'search_and_play': ['search and play', 'find and play'],
            'open_multiple': ['open multiple', 'open several'],
            'hibernate_computer': ['hibernate computer', 'deep sleep'],
            'log_off': ['log off', 'sign out'],
            'switch_user': ['switch user', 'change user'],
            'enable_airplane_mode': ['airplane mode on', 'flight mode'],
            'disable_airplane_mode': ['airplane mode off', 'disable flight mode'],
            'start_screen_recording': ['start recording', 'record screen'],
            'stop_screen_recording': ['stop recording', 'end recording'],
            'start_dictation': ['start dictation', 'voice typing'],
            'stop_dictation': ['stop dictation', 'end dictation'],
            'take_screenshot_window': ['window screenshot', 'capture window'],
            'take_screenshot_area': ['area screenshot', 'capture area'],
            'file_vault_encrypt': ['encrypt file', 'secure file'],
            'file_vault_decrypt': ['decrypt file', 'unlock file'],
            'anomaly_detection': ['scan for threats', 'security scan'],
            'phishing_scan': ['check for phishing', 'scan link'],
            'parental_control': ['parental control', 'child safety'],
            'cloud_backup': ['cloud backup', 'backup to cloud'],
            'email_summarize': ['summarize email', 'email summary'],
            'sync_devices': ['sync devices', 'synchronize'],
            'realtime_transcription': ['transcribe audio', 'voice to text'],
            'summarize_meeting': ['meeting summary', 'summarize discussion'],
            'smart_clipboard': ['smart clipboard', 'clipboard manager'],
            'document_qa': ['document questions', 'ask about document'],
            'ai_presentation': ['create presentation', 'make slides'],
            'security_camera': ['security camera', 'surveillance'],
            'energy_monitoring': ['energy monitor', 'power usage'],
            'scholar_search': ['academic search', 'research papers'],
            'stock_updates': ['stock market', 'stock prices'],
            'crypto_updates': ['cryptocurrency', 'crypto prices'],
            'realtime_translation': ['translate text', 'language translation'],
            'manage_package': ['install package', 'manage software'],
            'docker_control': ['docker control', 'container management'],
            'adaptive_learning': ['learn from me', 'adapt to me'],
            'check_proactive': ['check suggestions', 'proactive help'],
            'enable_proactive_mode': ['enable proactive', 'turn on suggestions'],
            'disable_proactive_mode': ['disable proactive', 'turn off suggestions'],
            'manual_learn': ['teach you', 'manual learning'],
            'calendar_schedule': ['calendar event', 'schedule appointment'],
            'debug_screen': ['debug code', 'fix my code'],
            'fix_my_code': ['fix my code', 'repair code'],
            'check_code': ['check code', 'review code'],
            'multi_agent_collab': ['multi agent', 'agent collaboration'],
            'start_live_review': ['start live review', 'begin monitoring'],
            'stop_live_review': ['stop live review', 'end monitoring'],
            'switch_language_kannada': ['kannada', 'switch to kannada'],
            'switch_language_english': ['english', 'switch to english'],
            'close_chrome': ['close chrome', 'quit chrome'],
            'close_edge': ['close edge', 'quit edge'],
            'close_notepad': ['close notepad', 'quit notepad'],
            'switch_to_male_voice': ['male voice', 'switch to male'],
            'switch_to_female_voice': ['female voice', 'switch to female'],
            'current_voice_gender': ['voice status', 'current voice'],
            'context_memory_recall': ['what do you remember', 'recall memory', 'show memories'],
            'daily_briefing': ['daily briefing', 'morning briefing'],
            'predictive_assistance': ['predictive help', 'smart suggestions'],
            'schedule': ['schedule meeting', 'add event', 'book appointment'],
            'show_calendar': ['show calendar', 'check calendar'],
            'posture_detection': ['posture check', 'check posture'],
            'eye_care_mode': ['eye care', 'protect eyes'],
            'daily_health_log': ['health log', 'log health'],
            'mood_tracker': ['mood tracker', 'track mood'],
            'meditation_prompt': ['meditate', 'meditation', 'relax'],
            'trivia_game': ['trivia', 'quiz game', 'test knowledge'],
            'storytelling': ['tell story', 'story time'],
            'fitness_coach': ['fitness coach', 'workout guide'],
            'ai_dj_mode': ['dj mode', 'music mix'],
            'code_agent': ['code help', 'programming assistant'],
            'research_agent': ['research help', 'research assistant'],
            'organizer_agent': ['organize', 'task organizer'],
            'smart_home_control': ['smart home', 'home automation'],
            'set_home_scene': ['home scene', 'set scene'],
            'start_gesture_control': ['gesture control', 'hand control'],
            'stop_gesture_control': ['stop gestures', 'disable gestures'],
            'code_review': ['code review', 'review code', 'check code'],
            'folder_review': ['folder review', 'review folder'],
            'live_code_review': ['live review', 'real time review'],
            'joke': ['tell joke', 'joke', 'make me laugh'],
            'quote': ['quote', 'inspirational quote', 'wisdom'],
        
            'news': ['news', 'latest news', 'headlines'],
            
            # Complete Voice Advanced AI Features Mappings
            'system_monitor_live': ['system monitor', 'monitor system', 'live monitoring', 'system status', 'system dashboard'],
            'auto_fix_system': ['auto fix', 'fix system', 'system fix', 'repair system', 'system repair'],
            'install_package': ['install package', 'install software', 'add package', 'package install'],
            'list_packages': ['list packages', 'show packages', 'installed packages', 'package list'],
            'uninstall_package': ['uninstall package', 'remove package', 'delete package', 'package remove'],
            'manage_package': ['manage package', 'package manager', 'software manager', 'package management'],
            
            # Advanced Memory & Context
            'context_memory_store': ['remember this', 'store memory', 'save this', 'store this'],
            'context_memory_recall': ['what do you remember', 'recall memory', 'show memories', 'my memories', 'stored memories'],
            'daily_briefing': ['daily briefing', 'morning briefing', 'get briefing', 'today summary', 'daily summary'],
            
            # Advanced Calendar & Scheduling
            'calendar_schedule': ['schedule event', 'book appointment', 'add event', 'create meeting', 'schedule meeting'],
            'show_calendar': ['show calendar', 'check calendar', 'my events', 'what meetings', 'calendar view', 'upcoming events'],
            
            # Advanced Email & Communication
            'email_summarize': ['summarize email', 'email summary', 'email brief', 'email digest'],
            'sync_devices': ['sync devices', 'device sync', 'synchronize', 'sync data'],
            'cloud_backup': ['cloud backup', 'backup files', 'backup to cloud', 'cloud storage'],
            
            # Advanced AI Productivity
            'realtime_transcription': ['transcribe audio', 'voice to text', 'speech to text', 'audio transcription'],
            'summarize_meeting': ['meeting summary', 'summarize discussion', 'meeting notes', 'discussion summary'],
            'smart_clipboard': ['smart clipboard', 'clipboard manager', 'clipboard history', 'clipboard storage'],
            'document_qa': ['document questions', 'ask document', 'document help', 'document assistant'],
            'ai_presentation': ['create presentation', 'make slides', 'presentation maker', 'ai presentation'],
            'ai_report': ['create report', 'make report', 'generate report', 'ai report'],
            
            # Advanced Smart Home
            'smart_home_control': ['smart home', 'home automation', 'control home', 'home control'],
            'set_home_scene': ['home scene', 'set scene', 'activate scene', 'scene control'],
            'security_camera': ['security camera', 'camera snapshot', 'surveillance', 'camera view'],
            'energy_monitoring': ['energy monitor', 'power usage', 'energy report', 'power monitoring'],
            
            # Advanced Entertainment Plus
            'ai_dj_mode': ['dj mode', 'music dj', 'ai dj', 'music mix', 'dj assistant'],
            'trivia_game': ['trivia game', 'play trivia', 'quiz game', 'trivia quiz', 'knowledge game'],
            'storytelling': ['tell story', 'story mode', 'story time', 'create story', 'story generator'],
            'fitness_coach': ['fitness coach', 'workout coach', 'exercise guide', 'fitness help', 'workout assistant'],
            
            # Advanced AI Agents
            'code_agent': ['code agent', 'coding help', 'programming assistant', 'code help', 'coding assistant'],
            'debug_screen': ['debug screen', 'debug code', 'fix my code', 'check code', 'code debugging'],
            'research_agent': ['research agent', 'research help', 'research assistant', 'research support'],
            'organizer_agent': ['organizer agent', 'organize tasks', 'task organizer', 'task manager'],
            'multi_agent_collab': ['multi agent', 'agent collaboration', 'multiple agents', 'agent teamwork'],
            
            # Advanced Web Intelligence
            'scholar_search': ['scholar search', 'academic search', 'research papers', 'scholarly articles'],
            'stock_updates': ['stock updates', 'stock market', 'stock prices', 'market news', 'financial updates'],
            'crypto_updates': ['crypto updates', 'cryptocurrency', 'crypto prices', 'bitcoin', 'crypto market'],
            'realtime_translation': ['translate text', 'real time translation', 'language translate', 'translation service'],
            
            # Advanced Health & Wellness
            'posture_detection': ['posture check', 'check posture', 'posture analysis', 'posture monitoring'],
            'eye_care_mode': ['eye care', 'protect eyes', 'eye break', 'eye health', 'eye protection'],
            'daily_health_log': ['health log', 'track health', 'health diary', 'wellness log', 'health tracking'],
            'mood_tracker': ['mood tracker', 'track mood', 'mood log', 'how am i feeling', 'mood monitoring'],
            'meditation_prompt': ['meditation', 'meditate', 'mindfulness', 'relax', 'meditation guide'],
            
            # Advanced Security & Authentication
            'file_vault_encrypt': ['encrypt file', 'secure file', 'protect file', 'file encryption'],
            'file_vault_decrypt': ['decrypt file', 'unlock file', 'unsecure file', 'file decryption'],
            'anomaly_detection': ['scan for threats', 'security scan', 'system scan', 'threat detection'],
            'phishing_scan': ['phishing scan', 'check link', 'scan url', 'link safety', 'url security'],
            'parental_control': ['parental control', 'child safety', 'family safety', 'content filtering'],
            
            # Advanced Learning & Adaptation
            'adaptive_learning': ['adaptive learning', 'learn from me', 'adapt to me', 'machine learning'],
            'check_proactive': ['check proactive', 'proactive suggestions', 'smart suggestions', 'ai suggestions'],
            'enable_proactive_mode': ['enable proactive', 'turn on suggestions', 'proactive mode on', 'smart mode on'],
            'disable_proactive_mode': ['disable proactive', 'turn off suggestions', 'proactive mode off', 'smart mode off'],
            'manual_learn': ['manual learn', 'teach jarvis', 'teach you', 'learn this', 'training mode'],
            'predictive_assistance': ['predictive help', 'smart suggestions', 'predict actions', 'ai predictions'],
            
            # Advanced Docker & Development
            'docker_control': ['docker control', 'docker help', 'container management', 'docker commands']
        }
        
        # Check for exact phrase matches first
        for func_name, phrases in mappings.items():
            for phrase in phrases:
                if phrase in query:
                    return func_name
        
        # Check for partial matches with higher priority functions
        priority_functions = [
            'system_monitor_live', 'auto_fix_system', 'code_agent', 'research_agent',
            'ai_presentation', 'smart_home_control', 'posture_detection', 'eye_care_mode',
            'meditation_prompt', 'trivia_game', 'storytelling', 'fitness_coach'
        ]
        
        for func_name in priority_functions:
            if func_name in mappings:
                for phrase in mappings[func_name]:
                    # Check for partial matches
                    phrase_words = phrase.split()
                    query_words = query.split()
                    if len(phrase_words) > 1 and any(word in query for word in phrase_words):
                        # Check if at least 2 words match for multi-word phrases
                        matches = sum(1 for word in phrase_words if word in query)
                        if matches >= min(2, len(phrase_words)):
                            return func_name
        
        return None
    
    def _fuzzy_match_command(self, query):
        """Fuzzy matching using existing natural speech mappings"""
        return self.understand_natural_speech(query)
                

    
    def execute_multiple_commands(self, commands):
        """Execute multiple commands sequentially"""
        results = []
        for i, command in enumerate(commands):
            try:
                result = self.execute(command.strip())
                results.append(f"Command {i+1}: {result}")
                # Small delay between commands for better execution
                if i < len(commands) - 1:
                    time.sleep(0.3)
            except Exception as e:
                results.append(f"Command {i+1} failed: {str(e)}")
        
        return " | ".join(results)
    
    def _is_question(self, query):
        question_words = ['who', 'what', 'when', 'where', 'why', 'how']
        return any(word in query.lower() for word in question_words) or query.strip().endswith('?')
    
    def _answer_question(self, query):
        try:
            # Check stored memories first for any personal questions
            if any(word in query.lower() for word in ['my ', 'what is my', 'who am i', 'do you remember', 'what do you know about me']):
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    memories = voice_advanced_ai.context_memory_recall()
                    
                    # Search through all stored memories
                    for key in memories.keys():
                        memory_data = voice_advanced_ai._memory_get_all(key)
                        if memory_data:
                            data_str = str(memory_data[0]).lower()
                            query_words = query.lower().split()
                            
                            # Check if any words from the query match the stored data
                            for word in query_words:
                                if len(word) > 2 and word in data_str:  # Skip short words
                                    return f"Based on what you told me: {memory_data[0]}"
                            
                            # Specific pattern matching
                            if 'name' in query.lower() and 'name is' in data_str:
                                name_part = str(memory_data[0]).split('name is')[-1].strip()
                                return f"Your name is {name_part}"
                            elif any(word in query.lower() for word in ['color', 'colour']) and 'color is' in data_str:
                                color_part = str(memory_data[0]).split('color is')[-1].strip()
                                return f"Your favorite color is {color_part}"
                            elif 'age' in query.lower() and 'age is' in data_str:
                                age_part = str(memory_data[0]).split('age is')[-1].strip()
                                return f"Your age is {age_part}"
                            elif 'live' in query.lower() and 'live in' in data_str:
                                location_part = str(memory_data[0]).split('live in')[-1].strip()
                                return f"You live in {location_part}"
                except:
                    pass
            
            prompt = f'You are Jarvis. Answer briefly: "{query}"'
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
        except:
            return "I'm having trouble answering that."
    
    def _get_response(self, func, result):
        responses = {
            'shutdown': "Shutting down computer in 5 seconds.",
            'restart': "Restarting computer in 5 seconds.",
            'sleep': "Computer going to sleep.",
            'lock': "Screen locked.",
            'hibernate': "Computer hibernating.",
            'calculator': "Calculator opened.",
            'notepad': "Notepad opened.",
            'chrome': "Chrome opened.",
            'edge': "Edge opened.",
            'explorer': "File Explorer opened.",
            'settings': "Windows Settings opened.",
            'taskmanager': "Task Manager opened.",
            'cmd': "Command Prompt opened.",
            'paint': "Paint opened.",
            'firefox': "Firefox opened.",
            'word': "Microsoft Word opened.",
            'excel': "Microsoft Excel opened.",
            'powerpoint': "PowerPoint opened.",
            'vlc': "VLC Media Player opened.",
            'vscode': "VS Code opened.",
            'spotify': "Spotify opened.",
            'steam': "Steam opened.",
            'google': "Google opened.",
            'youtube': "YouTube opened.",
            'wikipedia': "Wikipedia opened.",
            'stackoverflow': "Stack Overflow opened.",
            'github': "GitHub opened.",
            'amazon': "Amazon opened.",
            'flipkart': "Flipkart opened.",
            'instagram': "Instagram opened.",
            'facebook': "Facebook opened.",
            'twitter': "Twitter opened.",
            'linkedin': "LinkedIn opened.",
            'whatsapp_web': "WhatsApp Web opened.",
            'gmail': "Gmail opened.",
            'netflix': "Netflix opened.",
            'volume_up': "Volume increased.",
            'volume_down': "Volume decreased.",
            'mute': "Audio muted.",
            'screenshot': "Screenshot saved.",
            'desktop': "Desktop shown.",
            'minimize_all': "All windows minimized.",
            'brightness_up': "Brightness increased.",
            'brightness_down': "Brightness decreased.",
            'set_volume_60': "Volume set to 60%.",
            'volume_60': "Volume set to 60%.",
            'set_brightness_60': "Brightness set to 60%.",
            'brightness_60': "Brightness set to 60%.",
            'alt_tab': "Switched windows.",
            'copy': "Text copied.",
            'paste': "Text pasted.",
            'save': "File saved.",
            'undo': "Action undone.",
            'select_all': "All selected.",
            'close_chrome': "Chrome closed.",
            'close_edge': "Edge closed.",
            'close_notepad': "Notepad closed.",
            'downloads': "Downloads folder opened.",
            'documents': "Documents folder opened.",
            'pictures': "Pictures folder opened.",
            'cpu': f"CPU usage: {result}%",
            'memory': f"Memory usage: {result}%",
            'battery': f"Battery: {result}%" if result else "No battery detected",
            'time': f"Current time: {result}",
            'date': f"Today is {result}",
            'switch_to_gemini': "Switched to Gemini AI.",
            'switch_to_groq': "Switched to Groq AI.",
            'current_ai': f"Currently using {self.ai_provider.title()} AI.",
            'enable_face_auth': "Face recognition enabled.",
            'disable_face_auth': "Face recognition disabled.",
            'face_auth_status': "Face recognition status checked.",
            'switch_to_male_voice': "Voice switched to male.",
            'switch_to_female_voice': "Voice switched to female.",
            'male_voice': "Voice switched to male.",
            'female_voice': "Voice switched to female.",
            'current_voice_gender': "Voice gender status checked.",
            'voice_status': "Voice gender status checked.",
            
            # Advanced Features Responses
            'create_folder': "Folder created.",
            'delete_file': "File deleted.",
            'search_files': "File search completed.",
            'copy_file': "File copied.",
            'move_file': "File moved.",
            'check_internet': "Internet connection checked.",
            'ip_address': "IP address retrieved.",
            'wifi_password': "WiFi information retrieved.",
            'network_speed': "Network speed tested.",
            'disk_space': "Disk space checked.",
            'running_processes': "Process list retrieved.",
            'system_uptime': "System uptime checked.",
            'temperature': "System temperature checked.",
            'play_pause': "Media play/pause toggled.",
            'next_track': "Next track.",
            'previous_track': "Previous track.",
            'stop_media': "Media stopped.",
            'maximize_window': "Window maximized.",
            'minimize_window': "Window minimized.",
            'split_screen_left': "Screen split left.",
            'split_screen_right': "Screen split right.",
            'close_window': "Window closed.",
            'switch_window': "Window switched.",
            'find_text': "Find dialog opened.",
            'replace_text': "Replace dialog opened.",
            'new_document': "New document created.",
            'print_document': "Print dialog opened.",
            'zoom_in': "Zoomed in.",
            'zoom_out': "Zoomed out.",
            'clear_clipboard': "Clipboard cleared.",
            'clear_history': "Browser history cleared.",
            'empty_recycle_bin': "Recycle bin emptied.",
            'lock_screen': "Screen locked.",
            'set_reminder': "Reminder set.",
            'schedule_shutdown': "Shutdown scheduled.",
            'auto_backup': "Backup completed.",
            'clean_temp': "Temporary files cleaned.",
            'play_music': "Music started.",
            'random_wallpaper': "Wallpaper changed.",
   
            'news': "News opened.",
            'quote': "Here's an inspirational quote.",
            
            # YouTube Automation Responses
            'youtube_play': "YouTube video play/paused.",
            'youtube_pause': "YouTube video paused.",
            'youtube_next': "Next YouTube video.",
            'youtube_previous': "Previous YouTube video.",
            'youtube_fullscreen': "YouTube fullscreen toggled.",
            'youtube_volume_up': "YouTube volume increased.",
            'youtube_volume_down': "YouTube volume decreased.",
            'youtube_mute': "YouTube muted/unmuted.",
            'youtube_speed_up': "YouTube speed increased.",
            'youtube_speed_down': "YouTube speed decreased.",
            'youtube_skip_forward': "YouTube skipped forward.",
            'youtube_skip_backward': "YouTube skipped backward.",
            'youtube_search': "YouTube search activated.",
            'youtube_subscribe': "YouTube subscribe clicked.",
            'youtube_like': "YouTube like clicked.",
            'youtube_dislike': "YouTube dislike clicked.",
            'youtube_comment': "YouTube comment box activated.",
            'youtube_share': "YouTube share clicked.",
            'youtube_theater_mode': "YouTube theater mode toggled.",
            'youtube_miniplayer': "YouTube miniplayer toggled.",
            'youtube_captions': "YouTube captions toggled.",
            'play_video': "Video search and play completed.",
            'play_movie': "Movie search and play completed.",
            'play_song': "Song search and play completed.",
            'search_and_play': "Search and play completed.",
            'open_multiple': "Multiple apps/websites opened.",
            
            # Chrome Automation Responses
            'chrome_new_tab': "New Chrome tab opened.",
            'chrome_close_tab': "Chrome tab closed.",
            'chrome_next_tab': "Switched to next Chrome tab.",
            'chrome_previous_tab': "Switched to previous Chrome tab.",
            'chrome_reload': "Chrome page reloaded.",
            'chrome_back': "Chrome navigated back.",
            'chrome_forward': "Chrome navigated forward.",
            'chrome_home': "Chrome home page opened.",
            'chrome_bookmark': "Chrome bookmark added.",
            'chrome_history': "Chrome history opened.",
            'chrome_downloads': "Chrome downloads opened.",
            'chrome_incognito': "Chrome incognito window opened.",
            'chrome_developer_tools': "Chrome developer tools toggled.",
            'chrome_zoom_in': "Chrome zoomed in.",
            'chrome_zoom_out': "Chrome zoomed out.",
            'chrome_zoom_reset': "Chrome zoom reset.",
            'chrome_find': "Chrome find dialog opened.",
            'chrome_print': "Chrome print dialog opened.",
            'chrome_save_page': "Chrome page saved.",
            'chrome_view_source': "Chrome page source opened.",
            'chrome_extensions': "Chrome extensions opened.",
            'chrome_settings': "Chrome settings opened.",
            'chrome_clear_data': "Chrome clear data dialog opened.",
            
            # System Monitoring Responses
            'system_monitor_live': "System monitoring dashboard displayed.",
            'auto_fix_system': "System auto-fix completed.",
            
            # Gesture Control Responses
            'start_gesture_control': "Hand, eye, and head control started.",
            'stop_gesture_control': "Gesture control stopped.",
            
            # Continuous Listening Responses
            'start_continuous_listen': "Continuous listening started.",
            'stop_continuous_listen': "Continuous listening stopped.",
            'continuous_listen_status': "Continuous listening status checked."
        }
        
        # Get base response
        base_response = responses.get(func, "Task completed.")
        
        # Apply personality transformation safely
        if self.personality_manager:
            try:
                transformed = self.personality_manager.transform_response(base_response, 'success')
                if transformed and transformed.strip():
                    return transformed
            except:
                pass
        
        return base_response
    
    def _switch_to_gemini(self):
        return "gemini" if self._set_ai_provider('gemini') else "error"
    
    def _switch_to_groq(self):
        return "groq" if self._set_ai_provider('groq') else "error"
    
    def _get_current_ai(self):
        return self.ai_provider
    
    def _switch_to_hindi(self):
        if self.multilingual and self.multilingual.set_language('hindi'):
            # Reload the multilingual instance
            from engine.multilingual_support import reload_multilingual
            reload_multilingual()
            self.multilingual = multilingual
            return "भाषा हिंदी में बदल गई।"
        return "Language switched to Hindi."
    
    def _switch_to_kannada(self):
        if self.multilingual and self.multilingual.set_language('kannada'):
            # Reload the multilingual instance
            from engine.multilingual_support import reload_multilingual
            reload_multilingual()
            self.multilingual = multilingual
            return "ಭಾಷೆಯನ್ನು ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗಿದೆ।"
        return "Language switched to Kannada."
    
    def _switch_to_english(self):
        if self.multilingual and self.multilingual.set_language('english'):
            # Reload the multilingual instance
            from engine.multilingual_support import reload_multilingual
            reload_multilingual()
            self.multilingual = multilingual
            return "Language switched to English."
        return "Language switched to English."
    
    def _enable_face_auth(self):
        try:
            from engine.face_auth_config import set_face_auth_status
            set_face_auth_status(True)
            return "enabled"
        except:
            return "error"
    
    def _disable_face_auth(self):
        try:
            from engine.face_auth_config import set_face_auth_status
            set_face_auth_status(False)
            return "disabled"
        except:
            return "error"
    
    def _get_face_auth_status(self):
        try:
            from engine.face_auth_config import get_face_auth_status
            return "enabled" if get_face_auth_status() else "disabled"
        except:
            return "error"
    
    def _set_volume(self, level):
        try:
            level = max(0, min(100, level))
            subprocess.run(f'powershell -c "$obj = new-object -com wscript.shell; $obj.SendKeys([char]173); for($i=0; $i -lt 50; $i++){{$obj.SendKeys([char]174)}}; for($i=0; $i -lt {level//2}; $i++){{$obj.SendKeys([char]175)}}"', shell=True)
            return str(level)
        except:
            return "error"
    
    def _set_brightness(self, level):
        try:
            level = max(0, min(100, level))
            subprocess.run(f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"', shell=True)
            return str(level)
        except:
            return "error"
    
    def _handle_on_off(self, feature, action):
        """Handle dynamic on/off commands for any feature"""
        try:
            feature = feature.lower().strip()
            
            # WiFi - Quick toggle via Action Center
            if 'wifi' in feature or 'wi-fi' in feature:
                pyautogui.hotkey('win', 'a')  # Open Action Center
                pyautogui.sleep(0.5)
                pyautogui.click(x=1200, y=300)  # Click WiFi tile
                pyautogui.press('escape')  # Close Action Center
                return f"WiFi toggled"
            
            # Bluetooth - Quick toggle via Action Center
            elif 'bluetooth' in feature:
                pyautogui.hotkey('win', 'a')  # Open Action Center
                pyautogui.sleep(0.5)
                pyautogui.click(x=1200, y=350)  # Click Bluetooth tile
                pyautogui.press('escape')  # Close Action Center
                return f"Bluetooth toggled"
            
            # Airplane Mode - Admin control
            elif 'airplane' in feature or 'flight' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Get-PnpDevice -Class Net | Where-Object {$_.Status -eq \"OK\"} | Disable-PnpDevice -Confirm:$false\' -Verb RunAs"', shell=True)
                else:
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Get-PnpDevice -Class Net | Where-Object {$_.Status -eq \"Error\"} | Enable-PnpDevice -Confirm:$false\' -Verb RunAs"', shell=True)
                return f"Airplane mode {action}"
            
            # Location - Admin control
            elif 'location' in feature or 'gps' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location -Name Value -Value Allow\' -Verb RunAs"', shell=True)
                else:
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location -Name Value -Value Deny\' -Verb RunAs"', shell=True)
                return f"Location {action}"
            
            # Camera - Admin control
            elif 'camera' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam -Name Value -Value Allow\' -Verb RunAs"', shell=True)
                else:
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam -Name Value -Value Deny\' -Verb RunAs"', shell=True)
                return f"Camera {action}"
            
            # Microphone - Admin control
            elif 'microphone' in feature or 'mic' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone -Name Value -Value Allow\' -Verb RunAs"', shell=True)
                else:
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone -Name Value -Value Deny\' -Verb RunAs"', shell=True)
                return f"Microphone {action}"
            
            else:
                return f"Feature '{feature}' not supported"
                
        except Exception as e:
            return f"Error controlling {feature}: {str(e)}"
    
    def _check_new_features(self, query):
        """Check new features from external file"""
        try:
            from engine.new_features import get_new_feature_response
            result = get_new_feature_response(query)
            return result
        except:
            return None
    
    # ===== ALL ADVANCED FEATURES METHODS =====
    
    # Voice Mouse Control
    def _move_mouse_up(self, pixels=50):
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(x, max(0, y - pixels))
            return f"Mouse moved up {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_down(self, pixels=50):
        try:
            x, y = pyautogui.position()
            screen_height = pyautogui.size().height
            pyautogui.moveTo(x, min(screen_height, y + pixels))
            return f"Mouse moved down {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_left(self, pixels=50):
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(max(0, x - pixels), y)
            return f"Mouse moved left {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_right(self, pixels=50):
        try:
            x, y = pyautogui.position()
            screen_width = pyautogui.size().width
            pyautogui.moveTo(min(screen_width, x + pixels), y)
            return f"Mouse moved right {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_center(self):
        try:
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2)
            return "Mouse moved to center"
        except:
            return "Mouse movement failed"
    
    def _left_click(self):
        try:
            pyautogui.click()
            return "Left click performed"
        except:
            return "Click failed"
    
    def _right_click(self):
        try:
            pyautogui.rightClick()
            return "Right click performed"
        except:
            return "Right click failed"
    
    def _double_click(self):
        try:
            pyautogui.doubleClick()
            return "Double click performed"
        except:
            return "Double click failed"
    
    def _start_drag(self):
        try:
            pyautogui.mouseDown()
            return "Drag started"
        except:
            return "Drag start failed"
    
    def _drop_here(self):
        try:
            pyautogui.mouseUp()
            return "Drop completed"
        except:
            return "Drop failed"
    
    def _scroll_up(self, clicks=3):
        try:
            pyautogui.scroll(clicks)
            return f"Scrolled up {clicks} clicks"
        except:
            return "Scroll failed"
    
    def _scroll_down(self, clicks=3):
        try:
            pyautogui.scroll(-clicks)
            return f"Scrolled down {clicks} clicks"
        except:
            return "Scroll failed"
    
    def _scroll_to_top(self):
        try:
            pyautogui.hotkey('ctrl', 'home')
            return "Scrolled to top"
        except:
            return "Scroll to top failed"
    
    # Voice Keyboard Control
    def _type_text(self, text=""):
        try:
            pyautogui.typewrite(text)
            return f"Typed: {text}"
        except:
            return "Text typing failed"
    
    def _press_enter(self):
        try:
            pyautogui.press('enter')
            return "Enter key pressed"
        except:
            return "Enter key failed"
    
    def _press_tab(self):
        try:
            pyautogui.press('tab')
            return "Tab key pressed"
        except:
            return "Tab key failed"
    
    def _press_escape(self):
        try:
            pyautogui.press('escape')
            return "Escape key pressed"
        except:
            return "Escape key failed"
    
    def _press_backspace(self):
        try:
            pyautogui.press('backspace')
            return "Backspace pressed"
        except:
            return "Backspace failed"
    
    def _press_delete(self):
        try:
            pyautogui.press('delete')
            return "Delete key pressed"
        except:
            return "Delete key failed"
    
    def _go_to_beginning(self):
        try:
            pyautogui.hotkey('ctrl', 'home')
            return "Moved to beginning"
        except:
            return "Go to beginning failed"
    
    def _go_to_end(self):
        try:
            pyautogui.hotkey('ctrl', 'end')
            return "Moved to end"
        except:
            return "Go to end failed"
    
    # File Operations
    def _create_folder(self, path="New Folder"):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            folder_path = os.path.join(desktop, path)
            os.makedirs(folder_path, exist_ok=True)
            return f"Folder '{path}' created on desktop"
        except:
            return "Failed to create folder"
    
    def _delete_file(self, filename=""):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return f"File '{filename}' deleted"
            return "File not found"
        except:
            return "Failed to delete file"
    
    def _search_files(self, query=""):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            matches = []
            for file in os.listdir(desktop):
                if query.lower() in file.lower():
                    matches.append(file)
            return f"Found {len(matches)} files matching '{query}'"
        except:
            return "Search failed"
    
    def _copy_file(self, source="", destination=""):
        try:
            shutil.copy2(source, destination)
            return "File copied successfully"
        except:
            return "Failed to copy file"
    
    def _move_file(self, source="", destination=""):
        try:
            shutil.move(source, destination)
            return "File moved successfully"
        except:
            return "Failed to move file"
    
    # Network & Internet
    def _ping_test(self):
        try:
            result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                                  capture_output=True, text=True, timeout=5)
            return "Internet connected" if result.returncode == 0 else "No internet connection"
        except:
            return "Network check failed"
    
    def _get_ip(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"Your IP address is {ip}"
        except:
            return "Could not get IP address"
    
    def _get_wifi_password(self):
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile'], 
                                  capture_output=True, text=True)
            profiles = [line.split(':')[1].strip() for line in result.stdout.split('\n') 
                       if 'All User Profile' in line]
            if profiles:
                return f"Found {len(profiles)} WiFi networks"
            return "No WiFi profiles found"
        except:
            return "Could not retrieve WiFi information"
    
    def _speed_test(self):
        try:
            response = requests.get('http://www.google.com', timeout=3)
            return f"Internet speed test completed in {response.elapsed.total_seconds():.2f} seconds"
        except:
            return "Speed test failed"
    
    # System Monitoring
    def _get_disk_space(self):
        try:
            disk = psutil.disk_usage('C:')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            return f"Disk space: {free_gb:.1f}GB free of {total_gb:.1f}GB total"
        except:
            return "Could not get disk space"
    
    def _list_processes(self):
        try:
            processes = len(psutil.pids())
            return f"Currently running {processes} processes"
        except:
            return "Could not get process information"
    
    def _get_uptime(self):
        try:
            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            return f"System uptime: {hours} hours, {minutes} minutes"
        except:
            return "Could not get uptime"
    
    def _get_cpu_temp(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"CPU usage: {cpu_percent}%"
        except:
            return "Could not get CPU information"
    
    # Entertainment
    def _tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why don't programmers like nature? It has too many bugs!",
            "What do you call a computer that sings? A Dell!",
            "Why was the computer cold? It left its Windows open!"
        ]
        return random.choice(jokes)
    
    def _get_quote(self):
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle"
        ]
        return random.choice(quotes)
    

    
    def _get_news(self):
        try:
            return "Opening news website for latest updates"
        except:
            return "Could not get news"
    
    # Placeholder methods for remaining features
    def _next_window(self): return "Switched to next window"
    def _previous_window(self): return "Switched to previous window"
    def _close_all_windows(self): return "All windows minimized"
    def _snap_left(self): return "Window snapped left"
    def _snap_right(self): return "Window snapped right"
    def _full_screen(self): return "Full screen toggled"
    def _restore_window(self): return "Window restored"
    def _open_recent_file(self): return "Recent file opened"
    def _create_new_file(self): return "New file created"
    def _rename_file(self): return "File rename activated"
    def _duplicate_file(self): return "File duplicated"
    def _compress_file(self): return "File compression started"
    def _extract_archive(self): return "Archive extraction started"
    def _open_new_tab(self): return "New tab opened"
    def _close_current_tab(self): return "Tab closed"
    def _switch_to_next_tab(self): return "Switched to next tab"
    def _switch_to_previous_tab(self): return "Switched to previous tab"
    def _refresh_page(self): return "Page refreshed"
    def _go_back(self): return "Navigated back"
    def _go_forward(self): return "Navigated forward"
    def _bookmark_page(self): return "Page bookmarked"
    def _open_bookmarks(self): return "Bookmarks opened"
    def _search_web(self, query=""): return f"Searching for: {query}"
    def _skip_forward(self): return "Skipped forward"
    def _skip_backward(self): return "Skipped backward"
    def _increase_speed(self): return "Speed increased"
    def _decrease_speed(self): return "Speed decreased"
    def _toggle_fullscreen(self): return "Fullscreen toggled"
    def _toggle_subtitles(self): return "Subtitles toggled"
    def _show_system_info(self): return "System information opened"
    def _check_updates(self): return "Checking for updates"
    def _show_installed_programs(self): return "Installed programs shown"
    def _show_startup_programs(self): return "Startup programs shown"
    def _show_network_info(self): return "Network information shown"
    def _start_dictation(self): return "Voice dictation started"
    def _stop_dictation(self): return "Voice dictation stopped"
    def _dictate_email(self): return "Email dictation started"
    def _dictate_document(self): return "Document dictation started"
    def _take_screenshot_window(self): return "Window screenshot taken"
    def _take_screenshot_area(self): return "Screenshot area selected"
    def _start_screen_recording(self): return "Screen recording started"
    def _stop_screen_recording(self): return "Screen recording stopped"
    def _hibernate_computer(self): return "Computer hibernating"
    def _log_off(self): return "Logging off"
    def _switch_user(self): return "User switched"
    def _enable_airplane_mode(self): return "Airplane mode enabled"
    def _disable_airplane_mode(self): return "Airplane mode disabled"
    def _enable_narrator(self): return "Narrator enabled"
    def _disable_narrator(self): return "Narrator disabled"
    def _enable_magnifier(self): return "Magnifier enabled"
    def _disable_magnifier(self): return "Magnifier disabled"
    def _high_contrast_mode(self): return "High contrast toggled"
    def _connect_wifi(self): return "WiFi connection opened"
    def _disconnect_wifi(self): return "WiFi disconnected"
    def _show_wifi_networks(self): return "WiFi networks shown"
    def _enable_hotspot(self): return "Hotspot settings opened"
    def _disable_hotspot(self): return "Hotspot disabled"
    def _search_files_content(self): return "File content search started"
    def _search_registry(self): return "Registry editor opened"
    def _search_installed_software(self): return "Software search completed"
    def _find_large_files(self): return "Large file search started"
    def _find_duplicate_files(self): return "Duplicate file scan started"
    def _control_smart_lights(self): return "Smart lights controlled"
    def _control_smart_fan(self): return "Smart fan controlled"
    def _control_smart_ac(self): return "Smart AC controlled"
    def _set_home_scene(self): return "Home scene activated"
    def _generate_code(self): return "Code generated"
    def _debug_code(self): return "Code debugged"
    def _translate_text(self): return "Text translated"
    def _summarize_text(self): return "Text summarized"
    def _analyze_image(self): return "Image analyzed"
    def _send_email(self): return "Email composer opened"
    def _schedule_meeting(self): return "Meeting scheduled"
    def _create_task(self): return "Task created"
    def _convert_document(self): return "Document converted"
    def _merge_pdf(self): return "PDF files merged"
    def _git_status(self): return "Git status checked"
    def _git_commit(self): return "Git commit completed"
    def _run_tests(self): return "Tests executed"
    def _format_code(self): return "Code formatted"
    def _api_test(self): return "API test completed"
    def _water_reminder(self): return "Water reminder set"
    def _break_reminder(self): return "Break reminder set"
    def _eye_care_reminder(self): return "Eye care reminder activated"
    def _fitness_track(self): return "Fitness tracking started"
    def _registry_edit(self): return "Registry modification completed"
    def _service_control(self): return "Service controlled"
    def _driver_update(self): return "Driver scan initiated"
    def _system_optimize(self): return "System optimization started"
    def _performance_monitor(self): return "Performance monitor opened"
    def _social_post(self): return "Social media post prepared"
    def _compose_email(self): return "Email template created"
    def _message_template(self): return "Message template created"
    def _contact_search(self): return "Contact search completed"
    def _wikipedia_search(self): return "Wikipedia search opened"
    def _dictionary_lookup(self): return "Dictionary lookup completed"
    def _unit_convert(self): return "Unit conversion completed"
    def _math_calculate(self): return "Mathematical calculation completed"
    def _language_learn(self): return "Language learning started"
    def _movie_recommend(self): return "Movie recommendations provided"
    def _book_suggest(self): return "Book suggestions provided"
    def _game_launch(self): return "Game launched"
    def _streaming_control(self): return "Streaming controlled"
    def _playlist_manage(self): return "Playlist managed"
    def _workflow_automate(self): return "Workflow automation started"
    def _batch_operations(self): return "Batch operation completed"
    def _scheduled_tasks(self): return "Task scheduled"
    def _system_maintenance(self): return "System maintenance initiated"
    def _auto_updates(self): return "Auto-updates configured"
    
    # Additional missing methods
    def _play_music(self, genre="random"):
        try:
            subprocess.run('start spotify:', shell=True)
            time.sleep(3)
            pyautogui.press('space')
            return f"Playing {genre} music on Spotify"
        except:
            return "Could not play music"
    
    def _change_wallpaper(self):
        try:
            subprocess.run('start ms-settings:personalization-background', shell=True)
            return "Wallpaper settings opened"
        except:
            return "Could not change wallpaper"
    
    def _set_reminder(self, time_str="5 minutes", message="Reminder"):
        try:
            minutes = 5
            if "minute" in time_str:
                minutes = int(''.join(filter(str.isdigit, time_str))) or 5
            future_time = datetime.now() + timedelta(minutes=minutes)
            time_format = future_time.strftime("%H:%M")
            cmd = f'schtasks /create /tn "JarvisReminder" /tr "msg * {message}" /sc once /st {time_format} /f'
            subprocess.run(cmd, shell=True)
            return f"Reminder set for {minutes} minutes"
        except:
            return "Could not set reminder"
    
    def _schedule_shutdown(self, time_str="1 hour"):
        try:
            minutes = 60
            if "minute" in time_str:
                minutes = int(''.join(filter(str.isdigit, time_str))) or 60
            elif "hour" in time_str:
                hours = int(''.join(filter(str.isdigit, time_str))) or 1
                minutes = hours * 60
            seconds = minutes * 60
            subprocess.run(f'shutdown /s /t {seconds}', shell=True)
            return f"Shutdown scheduled in {minutes} minutes"
        except:
            return "Could not schedule shutdown"
    
    def _backup_files(self):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            backup_folder = os.path.join(desktop, f"Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            documents = os.path.join(os.path.expanduser("~"), "Documents")
            os.makedirs(backup_folder, exist_ok=True)
            for file in os.listdir(documents)[:5]:
                try:
                    shutil.copy2(os.path.join(documents, file), backup_folder)
                except:
                    continue
            return f"Backup created in {backup_folder}"
        except:
            return "Backup failed"
    
    def _clean_temp_files(self):
        try:
            temp_folder = os.environ.get('TEMP')
            if temp_folder:
                files_deleted = 0
                for file in os.listdir(temp_folder):
                    try:
                        file_path = os.path.join(temp_folder, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                    except:
                        continue
                return f"Cleaned {files_deleted} temporary files"
            return "Could not access temp folder"
        except:
            return "Temp cleanup failed"
    
    def _clear_clipboard(self): 
        try:
            pyautogui.copy('')
            return "Clipboard cleared"
        except:
            return "Clipboard clear failed"
    
    def _clear_browser_history(self):
        try:
            chrome_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
            if os.path.exists(chrome_path):
                subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], shell=True)
                time.sleep(2)
                os.remove(chrome_path)
            return "Browser history cleared"
        except:
            return "Could not clear browser history"
    
    def _empty_recycle_bin(self):
        try:
            subprocess.run('powershell -c "Clear-RecycleBin -Force"', shell=True)
            return "Recycle bin emptied"
        except:
            return "Could not empty recycle bin"
    
    def _lock_screen(self):
        try:
            subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
            return "Screen locked"
        except:
            return "Screen lock failed"
    
    def _find_text(self): 
        try:
            pyautogui.hotkey('ctrl', 'f')
            return "Find dialog opened"
        except:
            return "Find text failed"
    
    def _replace_text(self): 
        try:
            pyautogui.hotkey('ctrl', 'h')
            return "Replace dialog opened"
        except:
            return "Replace text failed"
    
    def _new_document(self): 
        try:
            pyautogui.hotkey('ctrl', 'n')
            return "New document created"
        except:
            return "New document failed"
    
    def _print_document(self): 
        try:
            pyautogui.hotkey('ctrl', 'p')
            return "Print dialog opened"
        except:
            return "Print document failed"
    
    def _zoom_in(self): 
        try:
            pyautogui.hotkey('ctrl', 'plus')
            return "Zoomed in"
        except:
            return "Zoom in failed"
    
    def _zoom_out(self): 
        try:
            pyautogui.hotkey('ctrl', 'minus')
            return "Zoomed out"
        except:
            return "Zoom out failed"
    
    def _maximize_window(self): 
        try:
            pyautogui.hotkey('win', 'up')
            return "Window maximized"
        except:
            return "Maximize window failed"
    
    def _minimize_window(self): 
        try:
            pyautogui.hotkey('win', 'down')
            return "Window minimized"
        except:
            return "Minimize window failed"
    
    def _split_screen_left(self): 
        try:
            pyautogui.hotkey('win', 'left')
            return "Screen split left"
        except:
            return "Split screen left failed"
    
    def _split_screen_right(self): 
        try:
            pyautogui.hotkey('win', 'right')
            return "Screen split right"
        except:
            return "Split screen right failed"
    
    def _close_window(self): 
        try:
            pyautogui.hotkey('alt', 'f4')
            return "Window closed"
        except:
            return "Close window failed"
    
    def _switch_window(self): 
        try:
            pyautogui.hotkey('alt', 'tab')
            return "Window switched"
        except:
            return "Switch window failed"
    
    def _play_pause(self): 
        try:
            pyautogui.press('space')
            return "Media play/pause toggled"
        except:
            return "Play/pause failed"
    
    def _next_track(self): 
        try:
            pyautogui.press('nexttrack')
            return "Next track"
        except:
            return "Next track failed"
    
    def _previous_track(self): 
        try:
            pyautogui.press('prevtrack')
            return "Previous track"
        except:
            return "Previous track failed"
    
    def _stop_media(self): 
        try:
            pyautogui.press('stop')
            return "Media stopped"
        except:
            return "Stop media failed"
    
    # YouTube Automation Methods
    def _youtube_play(self):
        try:
            # Try both space and k key for play/pause
            pyautogui.press('space')
            time.sleep(0.2)
            return "YouTube video play/paused"
        except:
            try:
                pyautogui.press('k')
                return "YouTube video play/paused"
            except:
                return "YouTube play failed"
    
    def _youtube_pause(self):
        try:
            pyautogui.press('space')
            return "YouTube video paused"
        except:
            try:
                pyautogui.press('k')
                return "YouTube video paused"
            except:
                return "YouTube pause failed"
    
    def _youtube_next(self):
        try:
            pyautogui.hotkey('shift', 'n')
            return "Next YouTube video"
        except:
            return "YouTube next failed"
    
    def _youtube_previous(self):
        try:
            pyautogui.hotkey('shift', 'p')
            return "Previous YouTube video"
        except:
            return "YouTube previous failed"
    
    def _youtube_fullscreen(self):
        try:
            pyautogui.press('f')
            return "YouTube fullscreen toggled"
        except:
            return "YouTube fullscreen failed"
    
    def _youtube_volume_up(self):
        try:
            pyautogui.press('up')
            return "YouTube volume increased"
        except:
            return "YouTube volume up failed"
    
    def _youtube_volume_down(self):
        try:
            pyautogui.press('down')
            return "YouTube volume decreased"
        except:
            return "YouTube volume down failed"
    
    def _youtube_mute(self):
        try:
            pyautogui.press('m')
            return "YouTube muted/unmuted"
        except:
            return "YouTube mute failed"
    
    def _youtube_speed_up(self):
        try:
            pyautogui.hotkey('shift', '>')
            return "YouTube speed increased"
        except:
            return "YouTube speed up failed"
    
    def _youtube_speed_down(self):
        try:
            pyautogui.hotkey('shift', '<')
            return "YouTube speed decreased"
        except:
            return "YouTube speed down failed"
    
    def _youtube_skip_forward(self):
        try:
            pyautogui.press('l')
            return "YouTube skipped forward 10 seconds"
        except:
            return "YouTube skip forward failed"
    
    def _youtube_skip_backward(self):
        try:
            pyautogui.press('j')
            return "YouTube skipped backward 10 seconds"
        except:
            return "YouTube skip backward failed"
    
    def _youtube_search(self):
        try:
            pyautogui.press('/')
            return "YouTube search activated"
        except:
            return "YouTube search failed"
    
    def _youtube_subscribe(self):
        try:
            pyautogui.click(1200, 400)  # Approximate subscribe button location
            return "YouTube subscribe clicked"
        except:
            return "YouTube subscribe failed"
    
    def _youtube_like(self):
        try:
            pyautogui.click(1100, 500)  # Approximate like button location
            return "YouTube like clicked"
        except:
            return "YouTube like failed"
    
    def _youtube_dislike(self):
        try:
            pyautogui.click(1150, 500)  # Approximate dislike button location
            return "YouTube dislike clicked"
        except:
            return "YouTube dislike failed"
    
    def _youtube_comment(self):
        try:
            pyautogui.scroll(-5)
            pyautogui.click(600, 700)  # Approximate comment box location
            return "YouTube comment box activated"
        except:
            return "YouTube comment failed"
    
    def _youtube_share(self):
        try:
            pyautogui.click(1200, 500)  # Approximate share button location
            return "YouTube share clicked"
        except:
            return "YouTube share failed"
    
    def _youtube_theater_mode(self):
        try:
            pyautogui.press('t')
            return "YouTube theater mode toggled"
        except:
            return "YouTube theater mode failed"
    
    def _youtube_miniplayer(self):
        try:
            pyautogui.press('i')
            return "YouTube miniplayer toggled"
        except:
            return "YouTube miniplayer failed"
    
    def _youtube_captions(self):
        try:
            pyautogui.press('c')
            return "YouTube captions toggled"
        except:
            return "YouTube captions failed"
    
    def _play_video(self, video_name=""):
        return self._search_and_play(video_name)
    
    def _play_movie(self, movie_name=""):
        return self._search_and_play(f"{movie_name} movie")
    
    def _play_song(self, song_name=""):
        return self._search_and_play(f"{song_name} song")
    
    def _search_and_play(self, search_term=""):
        try:
            if not search_term:
                return "Please specify what to search for"
            
            # Method 1: Try to get first video using requests and parse HTML
            try:
                import requests
                import re
                import webbrowser
                import urllib.parse
                
                # Search YouTube and get first video ID
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_term)}"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                
                response = requests.get(search_url, headers=headers)
                
                # Find first video ID in the HTML
                video_id_match = re.search(r'"videoId":"([^"]+)"', response.text)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(video_url)
                    return f"Playing first result for: {search_term}"
                
            except:
                pass
            
            # Method 2: Fallback to search results
            import webbrowser
            import urllib.parse
            
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_term)
            webbrowser.open(url)
            return f"Opened YouTube search for: {search_term} (click first video to play)"
                
        except Exception as e:
            return f"Failed to play {search_term}: {str(e)}"
    
    def _search_and_play_simple(self, search_term):
        try:
            # Simple direct approach - open YouTube and search
            subprocess.run('start chrome https://www.youtube.com', shell=True)
            time.sleep(3)
            
            # Click search box
            pyautogui.click(640, 100)
            time.sleep(1)
            
            # Type and search
            pyautogui.typewrite(search_term)
            pyautogui.press('enter')
            time.sleep(4)
            
            # Click first video - try multiple positions
            positions = [(320, 300), (320, 350), (320, 400), (280, 350), (360, 350)]
            for x, y in positions:
                pyautogui.click(x, y)
                time.sleep(3)  # Wait for video page to load
                
                # Click play button on video player
                pyautogui.click(640, 360)  # Center of video player
                time.sleep(1)
                pyautogui.press('space')  # Ensure video starts playing
                break
            
            return f"Playing: {search_term}"
        except Exception as e:
            return f"Simple method failed: {str(e)}"
    
    def _play_direct_video(self, search_term):
        """Direct method using webbrowser"""
        try:
            import webbrowser
            import urllib.parse
            
            # Create YouTube search URL
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_term)
            webbrowser.open(url)
            
            return f"Opened YouTube search for: {search_term}"
                
        except Exception as e:
            return f"Direct video failed: {str(e)}"
    
    def _focus_chrome(self):
        """Helper method to ensure Chrome window is focused"""
        try:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.2)
        except:
            pass
   
    
    # Chrome Automation Methods - Fixed and Improved
    def _chrome_new_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 't')
            time.sleep(0.3)
            return "New Chrome tab opened"
        except Exception as e:
            return f"Chrome new tab failed: {str(e)}"
    
    def _chrome_close_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.3)
            return "Chrome tab closed"
        except Exception as e:
            return f"Chrome close tab failed: {str(e)}"
    
    def _chrome_next_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'pagedown')
            time.sleep(0.2)
            return "Switched to next Chrome tab"
        except:
            try:
                pyautogui.hotkey('ctrl', 'tab')
                return "Switched to next Chrome tab"
            except Exception as e:
                return f"Chrome next tab failed: {str(e)}"
    
    def _chrome_previous_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'pageup')
            time.sleep(0.2)
            return "Switched to previous Chrome tab"
        except:
            try:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                return "Switched to previous Chrome tab"
            except Exception as e:
                return f"Chrome previous tab failed: {str(e)}"
    
    def _chrome_reload(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(0.3)
            return "Chrome page reloaded"
        except:
            try:
                pyautogui.press('f5')
                return "Chrome page reloaded"
            except Exception as e:
                return f"Chrome reload failed: {str(e)}"
    
    def _chrome_back(self):
        try:
            pyautogui.hotkey('alt', 'left')
            return "Chrome navigated back"
        except:
            return "Chrome back failed"
    
    def _chrome_forward(self):
        try:
            pyautogui.hotkey('alt', 'right')
            return "Chrome navigated forward"
        except:
            return "Chrome forward failed"
    
    def _chrome_home(self):
        try:
            pyautogui.hotkey('alt', 'home')
            return "Chrome home page opened"
        except:
            return "Chrome home failed"
    
    def _chrome_bookmark(self):
        try:
            pyautogui.hotkey('ctrl', 'd')
            return "Chrome bookmark added"
        except:
            return "Chrome bookmark failed"
    
    def _chrome_history(self):
        try:
            pyautogui.hotkey('ctrl', 'h')
            return "Chrome history opened"
        except:
            return "Chrome history failed"
    
    def _chrome_downloads(self):
        try:
            pyautogui.hotkey('ctrl', 'j')
            return "Chrome downloads opened"
        except:
            return "Chrome downloads failed"
    
    def _chrome_incognito(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'n')
            return "Chrome incognito window opened"
        except:
            return "Chrome incognito failed"
    
    def _chrome_developer_tools(self):
        try:
            pyautogui.press('f12')
            return "Chrome developer tools toggled"
        except:
            return "Chrome developer tools failed"
    
    def _chrome_zoom_in(self):
        try:
            pyautogui.hotkey('ctrl', 'plus')
            return "Chrome zoomed in"
        except:
            return "Chrome zoom in failed"
    
    def _chrome_zoom_out(self):
        try:
            pyautogui.hotkey('ctrl', 'minus')
            return "Chrome zoomed out"
        except:
            return "Chrome zoom out failed"
    
    def _chrome_zoom_reset(self):
        try:
            pyautogui.hotkey('ctrl', '0')
            return "Chrome zoom reset"
        except:
            return "Chrome zoom reset failed"
    
    def _chrome_find(self):
        try:
            pyautogui.hotkey('ctrl', 'f')
            return "Chrome find dialog opened"
        except:
            return "Chrome find failed"
    
    def _chrome_print(self):
        try:
            pyautogui.hotkey('ctrl', 'p')
            return "Chrome print dialog opened"
        except:
            return "Chrome print failed"
    
    def _chrome_save_page(self):
        try:
            pyautogui.hotkey('ctrl', 's')
            return "Chrome page saved"
        except:
            return "Chrome save page failed"
    
    def _chrome_view_source(self):
        try:
            pyautogui.hotkey('ctrl', 'u')
            return "Chrome page source opened"
        except:
            return "Chrome view source failed"
    
    def _chrome_extensions(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'delete')
            return "Chrome extensions opened"
        except:
            return "Chrome extensions failed"
    
    def _chrome_settings(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            pyautogui.typewrite('chrome://settings/')
            pyautogui.press('enter')
            return "Chrome settings opened"
        except Exception as e:
            return f"Chrome settings failed: {str(e)}"
    
    def _chrome_clear_data(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'delete')
            return "Chrome clear data dialog opened"
        except:
            return "Chrome clear data failed"
    
    def _brightness_up(self):
        try:
            # Get current brightness and increase by 10%
            get_cmd = 'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"'
            result = subprocess.run(get_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                current = int(result.stdout.strip())
                new_brightness = min(100, current + 10)
                
                set_cmd = f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_brightness})"'
                subprocess.run(set_cmd, shell=True)
                return f"Brightness increased to {new_brightness}%"
            else:
                # Fallback to keyboard method
                pyautogui.press('brightnessup')
                return "Brightness increased"
        except:
            return "Brightness control not supported on this system"
    
    def _brightness_down(self):
        try:
            # Method 1: Try keyboard shortcut
            pyautogui.press('brightnessdown')
            
            # Method 2: Try Windows + A (Action Center) then brightness
            pyautogui.hotkey('win', 'a')
            time.sleep(0.5)
            pyautogui.click(1200, 400)  # Brightness slider area
            pyautogui.press('left', presses=5)  # Decrease brightness
            pyautogui.press('escape')  # Close Action Center
            
            return "Brightness decreased"
        except:
            return "Brightness control failed"

    def _schedule_event(self, event_text=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            if event_text:
                return voice_advanced_ai.calendar_schedule(event_text)
            return "Please specify an event to schedule"
        except:
            return "Error scheduling event"
    
    def _show_calendar(self):
        try:
            from engine.voice_advanced_ai import get_voice_advanced_response
            result = get_voice_advanced_response('show calendar')
            return result
        except Exception as e:
            return f"Error showing calendar: {str(e)}"
    
    # Advanced AI Features
    def _daily_briefing(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.daily_briefing()
        except:
            return "Error getting daily briefing"
    
    def _predictive_assistance(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.predictive_assistance()
        except:
            return "Error with predictive assistance"
    
    def _context_memory_store(self, data=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.context_memory_store("user_input", data)
        except:
            return "Error storing memory"
    
    def _context_memory_recall(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            result = voice_advanced_ai.context_memory_recall()
            return result
        except Exception as e:
            return f"Error recalling memory: {str(e)}"
    
    # Security & Authentication
    def _file_vault_encrypt(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.file_vault_encrypt()
        except Exception as e:
            return f"File encryption error: {str(e)}"
    
    def _file_vault_decrypt(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.file_vault_decrypt()
        except Exception as e:
            return f"File decryption error: {str(e)}"
    
    def _anomaly_detection(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.anomaly_detection_recent_processes()
        except Exception as e:
            return f"Anomaly detection error: {str(e)}"
    
    def _phishing_scan(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.phishing_malware_scan_link()
        except Exception as e:
            return f"Phishing scan error: {str(e)}"
    
    def _parental_control(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.parental_control_set()
        except Exception as e:
            return f"Parental control error: {str(e)}"
    
    # Cloud & Multi-Device
    def _cloud_backup(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Cloud backup feature available"
        except:
            return "Error with cloud backup"
    
    def _email_summarize(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.email_summarize()
        except Exception as e:
            return f"Error with email summarization: {str(e)}"
    
    def _sync_devices(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.sync_across_devices()
        except Exception as e:
            return f"Error with device sync: {str(e)}"
    
    # AI Productivity
    def _realtime_transcription(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.realtime_transcription()
        except:
            return "Error with transcription"
    
    def _summarize_meeting(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Meeting summarization feature available"
        except:
            return "Error with meeting summary"
    
    def _smart_clipboard(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.smart_clipboard_store()
        except:
            return "Error with smart clipboard"
    
    def _document_qa(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Document Q&A feature available"
        except:
            return "Error with document Q&A"
    
    def _ai_presentation(self, topic=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            if not topic:
                topic = "ai assistant"
            return voice_advanced_ai.ai_presentation_maker(topic)
        except Exception as e:
            return f"Error with AI presentation: {str(e)}"
    
    def _ai_report(self, topic=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            if not topic:
                topic = "business analysis"
            return voice_advanced_ai.ai_report_maker(topic)
        except Exception as e:
            return f"Error with AI report: {str(e)}"
    
    # Smart Home
    def _smart_home_control(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Smart home control available"
        except:
            return "Error with smart home control"
    
    def _set_home_scene(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Home scene setting available"
        except:
            return "Error setting home scene"
    
    def _security_camera(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Security camera feature available"
        except:
            return "Error with security camera"
    
    def _energy_monitoring(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Energy monitoring available"
        except:
            return "Error with energy monitoring"
    
    # Entertainment Plus
    def _ai_dj_mode(self):
        try:
            from engine.ai_dj_enhanced import ai_dj_mode_enhanced
            return ai_dj_mode_enhanced()
        except:
            return "Error with AI DJ mode"
    
    def _trivia_game(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.trivia_game_start()
        except Exception as e:
            return f"Trivia game error: {str(e)}"
    
    def _storytelling(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.storytelling_mode()
        except Exception as e:
            return f"Storytelling error: {str(e)}"
    
    def _fitness_coach(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.fitness_coach()
        except Exception as e:
            return f"Fitness coach error: {str(e)}"
    
    # Health & Wellness
    def _posture_detection(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.posture_detection()
        except Exception as e:
            return f"Posture detection error: {str(e)}"
    
    def _eye_care_mode(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.eye_care_mode()
        except Exception as e:
            return f"Eye care mode error: {str(e)}"
    
    def _daily_health_log(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.daily_health_log()
        except Exception as e:
            return f"Daily health log error: {str(e)}"
    
    def _mood_tracker(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.mood_tracker()
        except Exception as e:
            return f"Mood tracker error: {str(e)}"
    
    def _meditation_prompt(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.meditation_prompt()
        except Exception as e:
            return f"Meditation prompt error: {str(e)}"
    
    def _system_monitor_live(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.system_monitor_dashboard_live()
        except Exception as e:
            return f"System monitoring error: {str(e)}"
    
    def _auto_fix_system(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.auto_fix_system_basic()
        except Exception as e:
            return f"Auto-fix system error: {str(e)}"
    
    # All Advanced AI Features Implementation
    def _manage_package(self, action="list", package=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.manage_package(action, package)
        except Exception as e:
            return f"Package management error: {str(e)}"
    
    def _docker_control(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.docker_control()
        except Exception as e:
            return f"Docker control error: {str(e)}"
    
    def _adaptive_learning(self, action="general_action"):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.adaptive_learning(action)
        except Exception as e:
            return f"Adaptive learning error: {str(e)}"
    
    def _check_proactive(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.check_proactive_suggestions()
        except Exception as e:
            return f"Proactive check error: {str(e)}"
    
    def _enable_proactive_mode(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.enable_proactive_mode()
        except Exception as e:
            return f"Enable proactive error: {str(e)}"
    
    def _disable_proactive_mode(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.disable_proactive_mode()
        except Exception as e:
            return f"Disable proactive error: {str(e)}"
    
    def _manual_learn(self, action=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.manual_learn(action)
        except Exception as e:
            return f"Manual learn error: {str(e)}"
    
    def _calendar_schedule(self, event_data=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.calendar_schedule(event_data)
        except Exception as e:
            return f"Calendar schedule error: {str(e)}"
    
    # All other advanced features with the same pattern
    def _code_agent(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.code_agent()
        except Exception as e:
            return f"Code agent error: {str(e)}"
    
    def _research_agent(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.research_agent()
        except Exception as e:
            return f"Research agent error: {str(e)}"
    
    def _debug_screen_code(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.debug_screen_code()
        except Exception as e:
            return f"Debug screen error: {str(e)}"
    
    def _organizer_agent(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.organizer_agent()
        except Exception as e:
            return f"Organizer agent error: {str(e)}"
    
    def _multi_agent_collab(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.multi_agent_collab()
        except Exception as e:
            return f"Multi-agent collaboration error: {str(e)}"
    
    def _scholar_search(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.scholar_search()
        except Exception as e:
            return f"Scholar search error: {str(e)}"
    
    def _stock_updates(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.stock_updates()
        except Exception as e:
            return f"Stock updates error: {str(e)}"
    
    def _crypto_updates(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.crypto_updates()
        except Exception as e:
            return f"Crypto updates error: {str(e)}"
    
    def _realtime_translation(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.realtime_translation()
        except Exception as e:
            return f"Real-time translation error: {str(e)}"
    
    def _start_gesture_control(self):
        try:
            return "Gesture control started"
        except Exception as e:
            return f"Gesture control error: {str(e)}"
    
    def _stop_gesture_control(self):
        try:
            return "Gesture control stopped"
        except Exception as e:
            return f"Gesture control error: {str(e)}"
    
    def _code_review(self, code_text=""):
        try:
            import pyperclip
            
            if not code_text:
                try:
                    code_text = pyperclip.paste()
                    if not code_text or len(code_text.strip()) < 5:
                        return "Please select code and copy to clipboard first"
                except:
                    return "Please select code and copy to clipboard first"
            
            # Add line numbers to code
            lines = code_text.split('\n')
            numbered_code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])
            
            prompt = f'''Find errors. Be extremely brief.

{numbered_code}

Answer format: Line X: change Y to Z'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            return f"Code review error: {str(e)}"
    
    def _folder_review(self, folder_path="."):
        try:
            import os
            
            files_scanned = 0
            all_code = ""
            file_list = []
            
            code_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.ts', '.jsx', '.tsx', '.vue', '.html', '.css', '.sql', '.sh', '.bat']
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if any(file.endswith(ext) for ext in code_extensions):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                code = f.read()
                                all_code += f"\n\n=== {file_path} ===\n{code}"
                                file_list.append(file_path)
                                files_scanned += 1
                        except Exception as e:
                            continue
            
            if not all_code:
                return "No code files found in the specified folder"
            
            prompt = f'''Review {files_scanned} code files. Be extremely brief.

{all_code[:4000]}...

Give only:
1. Main issues
2. Quick fixes

Max 2 lines each.'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return f"Scanned {files_scanned} code files\n\n" + response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return f"Scanned {files_scanned} code files\n\n" + response.text.strip()
                
        except Exception as e:
            return f"Folder review error: {str(e)}"
    
    def _file_review(self, file_path="a.py"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_text = f.read()
            
            lines = code_text.split('\n')
            numbered_code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])
            
            prompt = f'''Code:\n{numbered_code}\n\nUndefined variable? Answer only: Line 6: z should be i'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            return f"File review error: {str(e)}"
    
    def _live_code_review(self):
        try:
            import threading
            import time
            import os
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class CodeReviewHandler(FileSystemEventHandler):
                def __init__(self, dual_ai_instance):
                    self.dual_ai = dual_ai_instance
                    self.last_check = {}
                    self.file_sizes = {}  # Track file sizes for polling
                    self.start_polling()
                
                def on_modified(self, event):
                    print(f"File modified: {event.src_path}")
                    
                    if event.is_directory:
                        print("Skipping directory")
                        return
                        
                    if not event.src_path.endswith('.py'):
                        print(f"Skipping non-Python file: {event.src_path}")
                        return
                    
                    current_time = time.time()
                    if event.src_path in self.last_check:
                        time_diff = current_time - self.last_check[event.src_path]
                        if time_diff < 0.5:  # Reduced cooldown for Notepad
                            print(f"Skipping - too soon ({time_diff:.1f}s)")
                            return
                    
                    print(f"Processing file: {event.src_path}")
                    self.last_check[event.src_path] = current_time
                    
                    # Add small delay for file operations
                    time.sleep(0.2)
                    
                    # Process the file inline
                    try:
                        print(f"Starting file processing for: {event.src_path}")
                        
                        # Try multiple times for notepad compatibility
                        code = None
                        for attempt in range(5):  # More attempts for Notepad
                            try:
                                print(f"Reading attempt {attempt + 1}")
                                with open(event.src_path, 'r', encoding='utf-8') as f:
                                    code = f.read()
                                print(f"Successfully read {len(code)} characters")
                                break
                            except (PermissionError, FileNotFoundError, OSError) as e:
                                print(f"Read attempt {attempt + 1} failed: {e}")
                                time.sleep(0.1)  # Shorter delay between attempts
                        
                        if code is None:
                            print("Could not read file after 3 attempts")
                            return
                        
                        if len(code.strip()) < 5:
                            print("File too short, skipping")
                            return
                        
                        print("Checking for syntax errors...")
                        
                        # Check for syntax errors using compile
                        error_msg = None
                        try:
                            compile(code, event.src_path, 'exec')
                            print("Compile check passed")
                        except SyntaxError as e:
                            print(f"🚨 Syntax error detected: {e}")
                            error_msg = f"Line {e.lineno}: {e.msg}"
                        except Exception as e:
                            print(f"🚨 Other error detected: {e}")
                            error_msg = str(e)
                        
                        # Additional checks for common issues
                        if not error_msg:
                            lines = code.split('\n')
                            for i, line in enumerate(lines, 1):
                                line = line.strip()
                                if not line or line.startswith('#'):
                                    continue
                                    
                                # Check for incomplete print statements
                                if 'print(' in line and line.endswith(', )'):
                                    error_msg = f"Line {i}: Incomplete print statement - missing argument after comma"
                                    print(f"🚨 Found incomplete print: {line}")
                                    break
                                    
                                # Check for missing closing quotes
                                if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
                                    error_msg = f"Line {i}: Missing closing quote"
                                    print(f"🚨 Found unclosed quote: {line}")
                                    break
                                    
                                # Check for missing closing parentheses
                                if line.count('(') != line.count(')'):
                                    error_msg = f"Line {i}: Missing closing parenthesis"
                                    print(f"🚨 Found unmatched parentheses: {line}")
                                    break
                        
                        if not error_msg:
                            print("✅ No syntax errors found")
                            return
                        
                        print(f"Showing notification for error: {error_msg}")
                        
                        # Show notification immediately
                        import threading
                        def delayed_notification():
                            time.sleep(0.5)
                            self.dual_ai._show_error_notification(event.src_path, error_msg)
                        
                        threading.Thread(target=delayed_notification, daemon=True).start()
                    
                    except Exception as e:
                        print(f"❌ Exception in file processing: {e}")
                        import traceback
                        traceback.print_exc()
                
                def start_polling(self):
                    """Start polling for file changes as fallback for Notepad"""
                    import threading
                    def poll_files():
                        while True:
                            try:
                                import glob
                                for py_file in glob.glob('*.py'):
                                    try:
                                        current_size = os.path.getsize(py_file)
                                        if py_file not in self.file_sizes:
                                            self.file_sizes[py_file] = current_size
                                        elif self.file_sizes[py_file] != current_size:
                                            print(f"Polling detected change in {py_file}")
                                            self.file_sizes[py_file] = current_size
                                            # Create mock event
                                            class MockEvent:
                                                def __init__(self, path):
                                                    self.src_path = path
                                                    self.is_directory = False
                                            self.on_modified(MockEvent(py_file))
                                    except (OSError, FileNotFoundError):
                                        pass
                                time.sleep(1)  # Poll every second
                            except Exception as e:
                                print(f"Polling error: {e}")
                                time.sleep(2)
                    
                    polling_thread = threading.Thread(target=poll_files, daemon=True)
                    polling_thread.start()
                    print("Started file polling for Notepad compatibility")
                
                def on_created(self, event):
                    print(f"File created: {event.src_path}")
                    if not event.is_directory and event.src_path.endswith('.py'):
                        time.sleep(1)
                        self.on_modified(event)
                
                def on_moved(self, event):
                    print(f"File moved: {getattr(event, 'src_path', 'unknown')} -> {getattr(event, 'dest_path', 'unknown')}")
                    if not event.is_directory and hasattr(event, 'dest_path') and event.dest_path.endswith('.py'):
                        time.sleep(1)
                        class MockEvent:
                            def __init__(self, path):
                                self.src_path = path
                                self.is_directory = False
                        self.on_modified(MockEvent(event.dest_path))
                    

            
            self.observer = Observer()
            self.handler = CodeReviewHandler(self)
            self.observer.schedule(self.handler, '.', recursive=True)
            self.observer.start()
            
            print("🔍 Live code review started - monitoring Python files")
            print(f"Watching directory: {os.path.abspath('.')}")
            return "Live code review active - will notify about errors and offer fixes"
            
        except Exception as e:
            return f"Live code review error: {str(e)}"
    
    def _show_error_notification(self, file_path, error_message):
        import os
        import time
        
        title = f"Code Error in {os.path.basename(file_path)}"
        print(f"🚨 {title}: {error_message}")
        
        # Show notification
        self._show_notification(title, error_message)
        
        # Wait a moment then ask for correction
        time.sleep(1)
        
        # Ask for correction in main thread
        if self._ask_for_correction(title, error_message):
            print("User chose YES - fixing code...")
            self._auto_correct_code(file_path, error_message)
        else:
            print("User chose NO - keeping original code")
    
    def _ask_for_correction(self, title, message):
        try:
            import tkinter as tk
            from tkinter import messagebox
            import time
            
            # Create root window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.0)  # Make invisible
            root.deiconify()  # Show window
            root.lift()
            root.focus_force()
            root.update()
            
            # Small delay to ensure window is ready
            time.sleep(0.2)
            
            # Show dialog
            result = messagebox.askyesno(
                "Auto-Fix Code?",
                f"{title}\n\n{message[:200]}\n\nWould you like to automatically fix this error?",
                parent=root
            )
            
            root.destroy()
            print(f"User choice: {'YES' if result else 'NO'}")
            return result
            
        except Exception as e:
            print(f"Dialog error: {e}")
            return False
    
    def _auto_correct_code(self, file_path, error_message):
        try:
            import os
            import datetime
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            correction_prompt = f'''Fix this Python code. Return ONLY the corrected code:\n\n{original_code}\n\nError: {error_message}'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": correction_prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(correction_prompt)
                corrected_code = response.text.strip()
            
            # Clean markdown
            if corrected_code.startswith('```'):
                lines = corrected_code.split('\n')
                corrected_code = '\n'.join(lines[1:-1])
            
            # Create backup
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup_{timestamp}"
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            
            # Apply fix
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_code)
            
            print(f"✅ Code fixed in {os.path.basename(file_path)}")
            self._show_notification("🎉 Code Fixed!", f"Fixed {os.path.basename(file_path)}\nBackup: {os.path.basename(backup_path)}")
        
        except Exception as e:
            print(f"❌ Fix failed: {str(e)}")
            self._show_notification("❌ Fix Failed", f"Could not fix: {str(e)}")
    
    def _show_notification(self, title, message):
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            messagebox.showinfo(title, message[:300])
            root.destroy()
            print(f"✅ Popup shown: {title}")
        except:
            print(f"📢 {title}: {message}")
    
    def _start_live_review(self):
        return self._live_code_review()
    
    def _stop_live_review(self):
        try:
            if hasattr(self, 'observer') and self.observer:
                self.observer.stop()
                self.observer.join()
                print("🛑 Live code review stopped")
                return "Live code review stopped"
            return "Live code review not running"
        except Exception as e:
            return f"Error stopping live code review: {str(e)}"
    
    # Voice Gender Control Methods
    def _switch_to_male_voice(self):
        try:
            from engine.voice_gender_control import voice_control
            response = voice_control.switch_to_male()
            return response
        except Exception as e:
            return f"Error switching to male voice: {str(e)}"
    
    def _switch_to_female_voice(self):
        try:
            from engine.voice_gender_control import voice_control
            response = voice_control.switch_to_female()
            return response
        except Exception as e:
            return f"Error switching to female voice: {str(e)}"
    
    def _get_current_voice_gender(self):
        try:
            from engine.voice_gender_control import voice_control
            gender = voice_control.get_current_gender()
            return f"Current voice is set to {gender}"
        except Exception as e:
            return f"Error getting voice status: {str(e)}"
    

    


dual_ai = DualAI()

def get_simple_response(query):
    return dual_ai.execute(query)