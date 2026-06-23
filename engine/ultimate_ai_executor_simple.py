import os
import subprocess
import pyautogui
import time
import win32com.client
import requests
import webbrowser
from PIL import Image
from engine.dual_ai import dual_ai
import sqlite3
import json
from datetime import datetime, timedelta
from collections import Counter
import psutil

class UltimateAIExecutor:
    def __init__(self):
        self.confirmation_required = False
        self.learning_db = os.path.join(os.path.expanduser('~'), '.jarvis_learning.db')
        self._init_learning_db()
        self.next_move_predictions_enabled = False
        
    def get_ai_response(self, user_command):
        """Get AI response with simplified prompt"""
        prompt = f"""
You are a Windows automation system. Convert user commands to executable code.

User Command: "{user_command}"

Output format:
METHOD: <system | pyautogui | office | screen | search | file | ai>
COMMAND: <exact Python code>

Method Rules:
- system: Apps, files, system control
- pyautogui: Typing, clicking, shortcuts  
- office: Word, Excel, PowerPoint
- screen: Screenshot analysis
- search: Google search
- file: Read file contents
- ai: AI-powered tasks

Generate working Python code for any desktop automation task.
"""

        # Try 70B model first for complex automation tasks
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            groq_client = Groq(api_key=GROQ_API_KEY)
            
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            result = response.choices[0].message.content.strip()
            if result:
                return result
        except Exception as e:
            print(f"70B model failed: {e}, falling back to dual_ai")
        
        # Fallback to dual_ai
        from engine.dual_ai import dual_ai
        result = dual_ai._answer_question(prompt)
        if result:
            return result

    def run_system_call(self, command):
        print(f"[System Call] -> {command}")
        if command.startswith('os.system(') or 'import' in command:
            exec(command, globals())
        else:
            os.system(command)

    def run_pyautogui(self, command):
        print(f"[PyAutoGUI] executing ->")
        exec_globals = {
            'os': os,
            'time': time,
            'pyautogui': pyautogui,
            'subprocess': subprocess
        }
        exec(command, exec_globals)

    def run_office(self, command):
        print(f"[Office Automation] executing ->")
        exec(command, globals())
        
    def run_screen_analysis(self, command):
        print(f"[Screen Analysis] executing ->")
        exec_globals = {
            'pyautogui': pyautogui,
            'time': time,
            'os': os,
            'subprocess': subprocess,
            'win32gui': None
        }
        try:
            import win32gui
            exec_globals['win32gui'] = win32gui
        except:
            pass
        exec(command, exec_globals)
        
    def run_search_explanation(self, command):
        print(f"[Search & Explain] executing ->")
        exec_globals = {
            'webbrowser': webbrowser,
            'requests': requests
        }
        exec(command, exec_globals)
        
    def run_file_analysis(self, command):
        print(f"[File Analysis] executing ->")
        exec(command, globals())
    
    def _init_learning_db(self):
        conn = sqlite3.connect(self.learning_db)
        conn.execute('''CREATE TABLE IF NOT EXISTS command_history 
                       (id INTEGER PRIMARY KEY, command TEXT, method TEXT, 
                        success INTEGER, timestamp TEXT, context TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS user_patterns 
                       (id INTEGER PRIMARY KEY, pattern TEXT, frequency INTEGER, 
                        last_used TEXT, context TEXT)''')
        conn.close()
    
    def success_failure_tracker(self, command, method, success, context=""):
        conn = sqlite3.connect(self.learning_db)
        conn.execute('INSERT INTO command_history VALUES (NULL, ?, ?, ?, ?, ?)',
                    (command, method, success, datetime.now().isoformat(), context))
        conn.commit()
        conn.close()
    
    def execute_command(self, user_command):
        """Main function to execute any desktop command"""
        try:
            # Get AI response for the command
            ai_response = self.get_ai_response(user_command)
            if not ai_response:
                return "Command not recognized"
            
            # Parse METHOD and COMMAND from AI response
            lines = ai_response.split('\n')
            method = None
            command = []
            
            for line in lines:
                if line.startswith('METHOD:'):
                    method = line.replace('METHOD:', '').strip()
                elif line.startswith('COMMAND:'):
                    command = []
                elif method and line.strip():
                    command.append(line)
            
            if not method or not command:
                return "Invalid command format"
            
            # Execute based on method
            command_code = '\n'.join(command)
            
            if method == 'system':
                self.run_system_call(command_code)
            elif method == 'pyautogui':
                self.run_pyautogui(command_code)
            elif method == 'office':
                self.run_office(command_code)
            elif method == 'ai':
                exec(command_code, globals())
            elif method == 'screen':
                self.run_screen_analysis(command_code)
            elif method == 'search':
                self.run_search_explanation(command_code)
            elif method == 'file':
                self.run_file_analysis(command_code)
            else:
                return f"Unknown method: {method}"
            
            return "Command executed successfully"
            
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def execute(self, user_command):
        """Universal execution of any natural language command"""
        try:
            plan = self.get_ai_response(user_command)
            print("\nAI Generated Plan:")
            print(plan)
            print("=" * 60)

            method = ""
            command = ""

            lines = plan.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("METHOD:"):
                    method = line.split(":", 1)[1].strip().lower()
                elif line.startswith("COMMAND:"):
                    # Get command and all following lines
                    command_parts = [line.split(":", 1)[1].strip()]
                    for j in range(i + 1, len(lines)):
                        if not lines[j].startswith("----") and lines[j].strip():
                            command_parts.append(lines[j])
                        elif lines[j].startswith("----"):
                            break
                    command = "\n".join(command_parts)

            if not method or not command:
                print("ERROR: Could not parse AI output.")
                return

            try:
                if method == "pyautogui":
                    self.run_pyautogui(command)
                elif method == "office":
                    self.run_office(command)
                elif method == "screen":
                    self.run_screen_analysis(command)
                elif method == "search":
                    self.run_search_explanation(command)
                elif method == "file":
                    self.run_file_analysis(command)
                elif method == "system":
                    self.run_system_call(command)
                else:
                    print("WARNING: Unknown method, fallback to system call.")
                    self.run_system_call(command)
                    
                print("SUCCESS: Command executed successfully!")
                self.success_failure_tracker(user_command, method, 1)
                return "Command executed successfully"
                
            except Exception as e:
                print(f"ERROR executing: {e}")
                self.success_failure_tracker(user_command, method, 0, str(e))
                return f"Failed to execute: {user_command}"
                
        except Exception as e:
            return f"Error: {str(e)}"

# Global instance
ultimate_ai = UltimateAIExecutor()

# Main function to use from other modules
def execute_desktop_command(command):
    """Execute any desktop automation command"""
    return ultimate_ai.execute_command(command)

def execute_command(cmd):
    """Simple function to execute any command"""
    return ultimate_ai.execute(cmd)

if __name__ == "__main__":
    print("Ultimate AI Executor Ready!")
    print("Examples: 'open calculator', 'create word document', 'take screenshot'")
    
    while True:
        cmd = input("\nYou: ").strip()
        if cmd.lower() in ["exit", "quit"]:
            break
        execute_command(cmd)