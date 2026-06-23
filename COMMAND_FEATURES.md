# Jarvis Command Features Documentation

## Core Voice & Text Processing

### Voice Recognition & Speech
- **Function**: `takecommand()` - Captures voice input
- **Function**: `speak(text)` - Text-to-speech output with emotion adaptation
- **Example**: Voice commands are automatically processed and responded to

### Multi-Command Processing
- **Function**: `parse_multiple_commands(query)` - Handles multiple commands in one input
- **Example**: "open notepad and then open calculator" executes both commands sequentially

## Emotion Detection System

### Emotion Management
- **Enable**: "start emotion" or "enable emotion"
- **Disable**: "stop emotion" or "disable emotion" 
- **Status**: "emotion status" or "current emotion"
- **Example**: "start emotion" - Activates real-time emotion monitoring

### Emotion Features
- **Encouragement**: "encourage me" or "cheer me up"
- **Humor**: "make me laugh" or "tell joke"
- **Example**: "encourage me" - Gets AI-powered encouraging message based on current emotion

### Voice Adaptation
- **Function**: Automatically adapts voice rate and volume based on detected emotion
- **Emotions**: happy, sad, stressed, angry, excited, neutral

## Communication Features

### Contact Management
- **Add Contact**: "add contact [name] [number]"
- **Delete Contact**: "delete contact [name]"
- **View Contacts**: "view contacts" or "show contacts" or "list contacts"
- **Example**: "add contact john 1234567890"

### Messaging & Calls
- **Direct Message**: "send message to [name] on whatsapp [message]"
- **WhatsApp Message**: "whatsapp message to [name] [message]"
- **SMS**: "sms to [name] [message]"
- **Phone Call**: "phone call [name]" or "call [name]"
- **Video Call**: "video call [name]"
- **Example**: "send message to john on whatsapp hello how are you"

### SMS Testing
- **Test SMS**: "test sms" or "sms test"
- **Example**: Tests SMS functionality

## Voice & Language Control

### Voice Gender Control
- **Switch to Female**: "switch to female" or "female voice"
- **Switch to Male**: "switch to male" or "male voice"
- **Voice Status**: "current voice" or "voice status"
- **Example**: "switch to female voice"

### Language Switching
- **Change Language**: "switch to [language]" or "change language to [language]"
- **Supported**: English, Hindi, Kannada, Bengali, Gujarati, Malayalam, Marathi, Tamil, Telugu, Urdu
- **Example**: "switch to hindi"

## Listening Control

### Continuous Listening
- **Start**: "start continuous" or "continuous listen"
- **Stop**: "stop continuous"
- **Status**: "continuous status"
- **Example**: "start continuous" - Enables hands-free continuous voice commands

### Listening Management
- **Pause**: "pause listening"
- **Resume**: "resume listening"
- **Mute Jarvis**: "mute jarvis" or "mute voice"
- **Unmute Jarvis**: "unmute jarvis" or "unmute voice"
- **Example**: "pause listening" - Temporarily stops microphone input

## Task Scheduling

### Task Scheduler
- **Schedule Task**: "schedule [command] in [time]"
- **List Tasks**: "list scheduled" or "show scheduled"
- **Time Formats**: "30 seconds", "5 minutes", "2 hours", "2pm", "14:30"
- **Example**: "schedule open notepad in 5 minutes"

### Calendar Events
- **Add Event**: "add event [description] at [time]"
- **Show Calendar**: "show calendar" or "check calendar" or "my events"
- **Example**: "add event meeting at 3pm tomorrow"

## Command History

### Previous Commands
- **Execute Previous**: "execute previous command" or "run previous command" or "repeat last command"
- **View Previous**: "what is previous command" or "last command" or "previous command"
- **Example**: "execute previous command" - Repeats the last executed command

## Application Management

### Universal App Control
- **Open App**: "open [app_name]" or "launch [app_name]" or "run [app_name]"
- **Close App**: "close [app_name]" or "quit [app_name]" or "exit [app_name]" or "kill [app_name]"
- **Example**: "open notepad", "close chrome"

### Browser & Website Management
- **Open Browser/Website**: "open browser" or "open website [url]"
- **Close Browser/Website**: "close browser" or "close website"
- **Example**: "open website google.com"

### Calculator
- **Direct Access**: "open calculator"
- **Example**: Opens Windows calculator application

## Phone Integration

### Phone Commands
- **Requirement**: Commands must end with "on phone"
- **Function**: `handle_phone_commands(query)` from engine.phone
- **Example**: "make call on phone", "send sms on phone"

## Advanced AI Features

### Aura Mode
- **Activation**: Include "aura" in any command
- **Function**: Uses Ultimate AI with next-move prediction
- **Example**: "aura open notepad" - Executes with AI enhancement and suggests next actions

### Dual AI Processing
- **Function**: Handles complex queries and natural language processing
- **Fallback**: All unmatched commands are processed by Dual AI
- **Example**: Natural conversation and complex requests

## System Functions

### Core Processing
- **Function**: `allCommands(message)` - Main command processor
- **Function**: `process_single_command(query)` - Individual command handler
- **Voice Input**: Automatic when message=1
- **Text Input**: Direct when message is string

### Configuration Management
- **Function**: `save_ui_setting(key, value)` - Saves settings to ui_config.json
- **Function**: `load_ui_settings()` - Loads settings on startup
- **Settings**: listening_paused, jarvis_muted

### Error Handling
- **Graceful Degradation**: Falls back to simpler methods on errors
- **Multilingual Support**: Error messages in current language
- **Silent Operations**: Many functions operate without verbose output

## Usage Examples

### Basic Commands
```
"open notepad"
"close chrome"
"what time is it"
"weather today"
```

### Communication
```
"send message to john on whatsapp hello"
"call mary"
"add contact alice 9876543210"
```

### Advanced Features
```
"aura create a presentation"
"schedule open calculator in 30 seconds"
"switch to female voice"
"start continuous listening"
```

### Multi-Commands
```
"open notepad and then open calculator"
"mute jarvis and then pause listening"
"add contact bob 1234567890 and then call bob"
```

## Integration Points

### External Modules
- **engine.dual_ai**: Main AI processing
- **engine.ultimate_ai_executor**: Aura mode functionality
- **engine.new_features**: Extended feature set
- **engine.features**: Core features (contacts, messaging)
- **engine.phone**: Phone-specific commands
- **engine.voice_gender_control**: Voice switching
- **engine.multilingual_support**: Language support
- **engine.personality_manager**: Response personalization
- **engine.command_history**: Command tracking

### Database Integration
- **jarvis.db**: SQLite database for contacts
- **Tables**: contacts (name, mobile_no)

### Configuration Files
- **ui_config.json**: UI settings storage
- **emotion_config.json**: Emotion system data
- **scheduled_tasks.json**: Task scheduler data

This documentation covers all major features and functions available in the command.py system, providing both technical details and practical usage examples.