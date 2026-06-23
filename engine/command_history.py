import json
import os
from datetime import datetime

class CommandHistory:
    def __init__(self):
        self.history_file = 'command_history.json'
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Load command history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading command history: {e}")
            self.history = []
    
    def save_history(self):
        """Save command history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving command history: {e}")
    
    def add_command(self, user_input, jarvis_response, is_voice=False):
        """Add a command to history"""
        try:
            command_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'jarvis_response': jarvis_response,
                'input_type': 'voice' if is_voice else 'text'
            }
            
            self.history.append(command_entry)
            
            # Keep only last 100 commands to prevent file from getting too large
            if len(self.history) > 100:
                self.history = self.history[-100:]
            
            self.save_history()
        except Exception as e:
            print(f"Error adding command to history: {e}")
    
    def get_recent_commands(self, count=10):
        """Get recent commands"""
        return self.history[-count:] if len(self.history) >= count else self.history
    
    def search_commands(self, query="", date_filter="", input_type=""):
        """Search commands by query, date, or type"""
        filtered = self.history
        
        if query:
            filtered = [cmd for cmd in filtered if query.lower() in cmd['user_input'].lower()]
        
        if date_filter:
            from datetime import datetime, timedelta
            today = datetime.now()
            if date_filter == "today":
                start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date_filter == "week":
                start_date = today - timedelta(days=7)
            elif date_filter == "month":
                start_date = today - timedelta(days=30)
            else:
                return filtered
            
            filtered = [cmd for cmd in filtered if datetime.fromisoformat(cmd['timestamp']) >= start_date]
        
        if input_type:
            filtered = [cmd for cmd in filtered if cmd['input_type'] == input_type]
        
        return filtered
    
    def get_statistics(self):
        """Get command statistics"""
        if not self.history:
            return {"total": 0, "voice": 0, "text": 0, "most_used": [], "success_rate": 0}
        
        total = len(self.history)
        voice_count = sum(1 for cmd in self.history if cmd['input_type'] == 'voice')
        text_count = total - voice_count
        
        # Count command frequency
        command_freq = {}
        successful = 0
        
        for cmd in self.history:
            base_cmd = cmd['user_input'].strip().lower().split()[0] if cmd['user_input'].strip() else "unknown"
            command_freq[base_cmd] = command_freq.get(base_cmd, 0) + 1
            
            if cmd['jarvis_response'] and "error" not in cmd['jarvis_response'].lower() and "failed" not in cmd['jarvis_response'].lower():
                successful += 1
        
        # Get top 5 most used commands
        most_used = sorted(command_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        success_rate = round((successful / total) * 100, 1) if total > 0 else 0
        
        return {
            "total": total,
            "voice": voice_count,
            "text": text_count,
            "most_used": most_used,
            "success_rate": success_rate
        }
    
    def clear_history(self):
        """Clear all command history"""
        self.history = []
        self.save_history()

# Global instance
command_history = CommandHistory()