# JARVIS AI Assistant - UML Diagrams

## Class Diagram

```mermaid
classDiagram
    class JarvisMain {
        +start()
        +initialize()
        +authenticate()
        +shutdown()
    }
    
    class VoiceProcessor {
        -recognizer: SpeechRecognition
        -tts_engine: pyttsx3
        +listen(): string
        +speak(text: string)
        +set_voice_gender(gender: string)
    }
    
    class AIManager {
        -groq_client: GroqClient
        -gemini_client: GeminiClient
        +process_query(query: string): string
        +get_response(text: string): string
        +switch_provider(provider: string)
    }
    
    class AuthenticationManager {
        -face_recognizer: FaceRecognizer
        -fingerprint_auth: FingerprintAuth
        +authenticate_face(): boolean
        +authenticate_fingerprint(): boolean
        +register_user(user_data: dict)
    }
    
    class CommandProcessor {
        -command_history: CommandHistory
        +parse_command(text: string): Command
        +execute_command(command: Command): Result
        +get_command_suggestions(): list
    }
    
    class SystemController {
        +open_application(app_name: string)
        +close_application(app_name: string)
        +take_screenshot(): string
        +get_system_stats(): dict
    }
    
    class PhoneController {
        -adb_client: ADBClient
        +send_message(contact: string, message: string)
        +make_call(contact: string)
        +get_notifications(): list
    }
    
    JarvisMain --> VoiceProcessor
    JarvisMain --> AIManager
    JarvisMain --> AuthenticationManager
    JarvisMain --> CommandProcessor
    CommandProcessor --> SystemController
    CommandProcessor --> PhoneController
```

## Sequence Diagram - Voice Command Processing

```mermaid
sequenceDiagram
    participant User
    participant VoiceProcessor
    participant CommandProcessor
    participant AIManager
    participant SystemController
    participant UI
    
    User->>VoiceProcessor: Voice Command
    VoiceProcessor->>VoiceProcessor: Speech Recognition
    VoiceProcessor->>CommandProcessor: Text Command
    CommandProcessor->>CommandProcessor: Parse Command
    
    alt AI Query
        CommandProcessor->>AIManager: Process Query
        AIManager->>AIManager: Generate Response
        AIManager-->>CommandProcessor: AI Response
    else System Command
        CommandProcessor->>SystemController: Execute Command
        SystemController->>SystemController: Perform Action
        SystemController-->>CommandProcessor: Action Result
    end
    
    CommandProcessor-->>VoiceProcessor: Response Text
    VoiceProcessor->>VoiceProcessor: Text-to-Speech
    VoiceProcessor-->>User: Voice Response
    CommandProcessor->>UI: Update Interface
```

## State Diagram - Authentication Flow

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> AuthenticationRequired
    
    AuthenticationRequired --> FaceAuth: Face Auth Enabled
    AuthenticationRequired --> FingerprintAuth: Fingerprint Auth Enabled
    AuthenticationRequired --> Authenticated: No Auth Required
    
    FaceAuth --> FaceProcessing
    FaceProcessing --> FaceSuccess: Recognition Success
    FaceProcessing --> FaceFailed: Recognition Failed
    
    FingerprintAuth --> FingerprintProcessing
    FingerprintProcessing --> FingerprintSuccess: Unlock Success
    FingerprintProcessing --> FingerprintFailed: Unlock Failed
    
    FaceSuccess --> DualAuthCheck: Dual Auth Mode
    FingerprintSuccess --> DualAuthCheck: Dual Auth Mode
    FaceSuccess --> Authenticated: Single Auth Mode
    FingerprintSuccess --> Authenticated: Single Auth Mode
    
    DualAuthCheck --> Authenticated: Both Successful
    DualAuthCheck --> AuthenticationFailed: Either Failed
    
    FaceFailed --> AuthenticationFailed
    FingerprintFailed --> AuthenticationFailed
    
    AuthenticationFailed --> [*]: Exit Application
    Authenticated --> Running
    
    Running --> Listening: Voice Mode
    Running --> Processing: Command Received
    Processing --> Executing: Valid Command
    Executing --> Responding: Action Complete
    Responding --> Listening: Response Sent
    
    Running --> Shutdown: User Exit
    Shutdown --> [*]
```

## Activity Diagram - Command Execution Flow

```mermaid
flowchart TD
    A[Start] --> B[Listen for Command]
    B --> C{Voice or Text?}
    
    C -->|Voice| D[Speech Recognition]
    C -->|Text| E[Text Input]
    
    D --> F[Parse Command]
    E --> F
    
    F --> G{Command Type?}
    
    G -->|System| H[System Command]
    G -->|AI Query| I[AI Processing]
    G -->|Phone| J[Phone Command]
    G -->|Unknown| K[Error Response]
    
    H --> L[Execute System Action]
    I --> M[Get AI Response]
    J --> N[Execute Phone Action]
    
    L --> O[Generate Response]
    M --> O
    N --> O
    K --> O
    
    O --> P[Text-to-Speech]
    P --> Q[Update UI]
    Q --> R[Log Command]
    R --> B
    
    B --> S{Exit Command?}
    S -->|No| B
    S -->|Yes| T[End]
```

## Use Case Diagram

```mermaid
flowchart LR
    subgraph "JARVIS AI Assistant System"
        UC1[Voice Commands]
        UC2[System Control]
        UC3[Phone Integration]
        UC4[AI Queries]
        UC5[Authentication]
        UC6[Settings Management]
        UC7[File Operations]
        UC8[Automation]
    end
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    
    UC1 --> VoiceSystem[Voice Recognition System]
    UC2 --> SystemAPI[System APIs]
    UC3 --> PhoneAPI[Phone APIs]
    UC4 --> AIProviders[AI Providers]
    UC5 --> BiometricSystems[Biometric Systems]
    UC6 --> ConfigSystem[Configuration System]
    UC7 --> FileSystem[File System]
    UC8 --> Scheduler[Task Scheduler]
```

## Component Diagram

```mermaid
graph TB
    subgraph "JARVIS Core System"
        subgraph "UI Layer"
            WebUI[Web Interface]
            VoiceUI[Voice Interface]
        end
        
        subgraph "Application Layer"
            CommandEngine[Command Engine]
            AIEngine[AI Engine]
            AuthEngine[Authentication Engine]
        end
        
        subgraph "Service Layer"
            VoiceService[Voice Service]
            SystemService[System Service]
            PhoneService[Phone Service]
            FileService[File Service]
        end
        
        subgraph "Data Layer"
            ConfigDB[(Configuration)]
            UserDB[(User Data)]
            HistoryDB[(Command History)]
            MemoryDB[(AI Memory)]
        end
        
        subgraph "External Systems"
            GroqAPI[Groq AI API]
            GeminiAPI[Gemini AI API]
            AndroidDevice[Android Device]
            WindowsAPI[Windows APIs]
        end
    end
    
    WebUI --> CommandEngine
    VoiceUI --> VoiceService
    VoiceService --> CommandEngine
    CommandEngine --> AIEngine
    CommandEngine --> AuthEngine
    AIEngine --> GroqAPI
    AIEngine --> GeminiAPI
    AuthEngine --> UserDB
    CommandEngine --> SystemService
    CommandEngine --> PhoneService
    CommandEngine --> FileService
    SystemService --> WindowsAPI
    PhoneService --> AndroidDevice
    CommandEngine --> HistoryDB
    AIEngine --> MemoryDB
    AuthEngine --> ConfigDB
```

## Deployment Diagram

```mermaid
graph TB
    subgraph "User's Computer"
        subgraph "JARVIS Application"
            MainProcess[Main Process]
            HotwordProcess[Hotword Detection]
            ProactiveProcess[Proactive Service]
            WebServer[Web Server]
        end
        
        subgraph "System Resources"
            FileSystem[Local File System]
            SystemAPIs[Windows APIs]
            AudioDevices[Audio Devices]
            Camera[Camera Device]
        end
        
        subgraph "Web Browser"
            UIInterface[User Interface]
        end
    end
    
    subgraph "Android Device"
        ADBService[ADB Service]
        PhoneApps[Phone Applications]
    end
    
    subgraph "Cloud Services"
        GroqCloud[Groq AI Service]
        GeminiCloud[Gemini AI Service]
    end
    
    MainProcess --> FileSystem
    MainProcess --> SystemAPIs
    MainProcess --> AudioDevices
    MainProcess --> Camera
    WebServer --> UIInterface
    MainProcess --> ADBService
    ADBService --> PhoneApps
    MainProcess --> GroqCloud
    MainProcess --> GeminiCloud
```

## Package Diagram

```mermaid
graph TB
    subgraph "jarvis"
        subgraph "engine"
            auth[auth]
            features[features]
            command[command]
            dual_ai[dual_ai]
            voice[voice_processing]
            phone[phone_integration]
            system[system_control]
        end
        
        subgraph "ui"
            web[web_interface]
            assets[assets]
        end
        
        subgraph "docs"
            documentation[documentation]
            diagrams[diagrams]
        end
        
        subgraph "config"
            settings[settings]
            credentials[credentials]
        end
        
        main[main.py]
        run[run.py]
    end
    
    main --> engine
    run --> main
    engine --> config
    web --> assets
    auth --> config
    features --> auth
    command --> features
    dual_ai --> command
    voice --> dual_ai
    phone --> voice
    system --> phone
```