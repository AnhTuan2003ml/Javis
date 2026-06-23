"""
Dictation methods for dual_ai.py
"""

def dictate_to_file(self, query=""):
    """Voice-to-text dictation to file"""
    try:
        import speech_recognition as sr
        import re
        import os
        from datetime import datetime
        
        # Extract filename from query
        filename = "dictation.txt"  # default
        mode = "write"  # default
        
        file_match = re.search(r'to file\s+([^\s]+)', query.lower())
        if file_match:
            filename = file_match.group(1).strip()
            if not filename.endswith('.txt'):
                filename += '.txt'
    
        if "append" in query.lower():
            mode = "append"
    
        # Initialize recognizer
        r = sr.Recognizer()
    
        # Start recording
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source)
            print(f"🎤 Dictating to {filename}. Say 'stop dictation' to finish...")
        
            text_content = ""
        
            while True:
                try:
                    # Listen for audio
                    audio = r.listen(source, timeout=1, phrase_time_limit=5)
                
                    # Convert to text
                    text = r.recognize_google(audio)
                
                    # Check for stop command
                    if "stop dictation" in text.lower():
                        break
                
                    # Process punctuation commands
                    text = self._process_punctuation_commands(text)
                
                    text_content += text + " "
                    print(f"📝 {text}")
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    return f"Speech recognition error: {e}"
    
        # Save to file
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

def dictate_to_document(self, query=""):
    """Advanced voice-to-text for formatted documents"""
    try:
        import speech_recognition as sr
        import re
        from datetime import datetime
    
        # Determine document type
        doc_type = "word"
        if "google docs" in query.lower():
            doc_type = "gdocs"
        elif "email" in query.lower():
            doc_type = "email"
    
        # Initialize recognizer
        r = sr.Recognizer()
    
        # Start recording
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source)
            print(f"🎤 Dictating to {doc_type}. Say formatting commands like 'bold this', 'new paragraph'...")
        
            document_content = []
            current_text = ""
        
            while True:
                try:
                    # Listen for audio
                    audio = r.listen(source, timeout=1, phrase_time_limit=5)
                
                    # Convert to text
                    text = r.recognize_google(audio)
                
                    # Check for stop command
                    if "stop dictation" in text.lower():
                        break
                
                    # Process formatting commands
                    if self._is_formatting_command(text):
                        formatted_text = self._process_formatting_command(text, current_text)
                        document_content.append(formatted_text)
                        current_text = ""
                    else:
                        # Process punctuation commands
                        text = self._process_punctuation_commands(text)
                        current_text += text + " "
                        print(f"📝 {text}")
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    return f"Speech recognition error: {e}"
    
        # Add remaining text
        if current_text.strip():
            document_content.append(current_text.strip())
    
        # Save formatted document
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

def process_punctuation_commands(self, text):
    """Process voice punctuation commands"""
    punctuation_map = {
        'period': '.',
        'comma': ',',
        'question mark': '?',
        'exclamation point': '!',
        'colon': ':',
        'semicolon': ';',
        'new line': '\n',
        'new paragraph': '\n\n'
    }

    for command, punctuation in punctuation_map.items():
        text = text.replace(command, punctuation)

    return text

def is_formatting_command(self, text):
    """Check if text contains formatting commands"""
    formatting_commands = [
        'bold this', 'italic this', 'underline this',
        'bullet point', 'numbered list', 'new paragraph',
        'heading', 'title', 'center this'
    ]

    return any(cmd in text.lower() for cmd in formatting_commands)

def process_formatting_command(self, command, text):
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

def format_as_email(self, content_list):
    """Format content as email"""
    email_content = "Subject: [Your Subject]\n\n"
    email_content += "Dear [Recipient],\n\n"

    for content in content_list:
        email_content += content + "\n\n"

    email_content += "Best regards,\n[Your Name]"
    return email_content

def format_as_document(self, content_list):
    """Format content as document"""
    document_content = ""

    for content in content_list:
        document_content += content + "\n\n"

    return document_content.strip()