import socket
import hashlib
import json
import os
import time

class FingerprintAuth:
    def __init__(self):
        self.data_file = 'engine/auth/fingerprint_data.json'
        self.fingerprint_data = self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.fingerprint_data, f)
    
    def authenticate(self):
        if not self.fingerprint_data:
            print("No fingerprint registered. Register first.")
            return False
        
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', 8888))
            server.listen(1)
            server.settimeout(15)
            
            print("Place finger on phone scanner...")
            conn, addr = server.accept()
            
            data = conn.recv(1024).decode()
            fingerprint_hash = hashlib.sha256(data.encode()).hexdigest()
            
            for user_id, stored_data in self.fingerprint_data.items():
                if stored_data['hash'] == fingerprint_hash:
                    conn.send(b"SUCCESS")
                    server.close()
                    return True
            
            conn.send(b"FAILED")
            server.close()
            return False
            
        except:
            return False
    
    def register(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', 8888))
            server.listen(1)
            server.settimeout(30)
            
            print("Place finger on phone to register...")
            conn, addr = server.accept()
            
            data = conn.recv(1024).decode()
            fingerprint_hash = hashlib.sha256(data.encode()).hexdigest()
            
            self.fingerprint_data['user1'] = {
                'hash': fingerprint_hash,
                'time': time.time()
            }
            self.save_data()
            
            conn.send(b"REGISTERED")
            server.close()
            return True
            
        except:
            return False

def AuthenticateFingerprint():
    auth = FingerprintAuth()
    if not auth.fingerprint_data:
        if auth.register():
            return auth.authenticate()
        return False
    return auth.authenticate()