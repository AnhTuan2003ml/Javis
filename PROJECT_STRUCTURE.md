# JARVIS Project Structure

The root folder now contains only entrypoints, top-level documentation, and project metadata. Runtime files are grouped by purpose.

```text
Javis/
├── main.py                 # Eel UI bootstrap and exposed UI functions
├── run.py                  # Process runner for UI, hotword, and proactive AI
├── jarvis_startup.py       # Windows startup helper
├── core/                   # Application code
│   ├── ai/                 # Dual AI, advanced features, AI executors
│   ├── auth/               # Face and fingerprint authentication
│   ├── commands/           # Command parsing, command history, UI feature glue
│   ├── config/             # Config helper modules
│   ├── media/              # Image and video generation helpers
│   ├── phone/              # Phone integration and notification support
│   ├── system/             # System monitoring helpers
│   └── voice/              # Voice, hotword, gender, and multilingual support
├── config/                 # Runtime configuration files
├── data/
│   ├── databases/          # SQLite databases
│   ├── secrets/            # Local encrypted secrets and keys
│   └── state/              # Runtime state, history, reminders, notes
├── reports/                # Generated reports
├── scripts/                # Windows helper scripts
├── www/                    # Eel web UI
├── ui/                     # Screenshots and design reference assets
├── docs/                   # API, architecture, UML, and feature docs
├── demos/                  # Demo guide
├── requirements.txt        # Python dependencies
├── package.json            # Project metadata
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## Core Layout

| Folder | Purpose |
| --- | --- |
| `core/ai` | AI providers, high-level AI routing, advanced feature execution. |
| `core/auth` | Face recognition, fingerprint authentication, model training assets. |
| `core/commands` | User command handling, command history, helper functions, Eel-facing commands. |
| `core/config` | Lightweight configuration helpers and personality state. |
| `core/media` | Simple image and video generation helpers. |
| `core/phone` | Phone command handling, SMS/call helpers, notification monitoring. |
| `core/system` | System metrics and monitoring. |
| `core/voice` | TTS/STT-adjacent voice helpers, hotword detection, multilingual behavior. |

## Runtime Layout

| Folder | Purpose |
| --- | --- |
| `config` | User-facing settings such as voice, UI, language, biometric, AI provider. |
| `data/databases` | SQLite databases such as contacts, memory, and knowledge. |
| `data/state` | Generated state such as reminders, history, notes, usage, calendar, health. |
| `data/secrets` | Local password vault files and keys. |
| `reports` | Generated reports such as battery reports. |
| `scripts` | Batch scripts for install, device checks, and startup. |

## Entrypoints

- `python run.py` starts the full Jarvis process group.
- `python main.py` starts the Eel app directly.
- `jarvis_startup.py` and `scripts/start_jarvis.bat` are Windows startup helpers.

## Notes

- Code should import from `core.*`; the old `engine.*` package has been removed.
- Runtime JSON, DB, TXT, key, report, and BAT files should not live in the root.
- Generated Python cache folders (`__pycache__`) are not part of the source tree.
