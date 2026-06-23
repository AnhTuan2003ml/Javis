import subprocess
import pyautogui
import psutil
from datetime import datetime, timedelta
import json
import os
import ctypes
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
from tkinter import simpledialog
import re, subprocess, urllib.parse
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Import multilingual support
try:
    from engine.multilingual_support import multilingual
except:
    multilingual = None

class DualAI:
    def __init__(self):
        """Initialize DualAI with dictation state"""
        self.ai_provider = self._get_ai_provider()
        self._init_ai_models()
        self.active_alarm = None
        # Load saved alarm
        try:
            import json
            from datetime import datetime
            with open('alarm.json', 'r') as f:
                data = json.load(f)
                saved_time = datetime.fromisoformat(data['time'])
                if saved_time > datetime.now():
                    self.active_alarm = saved_time
                    self._start_alarm_thread(saved_time)
        except:
            pass
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
             'sleep': lambda: subprocess.run('powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)"',shell=True),
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
            'powerpoint': self._ai_presentation,
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
            'show desktop': lambda: pyautogui.hotkey('win', 'd'),
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
            'downloads': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Downloads")}"', shell=True),
            'documents': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Documents")}"', shell=True),
            'pictures': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Pictures")}"', shell=True),
            'videos': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Videos")}"', shell=True),
            'music': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Music")}"', shell=True),
            'desktop': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Desktop")}"', shell=True),
            'appdata': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "AppData")}"', shell=True),
            'temp': lambda: subprocess.run('explorer "%TEMP%"', shell=True),
            'programfiles': lambda: subprocess.run('explorer "C:\\Program Files"', shell=True),
            'programfilesx86': lambda: subprocess.run('explorer "C:\\Program Files (x86)"', shell=True),
            'windows': lambda: subprocess.run('explorer "C:\\Windows"', shell=True),
            'system32': lambda: subprocess.run('explorer "C:\\Windows\\System32"', shell=True),
            'startup': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")}"', shell=True),
            'recent': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Recent")}"', shell=True),
            'open_path': self._open_path,

        
            'open_file': self._open_path,
            'open_folder': self._open_path,
            'launch_file': self._open_path,
            'launch_folder': self._open_path,
            'show_me': self._open_path,
            'find_file': self._open_path,
            'locate_file': self._open_path,
            
            # Random generators
            'dice': self._roll_dice,
            'coin': self._flip_coin,
            'roll_dice': self._roll_dice,
            'flip_coin': self._flip_coin,
            'age_calculator': self._age_calculator,
            'calculate_age': self._age_calculator,
            
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
            # 'system_monitor_live': self._system_monitor_live,
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
            
            # Token Usage
            'token_usage': self._get_token_usage,
            'tokens_used': self._get_token_usage,
            'token_status': self._get_token_usage,
            'reset_tokens': self._reset_token_count,
            

            
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
            'rename_file': self._rename_file_cmd,
            'zip_file': self._zip_file,
            'unzip_file': self._unzip_file,
            'file_size': self._get_file_size,
            'list_files': self._list_files,
            
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
            
            # Voice Dictation
            'start_dictation': self._start_dictation,
            'stop_dictation': self._stop_dictation,
  
            
            # Screen Control
            'take_screenshot_window': self._take_screenshot_window,
            'take_screenshot_area': self._take_screenshot_area,
            'start_screen_recording': self._start_screen_recording,
            'stop_screen_recording': self._stop_screen_recording,

            

            # Learning & Education
            'wikipedia_search': self._wikipedia_search,
            
            # Entertainment Plus
            'movie_recommend': self._movie_recommend,
         
            'game_launch': self._game_launch,
            'streaming_control': self._streaming_control,
            'playlist_manage': self._playlist_manage,
            
          
            
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
            
            # Code Writer Functions
            'write_code': self._write_code,
            'create_project': self._create_project,
            'generate_code': self._write_code,
            'code_generator': self._write_code,
            'build_project': self._create_project,
            'make_project': self._create_project,
            
            # Mapping Functions
            'open_maps': self._open_maps,
            'find_location': self._find_location,
            'get_directions': self._get_directions,
            'nearby_places': self._nearby_places,
            'traffic_info': self._traffic_info,
            'map_satellite': self._map_satellite,
            'map_terrain': self._map_terrain,
            'save_location': self._save_location,
            'my_location': self._my_location,
            'dictate_to_file': self._dictate_to_file,
            'dictate_to_document': self._dictate_to_document,
            'start_dictation': self._start_dictation,
            'stop_dictation': self._stop_dictation,
            'dictate_anywhere': self._dictate_anywhere,
            
            # Advanced File Management
            'search_content': self._search_content,
            'find_similar': self._find_similar_files,
            'suggest_folder': self._suggest_folder,
            'map_relationships': self._map_file_relationships,
            
            # Google Search
            'search_google': self._search_google,
            'search_images': self._search_images,
            'search_gifs': self._search_gifs,
            'copy_webpage_link': self._copy_webpage_link,
            'translate_webpage': self._translate_webpage,
            'check_website_status': self._check_website_status,
            'play_radio': self._play_radio,
            'play_podcast': self._play_podcast,
            'weekday': self._get_weekday,
            'current_weekday': self._get_weekday,
            'traffic_updates': self._get_traffic,
            'public_holidays': self._get_holidays,
            'covid_stats': self._get_covid_stats,
            
            # Product Price Tracking
            'track_amazon_price': self._track_amazon_price,
            'track_flipkart_price': self._track_flipkart_price,
            'check_product_price': self._check_product_price,
            
            # DEBUG Product Price Tracking
            'track_amazon_price_debug': self._track_amazon_price_debug,
            'track_flipkart_price_debug': self._track_flipkart_price_debug,
            'check_product_price_debug': self._check_product_price_debug,
            
            # Timer & Stopwatch
            'countdown_timer': self._countdown_timer,
            'start_timer': self._countdown_timer,
            'set_timer': self._countdown_timer,
            'start_stopwatch': self._start_stopwatch,
            'stop_stopwatch': self._stop_stopwatch,
            'reset_stopwatch': self._reset_stopwatch,
            'show_elapsed': self._show_elapsed,
            
            # Mini Games
            'open_mini_game': self._open_mini_game,
            'play_game': self._open_mini_game,
            'launch_game': self._open_mini_game,
            
            # Travel Search
            'search_flights': self._search_flights,
            'search_hotels': self._search_hotels,
            'find_flights': self._search_flights,
            'find_hotels': self._search_hotels,
            
            # Streaming Search
            'find_movie_streaming': self._find_movie_streaming,
            'find_show_streaming': self._find_show_streaming,
            'where_to_watch': self._where_to_watch,
            'streaming_availability': self._streaming_availability,
            
            # Continuous Listening Functions
            
            
            
            # Smart Clipboard Assistant
            'clipboard_assistant': self._clipboard_assistant,
            'start_clipboard_assistant': self._start_clipboard_assistant,
            'stop_clipboard_assistant': self._stop_clipboard_assistant,
            'set_alarm': self._set_alarm,
            'cancel_alarm': self._cancel_alarm,
            
            # AI Image Generation
            'create_image': self._create_image,
            'generate_image': self._create_image,
            'make_image': self._create_image,
            'ai_image': self._create_image,
            
            # AI Video Generation
            'create_video': self._create_video,
            'generate_video': self._create_video,
            'make_video': self._create_video,
            'ai_video': self._create_video,
            
            # File Sorting
            'sort_files': self._sort_files,
            'ai_document': self._ai_document_maker,
            'create_document': self._ai_document_maker,
            'create_report': self._ai_document_maker,
            'create_letter': self._ai_document_maker,

        }
    
    # Ambient Awareness Methods
 
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
                self.primary_model = "llama-3.1-8b-instant"
                self.fallback_model = "llama-3.3-70b-versatile"
                self.token_count = 0
                self.token_limit = 6000
                # Test the API key with a simple request
                test_response = self.groq_client.chat.completions.create(
                    model=self.primary_model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
            except Exception as e:
                print(f"Groq failed: {e}, switching to Gemini")
                self.ai_provider = 'gemini'
                self._init_gemini()

        else:
            self._init_gemini()
        
        # Initialize GPT4All as final fallback
        self._init_gpt4all()
    
    def _get_groq_model(self):
        """Get appropriate Groq model based on token usage"""
        if self.token_count >= self.token_limit:
            print(f"Token limit reached ({self.token_count}/{self.token_limit}), switching to 70B model")
            return self.fallback_model
        return self.primary_model
    
    def _reset_token_count(self):
        """Reset token count (call this every minute or when needed)"""
        self.token_count = 0
        return "Token count reset to 0"
    
    def _get_token_usage(self):
        """Get current token usage status"""
        if self.ai_provider == 'groq':
            percentage = (self.token_count / self.token_limit) * 100
            current_model = "70B" if self.token_count >= self.token_limit else "8B"
            return f"Tokens used: {self.token_count}/{self.token_limit} ({percentage:.1f}%) - Current model: {current_model}"
        else:
            return "Token tracking only available for Groq AI"
               
     
    
    def _init_gemini(self):
        try:
            import google.generativeai as genai
            from engine.gemini_config import GEMINI_API_KEY
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            print("Using Gemini AI")
        except Exception as e:
            print(f"AI init error: {e}")
    
    def _init_gpt4all(self):
        """Initialize GPT4All as final fallback"""
        try:
            from gpt4all import GPT4All
            import os
            
            # Use model from GPT4All default directory
            model_path = r"C:\Users\Hp\AppData\Local\nomic.ai\GPT4All"
            available_models = [
                "Llama-3.2-1B-Instruct-Q4_0.gguf",
            ]
            
            model_name = None
            for model in available_models:
                if os.path.exists(os.path.join(model_path, model)):
                    model_name = model
                    break
            
            if model_name:
                self.local_model = GPT4All(
                    model_name,
                    model_path=model_path,
                    verbose=False,
                    device='cpu',
                    n_threads=6,
                    n_ctx=1024
                )
                print(f"SUCCESS: GPT4All {model_name} initialized (optimized)")
            else:
                print("No GPT4All models found in default directory")
                self.local_model = None
        except Exception as e:
            print(f"ERROR: GPT4All init failed: {e}")
            self.local_model = None
    
    def execute(self, query):
        try:
            # Store current query for functions that need it
            self._current_query = query
            
            # Handle timer/stopwatch commands - ABSOLUTE HIGHEST PRIORITY
            query_lower = query.lower().strip()
            if 'stopwatch' in query_lower:
                if 'start' in query_lower:
                    return self._start_stopwatch()
                elif 'stop' in query_lower:
                    return self._stop_stopwatch()
                elif 'reset' in query_lower:
                    return self._reset_stopwatch()
                elif 'show' in query_lower or 'elapsed' in query_lower:
                    return self._show_elapsed()
            elif any(word in query_lower for word in ['timer', 'countdown']) and any(num.isdigit() for num in query_lower.split()):
                return self._countdown_timer()
            
            # Handle game commands - VERY HIGH PRIORITY
            if 'play' in query_lower and any(game in query_lower for game in ['chess', 'snake', 'tetris', '2048', 'dino', 'mario', 'solitaire', 'sudoku', 'game']):
                return self._open_mini_game()
            
            # Handle image creation commands FIRST (highest priority)
            if any(cmd in query_lower for cmd in ['create image', 'generate image', 'make image', 'ai image']):
                return self._create_image()
            
            # Handle video creation commands (highest priority)
            if any(cmd in query_lower for cmd in ['create video', 'generate video', 'make video', 'ai video']):
                return self._create_video()
            
            # Handle clipboard assistant commands FIRST (highest priority)
            if 'clipboard assistant' in query_lower:
                if 'start' in query_lower:
                    return self._start_clipboard_assistant()
                elif 'stop' in query_lower:
                    return self._stop_clipboard_assistant()
                else:
                    return self._clipboard_assistant()
            
        
            
            # Handle voice gender switching commands FIRST (highest priority)
            
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
            
            # Handle token usage commands
            if any(cmd in query_lower for cmd in ['token usage', 'tokens used', 'token status']):
                return self._get_token_usage()
            elif 'reset tokens' in query_lower:
                return self._reset_token_count()
            
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
            
                        # Check new features FIRST before any other processing
            new_feature_result = self._check_new_features(query)
            if new_feature_result:
                return new_feature_result
            
            if query_clean.startswith('folder review '):
                folder_name = query[14:].strip()
                return self._folder_review(folder_name)
            
            if "start dictation" in query_lower or "begin dictation" in query_lower or "start writing" in query_lower:
                return self._start_dictation(query)
            elif "stop dictation" in query_lower or "end dictation" in query_lower or "stop writing" in query_lower:
                return self._stop_dictation()
            elif "dictate document" in query_lower:
                return self._dictate_document(query)
            elif "dictate email" in query_lower:
                return self._dictate_document(query, "email")
            elif "dictate anywhere" in query_lower or "write anywhere" in query_lower:
                return self._dictate_anywhere(query)
            
            
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
            
            # Handle age calculation commands - HIGH PRIORITY
            if 'my age' in query.lower() or 'calculate my age' in query.lower() or 'age calculator' in query.lower():
                return self._age_calculator()
            
            # Handle code writer commands - HIGH PRIORITY
            if any(cmd in query.lower() for cmd in ['write code', 'generate code', 'create code', 'code generator', 'write python code', 'write javascript code', 'write java code', 'write c++ code', 'write c# code', 'write html code', 'write css code', 'write php code', 'write ruby code', 'write go code', 'write rust code', 'write swift code', 'write kotlin code']):
                return self._write_code()
            
            # Handle project creation commands - HIGH PRIORITY
            if any(cmd in query.lower() for cmd in ['create project', 'build project', 'make project']):
                return self._create_project()
            
            # Handle "create document" commands - HIGH PRIORITY
            if any(cmd in query.lower() for cmd in ['create document', 'create report', 'create letter']):
                return self._ai_document_maker()
            
            # Handle "create file" commands - HIGH PRIORITY
            if 'create file' in query.lower() or 'new file' in query.lower():
                result = self._create_new_file()
                return result
            
            # Handle "copy file" commands - HIGH PRIORITY
            if query.lower().startswith('copy ') and ' to ' in query.lower():
                result = self._copy_file()
                return result
            
            # Handle "move file" commands - HIGH PRIORITY
            if query.lower().startswith('move ') and ' to ' in query.lower():
                result = self._move_file()
                return result
            
            # Handle file operations
            if query.lower().startswith('rename '):
                return self._rename_file_cmd()
            if query.lower().startswith('delete ') and 'file' in query.lower():
                return self._delete_file()
            if 'zip' in query.lower() and 'file' in query.lower():
                return self._zip_file()
            if 'unzip' in query.lower() or 'extract' in query.lower():
                return self._unzip_file()
            if 'file size' in query.lower():
                return self._get_file_size()
            if 'list files' in query.lower():
                return self._list_files()
            if 'find file' in query.lower() or 'search file' in query.lower():
                return self._find_file()
            if 'duplicate' in query.lower() and 'file' in query.lower():
                return self._find_duplicates()
            if 'large file' in query.lower() or 'big file' in query.lower():
                return self._find_large_files()
            if 'empty folder' in query.lower():
                return self._find_empty_folders()
            if 'file info' in query.lower():
                return self._get_file_info()
            if 'backup' in query.lower() and 'folder' in query.lower():
                return self._backup_folder()
            if 'search content' in query.lower() or 'content search' in query.lower():
                return self._search_content()
            if 'find similar' in query.lower() or 'similar files' in query.lower():
                return self._find_similar_files()
            if 'suggest folder' in query.lower() or 'smart folder' in query.lower():
                return self._suggest_folder()
            if 'map relationships' in query.lower() or 'file relationships' in query.lower():
                return self._map_file_relationships()
           
            
            # Handle Google search commands
            if 'search google' in query.lower() or 'google search' in query.lower():
                return self._search_google()
            
            # Handle Wikipedia search commands (with typo handling)
            if 'wikipedia search' in query.lower() or 'wekipidea search' in query.lower() or 'wiki search' in query.lower():
                search_term = re.sub(r'(?:wikipedia|wekipidea|wiki)\s+search\s+(?:for\s+)?', '', query.lower()).strip()
                return self._wikipedia_search(search_term)
            
            # Handle image search commands
            if 'search images' in query.lower() or 'image search' in query.lower() or 'search for images' in query.lower():
                return self._search_images()
            
            # Handle GIF search commands
            if 'search gifs' in query.lower() or 'gif search' in query.lower() or 'search for gifs' in query.lower():
                return self._search_gifs()
            
            # Handle copy webpage link commands
            if 'copy link' in query.lower() or 'copy webpage link' in query.lower() or 'copy url' in query.lower():
                return self._copy_webpage_link()
            
            # Handle translate webpage commands
            if 'translate page' in query.lower() or 'translate webpage' in query.lower() or 'translate this page' in query.lower():
                return self._translate_webpage()
            
            # Handle website status check commands
            if 'check website' in query.lower() or 'website status' in query.lower() or 'is website up' in query.lower():
                return self._check_website_status()
            
            # Handle radio commands
            if 'play radio' in query.lower() or 'online radio' in query.lower() or 'radio station' in query.lower():
                return self._play_radio()
            
            # Handle podcast commands
            if 'play podcast' in query.lower() or 'online podcast' in query.lower() or 'listen podcast' in query.lower():
                return self._play_podcast()
            
            # Handle radio commands before YouTube search
            if 'radio' in query.lower() and ('play' in query.lower() or 'listen' in query.lower()):
                return self._play_radio()
            
            # Handle traffic commands - HIGH PRIORITY
            if 'traffic' in query.lower() and ('updates' in query.lower() or 'info' in query.lower() or 'conditions' in query.lower() or query.lower().strip() == 'traffic'):
                return self._get_traffic()
            

            

            
            # Handle travel search commands - HIGH PRIORITY
            if 'search' in query.lower():
                if 'flight' in query.lower() or 'flights' in query.lower():
                    return self._search_flights()
                elif 'hotel' in query.lower() or 'hotels' in query.lower():
                    return self._search_hotels()
            
            # Handle price tracking commands - HIGH PRIORITY
            if 'track' in query.lower() and 'price' in query.lower():
                if 'amazon' in query.lower():
                    return self._track_amazon_price_debug()
                elif 'flipkart' in query.lower():
                    return self._track_flipkart_price_debug()
                else:
                    return self._check_product_price_debug()
            
            # Handle reminder commands - HIGHEST PRIORITY
            if 'set reminder' in query.lower() or 'remind me' in query.lower() or 'task reminder' in query.lower():
                try:
                    from engine.new_features import task_reminder
                    return task_reminder(query)
                except Exception as e:
                    return f"Reminder feature error: {str(e)}"
            
            # Handle AI presentation commands - HIGHEST PRIORITY
            if any(phrase in query.lower() for phrase in ['make slides', 'create slides', 'create presentation', 'make presentation', 'slides of', 'presentation of', 'create ppt', 'make ppt']):
                return self._ai_presentation()
            
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
                # Handle singular/plural variations
                if chrome_cmd == 'setting':
                    chrome_cmd = 'settings'
                chrome_function = f'chrome_{chrome_cmd}'
                if chrome_function in self.functions:
                    result = self.functions[chrome_function]()
                    return self._get_response(chrome_function, result)
            
            # YouTube automation commands  
            if query.lower().startswith('youtube '):
                youtube_cmd = query.lower().replace('youtube ', '').strip()
                # Handle common variations
                if 'next video' in youtube_cmd or 'next song' in youtube_cmd:
                    youtube_cmd = 'next'
                elif 'previous video' in youtube_cmd or 'previous song' in youtube_cmd:
                    youtube_cmd = 'previous'
                elif 'skip forward' in youtube_cmd:
                    youtube_cmd = 'skip_forward'
                elif 'skip backward' in youtube_cmd or 'skip back' in youtube_cmd:
                    youtube_cmd = 'skip_backward'
                
                youtube_cmd = youtube_cmd.replace(' ', '_')
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
                    # Only trigger YouTube search if "youtube", "search", or "play" is explicitly mentioned
                    if ('youtube' in query.lower() and 'search' in query.lower() or 'play' in query.lower()) and search_term:
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
                print(f"Exact match found: {func_name}")
            else:
                # Try natural language understanding with enhanced matching
                func_name = self.understand_natural_speech(query)
                print(f"Natural language result: {func_name}")
                
                # If still no match, try fuzzy matching for common commands
                if not func_name:
                    func_name = self._fuzzy_match_command(query_lower)
                    print(f"Fuzzy match result: {func_name}")
                
                
                if not func_name:
                  
                    # try:
                    #     from engine.voice_advanced_ai import get_voice_advanced_response
                    #     advanced_response = get_voice_advanced_response(query)
                    #     print(f"Advanced AI response: '{advanced_response}'")
                    #     if advanced_response and "Voice command not recognized" not in advanced_response and "Error:" not in advanced_response:
                    #         print("Returning advanced AI response")
                    #         return advanced_response
                    # except Exception as e:
                    #     print(f"Advanced AI failed: {e}")
                    #     pass
                    
                    # Final fallback to AI model for function selection
                    # Check new features first
                    try:
                        from engine.new_features import get_new_feature_response
                        new_feature_result = get_new_feature_response(query)
                        if new_feature_result:
                            return new_feature_result
                    except:
                        pass
                    
                    # AI mapping for both dual_ai and new_features
                    print("Starting AI mapping process...")
                    all_functions = list(self.functions.keys())
                    try:
                        from engine.new_features import _new_features_instance
                        if _new_features_instance:
                            all_functions.extend(list(_new_features_instance.features.keys()))
                    except:
                        pass
                    
                    prompt = f'''TASK: Find exact function name for user command.

USER COMMAND: "{query}"
AVAILABLE FUNCTIONS: {all_functions}

MATCH EXAMPLES:
"mouse to center" = move_mouse_center
"turn off computer" = shutdown
"make louder" = volume_up
"take picture" = screenshot
"remind me" = task_reminder

INSTRUCTIONS:
- Return ONLY the exact function name from the list
- If no match found, return: none
- No explanations, no extra text

RESPONSE:'''
                    
                    try:
                        raw_response = self.get_ai_response(prompt)
                        print(f"Raw AI response: '{raw_response}'")
                        # Clean and validate the AI response
                        func_name = self._clean_ai_response(raw_response, all_functions)
                      
                        if func_name:
                            print(f"AI mapping successful: '{query}' -> {func_name}")
                        else:
                            print(f"AI mapping failed for: '{query}' (raw response: '{raw_response}')")
                    except Exception as e:
                        print(f"AI API error: {e}")
                        # Reset token count if we hit rate limits
                        if 'rate limit' in str(e).lower():
                            print("Rate limit hit, resetting token count")
                            self._reset_token_count()
                        func_name = None
                        

            # Check dual_ai functions first
            if func_name and func_name in self.functions:
                print(f"Executing dual_ai function: {func_name}")
                result = self.functions[func_name]()
                # For advanced features, return the actual result
                advanced_result_features = ['joke', 'quote', 'disk_space', 'ip_address', 'system_uptime', 'temperature', 'running_processes', 'check_internet', 'wifi_password', 'network_speed', 'create_folder', 'create_new_file', 'delete_file', 'search_files', 'set_reminder', 'schedule_shutdown', 'auto_backup', 'clean_temp', 'move_mouse_up', 'move_mouse_down', 'move_mouse_left', 'move_mouse_right', 'move_mouse_center', 'left_click', 'right_click', 'double_click', 'start_drag', 'drop_here', 'scroll_up', 'scroll_down', 'scroll_to_top', 'type_text', 'press_enter', 'press_tab', 'press_escape', 'press_backspace', 'press_delete', 'go_to_beginning', 'go_to_end', 'play_video', 'play_movie', 'play_song', 'search_and_play', 'open_multiple', 'daily_briefing', 'predictive_assistance', 'context_memory_recall', 'show_calendar', 'schedule', 'email_summarize', 'sync_devices', 'auto_fix_system', 'manage_package', 'docker_control', 'adaptive_learning', 'check_proactive', 'enable_proactive_mode', 'disable_proactive_mode', 'manual_learn', 'file_vault_encrypt', 'file_vault_decrypt', 'anomaly_detection', 'phishing_scan', 'parental_control', 'calendar_schedule', 'cloud_backup', 'realtime_transcription', 'summarize_meeting', 'smart_clipboard', 'document_qa', 'ai_presentation', 'smart_home_control', 'set_home_scene', 'security_camera', 'energy_monitoring', 'ai_dj_mode', 'trivia_game', 'storytelling', 'fitness_coach', 'code_agent', 'research_agent', 'organizer_agent', 'multi_agent_collab', 'scholar_search', 'stock_updates', 'crypto_updates', 'realtime_translation', 'posture_detection', 'eye_care_mode', 'daily_health_log', 'mood_tracker', 'meditation_prompt', 'start_gesture_control', 'stop_gesture_control', 'weekday', 'current_weekday', 'traffic_updates', 'public_holidays', 'covid_stats', 'open_path', 'sort_files', 'create_document', 'create_report', 'create_letter', 'ai_document']
                if func_name in advanced_result_features:
                    return result
                response = self._get_response(func_name, result)
                return response
            # Check new_features functions
            elif func_name:
                try:
                    from engine.new_features import _new_features_instance
                    if _new_features_instance and func_name in _new_features_instance.features:
                        # Execute new features function with query parameter if needed
                        query_functions = ['weather_forecast', 'email_templates', 'meeting_scheduler', 'task_reminder', 'list_reminders', 'image_editor', 'audio_converter', 'video_downloader', 'voice_recorder', 'screen_recorder', 'water_reminder', 'exercise_timer', 'calorie_calculator', 'sleep_tracker', 'stress_meter', 'mood_tracker', 'heart_rate_monitor', 'medication_reminder', 'bmi_calculator', 'system_monitor', 'network_monitor', 'language_translator', 'dictionary_lookup', 'wikipedia_search', 'calculator_advanced', 'unit_converter', 'flashcard_system', 'quiz_generator', 'meme_generator', 'logo_generator', 'color_palette_generator', 'font_viewer', 'ascii_art_generator', 'barcode_generator', 'mind_map_creator', 'password_manager', 'startup_manager', 'git_helper', 'port_scanner', 'email_sender', 'financial_tools', 'speed_test', 'battery_health', 'thermal_monitor', 'quick_note_taker', 'large_file_scanner', 'file_search_engine', 'recent_files_tracker', 'open_app', 'close_app', 'open_website', 'close_website']
                        
                        if func_name in query_functions:
                            result = _new_features_instance.features[func_name](query)
                        else:
                            result = _new_features_instance.features[func_name]()
                        
                        return result if result else f"{func_name} completed"
                except:
                    pass
            
            # Final fallback
            print("Checking if question...")
            if self._is_question(query):
                print("Processing as question")
                response = self._answer_question(query)
                return response
            # Try multilingual processing as fallback
            print("Trying multilingual processing...")
            if self.multilingual:
                ml_response = self.multilingual.process_command_in_language(query, self.multilingual.current_language)
                print(f"Multilingual response: '{ml_response}'")
                if ml_response != self.multilingual.get_response('processing'):
                    print("Returning multilingual response")
                    return ml_response
            
            print("Returning 'Command not recognized'")
            return "Command not recognized"
                
        except Exception as e:
            print(f"Error: {e}")
            return "Command not recognized"
    
    def _clean_ai_response(self, response, valid_functions):
        """Clean and validate AI response to ensure it returns a valid function name"""
        if not response:
            return None
            
        # Clean the response - remove quotes, whitespace, and common prefixes
        cleaned = response.strip().strip('"').strip("'").strip()
        
        # Remove common AI response patterns
        patterns_to_remove = [
            'function name:', 'the function is:', 'answer:', 'result:', 
            'i suggest:', 'i recommend:', 'use:', 'call:', 'execute:'
        ]
        
        for pattern in patterns_to_remove:
            if cleaned.lower().startswith(pattern):
                cleaned = cleaned[len(pattern):].strip()
        
        # Handle multi-line responses - take only the first line
        cleaned = cleaned.split('\n')[0].strip()
        
        # Check if it's a valid function name
        if cleaned in valid_functions:
            return cleaned
        
        # Check for partial matches (case insensitive)
        cleaned_lower = cleaned.lower()
        for func in valid_functions:
            if func.lower() == cleaned_lower:
                return func
        
        # Check if response indicates no match
        no_match_indicators = ['none', 'no match', 'not found', 'unknown', 'null', 'n/a']
        if cleaned.lower() in no_match_indicators:
            return None
            
        return None

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
            'show desktop': ['show desktop', 'go to desktop', 'minimize all'],
            'calculator': ['calculator', 'calc', 'open calculator'],
            'notepad': ['notepad', 'text editor', 'open notepad'],
            'chrome': ['chrome', 'browser', 'open chrome', 'web browser'],
            'stop_ambient_awareness': ['stop ambient awareness', 'end ambient awareness'],
            'sort_files': ['sort files', 'sort by date', 'sort by time', 'sort by name', 'sort by size', 'arrange files', 'organize files', 'arrange files by size', 'arrange files by date', 'arrange files by name', 'sort files by size', 'sort files by date', 'sort files by name'],
            'ambient_status': ['ambient status', 'check ambient status'],
            'start_ambient_awareness': ['start ambient awareness', 'ambient awareness', 'start ambient', 'begin ambient awareness', 'activate ambient awareness'],
            'edge': ['edge', 'microsoft edge', 'open edge'],
            'firefox': ['firefox', 'open firefox', 'mozilla'],
            'word': ['word', 'microsoft word', 'document editor'],
            'excel': ['excel', 'spreadsheet', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'presentation', 'slides'],
            'vlc': ['vlc', 'video player', 'media player'],
            'vscode': ['vscode', 'code editor', 'visual studio'],
            'spotify': ['spotify', 'music', 'music player'],

            'steam': ['steam', 'games', 'gaming'],
            'explorer': ['explorer', 'file manager'],
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
            'time': ['time', 'what time is it', 'current time', 'tell me the time','time now','what is time now'],
            'date': ['date', 'what date is it', 'current date', 'today'],
            'cpu': ['cpu usage', 'processor usage', 'cpu load'],
            'memory': ['memory usage', 'ram usage', 'memory load'],
            'battery': ['battery', 'battery level', 'battery percentage'],
            'downloads': [ 'download folder','downloads folder'],
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
            'running_processes': ['processes', 'running programs', 'active processes', 'show running processes', 'list processes', 'running processes'],
            'check_internet': ['internet', 'check internet', 'connection test'],
            'ip_address': ['ip address', 'my ip', 'network address'],
            'wifi_password': ['wifi password', 'network password'],
            'network_speed': ['speed test', 'internet speed', 'connection speed'],
            'create_folder': ['create folder', 'new folder', 'make folder', 'folder create'],
            'create_new_file': ['create file', 'new file', 'make file', 'create new file'],
            'delete_file': ['delete file', 'remove file'],
            'search_files': ['search files', 'find files'],
            'copy_file': ['copy file', 'duplicate file', 'copy', 'file copy'],
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
            # 'system_monitor_live': ['system monitor', 'live monitoring'],
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
            'write_code': ['write code', 'generate code', 'create code', 'code generator', 'write python code', 'write javascript code', 'write java code', 'write html code', 'write css code', 'python code for', 'javascript code for', 'java code for', 'code for'],
            'create_project': ['create project', 'build project', 'make project', 'new project', 'project for'],
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
            
            # Mapping Commands
            'open_maps': ['open maps', 'show maps', 'google maps', 'maps'],
            'find_location': ['find location', 'search location', 'locate', 'where is'],
            'get_directions': ['directions', 'navigate to', 'route to', 'how to get to'],
            'nearby_places': ['nearby', 'find nearby', 'places near me', 'restaurants near me'],
            'traffic_info': ['traffic', 'traffic info', 'show traffic', 'traffic conditions'],
            'map_satellite': ['satellite view', 'satellite map', 'aerial view'],
            'map_terrain': ['terrain view', 'terrain map', 'topographic map'],
            'save_location': ['save location', 'bookmark location', 'remember this place'],
            'my_location': ['my location', 'current location', 'where am i'],
            'dictate_to_file': ['dictate to file', 'voice to file', 'speech to file'],
            'dictate_to_document': ['dictate document', 'voice document', 'speech document'],
            'hibernate_computer': ['hibernate computer', 'deep sleep'],
            'log_off': ['log off', 'sign out'],
            'switch_user': ['switch user', 'change user'],
            'enable_airplane_mode': ['airplane mode on', 'flight mode'],
            'disable_airplane_mode': ['airplane mode off', 'disable flight mode'],
            'start_screen_recording': ['start recording', 'record screen'],
            'stop_screen_recording': ['stop recording', 'end recording'],
            'start_dictation': ['start dictation', 'voice typing', 'dictate anywhere', 'open and dictate','start writting'],
            'stop_dictation': ['stop dictation', 'end dictation', 'stop lies', 'stop writing'],
            'dictate_anywhere': ['dictate anywhere', 'universal dictation', 'type anywhere'],
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
            'ai_presentation': ['create presentation', 'make slides','create ppt'],
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
            'dice': ['dice', 'roll dice', 'roll a dice', 'roll the dice'],
            'coin': ['coin', 'flip coin', 'coin flip', 'flip the coin'],
            'roll_dice': ['roll dice', 'roll a dice', 'roll the dice'],
            'flip_coin': ['flip coin', 'coin flip', 'flip the coin'],
            'age_calculator': ['age calculator', 'calculate age', 'my age', 'how old am i', 'calculate my age', 'age calculation'],
            'calculate_age': ['calculate age', 'age calculator', 'find my age', 'determine age', 'age finder'],
            
            # Complete Voice Advanced AI Features Mappings
            # 'system_monitor_live': ['system monitor', 'monitor system', 'live monitoring', 'system status', 'system dashboard'],
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
            'clipboard_assistant': ['clipboard assistant', 'smart clipboard help', 'clipboard helper'],
            'start_clipboard_assistant': ['start clipboard assistant', 'monitor clipboard', 'clipboard monitoring'],
            'stop_clipboard_assistant': ['stop clipboard assistant', 'stop clipboard monitoring'],
            'set_alarm': ['set alarm', 'alarm for', 'wake me up', 'reminder at', 'alarm at'],
            'cancel_alarm': ['cancel alarm', 'stop alarm', 'turn off alarm', 'disable alarm', 'remove alarm'],
            'create_image': ['create image', 'generate image', 'make image', 'ai image', 'image generation', 'draw image'],
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
            'open_path': ['open file', 'open folder', 'open path', 'launch file', 'launch folder', 'run file', 'run folder', 'open documents', 'open downloads', 'open desktop', 'open pictures', 'open music', 'open videos', 'open docs', 'open pics', 'open vids', 'show me', 'find file', 'find folder', 'locate file', 'locate folder', 'access file', 'access folder', 'browse to', 'navigate to', 'go to file', 'go to folder'],

            
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
            'docker_control': ['docker control', 'docker help', 'container management', 'docker commands'],
            
            # Google Search
            'search_google': ['search google', 'google search', 'search on google', 'google it', 'search web'],
            'search_images': ['search images', 'image search', 'sehiiiiiiiarch for images', 'find images'],
            'search_gifs': ['search gifs', 'gif search', 'search for gifs', 'find gifs'],
            'copy_webpage_link': ['copy link', 'copy webpage link', 'copy url', 'copy page link'],
            'translate_webpage': ['translate page', 'translate webpage', 'translate this page', 'page translate'],
            'weekday': ['weekday', 'what day', 'current day', 'today day', 'day of week'],
            'traffic_updates': ['traffic updates', 'traffic conditions', 'traffic info', 'check traffic', 'traffic status'],
            'public_holidays': ['public holidays', 'holidays today', 'holiday check', 'is today holiday', 'holiday status'],
            'covid_stats': ['covid stats', 'covid updates', 'coronavirus stats', 'covid cases', 'covid data'],
            
            # Product Price Tracking
            'track_amazon_price': ['track amazon price', 'amazon price track', 'check amazon price', 'amazon price check', 'track price on amazon', 'price track amazon', 'track price of', 'amazon track price'],
            'track_flipkart_price': ['track flipkart price', 'flipkart price track', 'check flipkart price', 'flipkart price check', 'track price on flipkart', 'price track flipkart', 'flipkart track price'],
            'check_product_price': ['check product price', 'compare price', 'price comparison', 'product price', 'check price', 'price check'],
            
            # Travel Search
            'search_flights': ['search flights', 'find flights', 'book flights', 'flight search', 'flight booking', 'flights from', 'flights to'],
            'search_hotels': ['search hotels', 'find hotels', 'book hotels', 'hotel search', 'hotel booking', 'hotels in', 'hotels at'],
            
            # Streaming Search
            'find_movie_streaming': ['find movie streaming', 'where to watch movie', 'movie streaming', 'watch movie online'],
            'find_show_streaming': ['find show streaming', 'where to watch show', 'show streaming', 'watch show online'],
            'where_to_watch': ['where to watch', 'streaming availability', 'find streaming', 'watch online'],
            'streaming_availability': ['streaming availability', 'available on streaming', 'streaming platforms', 'watch platforms'],
            
            # Debug price tracking functions
            'track_amazon_price_debug': ['track amazon price debug', 'debug amazon price', 'amazon price debug'],
            'track_flipkart_price_debug': ['track flipkart price debug', 'debug flipkart price', 'flipkart price debug'],
            'check_product_price_debug': ['check product price debug', 'debug product price', 'price debug'],
            
            # File Sorting
            'sort_files': ['sort files', 'sort by date', 'sort by time', 'sort by name', 'sort by size', 'arrange files', 'organize files', 'arrange files by size', 'arrange files by date', 'arrange files by name', 'sort files by size', 'sort files by date', 'sort files by name']
                      
        }
        
        # Check for exact phrase matches first
        for func_name, phrases in mappings.items():
            for phrase in phrases:
                if phrase in query:
                    return func_name
        
        # Check for partial matches with higher priority functions
        priority_functions = [
            # 'system_monitor_live', 'auto_fix_system', 'code_agent', 'research_agent',
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
    
    def get_ai_response(self, prompt):
        """Get AI response for function mapping with fallback mechanism"""
        try:
            if self.ai_provider == 'groq':
                # Get appropriate model based on token usage
                model = self._get_groq_model()
                
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    max_tokens=50
                )
                
                # Track token usage (approximate)
                self.token_count += len(prompt.split()) + len(response.choices[0].message.content.split())
                
                return response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            print(f"AI response error: {e}")
            # If 8B model fails due to rate limit, try 70B model
            if self.ai_provider == 'groq' and 'rate limit' in str(e).lower():
                try:
                    print("Trying fallback to 70B model...")
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=self.fallback_model,
                        max_tokens=50
                    )
                    return response.choices[0].message.content.strip()
                except:
                    pass
            return None
    
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
                # Get appropriate model based on token usage
                model = self._get_groq_model()
                
                try:
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model
                    )
                    
                    # Track token usage (approximate)
                    self.token_count += len(prompt.split()) + len(response.choices[0].message.content.split())
                    
                    return response.choices[0].message.content.strip()
                    
                except Exception as e:
                    # If rate limit reached, try fallback model
                    if 'rate limit' in str(e).lower() or self.token_count >= self.token_limit:
                        print(f"Switching to {self.fallback_model} due to rate limit")
                        try:
                            response = self.groq_client.chat.completions.create(
                                messages=[{"role": "user", "content": prompt}],
                                model=self.fallback_model
                            )
                            return response.choices[0].message.content.strip()
                        except:
                            return "I'm having trouble answering that."
                    raise e

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
            'create_new_file': "File created successfully.",
            'delete_file': "File deleted.",
            'search_files': "File search completed.",
            'copy_file': "File copied successfully.",
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
            
            # Mapping Responses
            'open_maps': "Google Maps opened.",
            'find_location': "Location search opened.",
            'get_directions': "Directions opened.",
            'nearby_places': "Nearby places search opened.",
            'traffic_info': "Traffic information displayed.",
            'map_satellite': "Satellite view activated.",
            'map_terrain': "Terrain view activated.",
            'save_location': "Location saved.",
            'my_location': "Current location displayed.",
            'dictate_to_file': "Dictation to file completed.",
            'dictate_to_document': "Document dictation completed.",
            
            # System Monitoring Responses
            # 'system_monitor_live': "System monitoring dashboard displayed.",
            'auto_fix_system': "System auto-fix completed.",
            
            # Gesture Control Responses
            'start_gesture_control': "Hand, eye, and head control started.",
            'stop_gesture_control': "Gesture control stopped.",
            
            # Continuous Listening Responses
            'start_continuous_listen': "Continuous listening started.",
            'stop_continuous_listen': "Continuous listening stopped.",
            'continuous_listen_status': "Continuous listening status checked.",
            'weekday': "Current weekday retrieved.",
            'current_weekday': "Current weekday retrieved.",
            'traffic_updates': "Traffic information retrieved.",
            'public_holidays': "Holiday information retrieved.",
            'covid_stats': "COVID-19 statistics retrieved.",
            
            # Product Price Tracking Responses
            'track_amazon_price': "Amazon price tracking opened.",
            'track_flipkart_price': "Flipkart price tracking opened.",
            'check_product_price': "Product price comparison opened.",
            
            # Travel Search Responses
            'search_flights': "Flight search opened.",
            'search_hotels': "Hotel search opened.",
            'find_flights': "Flight search opened.",
            'find_hotels': "Hotel search opened.",
            
            # Streaming Search Responses
            'find_movie_streaming': "Movie streaming search opened.",
            'find_show_streaming': "Show streaming search opened.",
            'where_to_watch': "Streaming availability search opened.",
            'streaming_availability': "Streaming platforms search opened.",
            
            # File/Folder Opening Response
            'open_path': "File or folder opened.",
            
            # Alarm Responses
            'set_alarm': "Alarm set successfully.",
            'cancel_alarm': "Alarm cancelled.",
            
            # Random Generator Responses
            'dice': f" Dice rolled: {result}",
            'coin': f" Coin flip: {result}",
            'roll_dice': f" Dice rolled: {result}",
            'flip_coin': f" Coin flip: {result}",
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
                pyautogui.press('space')  # Click WiFi tile
                pyautogui.press('escape')  # Close Action Center
                return f"WiFi toggled"
            
            # Bluetooth - Quick toggle via Action Center
            elif 'bluetooth' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                # Sometimes focus is not on first tile, so ensure keyboard focus lands
                pyautogui.press('right')   # Move focus to Bluetooth (if needed)
                time.sleep(0.2)
                pyautogui.press('space')      # Toggle Bluetooth (first tile focus)
                time.sleep(0.2)

                pyautogui.press('escape')
                return f"bluetooth toggled"
            
            # Airplane Mode - Admin control
            elif 'airplane' in feature or 'flight' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                # Sometimes focus is not on first tile, so ensure keyboard focus lands
                pyautogui.press('right')   # Move focus to Bluetooth (if needed)
                time.sleep(0.1)
                pyautogui.press('right')
                time.sleep(0.1) 
                pyautogui.press('space')      # Toggle Bluetooth (first tile focus)
                time.sleep(0.2)

                pyautogui.press('escape')
                return f"airplane toggled"
            
            elif 'battery saver' in feature or 'energy saver' in feature or 'save battery' in feature:
                    pyautogui.hotkey('win', 'a')   # Open Quick Settings
                    time.sleep(0.5)

                    pyautogui.press('down')        # Move to Battery Saver tile
                    time.sleep(0.1)

                    pyautogui.press('space')       # Toggle Battery Saver
                    time.sleep(0.2)

                    pyautogui.press('escape')      # Close panel
                    return "Battery Saver toggled"

            elif 'night' in feature or 'night mode' in feature or 'night light' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                pyautogui.press('down')        # Move to the second row
                time.sleep(0.1)
                pyautogui.press('right')       # Move to Night Mode tile
                time.sleep(0.1)
                pyautogui.press('space')       # Toggle Night Mode
                time.sleep(0.2)
                pyautogui.press('escape')      # Close Quick Settings
                return "Night Mode toggled"

            elif 'hotspot' in feature or 'mobile hotspot' in feature or 'wi-fi hotspot' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                pyautogui.press('down')        # Move to 2nd row
                time.sleep(0.1)
                pyautogui.press('down')        # Move to 3rd row (Hotspot row)
                time.sleep(0.1)
                pyautogui.press('right')       # Move to Hotspot tile
                time.sleep(0.1)
                pyautogui.press('space')       # Toggle Hotspot
                time.sleep(0.2)
                pyautogui.press('escape')      # Close Quick Settings
                return "Hotspot toggled"

            elif 'nearby' in feature or 'nearby share' in feature or 'share nearby' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                pyautogui.press('down')        # Move to 2nd row
                time.sleep(0.1)
                pyautogui.press('down')        # Move to 3rd row
                time.sleep(0.1)
                pyautogui.press('right')       # Move to next tile
                time.sleep(0.1)
                pyautogui.press('right')       # Move to Nearby Share tile
                time.sleep(0.1)
                pyautogui.press('space')       # Toggle Nearby Share
                time.sleep(0.2)
                pyautogui.press('escape')      # Close Quick Settings
                return "Nearby Share toggled"

            
            # Location - Admin control
            elif 'location' in feature or 'gps' in feature:
                # Open Location Settings Page
                subprocess.Popen('start ms-settings:privacy-location', shell=True)
                time.sleep(1.8)  # wait for settings to open
              
                pyautogui.press('space')
                time.sleep(0.2)
               

                return "Location toggled"


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
            
            # Dark Mode
            elif 'dark mode' in feature or 'dark theme' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0"', shell=True)
                else:
                    subprocess.run('powershell -c "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1"', shell=True)
                return f"Dark mode {action}"
  
            

                
        except Exception as e:
            return f"Error controlling {feature}: {str(e)}"
    

    
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
    


    def _scroll_up(self, clicks=5):
        try:
            for _ in range(clicks):
                ctypes.windll.user32.mouse_event(0x0800, 0, 0, 120, 0)
            return f"Scrolled up {clicks}"
        except:
            return "Scroll failed"

    def _scroll_down(self, clicks=5):
        try:
            for _ in range(clicks):
                ctypes.windll.user32.mouse_event(0x0800, 0, 0, -120, 0)
            return f"Scrolled down {clicks}"
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
            # Extract folder name and directory from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract folder name
                match = re.search(r'create folder\s+([^\s]+)', query)
                if match:
                    path = match.group(1)
                
                # Extract directory path
                target_dir = None
                dir_match = re.search(r'(?:on|in|to)\s+([^\s]+)', query)
                if dir_match:
                    dir_name = dir_match.group(1)
                    
                    # Common directory mappings
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads', 'doenload': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Check if it's a known directory
                    if dir_name in directory_map:
                        target_dir = os.path.join(os.path.expanduser("~"), directory_map[dir_name])
                    else:
                        # Use as direct path
                        if os.path.isabs(dir_name):
                            target_dir = dir_name
                        else:
                            home_path = os.path.join(os.path.expanduser("~"), dir_name)
                            target_dir = home_path if os.path.exists(home_path) else os.path.abspath(dir_name)
                
                # Default to Desktop if no directory specified
                if not target_dir:
                    target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            os.makedirs(target_dir, exist_ok=True)
            folder_path = os.path.join(target_dir, path)
            os.makedirs(folder_path, exist_ok=True)
            return f"Folder '{path}' created in {os.path.basename(target_dir)}"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"
    
    def _create_new_file(self, filename="new_file.txt", content=""):
        try:
            # Extract filename and directory from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract filename
                match = re.search(r'create (?:new )?file\s+([^\s]+)', query)
                if match:
                    filename = match.group(1)
                    if '.' not in filename:
                        filename += '.txt'
                
                # Extract directory path
                target_dir = None
                dir_match = re.search(r'(?:on|in|to)\s+([^\s]+)', query)
                if dir_match:
                    dir_name = dir_match.group(1)
                    
                    # Common directory mappings
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads', 'doenload': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Check if it's a known directory
                    if dir_name in directory_map:
                        target_dir = os.path.join(os.path.expanduser("~"), directory_map[dir_name])
                    else:
                        # Use as direct path
                        if os.path.isabs(dir_name):
                            target_dir = dir_name
                        else:
                            home_path = os.path.join(os.path.expanduser("~"), dir_name)
                            target_dir = home_path if os.path.exists(home_path) else os.path.abspath(dir_name)
                
                # Default to Desktop if no directory specified
                if not target_dir:
                    target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            os.makedirs(target_dir, exist_ok=True)
            file_path = os.path.join(target_dir, filename)
            
            # Handle duplicates
            counter = 1
            original_path = file_path
            while os.path.exists(file_path):
                name, ext = os.path.splitext(original_path)
                file_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Create the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content if content else "")
            
            return f"File '{os.path.basename(file_path)}' created at {file_path}"
            
        except Exception as e:
            return f"Error creating file: {str(e)}"
    
    def _delete_file(self, filename=""):
        try:
            # Extract filename and directory from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract filename
                match = re.search(r'delete file\s+([^\s]+)', query)
                if match:
                    filename = match.group(1)
                
                # Extract directory - support common directory names
                directory_map = {
                    'download': 'Downloads',
                    'downloads': 'Downloads', 
                    'doenload': 'Downloads',  # Handle typo
                    'document': 'Documents',
                    'documents': 'Documents',
                    'desktop': 'Desktop',
                    'picture': 'Pictures',
                    'pictures': 'Pictures',
                    'music': 'Music',
                    'video': 'Videos',
                    'videos': 'Videos'
                }
                
                target_dir = None
                for key, folder in directory_map.items():
                    if f'on {key}' in query or f'in {key}' in query or f'from {key}' in query:
                        target_dir = os.path.join(os.path.expanduser("~"), folder)
                        break
                
                # Default to Desktop if no directory specified
                if not target_dir:
                    target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            file_path = os.path.join(target_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return f"File '{filename}' deleted from {os.path.basename(target_dir)}"
            return f"File '{filename}' not found in {os.path.basename(target_dir)}"
        except Exception as e:
            return f"Failed to delete file: {str(e)}"
    
    def _search_files(self, query=""):
        try:
            # Extract filename from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query_text = self._current_query.lower()
                
                # Extract filename from "search file filename" pattern
                match = re.search(r'search file\s+([^\s]+)', query_text)
                if match:
                    query = match.group(1)
            
            if not query:
                return "Please specify filename to search for"
            
            # Search in common directories
            search_dirs = [
                os.path.join(os.path.expanduser("~"), "Desktop"),
                os.path.join(os.path.expanduser("~"), "Downloads"),
                os.path.join(os.path.expanduser("~"), "Documents"),
                os.path.join(os.path.expanduser("~"), "Pictures"),
                os.path.join(os.path.expanduser("~"), "Videos"),
                os.path.join(os.path.expanduser("~"), "Music")
            ]
            
            matches = []
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for file in os.listdir(search_dir):
                        if query.lower() in file.lower():
                            matches.append(f"{file} (in {os.path.basename(search_dir)})")
            
            if matches:
                return f"Found {len(matches)} files: {', '.join(matches[:5])}{'...' if len(matches) > 5 else ''}"
            else:
                return f"No files found matching '{query}'"
        except Exception as e:
            return f"Error finding files: {str(e)}"
    
    def _copy_file(self, source="", destination=""):
        try:
            # Extract file copy details from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Parse "copy filename from_location to to_location" pattern
                copy_match = re.search(r'copy\s+([^\s]+)\s+([^\s]+)\s+to\s+([^\s]+)', query)
                if copy_match:
                    filename = copy_match.group(1)
                    from_location = copy_match.group(2)
                    to_location = copy_match.group(3)
                    
                    # Map common directory names
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'deckstop': 'Desktop',  # Handle typo
                        'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Get source directory
                    if from_location in directory_map:
                        source_dir = os.path.join(os.path.expanduser("~"), directory_map[from_location])
                    else:
                        source_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                    
                    # Get destination directory
                    if to_location in directory_map:
                        dest_dir = os.path.join(os.path.expanduser("~"), directory_map[to_location])
                    else:
                        dest_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                    
                    source = os.path.join(source_dir, filename)
                    destination = os.path.join(dest_dir, filename)
                    
                    # Check if source file exists
                    if not os.path.exists(source):
                        return f"File '{filename}' not found in {os.path.basename(source_dir)}"
                    
                    # Create destination directory if it doesn't exist
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Handle duplicate files
                    counter = 1
                    original_dest = destination
                    while os.path.exists(destination):
                        name, ext = os.path.splitext(original_dest)
                        destination = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    # Copy the file
                    shutil.copy2(source, destination)
                    return f"File '{filename}' copied from {os.path.basename(source_dir)} to {os.path.basename(dest_dir)}"
            
            # Fallback to original parameters
            if source and destination:
                shutil.copy2(source, destination)
                return "File copied successfully"
            
            return "Please specify source and destination"
            
        except Exception as e:
            return f"Failed to copy file: {str(e)}"
    
    def _move_file(self, source="", destination=""):
        try:
            # Extract file move details from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Parse "move filename from_location to to_location" pattern
                move_match = re.search(r'move\s+([^\s]+)\s+(?:from\s+)?([^\s]+)\s+to\s+([^\s]+)', query)
                if move_match:
                    filename = move_match.group(1)
                    from_location = move_match.group(2)
                    to_location = move_match.group(3)
                    
                    # Map common directory names
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'deckstop': 'Desktop',  # Handle typo
                        'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Get source directory
                    if from_location in directory_map:
                        source_dir = os.path.join(os.path.expanduser("~"), directory_map[from_location])
                    else:
                        source_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                    
                    # Get destination directory
                    if to_location in directory_map:
                        dest_dir = os.path.join(os.path.expanduser("~"), directory_map[to_location])
                    else:
                        dest_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                    
                    source = os.path.join(source_dir, filename)
                    destination = os.path.join(dest_dir, filename)
                    
                    # Check if source file exists
                    if not os.path.exists(source):
                        return f"File '{filename}' not found in {os.path.basename(source_dir)}"
                    
                    # Create destination directory if it doesn't exist
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Handle duplicate files
                    counter = 1
                    original_dest = destination
                    while os.path.exists(destination):
                        name, ext = os.path.splitext(original_dest)
                        destination = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    # Move the file
                    shutil.move(source, destination)
                    return f"File '{filename}' moved from {os.path.basename(source_dir)} to {os.path.basename(dest_dir)}"
            
            # Fallback to original parameters
            if source and destination:
                shutil.move(source, destination)
                return "File moved successfully"
            
            return "Please specify source and destination"
            
        except Exception as e:
            return f"Failed to move file: {str(e)}"
    
    def _rename_file_cmd(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'rename\s+([^\s]+)\s+to\s+([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                old_name, new_name, location = match.groups()
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                old_path = os.path.join(target_dir, old_name)
                new_path = os.path.join(target_dir, new_name)
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    return f"Renamed '{old_name}' to '{new_name}' in {os.path.basename(target_dir)}"
                return f"File '{old_name}' not found in {os.path.basename(target_dir)}"
            return "Usage: rename oldname to newname [in folder]"
        except Exception as e:
            return f"Rename failed: {str(e)}"
    
    def _zip_file(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'zip\s+(?:file\s+)?([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                filename, location = match.groups()
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(target_dir, filename)
                zip_path = file_path + '.zip'
                if os.path.exists(file_path):
                    with zipfile.ZipFile(zip_path, 'w') as zf:
                        zf.write(file_path, filename)
                    return f"Created {filename}.zip in {os.path.basename(target_dir)}"
                return f"File '{filename}' not found in {os.path.basename(target_dir)}"
            return "Usage: zip file filename [in folder]"
        except Exception as e:
            return f"Zip failed: {str(e)}"
    
    def _unzip_file(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'(?:unzip|extract)\s+([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                filename, location = match.groups()
                if not filename.endswith('.zip'):
                    filename += '.zip'
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                zip_path = os.path.join(target_dir, filename)
                if os.path.exists(zip_path):
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        zf.extractall(target_dir)
                    return f"Extracted {filename} in {os.path.basename(target_dir)}"
                return f"Zip file '{filename}' not found in {os.path.basename(target_dir)}"
            return "Usage: unzip filename [in folder]"
        except Exception as e:
            return f"Unzip failed: {str(e)}"
    
    def _get_file_size(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'(?:file\s+size|size\s+of)\s+([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                filename, location = match.groups()
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(target_dir, filename)
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    if size < 1024:
                        return f"{filename}: {size} bytes"
                    elif size < 1024*1024:
                        return f"{filename}: {size/1024:.1f} KB"
                    else:
                        return f"{filename}: {size/(1024*1024):.1f} MB"
                return f"File '{filename}' not found in {os.path.basename(target_dir)}"
            return "Usage: file size filename [in folder]"
        except Exception as e:
            return f"Get file size failed: {str(e)}"
    
    def _list_files(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'list\s+files(?:\s+in\s+([^\s]+))?', query)
            location = match.group(1) if match else None
            target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
            files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
            folders = [f for f in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, f))]
            return f"{os.path.basename(target_dir)}: {len(files)} files, {len(folders)} folders. Recent: {', '.join(files[:3])}"
        except Exception as e:
            return f"List files failed: {str(e)}"
    
    def _get_directory(self, query_or_location):
        """Get directory path from query or location name"""
        if not query_or_location:
            return os.path.join(os.path.expanduser("~"), "Desktop")
        
        # If it's a query, extract directory from it
        if isinstance(query_or_location, str) and len(query_or_location) > 20:
            import re
            # Look for directory patterns in query
            dir_match = re.search(r'(?:in|on|from|to)\s+([^\s]+)', query_or_location.lower())
            if dir_match:
                location = dir_match.group(1)
            else:
                location = None
        else:
            location = query_or_location
        
        if not location:
            return os.path.join(os.path.expanduser("~"), "Desktop")
        
        directory_map = {
            'download': 'Downloads', 'downloads': 'Downloads',
            'document': 'Documents', 'documents': 'Documents',
            'desktop': 'Desktop', 'deckstop': 'Desktop',
            'picture': 'Pictures', 'pictures': 'Pictures',
            'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
        }
        
        if location in directory_map:
            return os.path.join(os.path.expanduser("~"), directory_map[location])
        elif os.path.isabs(location):
            return location
        else:
            # Try as relative path from home directory
            home_path = os.path.join(os.path.expanduser("~"), location)
            if os.path.exists(home_path):
                return home_path
            # Fallback to Desktop
            return os.path.join(os.path.expanduser("~"), "Desktop")
    
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
    def _next_window(self):
        try:
            pyautogui.hotkey('alt', 'tab')
            return "Switched to next window"
        except:
            return "Window switch failed"
    
    def _previous_window(self):
        try:
            pyautogui.hotkey('alt', 'shift', 'tab')
            return "Switched to previous window"
        except:
            return "Window switch failed"
    
    def _close_all_windows(self):
        try:
            pyautogui.hotkey('win', 'd')
            return "All windows minimized"
        except:
            return "Minimize all failed"
    
    def _snap_left(self):
        try:
            pyautogui.hotkey('win', 'left')
            return "Window snapped left"
        except:
            return "Snap left failed"
    
    def _snap_right(self):
        try:
            pyautogui.hotkey('win', 'right')
            return "Window snapped right"
        except:
            return "Snap right failed"
    
    def _full_screen(self):
        try:
            pyautogui.press('f11')
            return "Full screen toggled"
        except:
            return "Full screen failed"
    
    def _restore_window(self):
        try:
            pyautogui.hotkey('win', 'up')
            return "Window restored"
        except:
            return "Window restore failed"
    
    def _open_recent_file(self):
        try:
            pyautogui.hotkey('ctrl', 'o')
            return "Recent file dialog opened"
        except:
            return "Open file failed"
    
    def _rename_file(self):
        try:
            pyautogui.press('f2')
            return "File rename activated"
        except:
            return "Rename failed"
    
    def _duplicate_file(self):
        try:
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey('ctrl', 'v')
            return "File duplicated"
        except:
            return "Duplicate failed"
    
    def _compress_file(self):
        try:
            pyautogui.rightClick()
            time.sleep(0.5)
            pyautogui.typewrite('compress')
            return "File compression started"
        except:
            return "Compression failed"
    
    def _extract_archive(self):
        try:
            pyautogui.rightClick()
            time.sleep(0.5)
            pyautogui.typewrite('extract')
            return "Archive extraction started"
        except:
            return "Extraction failed"
    
    def _open_new_tab(self):
        try:
            pyautogui.hotkey('ctrl', 't')
            return "New tab opened"
        except:
            return "New tab failed"
    
    def _close_current_tab(self):
        try:
            pyautogui.hotkey('ctrl', 'w')
            return "Tab closed"
        except:
            return "Close tab failed"
    
    def _switch_to_next_tab(self):
        try:
            pyautogui.hotkey('ctrl', 'tab')
            return "Switched to next tab"
        except:
            return "Tab switch failed"
    
    def _switch_to_previous_tab(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            return "Switched to previous tab"
        except:
            return "Tab switch failed"
    
    def _refresh_page(self):
        try:
            pyautogui.press('f5')
            return "Page refreshed"
        except:
            return "Refresh failed"
    
    def _go_back(self):
        try:
            pyautogui.hotkey('alt', 'left')
            return "Navigated back"
        except:
            return "Back navigation failed"
    
    def _go_forward(self):
        try:
            pyautogui.hotkey('alt', 'right')
            return "Navigated forward"
        except:
            return "Forward navigation failed"
    
    def _bookmark_page(self):
        try:
            pyautogui.hotkey('ctrl', 'd')
            return "Page bookmarked"
        except:
            return "Bookmark failed"
    
    def _open_bookmarks(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'b')
            return "Bookmarks opened"
        except:
            return "Bookmarks failed"
    
    def _search_web(self, query=""):
        try:
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.typewrite(query)
            pyautogui.press('enter')
            return f"Searching for: {query}"
        except:
            return "Web search failed"
    
    def _skip_forward(self):
        try:
            pyautogui.hotkey('ctrl', 'right')
            return "Skipped forward"
        except:
            return "Skip forward failed"
    
    def _skip_backward(self):
        try:
            pyautogui.hotkey('ctrl', 'left')
            return "Skipped backward"
        except:
            return "Skip backward failed"
    
    def _increase_speed(self):
        try:
            pyautogui.hotkey('shift', '>')
            return "Speed increased"
        except:
            return "Speed increase failed"
    
    def _decrease_speed(self):
        try:
            pyautogui.hotkey('shift', '<')
            return "Speed decreased"
        except:
            return "Speed decrease failed"
    
    def _toggle_fullscreen(self):
        try:
            pyautogui.press('f')
            return "Fullscreen toggled"
        except:
            return "Fullscreen failed"
    
    def _toggle_subtitles(self):
        try:
            pyautogui.press('c')
            return "Subtitles toggled"
        except:
            return "Subtitles failed"
    
    def _dictate_email(self):
        try:
            subprocess.Popen('start mailto:', shell=True)
            return "Email dictation started"
        except:
            return "Email dictation failed"
    
    def _dictate_document(self):
        try:
            subprocess.Popen('notepad', shell=True)
            return "Document dictation started"
        except:
            return "Document dictation failed"
    
    def _take_screenshot_window(self):
        try:
            pyautogui.hotkey('alt', 'printscreen')
            return "Window screenshot taken"
        except:
            return "Window screenshot failed"
    
    def _take_screenshot_area(self):
        try:
            pyautogui.hotkey('win', 'shift', 's')
            return "Screenshot area selected"
        except:
            return "Area screenshot failed"
    
    def _start_screen_recording(self):
        try:
            pyautogui.hotkey('win', 'g')
            return "Screen recording started"
        except:
            return "Screen recording failed"
    
    def _stop_screen_recording(self):
        try:
            pyautogui.hotkey('win', 'alt', 'r')
            return "Screen recording stopped"
        except:
            return "Stop recording failed"
    
    def _wikipedia_search(self, query=""):
        try:
            import urllib.parse
            if not query:
                subprocess.Popen('start https://wikipedia.org', shell=True)
            else:
                url = f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}"
                subprocess.Popen(f'start {url}', shell=True)
            return "Wikipedia search opened"
        except:
            return "Wikipedia search failed"
    
    def _movie_recommend(self):
        try:
            subprocess.Popen('start https://www.imdb.com/chart/top', shell=True)
            return "Movie recommendations opened"
        except:
            return "Movie recommendations failed"
    
   
    
    def _game_launch(self):
        try:
            subprocess.Popen('start steam:', shell=True)
            return "Game launcher opened"
        except:
            return "Game launch failed"
    
    def _streaming_control(self):
        try:
            subprocess.Popen('start https://netflix.com', shell=True)
            return "Streaming service opened"
        except:
            return "Streaming control failed"
    
    def _playlist_manage(self):
        try:
            subprocess.Popen('start spotify:', shell=True)
            return "Playlist manager opened"
        except:
            return "Playlist management failed"

   
    
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
                    # Wait for page to load then press space to play
                    import threading
                    def auto_play():
                        time.sleep(5)
                        pyautogui.press('space')
                    threading.Thread(target=auto_play, daemon=True).start()
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
            # Method 1: Try to open Chrome first, then navigate to settings
            subprocess.Popen('start chrome', shell=True)
            time.sleep(3)  # Wait for Chrome to open
            
            # Navigate to settings using keyboard shortcut
            pyautogui.hotkey('ctrl', 'l')  # Focus address bar
            time.sleep(0.5)
            pyautogui.typewrite('chrome://settings/')
            pyautogui.press('enter')
            time.sleep(1)
            return "Chrome settings opened"
        except Exception as e:
            try:
                # Method 2: Direct webbrowser approach
                import webbrowser
                webbrowser.open('chrome://settings/')
                time.sleep(2)
                return "Chrome settings opened"
            except Exception as e2:
                try:
                    # Method 3: Use Chrome command line
                    subprocess.Popen(['chrome', '--new-tab', 'chrome://settings/'], shell=True)
                    time.sleep(2)
                    return "Chrome settings opened"
                except Exception as e3:
                    return f"Chrome settings failed: {str(e3)}"
    
    def _chrome_clear_data(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'delete')
            return "Chrome clear data dialog opened"
        except:
            return "Chrome clear data failed"
    
    def _open_path(self, path_query=""):
        """Enhanced file/folder opening with smart mapping and search"""
        try:
            import os
            import subprocess
            import glob
            
            # Get query from current command if not provided
            if not path_query and hasattr(self, '_current_query'):
                path_query = self._current_query
            
            if not path_query:
                return "Please specify what to open"
            
            query = path_query.lower().strip()
            
            # Handle recent files commands
            if any(phrase in query for phrase in ["recent files", "recent documents", "recently used files", "show recent files", "show recently used", "open recent"]):
                try:
                    import glob
                    import time
                    
                    # Windows stores recent files in this folder
                    recent_folder = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Recent")
                    
                    # Get all recent items (*.lnk = shortcut files)
                    recent_files = glob.glob(os.path.join(recent_folder, "*.lnk"))
                    
                    if not recent_files:
                        return "No recent files found"
                    
                    # Filter out system files and keep only user documents
                    user_files = []
                    for file in recent_files:
                        name = os.path.basename(file).lower()
                        # Skip system files and keep user documents
                        if not any(skip in name for skip in ['ms-', 'system', 'windows', 'program', 'temp', 'cache']):
                            # Keep files with common document extensions
                            if any(ext in name for ext in ['.doc', '.pdf', '.ppt', '.xls', '.txt', '.jpg', '.png', '.mp4', '.mp3']):
                                user_files.append(file)
                    
                    # If no user files found, use all recent files
                    if not user_files:
                        user_files = recent_files
                    
                    # Sort by last modified (newest first)
                    user_files.sort(key=os.path.getmtime, reverse=True)
                    recent_files = user_files
                    
                    # Check if user wants to open recent file
                    if "open recent" in query:
                        # Open the first (most recent) file
                        first_recent = recent_files[0]
                        file_name = os.path.basename(first_recent).replace(".lnk", "")
                        # Clean file name to avoid encoding issues
                        file_name = ''.join(char for char in file_name if ord(char) < 128)
                        
                        # Try to resolve the shortcut and open the actual file
                        try:
                            # Use PowerShell to resolve the shortcut
                            ps_command = f'powershell -c "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(\"{first_recent}\"); $s.TargetPath"'
                            result = subprocess.run(ps_command, shell=True, capture_output=True, text=True)
                            
                            if result.returncode == 0 and result.stdout.strip():
                                target_path = result.stdout.strip()
                                if os.path.exists(target_path):
                                    subprocess.run(f'start "" "{target_path}"', shell=True)
                                    return f"{file_name} recent file opened"
                        except:
                            pass
                        
                        # Fallback: try to open the shortcut directly
                        subprocess.run(f'start "" "{first_recent}"', shell=True)
                        return f"{file_name} recent file opened"
                    
                    # Check for specific number of files to show
                    import re
                    number_match = re.search(r'(\d+)', query)
                    if number_match:
                        num_files = min(int(number_match.group(1)), len(recent_files))
                        top_recent = recent_files[:num_files]
                        # Limit the actual display to requested number
                        recent_files = top_recent
                    else:
                        # Default to 5 files
                        top_recent = recent_files[:5]
                        recent_files = top_recent
                    
                    # Get file names without .lnk extension and clean them
                    recent_names = []
                    for f in top_recent:
                        name = os.path.basename(f).replace(".lnk", "")
                        # Remove special characters that might cause encoding issues
                        clean_name = ''.join(char for char in name if ord(char) < 128)
                        recent_names.append(clean_name)
                    
                    # Open the Windows Recent Items folder
                    subprocess.run(f'explorer "{recent_folder}"', shell=True)
                    
                    # Create safe output string
                    if len(recent_names) > 3:
                        display_names = recent_names[:3]
                        return f"Showing {len(top_recent)} recent files: {', '.join(display_names)} and more"
                    else:
                        return f"Showing {len(top_recent)} recent files: {', '.join(recent_names)}"
                    
                except Exception as e:
                    # Handle encoding errors specifically
                    error_msg = str(e)
                    if 'charmap' in error_msg or 'codec' in error_msg:
                        return "Recent files found but cannot display due to special characters"
                    return f"Unable to show recent files: {error_msg}"
            
            # Enhanced folder shortcuts with multiple variations
            folder_shortcuts = {
                'downloads': ['downloads', 'download', 'dl'],
                'documents': ['documents', 'document', 'docs', 'doc'],
                'desktop': ['desktop', 'desk'],
                'pictures': ['pictures', 'picture', 'pics', 'pic', 'images', 'photos'],
                'music': ['music', 'songs', 'audio'],
                'videos': ['videos', 'video', 'movies', 'films'],
                'appdata': ['appdata', 'app data'],
                'temp': ['temp', 'temporary'],
                'startup': ['startup', 'start up']
            }
            
            # Check for folder shortcuts
            for folder, variations in folder_shortcuts.items():
                if any(var in query for var in variations):
                    if folder == 'appdata':
                        path = os.path.join(os.path.expanduser("~"), "AppData")
                    elif folder == 'temp':
                        path = os.environ.get('TEMP', 'C:\\Windows\\Temp')
                    elif folder == 'startup':
                        path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
                    else:
                        path = os.path.join(os.path.expanduser("~"), folder.title())
                    
                    if os.path.exists(path):
                        subprocess.run(f'explorer "{path}"', shell=True)
                        return f"{folder.title()} folder opened"
            
            # Extract filename from query FIRST
            import re
            # Look for patterns like "open file.txt" or "find document.pdf"
            file_match = re.search(r'(?:open|find|locate)\s+(?:file\s+)?([^\s]+\.[^\s]+)', query)
            if file_match:
                filename = file_match.group(1)
            else:
                # If no extension found, look for quoted filenames
                quote_match = re.search(r'["\']([^"\'\/\\]+\.[^"\'\/\\]+)["\']', query)
                if quote_match:
                    filename = quote_match.group(1)
                else:
                    filename = None
            
            if filename:
                
                # Search in common directories
                search_dirs = [
                    os.path.join(os.path.expanduser("~"), "Desktop"),
                    os.path.join(os.path.expanduser("~"), "Downloads"),
                    os.path.join(os.path.expanduser("~"), "Documents"),
                    os.path.join(os.path.expanduser("~"), "Pictures"),
                    os.path.join(os.path.expanduser("~"), "Videos"),
                    os.path.join(os.path.expanduser("~"), "Music")
                ]
                
                # Fuzzy search for files
                found_files = []
                for search_dir in search_dirs:
                    if os.path.exists(search_dir):
                        # Exact match
                        exact_path = os.path.join(search_dir, filename)
                        if os.path.exists(exact_path):
                            found_files.append(exact_path)
                        
                        # Fuzzy match
                        try:
                            matches = glob.glob(os.path.join(search_dir, f"*{filename}*"))
                            found_files.extend(matches)
                        except:
                            pass
                
                if found_files:
                    file_path = found_files[0]
                    if os.path.isfile(file_path):
                        subprocess.run(f'start "" "{file_path}"', shell=True)
                        return f"{os.path.basename(file_path)} opened"
                    else:
                        subprocess.run(f'explorer "{file_path}"', shell=True)
                        return f"{os.path.basename(file_path)} folder opened"
                else:
                    return f"'{filename}' not found"
            
            # Search for custom folder names with exact and fuzzy matching
            folder_name = None
            folder_patterns = [
                r'open\s+folder\s+(.+)',
                r'open\s+(.+)\s+folder',
                r'open\s+([^.]+)$'  # only match if no file extension
            ]
            for pat in folder_patterns:
                m = re.search(pat, query)
                if m:
                    folder_name = m.group(1).strip()
                    break

            if folder_name:
                folder_name = folder_name.lower()
                search_roots = [
                    os.path.join(os.path.expanduser("~"), "Desktop"),
                    os.path.join(os.path.expanduser("~"), "Documents"),
                    os.path.join(os.path.expanduser("~"), "Downloads"),
                    os.path.expanduser("~")
                ]

                exact_match = []
                fuzzy_match = []

                for root in search_roots:
                    for dirpath, dirnames, _ in os.walk(root):
                        for d in dirnames:
                            name = d.lower()
                            if name == folder_name:
                                exact_match.append(os.path.join(dirpath, d))
                            elif folder_name in name:
                                fuzzy_match.append(os.path.join(dirpath, d))

                if exact_match:
                    subprocess.run(f'explorer "{exact_match[0]}"', shell=True)
                    return f"Opened folder: {os.path.basename(exact_match[0])}"

                if fuzzy_match:
                    subprocess.run(f'explorer "{fuzzy_match[0]}"', shell=True)
                    return f"Opened folder: {os.path.basename(fuzzy_match[0])}"
                
                return f"Folder '{folder_name}' not found"
            
            # Default: open file explorer
            subprocess.run('explorer', shell=True)
            return "File Explorer opened"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _create_video(self):
        """Create AI video based on query"""
        try:
            # Extract prompt from query
            query = self._current_query.lower()
            
            # Remove command words to get the actual prompt
            for cmd in ['create video', 'generate video', 'make video', 'ai video']:
                if cmd in query:
                    prompt = query.replace(cmd, '').strip()
                    break
            else:
                prompt = query
            
            # Remove common words
            prompt = prompt.replace('of', '').replace('a', '').replace('an', '').strip()
            
            if not prompt:
                return "Please specify what video you want me to create"
            
            # Start video generation in background
            from engine.simple_video_gen import create_simple_video
            return create_simple_video(prompt)
            
        except Exception as e:
            return f"Video creation failed: {str(e)}"
    
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
            # Get current brightness and decrease by 10%
            get_cmd = 'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"'
            result = subprocess.run(get_cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0 and result.stdout.strip():
                current = int(result.stdout.strip())
                new_brightness = max(0, current - 10)

                set_cmd = f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_brightness})"'
                subprocess.run(set_cmd, shell=True)
                return f"Brightness decreased to {new_brightness}%"
            else:
                # Fallback to keyboard brightness down
                pyautogui.press('brightnessdown')
                return "Brightness decreased"
        except Exception as e:
            return f"Brightness control not supported on this system: {e}"


    def _schedule_event(self, event_text=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            if event_text:
                return voice_advanced_ai.calendar_schedule(event_text)
            return "Please specify an event to schedule"
        except Exception as e:
            return f"Scheduling failed: {str(e)}"
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
    
# Update your dual AI call to support PowerPoint creation

    def _ai_presentation(self, topic="", create_ppt=True):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            
            # Extract topic from current query if available
            if hasattr(self, '_current_query') and self._current_query and not topic:
                import re
                query = self._current_query.lower()
                
                # Extract topic from various patterns
                patterns = [
                    r'(?:make|create)\s+(?:slides|presentation|ppt)\s+(?:of|on|about)\s+(.+)',
                    r'(?:slides|presentation|ppt)\s+(?:of|on|about)\s+(.+)',
                    r'(?:make|create)\s+(.+?)\s+(?:slides|presentation|ppt)',
                    r'presentation\s+(.+)',
                    r'slides\s+(.+)'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, query)
                    if match:
                        topic = match.group(1).strip()
                        break
            
            if not topic:
                topic = "ai assistant"
                
            return voice_advanced_ai.ai_presentation_maker(topic, create_ppt)
        except Exception as e:
            return f"Error with AI presentation: {str(e)}"

# Usage examples:
# _ai_presentation("machine learning")           # Text outline only
# _ai_presentation("AI", create_ppt=True)        # Creates actual PowerPoint file
    
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

    def _check_new_features(self, query):
        """Check new features from external file"""
        try:
            from engine.new_features import get_new_feature_response
            result = get_new_feature_response(query)
            return result
        except:
            return None
    
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
                    self.corrected_files = {}  # Track corrected files with their content hash
                    self.processing_files = set()  # Track files currently being processed
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
                    # Check if file is already being processed
                    if event.src_path in self.processing_files:
                        print("Skipping - file already being processed")
                        return
                    
                    if event.src_path in self.last_check:
                        time_diff = current_time - self.last_check[event.src_path]
                        if time_diff < 2.0:  # Increased cooldown to prevent duplicates
                            print(f"Skipping - too soon ({time_diff:.1f}s)")
                            return
                    
                    print(f"Processing file: {event.src_path}")
                    self.last_check[event.src_path] = current_time
                    self.processing_files.add(event.src_path)
                    
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
                        
                        # Use AI to find all types of errors
                        if not error_msg:
                            print("Running AI analysis for all error types...")
                            error_msg = self.dual_ai._ai_code_analysis(code)
                            if error_msg:
                                print(f"🚨 AI detected error: {error_msg}")
                        
                        if not error_msg:
                            print("✅ No errors found")
                            return
                        
                        # Check if this file was recently corrected with same content
                        import hashlib
                        content_hash = hashlib.md5(code.encode()).hexdigest()
                        if event.src_path in self.corrected_files and self.corrected_files[event.src_path] == content_hash:
                            print("Skipping - file already corrected")
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
                    finally:
                        # Remove from processing set
                        self.processing_files.discard(event.src_path)
                
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
    
    def _ai_code_analysis(self, code):
        """Use AI to analyze code for all types of errors"""
        try:
            lines = code.split('\n')
            numbered_code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])
            
            prompt = f'''Check this Python code for CRITICAL errors only:\n{numbered_code}\n\nOnly report:\n- Undefined variables\n- Syntax errors\n- Missing imports that cause errors\n\nIgnore style suggestions, variable naming, and input validation.\n\nIf you find a CRITICAL error, respond with: "Line X: [error]"\nIf no critical errors, respond with: "OK"'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                result = response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                result = response.text.strip()
            
            # Check if AI found critical errors
            if 'line' in result.lower() and 'ok' not in result.lower():
                return result
            
            return None
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return None
    
    def _show_error_notification(self, file_path, error_message):
        import os
        import time
        
        title = f"Code Error in {os.path.basename(file_path)}"
        print(f"🚨 {title}: {error_message}")
        
        # Simple console notification to avoid crashes
        print(f"🚨 {title}: {error_message}")
        
        # Ask for correction
        if self._ask_for_correction(title, error_message):
            self._auto_correct_code(file_path, error_message)
        
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
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            print("Using AI to fix the code...")
            correction_prompt = f'''Fix this Python code error. Return ONLY the corrected code without explanations:\n\nOriginal code:\n{original_code}\n\nError: {error_message}\n\nCorrected code:'''
            
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
            
            # Clean AI response
            if corrected_code.startswith('```'):
                lines = corrected_code.split('\n')
                corrected_code = '\n'.join(lines[1:-1])
            
            # Create backup
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup_{timestamp}"
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            print(f"File created: {backup_path}")
            
            # Apply correction
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_code)
            
            # Mark file as corrected
            import hashlib
            content_hash = hashlib.md5(corrected_code.encode()).hexdigest()
            if hasattr(self, 'handler') and self.handler:
                self.handler.corrected_files[file_path] = content_hash
            
            print(f"✅ Code fixed in {os.path.basename(file_path)}")
            self._show_notification("🎉 Code Fixed!", f"Error corrected in {os.path.basename(file_path)}")
        
        except Exception as e:
            print(f"❌ Auto-correction failed: {e}")
            self._show_notification("Auto-Correction Failed", f"Could not fix: {str(e)}")
    
    def _old_auto_correct_code(self, file_path, error_message):
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
    
    # Mapping Functions
    def _open_maps(self):
        try:
            subprocess.Popen('start https://maps.google.com', shell=True)
            return "Google Maps opened"
        except:
            return "Failed to open maps"
    
    def _find_location(self, location=""):
        try:
            import urllib.parse
            if not location:
                location = "current location"
            encoded_location = urllib.parse.quote(location)
            url = f"https://maps.google.com/maps?q={encoded_location}"
            subprocess.Popen(f'start {url}', shell=True)
            return f"Searching for {location} on maps"
        except:
            return "Failed to search location"
    
    def _get_directions(self, destination=""):
        try:
            import urllib.parse
            if not destination:
                return "Please specify a destination"
            encoded_dest = urllib.parse.quote(destination)
            url = f"https://maps.google.com/maps/dir//{encoded_dest}"
            subprocess.Popen(f'start {url}', shell=True)
            return f"Getting directions to {destination}"
        except:
            return "Failed to get directions"
    
    def _nearby_places(self, place_type="restaurants"):
        try:
            import urllib.parse
            encoded_type = urllib.parse.quote(f"{place_type} near me")
            url = f"https://maps.google.com/maps/search/{encoded_type}"
            subprocess.Popen(f'start {url}', shell=True)
            return f"Finding nearby {place_type}"
        except:
            return "Failed to find nearby places"
    
    def _traffic_info(self):
        try:
            url = "https://maps.google.com/maps/@?layer=t"
            subprocess.Popen(f'start {url}', shell=True)
            return "Showing traffic information"
        except:
            return "Failed to show traffic info"
    
    def _map_satellite(self):
        try:
            url = "https://maps.google.com/maps/@?layer=s"
            subprocess.Popen(f'start {url}', shell=True)
            return "Switched to satellite view"
        except:
            return "Failed to switch to satellite view"
    
    def _map_terrain(self):
        try:
            url = "https://maps.google.com/maps/@?layer=p"
            subprocess.Popen(f'start {url}', shell=True)
            return "Switched to terrain view"
        except:
            return "Failed to switch to terrain view"
    
    def _save_location(self, location=""):
        try:
            if not location:
                return "Please specify a location to save"
            # Save to a simple text file
            with open('saved_locations.txt', 'a', encoding='utf-8') as f:
                f.write(f"{location}\n")
            return f"Location '{location}' saved"
        except:
            return "Failed to save location"
    
    def _my_location(self):
        try:
            url = "https://maps.google.com/maps/@?layer=c"
            subprocess.Popen(f'start {url}', shell=True)
            return "Showing your current location"
        except:
            return "Failed to show current location"

    def _dictate_to_file(self, query=""):
        """Voice-to-text dictation to file"""
        try:
            import speech_recognition as sr
            import re
            import os
            
            filename = "dictation.txt"
            file_match = re.search(r'to file\s+([^\s]+)', query.lower())
            if file_match:
                filename = file_match.group(1).strip()
                if not filename.endswith('.txt'):
                    filename += '.txt'
            
            mode = "append" if "append" in query.lower() else "write"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {filename}. Say 'stop dictation' to finish...")
                
                text_content = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        text = self._process_punctuation_commands(text)
                        text_content += text + " "
                        print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if text_content.strip():
                if mode == "append" and os.path.exists(filename):
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write("\n" + text_content.strip())
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text_content.strip())
                
                return f"📝 Dictation saved to {filename} ({len(text_content.split())} words)"
            else:
                return "No speech detected"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Dictation failed: {e}"

    def _dictate_to_document(self, query=""):
        """Advanced voice-to-text for formatted documents"""
        try:
            import speech_recognition as sr
            import re
            from datetime import datetime
            
            doc_type = "word"
            if "google docs" in query.lower():
                doc_type = "gdocs"
            elif "email" in query.lower():
                doc_type = "email"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {doc_type}. Say formatting commands like 'bold this', 'new paragraph'...")
                
                document_content = []
                current_text = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        if self._is_formatting_command(text):
                            formatted_text = self._process_formatting_command(text, current_text)
                            document_content.append(formatted_text)
                            current_text = ""
                        else:
                            text = self._process_punctuation_commands(text)
                            current_text += text + " "
                            print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if current_text.strip():
                document_content.append(current_text.strip())
            
            if document_content:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if doc_type == "email":
                    filename = f"email_draft_{timestamp}.txt"
                    content = self._format_as_email(document_content)
                elif doc_type == "gdocs":
                    filename = f"gdocs_draft_{timestamp}.txt"
                    content = self._format_as_document(document_content)
                else:
                    filename = f"document_{timestamp}.docx"
                    content = self._format_as_document(document_content)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                word_count = len(' '.join(document_content).split())
                return f"📄 Document saved to {filename} ({word_count} words)\nFormatting commands processed"
            else:
                return "No content dictated"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Document dictation failed: {e}"
    def _dictate_to_file(self, query=""):
        """Voice-to-text dictation to file"""
        try:
            import speech_recognition as sr
            import re
            import os
            
            filename = "dictation.txt"
            file_match = re.search(r'to file\s+([^\s]+)', query.lower())
            if file_match:
                filename = file_match.group(1).strip()
                if not filename.endswith('.txt'):
                    filename += '.txt'
            
            mode = "append" if "append" in query.lower() else "write"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {filename}. Say 'stop dictation' to finish...")
                
                text_content = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        text = self._process_punctuation_commands(text)
                        text_content += text + " "
                        print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if text_content.strip():
                if mode == "append" and os.path.exists(filename):
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write("\n" + text_content.strip())
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text_content.strip())
                
                return f"📝 Dictation saved to {filename} ({len(text_content.split())} words)"
            else:
                return "No speech detected"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Dictation failed: {e}"

    def _dictate_to_document(self, query=""):
        """Advanced voice-to-text for formatted documents"""
        try:
            import speech_recognition as sr
            import re
            from datetime import datetime
            
            doc_type = "word"
            if "google docs" in query.lower():
                doc_type = "gdocs"
            elif "email" in query.lower():
                doc_type = "email"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {doc_type}. Say formatting commands like 'bold this', 'new paragraph'...")
                
                document_content = []
                current_text = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        if self._is_formatting_command(text):
                            formatted_text = self._process_formatting_command(text, current_text)
                            document_content.append(formatted_text)
                            current_text = ""
                        else:
                            text = self._process_punctuation_commands(text)
                            current_text += text + " "
                            print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if current_text.strip():
                document_content.append(current_text.strip())
            
            if document_content:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if doc_type == "email":
                    filename = f"email_draft_{timestamp}.txt"
                    content = self._format_as_email(document_content)
                elif doc_type == "gdocs":
                    filename = f"gdocs_draft_{timestamp}.txt"
                    content = self._format_as_document(document_content)
                else:
                    filename = f"document_{timestamp}.docx"
                    content = self._format_as_document(document_content)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                word_count = len(' '.join(document_content).split())
                return f"📄 Document saved to {filename} ({word_count} words)\nFormatting commands processed"
            else:
                return "No content dictated"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Document dictation failed: {e}"

    def _process_punctuation_commands(self, text):
        """Process voice punctuation commands"""
        # More comprehensive punctuation mapping
        punctuation_map = {
            ' period': '.',
            ' comma': ',',
            ' question mark': '?',
            ' exclamation point': '!',
            ' exclamation mark': '!',
            ' colon': ':',
            ' semicolon': ';',
            ' new line': '\n',
            ' new paragraph': '\n\n',
            ' dot': '.',
            ' full stop': '.'
        }
    
        # Process punctuation commands (case insensitive)
        for command, punctuation in punctuation_map.items():
            text = text.replace(command, punctuation)
            text = text.replace(command.title(), punctuation)
            text = text.replace(command.upper(), punctuation)
    
        return text

    def _is_formatting_command(self, text):
        """Check if text contains formatting commands"""
        formatting_commands = [
            'bold this', 'italic this', 'underline this',
            'bullet point', 'numbered list', 'new paragraph',
            'heading', 'title', 'center this'
        ]
    
        return any(cmd in text.lower() for cmd in formatting_commands)

    def _process_formatting_command(self, command, text):
        """Process formatting commands and return formatted text"""
        command_lower = command.lower()
    
        if 'bold this' in command_lower:
            return f"**{text.strip()}**"
        elif 'italic this' in command_lower:
            return f"*{text.strip()}*"
        elif 'underline this' in command_lower:
            return f"_{text.strip()}_"
        elif 'bullet point' in command_lower:
            return f"• {text.strip()}"
        elif 'numbered list' in command_lower:
            return f"1. {text.strip()}"
        elif 'heading' in command_lower:
            return f"# {text.strip()}"
        elif 'title' in command_lower:
            return f"## {text.strip()}"
        elif 'center this' in command_lower:
            return f"<center>{text.strip()}</center>"
        else:
            return text

    def _format_as_email(self, content_list):
        """Format content as email"""
        email_content = "Subject: [Your Subject]\n\n"
        email_content += "Dear [Recipient],\n\n"
    
        for content in content_list:
            email_content += content + "\n\n"
    
        email_content += "Best regards,\n[Your Name]"
        return email_content

    def _format_as_document(self, content_list):
        """Format content as document"""
        document_content = ""
    
        for content in content_list:
            document_content += content + "\n\n"
    
        return document_content.strip()


    def _process_formatting_command(self, command, text):
        """Process formatting commands and return formatted text"""
        command_lower = command.lower()
    
        if 'bold this' in command_lower:
            return f"**{text.strip()}**"
        elif 'italic this' in command_lower:
            return f"*{text.strip()}*"
        elif 'underline this' in command_lower:
            return f"_{text.strip()}_"
        elif 'bullet point' in command_lower:
            return f"• {text.strip()}"
        elif 'numbered list' in command_lower:
            return f"1. {text.strip()}"
        elif 'heading' in command_lower:
            return f"# {text.strip()}"
        elif 'title' in command_lower:
            return f"## {text.strip()}"
        elif 'center this' in command_lower:
            return f"<center>{text.strip()}</center>"
        else:
            return text

    def _format_as_email(self, content_list):
        """Format content as email"""
        email_content = "Subject: [Your Subject]\n\n"
        email_content += "Dear [Recipient],\n\n"
    
        for content in content_list:
            email_content += content + "\n\n"
    
        email_content += "Best regards,\n[Your Name]"
        return email_content

    def _format_as_document(self, content_list):
        """Format content as document"""
        document_content = ""
    
        for content in content_list:
            document_content += content + "\n\n"
    
        return document_content.strip()

    def _simple_fallback_match(self, query):
        """Simple fallback matching for basic commands"""
        query_lower = query.lower()
        
        # Basic command mappings
        if 'open' in query_lower:
            if 'chrome' in query_lower:
                return 'chrome'
            elif 'notepad' in query_lower:
                return 'notepad'
            elif 'calculator' in query_lower:
                return 'calculator'
        
        if 'volume' in query_lower:
            if 'up' in query_lower:
                return 'volume_up'
            elif 'down' in query_lower:
                return 'volume_down'
        
        if 'brightness' in query_lower:
            if 'up' in query_lower:
                return 'brightness_up'
            elif 'down' in query_lower:
                return 'brightness_down'
        
        return None

    def _pause_dictation(self):
        """Pause dictation mode"""
        try:
            self.dictation_paused = True
            return "Dictation paused"
        except Exception as e:
            return f"Failed to pause dictation: {e}"
    
    def _resume_dictation(self):
        """Resume dictation mode"""
        try:
            self.dictation_paused = False
            return "Dictation resumed"
        except Exception as e:
            return f"Failed to resume dictation: {e}"
    def _start_dictation(self, query=""):
        """Start dictation mode - opens app and starts listening"""
        try:
            import speech_recognition as sr
            import pyautogui
            import time
            
            # Determine which app to open
            self.current_app = "notepad"  # default
            
            if "notepad" in query.lower():
                self.current_app = "notepad"
                subprocess.Popen('notepad', shell=True)
                time.sleep(2)
            elif "word" in query.lower():
                self.current_app = "word"
                subprocess.Popen('start winword', shell=True)
                time.sleep(3)  # Word takes longer to load
                # Create new document in Word
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.press('enter')   # Press enter after ctrl+n
            elif "chrome" in query.lower():
                self.current_app = "chrome"
                subprocess.Popen('start chrome', shell=True)
                time.sleep(2)
            elif "anywhere" in query.lower() or not query.strip():
                self.current_app = "anywhere"
                # Don't open any specific app, just start dictating
            else:
                # If no specific app mentioned, open notepad
                self.current_app = "notepad"
                subprocess.Popen('notepad', shell=True)
                time.sleep(2)
            
            # Start dictation
            return self._dictate_anywhere()
            
        except Exception as e:
            return f"Failed to start dictation: {e}"
    
    def _auto_save_file(self):
        """Auto-save the dictated file"""
        try:
            # Only save if we opened notepad or word
            if hasattr(self, 'current_app') and self.current_app in ['notepad', 'word']:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if self.current_app == 'word':
                    filename = f"dictation_{timestamp}"
                else:
                    filename = f"dictation_{timestamp}"
                
                # Press Ctrl+S to save
                pyautogui.hotkey('ctrl', 's')
                time.sleep(2)
                
                # Type filename and save
                pyautogui.typewrite(filename)
                time.sleep(1)
                pyautogui.press('enter')
                
                print(f"💾 File saved as {filename}")
        except Exception as e:
            print(f"Save error: {e}")
    
    def _stop_dictation(self):
        """Stop dictation mode"""
        try:
            self.dictation_active = False
            return "Dictation stopped"
        except Exception as e:
            return f"Failed to stop dictation: {e}"
    
    def _dictate_anywhere(self, query=""):
        """Universal dictation that works in any application"""
        try:
            import speech_recognition as sr
            import pyautogui
            import time
            
            r = sr.Recognizer()
            # Improve recognition settings
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.8
            r.phrase_threshold = 0.3
            
            self.dictation_active = True
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=2)
                print("🎤 Universal dictation started. Say 'stop dictation' to finish...")
                print("📝 Speaking will type directly into the active application")
                
                while self.dictation_active:
                    try:
                        # Adjust listening parameters for better recognition
                        audio = r.listen(source, timeout=3, phrase_time_limit=6)
                        text = r.recognize_google(audio, language='en-US', show_all=False)
                        
                        # Check for control commands
                        text_lower = text.lower()
                        if any(stop_phrase in text_lower for stop_phrase in ["stop dictation", "end dictation", "finish dictation", "stop writing", "stop typing"]):
                            self.dictation_active = False
                            print("🛑 Dictation stopped")
                            # Auto-save the file
                            self._auto_save_file()
                            break
                        # Automation features
                        elif "press enter" in text_lower or "new line" in text_lower:
                            pyautogui.press('enter')
                            print("↵ Enter pressed")
                            continue
                        elif "press tab" in text_lower:
                            pyautogui.press('tab')
                            print("⇥ Tab pressed")
                            continue
                        elif "press space" in text_lower:
                            pyautogui.press('space')
                            print("␣ Space pressed")
                            continue
                        elif "backspace" in text_lower or "delete back" in text_lower:
                            pyautogui.press('backspace')
                            print("⌫ Backspace pressed")
                            continue
                        elif "delete" in text_lower and "back" not in text_lower:
                            pyautogui.press('delete')
                            print("⌦ Delete pressed")
                            continue
                        elif any(pause_phrase in text_lower for pause_phrase in ["pause dictation", "pause typing"]):
                            if not hasattr(self, 'dictation_paused'):
                                self.dictation_paused = False
                            self.dictation_paused = True
                            print("⏸️ Dictation paused - say 'resume dictation' to continue")
                            continue
                        elif any(resume_phrase in text_lower for resume_phrase in ["resume dictation", "continue dictation"]):
                            if not hasattr(self, 'dictation_paused'):
                                self.dictation_paused = False
                            if self.dictation_paused:
                                self.dictation_paused = False
                                print("▶️ Dictation resumed")
                            continue
                        
                        # Skip typing if paused
                        if hasattr(self, 'dictation_paused') and self.dictation_paused:
                            continue
                        
                        # Clean up the text
                        text = text.strip()
                        if len(text) < 2:  # Skip very short utterances
                            continue
                            
                        # Process punctuation commands
                        text = self._process_punctuation_commands(text)
                        
                        # Type the text with proper spacing
                        if text:
                            pyautogui.typewrite(text + " ", interval=0.01)
                            print(f"📝 Typed: {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        # Don't print for every unrecognized audio to reduce noise
                        continue
                    except sr.RequestError as e:
                        print(f"Speech service error: {e}")
                        return f"Speech recognition error: {e}"
                    except Exception as e:
                        print(f"Typing error: {e}")
                        continue
            
            return "📝 Universal dictation completed"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Universal dictation failed: {e}"
        

    def _find_file(self):
        """Find files by name in specified directory"""
        try:
            query = self._current_query.lower()
            
            # Parse directory from query
            directory = self._get_directory(query)
            
            # Get search pattern
            pattern = simpledialog.askstring("Find File", "Enter filename or pattern to search for:")
            if not pattern:
                return "Search cancelled"
            
            found_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if pattern.lower() in file.lower():
                        found_files.append(os.path.join(root, file))
            
            if found_files:
                return f"Found {len(found_files)} files:\n" + "\n".join(found_files[:10])
            else:
                return f"No files found matching '{pattern}' in {directory}"
                
        except Exception as e:
            return f"Error finding files: {str(e)}"
    
    def _find_duplicates(self):
        """Find duplicate files in specified directory"""
        try:
            import hashlib
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            file_hashes = {}
            duplicates = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        
                        if file_hash in file_hashes:
                            duplicates.append((file_path, file_hashes[file_hash]))
                        else:
                            file_hashes[file_hash] = file_path
                    except:
                        continue
            
            if duplicates:
                result = f"Found {len(duplicates)} duplicate file pairs:\n"
                for dup in duplicates[:5]:
                    result += f"Duplicate: {dup[0]} = {dup[1]}\n"
                return result
            else:
                return f"No duplicate files found in {directory}"
                
        except Exception as e:
            return f"Error finding duplicates: {str(e)}"
    
    def _find_large_files(self):
        """Find large files in specified directory"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            large_files = []
            size_limit = 100 * 1024 * 1024  # 100MB
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        if size > size_limit:
                            large_files.append((file_path, size))
                    except:
                        continue
            
            if large_files:
                large_files.sort(key=lambda x: x[1], reverse=True)
                result = f"Found {len(large_files)} large files (>100MB):\n"
                for file_path, size in large_files[:10]:
                    size_mb = size / (1024 * 1024)
                    result += f"{file_path} - {size_mb:.1f}MB\n"
                return result
            else:
                return f"No large files found in {directory}"
                
        except Exception as e:
            return f"Error finding large files: {str(e)}"
    
    def _find_empty_folders(self):
        """Find empty folders in specified directory"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            empty_folders = []
            
            for root, dirs, files in os.walk(directory, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):
                            empty_folders.append(dir_path)
                    except:
                        continue
            
            if empty_folders:
                return f"Found {len(empty_folders)} empty folders:\n" + "\n".join(empty_folders[:10])
            else:
                return f"No empty folders found in {directory}"
                
        except Exception as e:
            return f"Error finding empty folders: {str(e)}"
    
    def _get_file_info(self):
        """Get detailed file information"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            file_name = simpledialog.askstring("File Info", "Enter filename:")
            if not file_name:
                return "Operation cancelled"
            
            file_path = os.path.join(directory, file_name)
            
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            import time
            stat = os.stat(file_path)
            
            info = f"File Information for {file_name}:\n"
            info += f"Path: {file_path}\n"
            info += f"Size: {stat.st_size} bytes ({stat.st_size / (1024*1024):.2f} MB)\n"
            info += f"Created: {time.ctime(stat.st_ctime)}\n"
            info += f"Modified: {time.ctime(stat.st_mtime)}\n"
            info += f"Accessed: {time.ctime(stat.st_atime)}\n"
            
            return info
            
        except Exception as e:
            return f"Error getting file info: {str(e)}"
    
    def _backup_folder(self):
        """Backup a folder in specified location"""
        try:
            import shutil
            from datetime import datetime
            
            query = self._current_query.lower()
            
            # Get folder to backup
            folder_path = simpledialog.askstring("Backup Folder", "Enter folder path to backup:")
            if not folder_path:
                return "Backup cancelled"
            
            # Handle relative paths and common names
            if not os.path.isabs(folder_path):
                folder_path = os.path.join(self._get_directory(query), folder_path)
            
            if not os.path.exists(folder_path):
                return f"Folder not found: {folder_path}"
            
            # Get backup location from query or use same directory
            backup_dir = self._get_directory(query) if 'in ' in query else os.path.dirname(folder_path)
            
            # Create backup with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.basename(folder_path)}_backup_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            shutil.copytree(folder_path, backup_path)
            return f"Folder backed up to: {backup_path}"
            
        except Exception as e:
            return f"Error backing up folder: {str(e)}"
        


    
    def _search_content(self):
        """Search inside files for content"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            search_term = simpledialog.askstring("Content Search", "Enter text to search for:")
            if not search_term:
                return "Search cancelled"
            
            results = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if file.lower().endswith(('.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml')):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if search_term.lower() in content.lower():
                                    results.append(file_path)
                        elif file.lower().endswith('.pdf'):
                            try:
                                import PyPDF2
                                with open(file_path, 'rb') as f:
                                    reader = PyPDF2.PdfReader(f)
                                    text = ''.join(page.extract_text() for page in reader.pages)
                                    if search_term.lower() in text.lower():
                                        results.append(file_path)
                            except:
                                pass
                    except:
                        continue
            
            if results:
                return f"Found '{search_term}' in {len(results)} files:\n" + "\n".join(results[:10])
            else:
                return f"No files found containing '{search_term}'"
                
        except Exception as e:
            return f"Error searching content: {str(e)}"
    
    def _find_similar_files(self):
        """Find files with similar content"""
        try:
            import difflib
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            file_contents = {}
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(('.txt', '.py', '.js', '.html', '.css', '.md')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                file_contents[file_path] = f.read()
                        except:
                            continue
            
            similar_pairs = []
            files = list(file_contents.keys())
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    similarity = difflib.SequenceMatcher(None, file_contents[file1], file_contents[file2]).ratio()
                    if similarity > 0.7:
                        similar_pairs.append((file1, file2, similarity))
            
            if similar_pairs:
                result = f"Found {len(similar_pairs)} similar file pairs:\n"
                for file1, file2, sim in similar_pairs[:5]:
                    result += f"{sim:.1%} similar: {os.path.basename(file1)} ↔ {os.path.basename(file2)}\n"
                return result
            else:
                return "No similar files found"
                
        except Exception as e:
            return f"Error finding similar files: {str(e)}"
    
    def _suggest_folder(self):
        """Suggest folder based on file content"""
        try:
            file_path = simpledialog.askstring("Smart Folder", "Enter file path to analyze:")
            if not file_path:
                return "Operation cancelled"
            
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            suggestions = []
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Extension-based suggestions
            ext_map = {
                '.py': 'Code/Python', '.js': 'Code/JavaScript', '.html': 'Web/HTML',
                '.pdf': 'Documents/PDFs', '.docx': 'Documents/Word', '.xlsx': 'Documents/Excel',
                '.jpg': 'Images/Photos', '.png': 'Images/Graphics', '.mp4': 'Media/Videos',
                '.mp3': 'Media/Audio', '.zip': 'Archives', '.exe': 'Programs'
            }
            
            if file_ext in ext_map:
                suggestions.append(ext_map[file_ext])
            
            # Content-based suggestions
            try:
                if file_ext in ['.txt', '.py', '.js', '.html']:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if 'import' in content or 'function' in content:
                            suggestions.append('Code/Scripts')
                        elif 'todo' in content or 'task' in content:
                            suggestions.append('Tasks/Notes')
                        elif 'project' in content:
                            suggestions.append('Projects')
            except:
                pass
            
            if suggestions:
                return f"Suggested folders for {os.path.basename(file_path)}:\n" + "\n".join(f"• {s}" for s in suggestions)
            else:
                return f"No specific folder suggestions for {os.path.basename(file_path)}"
                
        except Exception as e:
            return f"Error suggesting folder: {str(e)}"
    
    def _map_file_relationships(self):
        """Map relationships between files"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            relationships = {}
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relationships[file_path] = {'imports': [], 'references': [], 'similar_name': []}
                    
                    try:
                        if file.lower().endswith(('.py', '.js', '.html', '.css')):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                # Find imports/includes
                                for other_file in files:
                                    if other_file != file and other_file.replace('.', '') in content:
                                        relationships[file_path]['references'].append(other_file)
                                
                                # Find similar names
                                base_name = os.path.splitext(file)[0]
                                for other_file in files:
                                    if other_file != file and base_name in other_file:
                                        relationships[file_path]['similar_name'].append(other_file)
                    except:
                        continue
            
            result = "File Relationships:\n"
            for file_path, relations in relationships.items():
                if any(relations.values()):
                    result += f"\n{os.path.basename(file_path)}:\n"
                    if relations['references']:
                        result += f"  References: {', '.join(relations['references'])}\n"
                    if relations['similar_name']:
                        result += f"  Similar names: {', '.join(relations['similar_name'])}\n"
            
            return result if len(result) > 20 else "No file relationships found"
                
        except Exception as e:
            return f"Error mapping relationships: {str(e)}"
        



    def _search_google(self, query=""):
        """Search Google directly with query"""
        try:
            import webbrowser
            import urllib.parse
            
            # Extract search term from current query if available
            if hasattr(self, '_current_query') and self._current_query:
                import re
                search_query = self._current_query.lower()
                
                # Remove "search google" or "google search" from the query
                search_query = re.sub(r'(?:search\s+google|google\s+search)\s*', '', search_query)
                
                # If there's remaining text, use it as search term
                if search_query.strip():
                    query = search_query.strip()
            
            if not query:
                query = "python programming"  # Default search
            
            # Create Google search URL
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(search_url)
            
            return f"Searching Google for: {query}"
            
        except Exception as e:
            return f"Google search failed: {str(e)}"
        

    def _search_images(self, query=""):
        """Search Google Images"""
        try:
            import webbrowser
            import urllib.parse
            
            if hasattr(self, '_current_query') and self._current_query:
                import re
                search_query = self._current_query.lower()
                search_query = re.sub(r'(?:search\s+(?:for\s+)?images?|images?\s+search)\s*', '', search_query)
                if search_query.strip():
                    query = search_query.strip()
            
            if not query:
                query = "nature"
            
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
            webbrowser.open(search_url)
            return f"Searching images for: {query}"
            
        except Exception as e:
            return f"Image search failed: {str(e)}"

    def _search_gifs(self, query=""):
        """Search Google for GIFs"""
        try:
            import webbrowser
            import urllib.parse
            
            if hasattr(self, '_current_query') and self._current_query:
                import re
                search_query = self._current_query.lower()
                search_query = re.sub(r'(?:search\s+(?:for\s+)?gifs?|gifs?\s+search)\s*', '', search_query)
                if search_query.strip():
                    query = search_query.strip()
            
            if not query:
                query = "funny"
            
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}+gif&tbm=isch&tbs=itp:animated"
            webbrowser.open(search_url)
            return f"Searching GIFs for: {query}"
            
        except Exception as e:
            return f"GIF search failed: {str(e)}"
        

    def _copy_webpage_link(self):
        """Copy current webpage URL to clipboard"""
        try:
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.press('escape')
            return "Webpage link copied to clipboard"
        except Exception as e:
            return f"Failed to copy link: {str(e)}"

    def _translate_webpage(self):
        """Translate current webpage using Google Translate"""
        try:
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)
            
            import pyperclip
            current_url = pyperclip.paste()
            
            if current_url and current_url.startswith('http'):
                import webbrowser
                import urllib.parse
                translate_url = f"https://translate.google.com/translate?sl=auto&tl=en&u={urllib.parse.quote(current_url)}"
                webbrowser.open(translate_url)
                return "Opening webpage translation"
            else:
                return "No valid webpage URL found"
                
        except Exception as e:
            return f"Translation failed: {str(e)}"


    def _check_website_status(self):
        """Check if a website is up or down"""
        try:
            import re
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                # Extract website from query
                match = re.search(r'(?:check|status|up)\s+(?:website\s+)?([^\s]+)', query)
                if match:
                    website = match.group(1)
                    if not website.startswith('http'):
                        website = f"https://{website}"
                    
                    response = requests.get(website, timeout=5)
                    if response.status_code == 200:
                        return f"Website {website} is UP (Status: {response.status_code})"
                    else:
                        return f"Website {website} returned status: {response.status_code}"
                else:
                    return "Please specify a website to check"
            return "Please specify a website to check"
        except Exception as e:
            return f"Website appears to be DOWN or unreachable: {str(e)}"

    def _play_radio(self):
        """Play online radio stations"""
        try:
            import webbrowser
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                if 'bbc' in query:
                    webbrowser.open("https://www.bbc.co.uk/sounds/play/live:bbc_radio_one")
                elif 'npr' in query:
                    webbrowser.open("https://www.npr.org/player/live/500005/")
                elif 'classical' in query:
                    webbrowser.open("https://www.classicfm.com/radio/live/")
                else:
                    webbrowser.open("https://radio.garden/")
            else:
                webbrowser.open("https://radio.garden/")
            return "Opening online radio"
        except Exception as e:
            return f"Radio playback failed: {str(e)}"

    def _play_podcast(self):
        """Play online podcasts"""
        try:
            import webbrowser
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                if 'spotify' in query:
                    webbrowser.open("https://open.spotify.com/genre/podcasts-web")
                elif 'apple' in query:
                    webbrowser.open("https://podcasts.apple.com/")
                else:
                    webbrowser.open("https://www.google.com/podcasts")
            else:
                webbrowser.open("https://www.google.com/podcasts")
            return "Opening podcast platform"
        except Exception as e:
            return f"Podcast playback failed: {str(e)}"

    def _get_weekday(self):
        try:
            return datetime.now().strftime('%A')
        except:
            return "Could not get weekday"
    
    def _get_traffic(self, origin="current location", destination="office"):
        try:
            import webbrowser
            import urllib.parse
            
            # Extract locations from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                if 'from' in query and 'to' in query:
                    parts = query.split('from')[1].split('to')
                    if len(parts) == 2:
                        origin = parts[0].strip()
                        destination = parts[1].strip()
                elif 'traffic' in query and ('to' in query or 'from' in query):
                    # Handle "traffic to location" or "traffic from location"
                    if 'to' in query:
                        destination = query.split('to')[1].strip()
                    elif 'from' in query:
                        origin = query.split('from')[1].strip()
            
            # Open Google Maps with traffic layer
            if origin != "current location" and destination != "office":
                # Specific route
                maps_url = f"https://www.google.com/maps/dir/{urllib.parse.quote(origin)}/{urllib.parse.quote(destination)}/@?layer=t"
            elif destination != "office":
                # To specific destination
                maps_url = f"https://www.google.com/maps/dir//{urllib.parse.quote(destination)}/@?layer=t"
            else:
                # General traffic view
                maps_url = "https://www.google.com/maps/@?layer=t"
            
            webbrowser.open(maps_url)
            
            # Return informative message
            if origin != "current location" and destination != "office":
                return f"Opening traffic information from {origin} to {destination} in Google Maps"
            elif destination != "office":
                return f"Opening traffic information to {destination} in Google Maps"
            else:
                return "Opening Google Maps with live traffic information"
                
        except Exception as e:
            return f"Could not get traffic information: {str(e)}"
    
    def _get_holidays(self, country="IN"):
        try:
            year = datetime.now().year
            url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
            response = requests.get(url, timeout=5)
            
            # Handle 204 No Content or other non-200 responses
            if response.status_code == 204 or response.status_code != 200:
                return self._get_simple_holidays()
            
            # Check if response has content
            if not response.text.strip():
                return self._get_simple_holidays()
            
            # Try to parse JSON
            try:
                holidays = response.json()
            except json.JSONDecodeError:
                return self._get_simple_holidays()
            
            if not holidays or not isinstance(holidays, list):
                return self._get_simple_holidays()
            
            today = datetime.now().strftime("%Y-%m-%d")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            for holiday in holidays:
                if holiday.get('date') == today:
                    return f"Today is {holiday.get('localName', 'a holiday')}, a public holiday in {country}."
                elif holiday.get('date') == tomorrow:
                    return f"Tomorrow is {holiday.get('localName', 'a holiday')}, a public holiday in {country}."
            
            # Find next upcoming holiday
            upcoming = None
            for holiday in holidays:
                if holiday.get('date'):
                    try:
                        holiday_date = datetime.strptime(holiday['date'], "%Y-%m-%d")
                        if holiday_date > datetime.now():
                            upcoming = holiday
                            break
                    except ValueError:
                        continue
            
            if upcoming:
                try:
                    days_until = (datetime.strptime(upcoming['date'], "%Y-%m-%d") - datetime.now()).days
                    return f"Next holiday: {upcoming.get('localName', 'Holiday')} in {days_until} days ({upcoming['date']})."
                except ValueError:
                    return "Found upcoming holidays but couldn't calculate dates"
            
            return "No public holidays today or tomorrow."
        except requests.RequestException:
            return self._get_simple_holidays()
        except Exception as e:
            return self._get_simple_holidays()
    
    def _get_simple_holidays(self):
        """Fallback method for when API fails"""
        try:
            today = datetime.now()
            month = today.month
            day = today.day
            year = today.year
            
            # Common holidays with dates
            holidays = {
                (1, 1): "New Year's Day",
                (1, 26): "Republic Day (India)",
                (3, 8): "Holi (approximate)",
                (4, 14): "Baisakhi",
                (8, 15): "Independence Day (India)",
                (10, 2): "Gandhi Jayanti",
                (10, 31): "Halloween",
                (11, 14): "Children's Day (India)",
                (12, 25): "Christmas Day",
                (12, 31): "New Year's Eve"
            }
            
            # Check today
            if (month, day) in holidays:
                return f"Today is {holidays[(month, day)]}"
            
            # Check tomorrow
            tomorrow = today + timedelta(days=1)
            if (tomorrow.month, tomorrow.day) in holidays:
                return f"Tomorrow is {holidays[(tomorrow.month, tomorrow.day)]}"
            
            # Find next holiday
            for i in range(1, 365):
                future_date = today + timedelta(days=i)
                if (future_date.month, future_date.day) in holidays:
                    return f"Next major holiday: {holidays[(future_date.month, future_date.day)]} in {i} days ({future_date.strftime('%B %d')})"
            
            return "No major public holidays found in the next year"
        except Exception:
            return "Could not check holidays"
    
    def _get_covid_stats(self, country="India"):
        try:
            url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                return f"COVID API returned status code: {response.status_code}"
            
            if not response.text.strip():
                return "COVID API returned empty response"
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                return "COVID API returned invalid data format"
            
            new_cases = data.get('todayCases', 0)
            deaths = data.get('todayDeaths', 0)
            recovered = data.get('todayRecovered', 0)
            total_cases = data.get('cases', 0)
            
            return f"COVID-19 update for {country}: {new_cases:,} new cases, {deaths:,} deaths, and {recovered:,} recoveries today. Total cases: {total_cases:,}."
        except requests.RequestException:
            return "Could not connect to COVID-19 statistics service"
        except Exception as e:
            return f"Could not get COVID-19 statistics: {str(e)}"
        


    
    def _extract_product_name(self, query: str, site: str):
        """
        Extracts product name from query like 'track price of iPhone 15 on flipkart'
        """
        query = query.lower()
        print(f"DEBUG: Extracting from query: '{query}' for site: '{site}'")
        
        # Pattern 1: "track price of <product> on site"
        pattern1 = rf"track\s+price\s+of\s+(.+?)\s+on\s+{site}"
        match = re.search(pattern1, query)
        if match:
            result = match.group(1).strip()
            print(f"DEBUG: Pattern 1 matched: '{result}'")
            return result
        
        # Pattern 2: "track <product> on site"
        pattern2 = rf"track\s+(.+?)\s+on\s+{site}"
        match = re.search(pattern2, query)
        if match:
            result = match.group(1).strip()
            print(f"DEBUG: Pattern 2 matched: '{result}'")
            return result
        
        print(f"DEBUG: No pattern matched")
        return None

    # ===== PRODUCT PRICE TRACKING =====#
    def _track_amazon_price(self, product_name=""):
        try:
            if not product_name and hasattr(self, '_current_query'):
                product_name = self._extract_product_name(self._current_query, "amazon")
            
            if not product_name:
                product_name = "laptop"
            
            search_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
            subprocess.Popen(f'start chrome "{search_url}"', shell=True)
            return f"Opened Amazon price tracking for: {product_name}"
        except Exception as e:
            return f"Amazon price tracking failed: {str(e)}"

    def _track_flipkart_price(self, product_name=""):
        try:
            if not product_name and hasattr(self, '_current_query'):
                print(f"DEBUG: Current query: {self._current_query}")
                product_name = self._extract_product_name(self._current_query, "flipkart")
                print(f"DEBUG: Extracted product name: '{product_name}'")

            if not product_name:
                product_name = "smartphone"

            search_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
            subprocess.Popen(f'start chrome "{search_url}"', shell=True)
            return f"Opened Flipkart price tracking for: {product_name}"
        except Exception as e:
            return f"Flipkart price tracking failed: {str(e)}"
    
    def _check_product_price(self, product_name=""):
        try:
            if not product_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:check|price).*?(?:of|for)\s+(.+)', query)
                if match:
                    product_name = match.group(1).strip()
            
            if not product_name:
                return "Please specify a product to check price"
            
            # Open both Amazon and Flipkart for price comparison
            import urllib.parse
            amazon_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
            flipkart_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
            
            subprocess.Popen(f'start chrome "{amazon_url}"', shell=True)
            time.sleep(2)
            subprocess.Popen(f'start chrome "{flipkart_url}"', shell=True)
            
            return f"Opened price comparison for: {product_name} on Amazon and Flipkart"
        except Exception as e:
            return f"Price check failed: {str(e)}"
    
    # ===== TRAVEL SEARCH =====
    def _search_flights(self, route=""):
        try:
            if not route and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract route from query
                match = re.search(r'(?:flight|flights).*?(?:from|to)\s+(.+)', query)
                if match:
                    route = match.group(1).strip()
                else:
                    match = re.search(r'search.*?flights?\s+(.+)', query)
                    if match:
                        route = match.group(1).strip()
            
            if not route:
                route = "Delhi to Mumbai"
            
            # Open multiple flight booking sites
            flight_sites = [
                "https://www.makemytrip.com/flight/search",
                "https://www.goibibo.com/flights/",
                "https://www.cleartrip.com/flights"
            ]
            
            for site in flight_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Opened flight search for: {route}"
        except Exception as e:
            return f"Flight search failed: {str(e)}"
    
    def _search_hotels(self, location=""):
        try:
            if not location and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract location from query
                match = re.search(r'(?:hotel|hotels).*?(?:in|at)\s+(.+)', query)
                if match:
                    location = match.group(1).strip()
                else:
                    match = re.search(r'search.*?hotels?\s+(.+)', query)
                    if match:
                        location = match.group(1).strip()
            
            if not location:
                location = "Goa"
            
            # Open multiple hotel booking sites
            hotel_sites = [
                f"https://www.booking.com/searchresults.html?ss={location}",
                f"https://www.makemytrip.com/hotels/{location.lower().replace(' ', '-')}-hotels.html",
                f"https://www.oyo.com/search/?location={location}"
            ]
            
            for site in hotel_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Opened hotel search for: {location}"
        except Exception as e:
            return f"Hotel search failed: {str(e)}"
    
    # ===== STREAMING AVAILABILITY =====
    def _find_movie_streaming(self, movie_name=""):
        try:
            if not movie_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract movie name from query
                match = re.search(r'(?:movie|film).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    movie_name = match.group(1).strip()
                else:
                    match = re.search(r'(?:find|search).*?movie\s+(.+)', query)
                    if match:
                        movie_name = match.group(1).strip()
            
            if not movie_name:
                return "Please specify a movie name"
            
            # Open streaming platforms and search engines
            import urllib.parse
            search_query = f"{movie_name} streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={urllib.parse.quote(movie_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for movie: {movie_name}"
        except Exception as e:
            return f"Movie streaming search failed: {str(e)}"
    
    def _find_show_streaming(self, show_name=""):
        try:
            if not show_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract show name from query
                match = re.search(r'(?:show|series).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    show_name = match.group(1).strip()
                else:
                    match = re.search(r'(?:find|search).*?show\s+(.+)', query)
                    if match:
                        show_name = match.group(1).strip()
            
            if not show_name:
                return "Please specify a show name"
            
            # Open streaming platforms and search engines
            import urllib.parse
            search_query = f"{show_name} TV show streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(show_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(show_name)}",
                f"https://www.hotstar.com/in/search?q={urllib.parse.quote(show_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for show: {show_name}"
        except Exception as e:
            return f"Show streaming search failed: {str(e)}"
    
    def _where_to_watch(self, content_name=""):
        try:
            if not content_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract content name from query
                match = re.search(r'where.*?watch\s+(.+)', query)
                if match:
                    content_name = match.group(1).strip()
            
            if not content_name:
                return "Please specify what you want to watch"
            
            # Open JustWatch - the best platform for finding streaming availability
            import urllib.parse
            justwatch_url = f"https://www.justwatch.com/in/search?q={urllib.parse.quote(content_name)}"
            google_search = f"https://www.google.com/search?q={urllib.parse.quote(content_name + ' where to watch streaming')}"
            
            subprocess.Popen(f'start chrome "{justwatch_url}"', shell=True)
            time.sleep(2)
            subprocess.Popen(f'start chrome "{google_search}"', shell=True)
            
            return f"Finding where to watch: {content_name}"
        except Exception as e:
            return f"Streaming search failed: {str(e)}"
    
    def _streaming_availability(self, content_name=""):
        try:
            return self._where_to_watch(content_name)
        except Exception as e:
            return f"Streaming availability check failed: {str(e)}"
    
    def _get_weekday(self):
        try:
            return datetime.now().strftime('%A')
        except:
            return "Could not get weekday"
    
    def _get_traffic(self):
        try:
            subprocess.Popen('start https://maps.google.com/maps?layer=t', shell=True)
            return "Traffic information opened"
        except:
            return "Could not get traffic info"
    
    def _get_holidays(self):
        try:
            subprocess.Popen('start https://www.google.com/search?q=public+holidays+today+india', shell=True)
            return "Holiday information opened"
        except:
            return "Could not get holiday info"
    
    def _get_covid_stats(self):
        try:
            subprocess.Popen('start https://www.google.com/search?q=covid+cases+india+today', shell=True)
            return "COVID-19 statistics opened"
        except:
            return "Could not get COVID stats"
    
   
    
    # Advanced Flight/Hotel Search with API Integration
    def _search_flights(self, route=""):
        try:
            import requests, re, datetime
            
            if not route and hasattr(self, '_current_query'):
                query = self._current_query.lower()
                match = re.search(r'(?:flight|flights).*?(?:from|to)\s+(.+)', query)
                if match:
                    route = match.group(1).strip()
            
            if not route:
                route = "Delhi to Mumbai"
            
            # City code mapping
            city_map = {"bengaluru": "BLR", "delhi": "DEL", "mumbai": "BOM", "chennai": "MAA", "goa": "GOI"}
            from_city = next((city_map[k] for k in city_map if k in route.lower()), "DEL")
            to_city = next((city_map[k] for k in city_map if k in route.lower().split("to")[-1]), "BOM")
            
            # Open multiple flight booking sites
            flight_sites = [
                "https://www.makemytrip.com/flights/",
                "https://www.goibibo.com/flights/",
                "https://www.easemytrip.com/flights.html"
            ]
            
            for site in flight_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Flight search opened for: {route}"
        except Exception as e:
            return f"Flight search failed: {str(e)}"
    
    def _search_hotels(self, location=""):
        try:
            if not location and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:hotel|hotels).*?(?:in|at)\s+(.+)', query)
                if match:
                    location = match.group(1).strip()
            
            if not location:
                location = "Goa"
            
            # Open multiple hotel booking sites
            hotel_sites = [
                f"https://www.booking.com/searchresults.html?ss={location}",
                f"https://www.makemytrip.com/hotels/{location.lower().replace(' ', '-')}-hotels.html",
                f"https://www.oyo.com/search/?location={location}"
            ]
            
            for site in hotel_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Hotel search opened for: {location}"
        except Exception as e:
            return f"Hotel search failed: {str(e)}"
    
    # Advanced Movie/Show Streaming Search with TMDb API
    def _find_movie_streaming(self, movie_name=""):
        try:
            import requests
            
            if not movie_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:movie|film).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    movie_name = match.group(1).strip()
            
            if not movie_name:
                return "Please specify a movie name"
            
            # Use JustWatch and Google for streaming availability
            import urllib.parse
            search_query = f"{movie_name} streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={urllib.parse.quote(movie_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for movie: {movie_name}"
        except Exception as e:
            return f"Movie streaming search failed: {str(e)}"
    
    def _find_show_streaming(self, show_name=""):
        try:
            if not show_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:show|series).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    show_name = match.group(1).strip()
            
            if not show_name:
                return "Please specify a show name"
            
            # Open streaming platforms and search engines
            import urllib.parse
            search_query = f"{show_name} TV show streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(show_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(show_name)}",
                f"https://www.hotstar.com/in/search?q={urllib.parse.quote(show_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for show: {show_name}"
        except Exception as e:
            return f"Show streaming search failed: {str(e)}"
    
    def _where_to_watch(self, content_name=""):
        try:
            if not content_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'where.*?watch\s+(.+)', query)
                if match:
                    content_name = match.group(1).strip()
            
            if not content_name:
                return "Please specify what you want to watch"
            
            # Open JustWatch - the best platform for finding streaming availability
            import urllib.parse
            justwatch_url = f"https://www.justwatch.com/in/search?q={urllib.parse.quote(content_name)}"
            google_search = f"https://www.google.com/search?q={urllib.parse.quote(content_name + ' where to watch streaming')}"
            
            subprocess.Popen(f'start chrome "{justwatch_url}"', shell=True)
            time.sleep(2)
            subprocess.Popen(f'start chrome "{google_search}"', shell=True)
            
            return f"Finding where to watch: {content_name}"
        except Exception as e:
            return f"Streaming search failed: {str(e)}"
    
    def _streaming_availability(self, content_name=""):
        try:
            return self._where_to_watch(content_name)
        except Exception as e:
            return f"Streaming availability check failed: {str(e)}"



    # DEBUG Price Tracking Functions
    def _track_amazon_price_debug(self):
        try:
            print("DEBUG: Amazon price tracking function called")
            query = getattr(self, '_current_query', 'No query stored')
            print(f"DEBUG: Current query: {query}")
            
            # Extract product name from query
            import re
            product_match = re.search(r'track price.*?(?:of|for)\s+(.+?)\s+(?:on|in|from)\s+amazon', query.lower())
            if product_match:
                product_name = product_match.group(1).strip()
                print(f"DEBUG: Extracted product name: {product_name}")
                import urllib.parse
                search_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
                subprocess.Popen(['start', search_url], shell=True)
                return f"DEBUG: Amazon search opened for: {product_name}"
            else:
                subprocess.Popen('start https://www.amazon.in', shell=True)
                return "DEBUG: Amazon opened (no product extracted)"
        except Exception as e:
            return f"DEBUG: Amazon price tracking failed - {str(e)}"
    
    def _track_flipkart_price_debug(self):
        try:
            print("DEBUG: Flipkart price tracking function called")
            query = getattr(self, '_current_query', 'No query stored')
            print(f"DEBUG: Current query: {query}")
            
            # Extract product name from query
            import re
            product_match = re.search(r'track price.*?(?:of|for)\s+(.+?)\s+(?:on|in|from)\s+flipkart', query.lower())
            if product_match:
                product_name = product_match.group(1).strip()
                print(f"DEBUG: Extracted product name: {product_name}")
                import urllib.parse
                search_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
                subprocess.Popen(['start', search_url], shell=True)
                return f"DEBUG: Flipkart search opened for: {product_name}"
            else:
                subprocess.Popen('start https://www.flipkart.com', shell=True)
                return "DEBUG: Flipkart opened (no product extracted)"
        except Exception as e:
            return f"DEBUG: Flipkart price tracking failed - {str(e)}"
    
    def _check_product_price_debug(self):
        try:
            print("DEBUG: Product price comparison function called")
            query = getattr(self, '_current_query', 'No query stored')
            print(f"DEBUG: Current query: {query}")
            
            # Extract product name from query
            import re
            product_match = re.search(r'(?:track|check)\s+price.*?(?:of|for)\s+(.+)', query.lower())
            if product_match:
                product_name = product_match.group(1).strip()
                print(f"DEBUG: Extracted product name: {product_name}")
                import urllib.parse
                # Open multiple price comparison sites
                sites = [
                    f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}",
                    f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}",
                    f"https://www.google.com/search?q={urllib.parse.quote(product_name + ' price comparison')}"
                ]
                for site in sites:
                    subprocess.Popen(['start', site], shell=True)
                    time.sleep(1)
                return f"DEBUG: Price comparison opened for: {product_name}"
            else:
                subprocess.Popen('start https://www.pricehistory.in', shell=True)
                return "DEBUG: Price comparison opened (no product extracted)"
        except Exception as e:
            return f"DEBUG: Product price comparison failed - {str(e)}"
        

    # Timer & Stopwatch Features
    def __init_timer_vars(self):
        if not hasattr(self, 'stopwatch_start'):
            self.stopwatch_start = None
            self.elapsed_time = 0
            self.running = False
    
    def _countdown_timer(self):
        try:
            self.__init_timer_vars()
            import threading, re
            query = getattr(self, '_current_query', '')
            
            # Extract duration from query
            duration = 0
            words = query.lower().split()
            for i, word in enumerate(words):
                if word.isdigit():
                    duration = int(word)
                    if i+1 < len(words) and 'minute' in words[i+1]:
                        duration *= 60
                    break
            
            if duration > 0:
                def countdown():
                    seconds = duration
                    while seconds > 0:
                        mins, secs = divmod(seconds, 60)
                        print(f"\r⏳ Time left: {mins:02d}:{secs:02d}", end="")
                        time.sleep(1)
                        seconds -= 1
                    print("\n✅ Time's up!")
                    try:
                        from engine.command import speak
                        speak("Time's up!")
                    except:
                        pass
                
                threading.Thread(target=countdown, daemon=True).start()
                return f"Timer started for {duration} seconds"
            return "Please specify a valid duration"
        except Exception as e:
            return f"Timer error: {str(e)}"
    
    def _start_stopwatch(self):
        try:
            self.__init_timer_vars()
            if not self.running:
                self.stopwatch_start = time.time()
                self.running = True
                return "⏱️ Stopwatch started"
            return "Stopwatch already running"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    def _stop_stopwatch(self):
        try:
            self.__init_timer_vars()
            if self.running:
                self.elapsed_time += time.time() - self.stopwatch_start
                self.running = False
                return f"⏹️ Stopwatch stopped. Elapsed: {self.elapsed_time:.2f} seconds"
            return "Stopwatch not running"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    def _reset_stopwatch(self):
        try:
            self.__init_timer_vars()
            self.elapsed_time = 0
            self.stopwatch_start = None
            self.running = False
            return "🔁 Stopwatch reset"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    def _show_elapsed(self):
        try:
            self.__init_timer_vars()
            if self.running:
                current = self.elapsed_time + (time.time() - self.stopwatch_start)
            else:
                current = self.elapsed_time
            return f"⏳ Elapsed time: {current:.2f} seconds"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    # Mini Games Feature
    def _open_mini_game(self):
        try:
            query = getattr(self, '_current_query', '').lower()
            
            mini_games = {
                "chess": "https://www.chess.com/play/computer",
                "snake": "https://playsnake.org/",
                "flappy bird": "https://flappybird.io/",
                "car": "https://simmer.io/@gqcar/game-car-driving",
                "tetris": "https://tetris.com/play-tetris",
                "2048": "https://play2048.co/",
                "dino": "https://chromedino.com/",
                "pac man": "https://pacman.live/",
                "mario": "https://supermario-game.com/",
                "solitaire": "https://solitaired.com/",
                "sudoku": "https://sudoku.com/",
                "crossword": "https://crosswordpuzzles.com/",
                "bubble shooter": "https://bubble-shooter.co/",
                "candy crush": "https://king.com/game/candycrushsaga",
                "angry birds": "https://angrybirds.com/",
                "pool": "https://www.crazygames.com/game/8-ball-pool",
                "racing": "https://www.crazygames.com/game/madalin-stunt-cars-2",
                "puzzle": "https://www.jigsawplanet.com/",
                "word": "https://wordscapes.com/"
            }
            
            # Check for specific game in query
            for name, url in mini_games.items():
                if name in query:
                    subprocess.Popen(['start', url], shell=True)
                    return f"🎮 Opening {name} game"
            
            # Open default games site
            subprocess.Popen(['start', 'https://crazygames.com'], shell=True)
            return "🎯 Opening games collection"
        except Exception as e:
            return f"Game launch error: {str(e)}"



               # Smart Clipboard Assistant Methods
    def _clipboard_assistant(self):
        """Smart clipboard assistant that analyzes clipboard content"""
        try:
            import pyperclip
            import re
            
            clipboard_text = pyperclip.paste()
            if not clipboard_text or len(clipboard_text.strip()) < 3:
                return "Clipboard is empty or too short to analyze"
            
            # Analyze clipboard content using AI
            return self._analyze_clipboard_content(clipboard_text)
        except Exception as e:
            return f"Clipboard assistant error: {str(e)}"
    
    def _start_clipboard_assistant(self):
        """Start monitoring clipboard for context-aware help"""
        try:
            import threading
            import time
            import pyperclip
            
            if hasattr(self, 'clipboard_monitor_active') and self.clipboard_monitor_active:
                return "Clipboard assistant already running"
            
            self.clipboard_monitor_active = True
            self.last_clipboard = ""
            
            def monitor_clipboard():
                while self.clipboard_monitor_active:
                    try:
                        current_clipboard = pyperclip.paste()
                        if current_clipboard != self.last_clipboard and current_clipboard.strip():
                            self.last_clipboard = current_clipboard
                            suggestion = self._analyze_clipboard_content(current_clipboard)
                            if suggestion:
                                print(f"📋 Clipboard Assistant: {suggestion}")
                        time.sleep(2)
                    except:
                        time.sleep(2)
            
            threading.Thread(target=monitor_clipboard, daemon=True).start()
            return "Clipboard assistant started - monitoring clipboard for smart suggestions"
        except Exception as e:
            return f"Failed to start clipboard assistant: {str(e)}"
    
    def _stop_clipboard_assistant(self):
        """Stop clipboard monitoring"""
        try:
            self.clipboard_monitor_active = False
            return "Clipboard assistant stopped"
        except Exception as e:
            return f"Error stopping clipboard assistant: {str(e)}"
    
    def _analyze_clipboard_content(self, text):
        """Analyze clipboard content and provide context-aware suggestions"""
        try:
            import re
            
            text = text.strip()
            
            # Phone number detection
            if re.match(r'^[+]?[\d\s\-\(\)]{10,15}$', text):
                return "📞 Phone number detected! Want me to save this contact or make a call?"
            
            # Email detection
            if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', text):
                return "📧 Email address detected! Want me to compose an email or save this contact?"
            
            # URL detection
            if re.match(r'https?://[\w\.-]+', text):
                return "🔗 URL detected! Want me to open this link or bookmark it?"
            
            # Long text (paragraph)
            if len(text) > 100 and '.' in text:
                return "📄 Long text detected! Shall I summarize this or save it to a document?"
            
            # Code detection
            if any(keyword in text for keyword in ['def ', 'function', 'class ', 'import ', 'const ', 'var ']):
                return "💻 Code detected! Want me to format it, review it, or save to a file?"
            
            # Address detection
            if any(word in text.lower() for word in ['street', 'avenue', 'road', 'city', 'zip']):
                return "📍 Address detected! Want me to find directions or save this location?"
            
            # Date/time detection
            if re.search(r'\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\d{1,2}:\d{2}', text):
                return "📅 Date/time detected! Want me to create a calendar event or set a reminder?"
            
            # Password-like text
            if len(text) > 8 and re.search(r'[A-Z]', text) and re.search(r'[0-9]', text) and re.search(r'[!@#$%^&*]', text):
                return "🔐 Strong password detected! Want me to save this securely?"
            
            # Shopping list
            if '\n' in text and len(text.split('\n')) > 3:
                return "📝 List detected! Want me to organize this or create a task list?"
            
            # Default for other text
            if len(text) > 20:
                return "📋 Text copied! Want me to translate, search, or save this?"
            
            return None
        except Exception as e:
            return None
    


    
    def _create_image(self):
        """Create image using AI"""
        try:
            query = getattr(self, '_current_query', '')
            prompt = query.replace('create image', '').replace('generate image', '').replace('make image', '').strip()
            
            if not prompt:
                return "Please specify what image to create (e.g., 'create image of a sunset')"
            
            from engine.simple_image_gen import create_simple_image
            return create_simple_image(prompt)
        except Exception as e:
            return f"Image creation error: {str(e)}"
    
    def _explain_capabilities(self):
        """Explain what Jarvis can do"""
        return "I can control your computer (open apps, manage files, system controls), help with productivity (alarms, reminders, clipboard assistant), browse the web (YouTube, search, websites), create AI images, and answer questions using AI. I support voice commands for hands-free operation and can adapt to your preferences. Just ask me to open something, control media, set alarms, create images, or help with tasks!"
    
    def _set_alarm(self):
        """Set alarm with voice notification"""
        try:
            import threading
            import time
            import re
            import json
            from datetime import datetime, timedelta
            
            query = getattr(self, '_current_query', '')
            
            # Extract time from query
            time_match = re.search(r'(\d{1,2}):?(\d{2})\s*(am|pm)?', query.lower())
            if not time_match:
                time_match = re.search(r'(\d{1,2})\s*(am|pm)', query.lower())
                if time_match:
                    hour = int(time_match.group(1))
                    if 'pm' in query.lower() and hour != 12:
                        hour += 12
                    elif 'am' in query.lower() and hour == 12:
                        hour = 0
                    minute = 0
                else:
                    return "Please specify time (e.g., 'set alarm 7:30' or 'alarm 8 am')"
            else:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                # Handle AM/PM for time with minutes
                if 'pm' in query.lower() and hour != 12:
                    hour += 12
                elif 'am' in query.lower() and hour == 12:
                    hour = 0
            
            # Calculate alarm time
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Only set for tomorrow if time has already passed today
            if alarm_time <= now:
                alarm_time += timedelta(days=1)
            
            # Store alarm
            self.active_alarm = alarm_time
            
            # Save to file
            with open('alarm.json', 'w') as f:
                json.dump({'time': alarm_time.isoformat()}, f)
            
            self._start_alarm_thread(alarm_time)
            return f"⏰ Alarm set for {alarm_time.strftime('%I:%M %p')}"
            
        except Exception as e:
            return f"Error setting alarm: {e}"
    
    def _cancel_alarm(self):
        """Cancel active alarm with voice confirmation"""
        try:
            if self.active_alarm:
                self.active_alarm = None
                # Remove file
                import os
                if os.path.exists('alarm.json'):
                    os.remove('alarm.json')
                print("⏰ Alarm cancelled")
                return "⏰ Alarm cancelled successfully"
            else:
                return "No active alarm to cancel"
        except Exception as e:
            return f"Error cancelling alarm: {e}"
    



    def _start_alarm_thread(self, alarm_time):
        """Helper method to start alarm thread"""
        import threading
        import time
        from datetime import datetime
        
        def alarm_thread():
            while datetime.now() < alarm_time:
                if not self.active_alarm:
                    return
                time.sleep(1)
            
            # Trigger alarm notification
            try:
                from engine.voice_gender_control import voice_control
                voice_control.speak_with_gender("Good morning! This is your alarm notification. Wake up! Wake up! It's time to get up and start your day. Your alarm time has arrived. Please wake up now!")
            except:
                print("⏰ ALARM: Good morning! Wake up! Wake up! It's time to get up and start your day!")
            
            # Clean up
            self.active_alarm = None
            import os
            if os.path.exists('alarm.json'):
                os.remove('alarm.json')
        
        threading.Thread(target=alarm_thread, daemon=True).start()



    def _roll_dice(self):
        """Roll a dice and return the result"""
        result = random.randint(1, 6)
        return f" {result}"
    
    def _flip_coin(self):
        """Flip a coin and return the result"""
        result = random.choice(['Heads', 'Tails'])
        return f"  {result}"
    
    def _age_calculator(self):
        """Calculate age from birth date"""
        try:
            from datetime import datetime
            import re
            
            query = getattr(self, '_current_query', '')
            
            # Extract date from query (DD/MM/YYYY or DD-MM-YYYY)
            date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', query)
            if date_match:
                day, month, year = map(int, date_match.groups())
                
                # Validate year (reasonable range)
                if year < 1900 or year > 2024:
                    return f"Invalid year: {year}. Please use a year between 1900 and 2024"
                
                # Validate month
                if month < 1 or month > 12:
                    return f"Invalid month: {month}. Please use month between 1-12"
                
                # Validate day
                if day < 1 or day > 31:
                    return f"Invalid day: {day}. Please use day between 1-31"
                
                try:
                    birth_date = datetime(year, month, day)
                except ValueError as ve:
                    return f"Invalid date: {day}/{month}/{year}. {str(ve)}"
                
                today = datetime.now()
                
                # Check if birth date is in the future
                if birth_date > today:
                    return f"Birth date {day}/{month}/{year} is in the future!"
                
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                
                days_diff = (today - birth_date).days
                return f"Age: {age} years ({days_diff} days old)"
            
            return "Please provide birth date (e.g., 'my age 15/03/1990')"
        except Exception as e:
            return f"Age calculation error: {str(e)}"


    def _sort_files(self):
        """Sort files by date, time, name, or size"""
        try:
            import os
            import re
            from datetime import datetime
            
            query = getattr(self, '_current_query', '').lower()
            
            # Extract sort criteria and directory
            sort_by = 'name'  # default
            if 'date' in query or 'time' in query:
                sort_by = 'date'
            elif 'size' in query:
                sort_by = 'size'
            elif 'name' in query:
                sort_by = 'name'
            
            # Extract directory
            target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            dir_match = re.search(r'(?:in|on)\s+(\w+)', query)
            if dir_match:
                dir_name = dir_match.group(1)
                dirs = {
                    'downloads': 'Downloads', 'documents': 'Documents',
                    'desktop': 'Desktop', 'pictures': 'Pictures',
                    'music': 'Music', 'videos': 'Videos'
                }
                if dir_name in dirs:
                    target_dir = os.path.join(os.path.expanduser("~"), dirs[dir_name])
            
            if not os.path.exists(target_dir):
                return f"Directory not found: {target_dir}"
            
            # Get files
            files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
            
            if not files:
                return f"No files found in {os.path.basename(target_dir)}"
            
            # Sort files
            if sort_by == 'date':
                files.sort(key=lambda f: os.path.getmtime(os.path.join(target_dir, f)), reverse=True)
                criteria = "date (newest first)"
            elif sort_by == 'size':
                files.sort(key=lambda f: os.path.getsize(os.path.join(target_dir, f)), reverse=True)
                criteria = "size (largest first)"
            else:  # name
                files.sort()
                criteria = "name (A-Z)"
            
            # Show top 5 files with details
            result = f"Files in {os.path.basename(target_dir)} sorted by {criteria}:\n"
            for i, file in enumerate(files[:5]):
                file_path = os.path.join(target_dir, file)
                if sort_by == 'date':
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    result += f"{i+1}. {file} ({mod_time.strftime('%Y-%m-%d %H:%M')})\n"
                elif sort_by == 'size':
                    size = os.path.getsize(file_path)
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024*1024:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/(1024*1024):.1f} MB"
                    result += f"{i+1}. {file} ({size_str})\n"
                else:
                    result += f"{i+1}. {file}\n"
            
            if len(files) > 5:
                result += f"... and {len(files)-5} more files"
            
            return result.strip()
            
        except Exception as e:
            return f"Sort failed: {str(e)}"


    def _ai_document_maker(self, doc_type="document"):
        try:
            topic = "Document"
            user_info = ""
            num_pages = 2
            
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()

                # Document type
                if 'report' in query:
                    doc_type = "report"
                elif 'letter' in query:
                    doc_type = "letter"

                # Extract page count
                page_match = re.search(r'(\d+)\s+page', query)
                if page_match:
                    num_pages = int(page_match.group(1))

                # Extract topic correctly
                patterns = [
                    r'(?:create|make)\s+(?:a\s+)?(?:document|report|letter)\s+(?:about|on|regarding)\s+(.+?)(?:\s+\d+\s+page)?$',
                    r'(?:document|report|letter)\s+(?:about|on|regarding)\s+(.+?)(?:\s+\d+\s+page)?$',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, query)
                    if match:
                        topic = match.group(1).strip()
                        topic = re.sub(r'\b\d+\s*page(s)?\b', '', topic).strip()
                        break
            
            try:
                from engine.voice_advanced_ai import voice_advanced_ai
                return voice_advanced_ai.ai_document_maker(doc_type, topic, user_info, num_pages)
            except:
                return f"{doc_type.title()} creation started for: {topic} ({num_pages} pages)"
        except Exception as e:
            return f"Document creation error: {str(e)}"
    
    def _write_code(self):
        """AI Code Writer - Write code in any language"""
        try:
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract programming language
                languages = ['python', 'javascript', 'java', 'c++', 'c#', 'html', 'css', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin']
                language = 'python'  # default
                for lang in languages:
                    if lang in query:
                        language = lang
                        break
                
                # Extract code description with improved patterns
                patterns = [
                    r'write\s+(?:' + '|'.join(languages) + r')\s+code\s+(?:for|to)\s+(.+)',
                    r'write\s+code\s+(?:in\s+(?:' + '|'.join(languages) + r')\s+)?(?:for|to)\s+(.+)',
                    r'generate\s+(?:' + '|'.join(languages) + r')\s+code\s+(?:for|to)\s+(.+)',
                    r'generate\s+code\s+(?:in\s+(?:' + '|'.join(languages) + r')\s+)?(?:for|to)\s+(.+)',
                    r'create\s+(?:' + '|'.join(languages) + r')\s+code\s+(?:for|to)\s+(.+)',
                    r'create\s+code\s+(?:in\s+(?:' + '|'.join(languages) + r')\s+)?(?:for|to)\s+(.+)'
                ]
                
                description = None
                for pattern in patterns:
                    match = re.search(pattern, query)
                    if match:
                        description = match.group(1).strip()
                        break
                
                # Fallback extraction if patterns fail
                if not description:
                    # Remove common words and extract the main request
                    temp = query
                    for word in ['write', 'generate', 'create', 'code', 'program', 'script'] + languages:
                        temp = temp.replace(word, '')
                    temp = re.sub(r'\b(?:for|to|in|a|an|the)\b', '', temp)
                    description = temp.strip() or "a simple program"
                
                # Generate code using AI with better prompt
                prompt = f"""Write ONLY the {language} code for: {description}

Requirements:
- Write clean, working {language} code
- Include proper comments
- Make it functional and ready to run
- Focus specifically on: {description}
- No explanations, just code

Code:"""
                
                if self.ai_provider == 'groq':
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant",
                        max_tokens=1500
                    )
                    code = response.choices[0].message.content.strip()
                else:
                    response = self.gemini_model.generate_content(prompt)
                    code = response.text.strip()
                
                # Clean up the response to get only code
                if '```' in code:
                    # Extract code from markdown blocks
                    import re
                    code_match = re.search(r'```(?:python|javascript|java|html|css)?\n?([\s\S]*?)```', code)
                    if code_match:
                        code = code_match.group(1).strip()
                
                # Remove any leading explanatory text
                lines = code.split('\n')
                code_lines = []
                code_started = False
                for line in lines:
                    if not code_started and (line.strip().startswith('#') or line.strip().startswith('//') or 
                                           line.strip().startswith('def ') or line.strip().startswith('function ') or
                                           line.strip().startswith('class ') or line.strip().startswith('import ') or
                                           line.strip().startswith('from ') or line.strip().startswith('<!DOCTYPE') or
                                           line.strip().startswith('<') or line.strip().startswith('var ') or
                                           line.strip().startswith('let ') or line.strip().startswith('const ')):
                        code_started = True
                    if code_started:
                        code_lines.append(line)
                
                if code_lines:
                    code = '\n'.join(code_lines)
                
                # Save to file
                extensions = {
                    'python': '.py', 'javascript': '.js', 'java': '.java', 'c++': '.cpp',
                    'c#': '.cs', 'html': '.html', 'css': '.css', 'php': '.php',
                    'ruby': '.rb', 'go': '.go', 'rust': '.rs', 'swift': '.swift', 'kotlin': '.kt'
                }
                
                ext = extensions.get(language, '.txt')
                # Clean description for filename
                clean_desc = re.sub(r'[^a-zA-Z0-9_\s]', '', description)
                clean_desc = clean_desc.replace(' ', '_')[:20]
                filename = f"ai_code_{clean_desc}_{datetime.now().strftime('%H%M%S')}{ext}"
                file_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Open in notepad
                subprocess.Popen(f'notepad "{file_path}"', shell=True)
                
                return f"AI {language} code generated and opened: {filename}"
            
            return "Please specify what code to write (e.g., 'write python code for calculator')"
            
        except Exception as e:
            return f"Code generation failed: {str(e)}"
    

    def _create_project(self):
        """AI Project Creator - generates complete multi-file projects"""
        import os
        import re
        import subprocess

        try:
            if not hasattr(self, '_current_query') or not self._current_query:
                return "Please specify what project to create (e.g., 'create todo app using python')"

            query = self._current_query.strip()

            tech_keywords = ['python', 'javascript', 'html', 'css', 'react', 'flask', 'django', 'node', 'java', 'c++']
            mentioned_tech = [tech for tech in tech_keywords if tech in query.lower()]

            project_name_raw = query.replace("create", "").replace("project", "").strip()
            project_name = re.sub(r'[^a-zA-Z0-9_]', '_', project_name_raw)[:30]
            if not project_name:
                project_name = "AI_Project"

            prompt = f"""
Create a complete working project for: "{query}"

Technologies detected: {', '.join(mentioned_tech) if mentioned_tech else 'auto-select best stack'}

Generate 3–6 FULL files. Format EXACTLY like this:

**FILENAME: main.py**
```python
# code here
```

**FILENAME: README.md**
```markdown
# content here
```

CRITICAL RULES:
- ONLY complete, working code inside ``` blocks
- Enterprise-grade, production-ready implementation with better ui and backend
- Professional UI with perfect alignment, modern design, responsive layout
- Zero placeholders, TODOs, or incomplete features
- No explanations or text outside file blocks
- Comprehensive README with installation and usage
- All functionality must work flawlessly
"""

            ai_response = ""
            try:
                if hasattr(self, "groq_client") and self.groq_client:
                    resp = self.groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=4096
                    )
                    ai_response = resp.choices[0].message.content

                elif hasattr(self, "gemini_model") and self.gemini_model:
                    resp = self.gemini_model.generate_content(prompt)
                    ai_response = resp.text

                else:
                    return "❌ No AI provider available."
            except Exception as e:
                return f"❌ AI Generation Failed: {e}"

            if not ai_response:
                return "❌ AI returned empty response."

            file_blocks = re.findall(
                r'\*\*FILENAME:\s*(.*?)\*\*.*?```(?:[a-zA-Z]*)\n(.*?)```',
                ai_response,
                flags=re.DOTALL
            )

            files = []
            for filename, content in file_blocks:
                filename = filename.strip()
                content = content.strip("\n")
                files.append((filename, content))

            if not files:
                files = [
                    ("main.py", f'# Fallback generated project\nprint("Project: {query}")'),
                    ("README.md", f'# {project_name}\n\nAI formatting error fallback.')
                ]

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            project_dir = os.path.join(desktop, f"AI_Project_{project_name}")
            os.makedirs(project_dir, exist_ok=True)

            for filename, content in files:
                file_path = os.path.join(project_dir, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

            try:
                subprocess.run(["explorer", project_dir], check=False)
            except:
                pass

            return (
                f"✅ Project '{project_name}' created successfully!\n"
                f"📁 Location: {project_dir}\n"
                f"📄 Files created: {len(files)}\n"
                f"🚀 Folder opened automatically."
            )

        except Exception as e:
            return f"❌ Project creation failed: {str(e)}"


dual_ai = DualAI()

def get_simple_response(query):
    return dual_ai.execute(query)