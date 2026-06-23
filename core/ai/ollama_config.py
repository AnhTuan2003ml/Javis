"""Ollama local/remote model configuration for Javis.

Default target is the user's LAN Ollama server.
Override with environment variables when needed:
- OLLAMA_BASE_URL
- OLLAMA_MODEL_NAME
- OLLAMA_TIMEOUT
"""

import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "qwen3:4b-instruct")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "180"))
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}
