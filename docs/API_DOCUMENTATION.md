# JARVIS AI Assistant - API Documentation

## Overview

This document provides comprehensive API documentation for JARVIS AI Assistant, including all available endpoints, functions, and integration methods.

## Table of Contents

- [Core APIs](#core-apis)
- [Voice Processing](#voice-processing)
- [AI Integration](#ai-integration)
- [Authentication](#authentication)
- [System Control](#system-control)
- [Phone Integration](#phone-integration)
- [Configuration](#configuration)
- [Web Interface APIs](#web-interface-apis)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Core APIs

### Main Application Interface

#### `start()`
Initialize and start the JARVIS application.

```python
def start() -> None:
    """
    Start the JARVIS AI Assistant application.
    
    Initializes all subsystems including:
    - Web interface
    - Authentication system
    - Voice processing
    - AI integration
    - Phone connectivity
    """
```

#### `shutdown()`
Gracefully shutdown the application.

```python
def shutdown() -> bool:
    """
    Shutdown JARVIS application gracefully.
    
    Returns:
        bool: True if shutdown successful, False otherwise
    """
```

## Voice Processing

### Speech Recognition

#### `SpeechToText` Class

```python
class SpeechToText:
    """Advanced speech recognition with multiple engine support."""
    
    def __init__(self, config: Optional[SpeechConfig] = None):
        """Initialize speech recognition system."""
    
    def listen_once(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Listen for single speech input.
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            Recognized text or None if failed
        """
    
    def start_continuous_listening(self, callback: Callable[[str], None]) -> bool:
        """
        Start continuous speech recognition.
        
        Args:
            callback: Function to call with recognized text
            
        Returns:
            True if started successfully
        """
    
    def stop_continuous_listening(self) -> bool:
        """Stop continuous speech recognition."""
    
    def set_language(self, language: str) -> bool:
        """Set recognition language (e.g., 'en-US', 'es-ES')."""
    
    def get_available_microphones(self) -> Dict[int, str]:
        """Get list of available microphones."""
```

### Text-to-Speech

#### `TextToSpeech` Class

```python
class TextToSpeech:
    """Advanced text-to-speech with voice customization."""
    
    def __init__(self, config: Optional[VoiceConfig] = None):
        """Initialize text-to-speech system."""
    
    def speak(self, text: str, priority: int = 1, 
              callback: Optional[Callable] = None) -> bool:
        """
        Add text to speech queue.
        
        Args:
            text: Text to speak
            priority: Speech priority (lower = higher priority)
            callback: Optional callback when complete
            
        Returns:
            True if added to queue successfully
        """
    
    def speak_immediately(self, text: str, 
                         callback: Optional[Callable] = None) -> bool:
        """Speak text immediately, interrupting current speech."""
    
    def set_voice_gender(self, gender: VoiceGender) -> bool:
        """Set voice gender (MALE, FEMALE, NEUTRAL)."""
    
    def set_rate(self, rate: int) -> bool:
        """Set speech rate (50-400 WPM)."""
    
    def set_volume(self, volume: float) -> bool:
        """Set speech volume (0.0-1.0)."""
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices."""
```

## AI Integration

### Dual AI System

#### `AIManager` Class

```python
class AIManager:
    """Manages multiple AI providers with fallback support."""
    
    def process_query(self, query: str, context: Optional[Dict] = None) -> str:
        """
        Process AI query with context awareness.
        
        Args:
            query: User query text
            context: Optional context information
            
        Returns:
            AI response text
        """
    
    def set_primary_provider(self, provider: str) -> bool:
        """Set primary AI provider ('groq' or 'gemini')."""
    
    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all AI providers."""
    
    def clear_context(self) -> None:
        """Clear conversation context."""
```

### AI Response Processing

```python
def get_simple_response(query: str) -> str:
    """
    Get simple AI response for query.
    
    Args:
        query: User query
        
    Returns:
        AI response text
    """

def get_advanced_response(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get advanced AI response with metadata.
    
    Args:
        query: User query
        context: Conversation context
        
    Returns:
        Response dictionary with text, confidence, and metadata
    """
```

## Authentication

### Biometric Authentication

#### Face Recognition

```python
def authenticate_face() -> Tuple[bool, Optional[str]]:
    """
    Perform face authentication.
    
    Returns:
        Tuple of (success, user_id)
    """

def register_face(user_id: str, name: str) -> bool:
    """
    Register new face for user.
    
    Args:
        user_id: Unique user identifier
        name: User display name
        
    Returns:
        True if registration successful
    """
```

#### Fingerprint Authentication

```python
def authenticate_fingerprint() -> bool:
    """
    Perform fingerprint authentication via Android device.
    
    Returns:
        True if authentication successful
    """
```

### User Management

```python
def add_user(name: str) -> str:
    """
    Add new user to system.
    
    Args:
        name: User display name
        
    Returns:
        Generated user ID
    """

def get_user_info(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user information by ID."""

def update_user_preferences(user_id: str, preferences: Dict[str, Any]) -> bool:
    """Update user preferences."""
```

## System Control

### Application Management

```python
def open_application(app_name: str) -> bool:
    """
    Open application by name.
    
    Args:
        app_name: Name of application to open
        
    Returns:
        True if opened successfully
    """

def close_application(app_name: str) -> bool:
    """Close application by name."""

def get_running_applications() -> List[Dict[str, Any]]:
    """Get list of currently running applications."""
```

### File Operations

```python
def create_file(filepath: str, content: str = "") -> bool:
    """Create new file with optional content."""

def delete_file(filepath: str) -> bool:
    """Delete file at specified path."""

def read_file(filepath: str) -> Optional[str]:
    """Read file content."""

def write_file(filepath: str, content: str) -> bool:
    """Write content to file."""
```

### System Monitoring

```python
def get_system_stats() -> Dict[str, Any]:
    """
    Get current system statistics.
    
    Returns:
        Dictionary with CPU, memory, disk usage, etc.
    """

def take_screenshot(filepath: Optional[str] = None) -> str:
    """
    Take screenshot and save to file.
    
    Args:
        filepath: Optional custom save path
        
    Returns:
        Path to saved screenshot
    """
```

## Phone Integration

### SMS Management

```python
def send_message(contact: str, message: str, method: str = "whatsapp") -> bool:
    """
    Send message to contact.
    
    Args:
        contact: Contact name or number
        message: Message text
        method: Messaging method ('sms' or 'whatsapp')
        
    Returns:
        True if sent successfully
    """

def read_messages(limit: int = 10) -> List[Dict[str, Any]]:
    """Read recent messages from phone."""

def get_message_history(contact: str) -> List[Dict[str, Any]]:
    """Get message history with specific contact."""
```

### Call Management

```python
def make_call(contact: str) -> bool:
    """
    Initiate call to contact.
    
    Args:
        contact: Contact name or number
        
    Returns:
        True if call initiated successfully
    """

def get_call_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent call history."""
```

### Contact Management

```python
def add_contact(name: str, phone: str, email: Optional[str] = None) -> bool:
    """Add new contact to phone."""

def get_contacts() -> List[Dict[str, Any]]:
    """Get all contacts from phone."""

def search_contacts(query: str) -> List[Dict[str, Any]]:
    """Search contacts by name or number."""
```

## Configuration

### Settings Management

```python
def get_config(section: str) -> Dict[str, Any]:
    """Get configuration section."""

def set_config(section: str, config: Dict[str, Any]) -> bool:
    """Update configuration section."""

def reset_config(section: str) -> bool:
    """Reset configuration section to defaults."""
```

### Voice Configuration

```python
def set_voice_gender(gender: str) -> str:
    """Set voice gender ('male' or 'female')."""

def set_voice_speed(speed: str) -> str:
    """Set voice speed ('slow', 'normal', 'fast')."""

def set_voice_volume(volume: str) -> str:
    """Set voice volume ('low', 'medium', 'high')."""
```

### Language Settings

```python
def set_language(language: str) -> str:
    """Set system language."""

def get_current_language() -> str:
    """Get current system language."""

def get_supported_languages() -> List[str]:
    """Get list of supported languages."""
```

## Web Interface APIs

### Eel Exposed Functions

All web interface functions are exposed via the Eel framework for JavaScript interaction.

#### Authentication APIs

```javascript
// Get authentication status
eel.getFaceAuthStatus()((status) => {
    console.log("Face auth status:", status);
});

// Enable/disable face authentication
eel.enableFaceAuth()((result) => {
    console.log("Face auth enabled:", result);
});

eel.disableFaceAuth()((result) => {
    console.log("Face auth disabled:", result);
});
```

#### Voice Control APIs

```javascript
// Set voice gender
eel.setVoiceGender("female")((result) => {
    console.log("Voice gender set:", result);
});

// Get current voice gender
eel.getVoiceGender()((gender) => {
    console.log("Current voice gender:", gender);
});

// Set voice speed
eel.setVoiceSpeed("fast")((result) => {
    console.log("Voice speed set:", result);
});
```

#### System Control APIs

```javascript
// Start continuous listening
eel.startContinuousListen()((result) => {
    console.log("Continuous listening:", result);
});

// Get system statistics
eel.getSystemStats()((stats) => {
    console.log("System stats:", stats);
});
```

#### Command History APIs

```javascript
// Get command history
eel.getCommandHistory()((history) => {
    console.log("Command history:", history);
});

// Search commands
eel.searchCommands("open", "", "voice")((results) => {
    console.log("Search results:", results);
});

// Get command statistics
eel.getCommandStatistics()((stats) => {
    console.log("Command stats:", stats);
});
```

## Error Handling

### Exception Types

```python
class JarvisError(Exception):
    """Base exception for JARVIS errors."""

class AuthenticationError(JarvisError):
    """Authentication related errors."""

class VoiceProcessingError(JarvisError):
    """Voice processing related errors."""

class AIProcessingError(JarvisError):
    """AI processing related errors."""

class SystemControlError(JarvisError):
    """System control related errors."""

class PhoneIntegrationError(JarvisError):
    """Phone integration related errors."""
```

### Error Response Format

```python
{
    "success": False,
    "error": {
        "type": "AuthenticationError",
        "message": "Face authentication failed",
        "code": "AUTH_001",
        "details": {
            "reason": "No face detected",
            "suggestions": ["Ensure good lighting", "Position face in camera view"]
        }
    }
}
```

### Common Error Codes

| Code | Type | Description |
|------|------|-------------|
| AUTH_001 | Authentication | Face authentication failed |
| AUTH_002 | Authentication | Fingerprint authentication failed |
| VOICE_001 | Voice | Microphone not accessible |
| VOICE_002 | Voice | Speech recognition timeout |
| AI_001 | AI Processing | API key invalid |
| AI_002 | AI Processing | AI service unavailable |
| SYS_001 | System | Application not found |
| SYS_002 | System | Insufficient permissions |
| PHONE_001 | Phone | Device not connected |
| PHONE_002 | Phone | ADB connection failed |

## Examples

### Basic Voice Command Processing

```python
from src.speech_to_text import SpeechToText
from src.command_handler import CommandHandler
from src.text_to_speech import TextToSpeech

# Initialize components
stt = SpeechToText()
handler = CommandHandler()
tts = TextToSpeech()

# Process voice command
def process_voice_command():
    # Listen for speech
    text = stt.listen_once(timeout=5)
    
    if text:
        # Process command
        result = handler.process_text(text)
        
        # Respond with speech
        if result.success:
            tts.speak(result.message)
        else:
            tts.speak(f"Sorry, I couldn't process that command: {result.error}")
    else:
        tts.speak("I didn't hear anything. Please try again.")

# Example usage
process_voice_command()
```

### AI Query Processing

```python
from engine.dual_ai import get_simple_response, get_advanced_response

# Simple AI query
response = get_simple_response("What's the weather like today?")
print(response)

# Advanced AI query with context
context = {
    "user_location": "New York",
    "user_preferences": {"units": "fahrenheit"},
    "conversation_history": []
}

advanced_response = get_advanced_response("What's the weather?", context)
print(f"Response: {advanced_response['text']}")
print(f"Confidence: {advanced_response['confidence']}")
```

### Phone Integration Example

```python
from engine.phone import send_message, get_contacts

# Send WhatsApp message
success = send_message("John Doe", "Hello from JARVIS!", "whatsapp")
if success:
    print("Message sent successfully")

# Get contacts
contacts = get_contacts()
for contact in contacts[:5]:  # Show first 5 contacts
    print(f"Name: {contact['name']}, Phone: {contact['phone']}")
```

### System Control Example

```python
from engine.command import allCommands
from engine.system_monitor import getSystemStats

# Open application
allCommands("open calculator")

# Get system statistics
stats = getSystemStats()
print(f"CPU Usage: {stats['cpu_percent']}%")
print(f"Memory Usage: {stats['memory_percent']}%")
print(f"Disk Usage: {stats['disk_percent']}%")
```

### Web Interface Integration

```html
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS Control Panel</title>
    <script src="/eel.js"></script>
</head>
<body>
    <button onclick="startListening()">Start Listening</button>
    <button onclick="getStats()">Get System Stats</button>
    
    <script>
        function startListening() {
            eel.startContinuousListen()((result) => {
                console.log("Listening started:", result);
            });
        }
        
        function getStats() {
            eel.getSystemStats()((stats) => {
                document.getElementById('stats').innerHTML = 
                    `CPU: ${stats.cpu}%, Memory: ${stats.memory}%`;
            });
        }
    </script>
</body>
</html>
```

## Rate Limits and Quotas

### AI API Limits
- **Groq API**: 100 requests/minute
- **Gemini API**: 60 requests/minute
- **Fallback**: Automatic switching when limits reached

### Voice Processing Limits
- **Continuous Listening**: No limit
- **Single Recognition**: 30 second timeout
- **Speech Synthesis**: Queue-based, no limit

### Phone Integration Limits
- **SMS**: Depends on carrier limits
- **Calls**: No artificial limits
- **ADB Commands**: 10 commands/second max

## Authentication and Security

### API Key Management
```python
# API keys are stored encrypted
# Never commit API keys to version control
# Use environment variables or encrypted config files

# Example configuration
{
    "groq_api_key": "encrypted_key_here",
    "gemini_api_key": "encrypted_key_here"
}
```

### Biometric Data Security
- Face recognition data stored locally only
- Fingerprint authentication via device, no data stored
- User profiles encrypted at rest
- No biometric data transmitted over network

## Troubleshooting

### Common Issues

#### Voice Recognition Not Working
```python
# Test microphone
stt = SpeechToText()
test_result = stt.test_microphone()
print(test_result)

# Check available microphones
mics = stt.get_available_microphones()
print(mics)
```

#### AI API Errors
```python
# Check API key configuration
from engine.dual_ai import test_ai_connection
result = test_ai_connection()
print(f"Groq: {result['groq']}, Gemini: {result['gemini']}")
```

#### Phone Connection Issues
```python
# Test ADB connection
from engine.phone import test_phone_connection
connected = test_phone_connection()
print(f"Phone connected: {connected}")
```

---

For more detailed examples and advanced usage, see the [Demo Guide](../demos/DEMO_GUIDE.md) and [Contributing Guidelines](../CONTRIBUTING.md).