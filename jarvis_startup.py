import os
import shutil
import subprocess

def enable_auto_start():
    """Enable Jarvis auto-start on Windows boot"""
    try:
        # Get startup folder path
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        
        # Create batch file content
        batch_content = f'''@echo off
cd /d "{os.getcwd()}"
python run.py'''
        
        # Create batch file
        batch_path = os.path.join(os.getcwd(), 'jarvis_autostart.bat')
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        
        # Copy to startup folder
        startup_batch = os.path.join(startup_folder, 'jarvis_autostart.bat')
        shutil.copy2(batch_path, startup_batch)
        
        return True
    except Exception as e:
        print(f"Error enabling auto-start: {e}")
        return False

def disable_auto_start():
    """Disable Jarvis auto-start"""
    try:
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        startup_batch = os.path.join(startup_folder, 'jarvis_autostart.bat')
        
        if os.path.exists(startup_batch):
            os.remove(startup_batch)
        
        local_batch = os.path.join(os.getcwd(), 'jarvis_autostart.bat')
        if os.path.exists(local_batch):
            os.remove(local_batch)
        
        return True
    except Exception as e:
        print(f"Error disabling auto-start: {e}")
        return False

def is_auto_start_enabled():
    """Check if auto-start is enabled"""
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    startup_batch = os.path.join(startup_folder, 'jarvis_autostart.bat')
    return os.path.exists(startup_batch)