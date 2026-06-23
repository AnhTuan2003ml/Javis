# Face Authentication Configuration
import json
import os

CONFIG_FILE = 'face_auth_config.json'

def get_face_auth_status():
    """Get current face authentication status"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('face_auth_enabled', False)
        return False
    except:
        return False

def set_face_auth_status(enabled):
    """Set face authentication status"""
    try:
        config = {'face_auth_enabled': enabled}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return True
    except:
        return False